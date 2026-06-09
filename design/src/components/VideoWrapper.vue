<template>
  <div class="video-wrapper">
    <video playsinline autoplay muted loop :poster="poster">
      <source v-if="webmSrc" :src="webmSrc" type="video/webm" />
      <source :src="videoSrc" type="video/mp4" />
      Your browser does not support the video tag.
    </video>
  </div>
</template>

<script setup lang="ts">
interface Props {
  videoSrc: string;
  // Optional VP9/WebM alternative. Browsers pick the first <source> they
  // can play, so listing webm first lets non-Safari clients grab the
  // smaller file while Safari falls through to the mp4.
  webmSrc?: string;
  // Optional poster frame shown before autoplay starts (and when autoplay
  // is suppressed, e.g. iOS low-power mode).
  poster?: string;
}
defineProps<Props>();
</script>

<style lang="scss">
video {
  object-fit: cover;
  top: 0;
  left: 0;
  height: 100%;
  width: 100%;
}

.video-wrapper {
  border: 2px solid #000;
  height: 100%;
  position: relative;
  overflow: hidden;
  display: flex;
  align-items: end;
  justify-content: center;
  & > * {
    position: relative;
  }
  & > video {
    position: absolute;
  }
}
</style>
