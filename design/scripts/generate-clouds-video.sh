#!/usr/bin/env bash
# Generate public/clouds.webm from the 24 most-recent UNIQUE cloud alpha maps
# in https://github.com/joshuabinswanger/matteason_live-cloud-maps_downloader
# releases.
#
# Source PNGs (8192x4096, ~40 MB each) are cached in .cache/cloud-maps/ so
# re-runs only download new releases. Each lossless source is cropped to
# remove the symmetric mirror band (top 512 + bottom 512 -> 8192x3072), then
# resized to the target output dimensions and fed directly to ffmpeg so the
# only lossy step is the final VP9 encode.
#
# Knobs (env vars):
#   CRF=30          VP9 constant-quality target (lower = higher quality / larger file)
#   DURATION=10     Total loop length in seconds
#   WIDTH=1440      Output width in pixels (height auto = WIDTH * 3 / 8)
#   FRAMES=24       Number of unique frames to use
#   LOOKBACK=72     How many recent releases to scan for the 24 unique ones
#   CPU_USED=2      libvpx-vp9 speed (0=slowest/best, 5=fastest)
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
CACHE="$REPO_ROOT/.cache/cloud-maps"
OUTPUT="$REPO_ROOT/public/clouds.webm"
SOURCE_REPO="joshuabinswanger/matteason_live-cloud-maps_downloader"

CRF="${CRF:-30}"
DURATION="${DURATION:-10}"
WIDTH="${WIDTH:-1440}"
FRAMES="${FRAMES:-24}"
LOOKBACK="${LOOKBACK:-72}"
CPU_USED="${CPU_USED:-2}"

HEIGHT=$(( WIDTH * 3 / 8 ))  # source aspect after mirror crop is 8192:3072 = 8:3

WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT

mkdir -p "$CACHE"

echo "[1/4] Resolving 24 unique recent cloud maps (scanning last $LOOKBACK releases)..."
gh release list -R "$SOURCE_REPO" -L "$LOOKBACK" --json tagName --jq '.[].tagName' > "$WORK/tags.txt"

seen_hashes=""
kept_tags=()
while IFS= read -r tag; do
  [ "${#kept_tags[@]}" -ge "$FRAMES" ] && break

  cache_file="$CACHE/$tag.png"
  if [ ! -f "$cache_file" ]; then
    dl_dir="$(mktemp -d)"
    if ! gh release download "$tag" -R "$SOURCE_REPO" -p "clouds_alpha_*.png" --dir "$dl_dir" 2>/dev/null; then
      rm -rf "$dl_dir"
      echo "  - $tag (download failed, skipping)"
      continue
    fi
    src=$(ls "$dl_dir"/clouds_alpha_*.png 2>/dev/null | head -n1) || src=""
    if [ -z "$src" ]; then
      rm -rf "$dl_dir"
      continue
    fi
    mv "$src" "$cache_file"
    rm -rf "$dl_dir"
    echo "  + $tag (downloaded $(du -h "$cache_file" | cut -f1))"
  fi

  hash=$(md5 -q "$cache_file" 2>/dev/null || md5sum "$cache_file" | cut -d' ' -f1)
  if echo "$seen_hashes" | grep -q "$hash"; then
    echo "  = $tag (duplicate of an already-kept frame, skipping)"
    continue
  fi
  seen_hashes="$seen_hashes $hash"
  kept_tags+=("$tag")
done < "$WORK/tags.txt"

if [ "${#kept_tags[@]}" -lt "$FRAMES" ]; then
  echo "ERROR: only found ${#kept_tags[@]}/$FRAMES unique frames in last $LOOKBACK releases"
  echo "       try a larger LOOKBACK value (currently $LOOKBACK)"
  exit 1
fi
echo "  -> kept ${#kept_tags[@]} unique frames"

echo "[2/4] Cropping (8192x3072+0+512) and resizing to ${WIDTH}x${HEIGHT}..."
# Reverse so oldest plays first
i=0
for ((idx=${#kept_tags[@]}-1; idx>=0; idx--)); do
  tag="${kept_tags[$idx]}"
  out_idx=$(printf "%02d" $i)
  magick "$CACHE/$tag.png" \
    -crop "8192x3072+0+512" +repage \
    -resize "${WIDTH}x${HEIGHT}" \
    "$WORK/frame_${out_idx}.png"
  i=$((i+1))
done

fps=$(awk -v f="$FRAMES" -v d="$DURATION" 'BEGIN { printf "%.6f", f / d }')
echo "[3/4] Encoding VP9 webm (alpha, CRF=$CRF, ${DURATION}s, ${fps} fps, cpu-used=$CPU_USED)..."
ffmpeg -y -loglevel warning -framerate "$fps" -i "$WORK/frame_%02d.png" \
  -c:v libvpx-vp9 -pix_fmt yuva420p -auto-alt-ref 0 \
  -b:v 0 -crf "$CRF" \
  -cpu-used "$CPU_USED" -row-mt 1 -tile-columns 2 -threads 8 \
  "$OUTPUT"

echo "[4/5] Generating still-frame Safari fallback..."
# Safari mis-renders VP9 alpha in <video>. App.vue swaps the video for a
# single static still with a scroll-driven parallax (see @supports check
# there). Pick the middle frame so the snapshot is representative.
n="${#kept_tags[@]}"
mid=$(( n / 2 ))
in="$WORK/frame_$(printf '%02d' "$mid").png"
out="$REPO_ROOT/public/clouds-fallback.webp"
magick "$in" -quality 80 "$out"
ls -lh "$out"

echo "[5/5] Done."
ls -lh "$OUTPUT"
ffprobe -loglevel error -show_streams "$OUTPUT" 2>&1 \
  | grep -iE "width=|height=|codec_name=|TAG:ALPHA_MODE|TAG:DURATION"
