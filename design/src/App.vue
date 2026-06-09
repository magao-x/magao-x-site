<script setup lang="ts">
// StarGlobe and TelescopeModel are mounted lazily as "islands" by main.ts
// (look for `data-island` divs below) so their three.js bundles only load
// when the user scrolls near them. The rest of this template is treated as
// static HTML by the client — main.ts never calls `createApp(App).mount(...)`.
import SiteHeader from "./components/SiteHeader.vue";
import SiteFooter from "./components/SiteFooter.vue";
import VideoWrapper from "./components/VideoWrapper.vue";
</script>

<template>
  <SiteHeader />

  <div class="full-width stripe glamor-shots">
    <div class="column left">
      <picture>
        <source
          srcset="./styles/magao-x-on-platform.webp"
          type="image/webp"
        />
        <img
          src="./styles/magao-x-on-platform.png"
          alt="MagAO-X on the Magellan instrument platform"
        />
      </picture>
    </div>
    <div class="content column">
      <p>
        MagAO-X is an <em>extreme adaptive optics system</em> used on the
        Magellan Clay 6.5-meter telescope to achieve diffraction-limited imaging
        at H-&alpha; (656&nbsp;nm).
      </p>
      <p>
        It is also a testbed for novel wavefront control
        <a
          href="https://magao-x.org/docs/handbook/observers/usepolicy.html#laboratory-experiments"
          target="_blank"
          >experiments</a
        >
        and post-processing algorithms.
      </p>
          <p>
            Time on MagAO-X is available to Magellan partner institutions and
            <a
              href="https://noirlab.edu/science/observing-noirlab/proposals/call-for-proposals"
              target="_blank"
              >through NOIRLab</a
            >. Interested guest observers should contact P.I. Jared Males for
            information on submitting
            <a
              href="https://magao-x.org/docs/handbook/observers/usepolicy.html#proposals"
              target="_blank"
              >observing proposals</a
            >.
          </p>

    </div>
    <div class="column right">
      <picture>
        <source
          srcset="./styles/magao-x_beams_render.webp"
          type="image/webp"
        />
        <img
          src="./styles/magao-x_beams_render.png"
          alt="Rendered view of MagAO-X optical beams"
        />
      </picture>
    </div>
  </div>
  <div class="full-width fancy-border rot270 only-bottom">
    <div class="width-limiter" id="press">
      <h2>Press</h2>
    </div>
  </div>
  <div class="width-limiter content press-list">
    <details class="press-item" open>
      <summary class="grid cols-2">
        <div class="left-gutter">
          <time>2025</time>
        </div>
        <h3>MagAO-X reveals a baby planet's growth spurt</h3>
      </summary>
      <div class="grid cols-2">
        <div class="left-gutter"></div>
        <div class="body">
          <p>
            Prof. Laird Close of the MagAO-X team and Richelle van Capelleveen,
            an astronomy graduate student at Leiden Observatory, discovered and characterized the
            accreting young planet WISPIT 2b.
          </p>
          <div class="responsive grid cols-2 external-links">
            <div>
              <h4>Press</h4>
              <ul class="link-list">
                <li>
                  <a
                    href="https://www.usatoday.com/story/news/nation/2025/08/27/wispit-2b-new-young-planet/85828850007/"
                    target="_blank"
                    >USA&nbsp;Today</a
                  >
                </li>
                <li>
                  <a
                    href="https://www.space.com/astronomy/exoplanets/a-remarkable-discovery-astronomers-find-1st-exoplanet-in-multi-ring-disk-around-star"
                    target="_blank"
                    >Space.com</a
                  >
                </li>
                <li>
                  <a
                    href="https://people.com/jupiter-like-planet-discovered-orbiting-young-star-distant-solar-system-11799592"
                    target="_blank"
                    >People</a
                  >
                </li>
                <li>
                  <a
                    href="https://news.arizona.edu/news/growing-baby-planet-photographed-first-time-ring-darkness"
                    target="_blank"
                    >U.&nbsp;of&nbsp;Arizona press release</a
                  >
                </li>
                <li>
                  <a
                    href="https://www.universiteitleiden.nl/en/news/2026/03/two-planets-in-formation-discovered-around-young-star-wispit-2"
                    target="_blank"
                    >Leiden U. press release</a
                  >
                </li>
              </ul>
            </div>
            <div>
              <h4>Publications</h4>
              <ul class="link-list">
                <li>
                  <a
                    href="https://iopscience.iop.org/article/10.3847/2041-8213/adf7a5"
                    target="_blank"
                    >Close <em>et&nbsp;al.</em></a
                  >
                  (ApJL)
                </li>
                <li>
                  <a
                    href="https://iopscience.iop.org/article/10.3847/2041-8213/adf721"
                    target="_blank"
                    >van Capelleveen <em>et&nbsp;al.</em></a
                  >
                  (ApJL)
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </details>
    <details class="press-item" >
      <summary class="grid cols-2">
        <div class="left-gutter">
          <time>2025</time>
        </div>
        <h3>Team member Dr. Sebastiaan Haffert awarded New Horizons in Physics
        Prize</h3>
      </summary>
      <div class="grid cols-2">
        <div class="left-gutter"></div>
        <div class="body">
          <p>
            Dr. Sebastiaan Haffert of the MagAO-X team was awarded the New Horizons in Physics prize by the Breakthrough Prize board alongside Rebecca Jensen-Clem and Maaike van Kooten for work in extreme adaptive optics for exoplanet detection.
          </p>
          <div class="responsive grid cols-2 external-links">
            <div>
              <h4>Press</h4>
              <ul class="link-list">
                <li>
                  <a href="https://breakthroughprize.org/News/91" target="_blank"
                    >Breakthrough&nbsp;Prize press&nbsp;release</a
                  >
                </li>
                <li>
                  <a
                    href="https://astro.arizona.edu/news/search-earths-siblings-sebastiaan-haffert-wins-prestigious-new-horizons-prize"
                    target="_blank"
                    >U.&nbsp;of&nbsp;Arizona press&nbsp;release</a
                  >
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </details>
    <div class="more-publications">…and <a href="publications.html" target="_blank">NUMBER_OF_MAGAOX_PUBLICATIONS scientific publications</a></div>
  </div>


  <div class="full-width fancy-border rot90 only-bottom">
    <div class="width-limiter" id="telescope">
      <h2>Telescope</h2>
    </div>
  </div>
  <div class="full-width stripe telescope">
    <div
      class="background"
      data-island="telescope-model"
      data-prop-layout="left"
    ></div>
    <div class="width-limiter with-custom-bg">
      <div class="overlay left tilt">
        <div class="content fancy-border rot90">
          <h2>Magellan 6.5&ndash;meter</h2>
          <h3 class="subtitle">
            Clay first light: 2002-09-07<br />MagAO-X first light: 2019-12-03
          </h3>
          <p>
            Located on the peak of Cerro Manqui, the Magellan Telescopes enjoy
            exquisite seeing conditions.
          </p>
          <p>Remote observations are possible, but seeing is believing.</p>
        </div>
      </div>
    </div>
  </div>

  <div class="full-width fancy-border only-bottom">
    <div class="width-limiter" id="capabilities">
      <h2>Instrument capabilities</h2>
    </div>
  </div>

  <div class="full-width stripe proem">
    <div class="background"></div>
    <div class="center-content">
      <p class="bigfacts">
        Simultaneous <span style="color: #0a90ff">dual</span>-<span
          style="color: #ff0000"
          >band</span
        >
        imaging using two Princeton&nbsp;Instruments ProEM&nbsp;HS:&nbsp;1024BX3
        electron-multiplying CCD
        <a
          href="https://magao-x.org/docs/handbook/observers/cameras.html"
          target="_blank"
          >cameras.</a
        >
      </p>
    </div>
  </div>
  <div class="full-width stripe wavefront-control">
    <div class="background">
      <VideoWrapper
        videoSrc="/coron_speckles.mp4"
        class="offset-right"
      ></VideoWrapper>
    </div>
    <div class="width-limiter overlay left" style="min-height: 50vh">
      <div class="responsive grid three">
        <p class="bigfacts bmc2k">
          Woofer-tweeter wavefront control with 2040-actuator and 97-actuator
          deformable mirrors.
        </p>
        <p class="bigfacts ncpc">
          Dedicated non-common-path correction with 1020-actuator deformable
          mirror.
        </p>
      </div>
    </div>
  </div>

  <div class="full-width hex-tessellation">
    <div class="width-limiter center-content">
      <div class="improving">
        <p>Improving run after run since December 2019.</p>
      </div>
    </div>
    <div class="width-limiter patches">
      <div class="patch">
        <a href="https://xwcl.science/tag/2019b/" target="_blank"
          ><img
            src="/patches/patch2019B.svg"
            alt="Mission patch design for 2019B with Vizzy Viscacha"
        /></a>
      </div>
      <div class="patch">
        <a href="https://xwcl.science/2020/" target="_blank"
          ><img
            src="/patches/patch2020.svg"
            alt="Patch design for 2020 with a pooping coyote"
        /></a>
      </div>
      <div class="patch">
        <a href="https://xwcl.science/2021/" target="_blank"
          ><img
            src="/patches/patch2021.svg"
            alt="Patch design for 2021 with a barfing bobcat"
        /></a>
      </div>
      <div class="patch">
        <a href="https://xwcl.science/tag/2022a/" target="_blank"
          ><img
            src="/patches/patch2022A.svg"
            alt="Mission patch design for 2022A with Carlos Culpeo"
        /></a>
      </div>
      <div class="patch">
        <a href="https://xwcl.science/tag/2022b/" target="_blank"
          ><img
            src="/patches/patch2022B.svg"
            alt="Mission patch design for 2022B with Gabriela la gata Andina"
        /></a>
      </div>
      <div class="patch">
        <a href="https://xwcl.science/tag/2023a/" target="_blank"
          ><img
            src="/patches/patch2023A.svg"
            alt="Mission patch design for 2023A with el Condor"
        /></a>
      </div>
      <div class="patch">
        <a href="https://xwcl.science/tag/2024a/" target="_blank"
          ><img
            src="/patches/patch2024A.svg"
            alt="Mission patch design for 2024A with Hedwig"
        /></a>
      </div>
      <div class="patch">
        <a href="https://xwcl.science/tag/2024b/" target="_blank"
          ><img
            src="/patches/patch2024B.svg"
            alt="Mission patch design for 2024B"
        /></a>
      </div>
      <div class="patch">
        <a href="https://xwcl.science/tag/2025a/" target="_blank"
          ><img
            src="/patches/patch2025A.svg"
            alt="Mission patch design for 2025A"
        /></a>
      </div>
      <div class="patch">
        <a href="https://xwcl.science/tag/2025b/" target="_blank"
          ><img
            src="/patches/patch2025B.svg"
            alt="Mission patch design for 2025B with Gary Guanaco"
        /></a>
      </div>
      <div class="patch">
        <a href="https://xwcl.science/tag/2026a/" target="_blank"
          ><img
            src="/patches/patch2026A.svg"
            alt="Mission patch design for 2026A with a spotted false monitor lizard"
        /></a>
      </div>
      <div class="patch">
        <div class="patch-contents">TBA</div>
      </div>
    </div>
  </div>
  <div class="full-width stripe clouds">
    <video class="foreground" autoplay loop muted playsinline preload="auto">
      <source src="/clouds.webm" type="video/webm" />
    </video>
    <div class="clouds-still foreground" aria-hidden="true"></div>
    <div class="center-content">
      <p class="bigfacts" style="text-shadow: 0 0 13px #0a90ff">
        The only problem we can't fix is clouds.
      </p>
    </div>
  </div>

  <div class="full-width fancy-border rot180 only-bottom">
    <div class="width-limiter" id="team">
      <h2>Team</h2>
    </div>
  </div>

  <div class="full-width stripe team">
    <div class="background" data-island="star-globe"></div>
    <div class="width-limiter with-custom-bg">
      <div class="overlay tilt right">
        <div class="content fancy-border">
          <p>
            MagAO-X is an <strong>international collaboration</strong> involving
            faculty, graduate students, and postdocs in
            <span class="arizona">Arizona</span>,
            <span class="leiden">Leiden</span>,
            <span class="michigan">Michigan</span>,
            <span class="new-york">New York</span>, and
            <span class="washington-dc">Washington D.C.</span>
          </p>
          <p>
            Consult the eXtreme Wavefront Control Lab website for the
            <a href="https://xwcl.science/people/" target="_blank"
              >current roster</a
            >
            of team members and alumni.
          </p>
          <p>
            (We still like to think of ourselves as a small and scrappy
            traveling circus act, though.)
          </p>
        </div>
      </div>
    </div>
  </div>

  <VideoWrapper
    videoSrc="/drone_1080.mp4"
    webmSrc="/drone_1080.webm"
    poster="/drone_video_poster.jpg"
    class="full-width stripe drone"
  ></VideoWrapper>
  <SiteFooter />
</template>

<style lang="scss">
.hex-tessellation {
  position: relative;
  overflow: hidden;

  &::before {
    content: "";
    position: absolute;
    inset: 0;
    z-index: 0;
    pointer-events: none;
    background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 289.3 165.65'><defs><path id='h' d='M -90,0 L -45,-78 L 45,-78 L 90,0 L 45,78 L -45,78 Z' fill='none' stroke='white' stroke-opacity='0.1' stroke-width='2'/></defs><use href='%23h' x='90' y='78'/><use href='%23h' x='234.65' y='160.825'/><use href='%23h' x='-54.65' y='160.825'/><use href='%23h' x='234.65' y='-4.825'/><use href='%23h' x='-54.65' y='-4.825'/></svg>");
    background-size: 15rem 8.58rem;
    background-position: calc((100vw - 47rem) / 2) 1rem;
    background-repeat: repeat;
  }

  > * {
    position: relative;
    z-index: 1;
  }

  .center-content {
    height: auto;
  }

  .improving {
    height: 8.58rem;
    margin: 0;
    overflow: hidden;
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    font-weight: bold;

    p {
      margin: 0;
      font-size: 2rem;
      line-height: 1.1;
    }
  }
}

.patches {
  padding-top: 1rem;
  height: fit-content;
  padding-left: 1.5rem;

  --hex-width: 14rem;
  --gap-horizontal: 0.5rem;
  --gap-vertical: 0.5rem;
  --sqrt-of-3: 1.732;
  --hex-height: calc(var(--hex-width) / var(--sqrt-of-3));
  padding-bottom: calc(var(--hex-height) + var(--gap-vertical) / 2);
  display: grid;
  grid-template-columns: repeat(6, calc(var(--hex-width) / 2));
  column-gap: var(--gap-horizontal);
  row-gap: var(--gap-vertical);
  font-size: 0;

  .patch {
    width: fit-content;
    img,
    .patch-contents {
      --hex-scale: 1;
      height: var(--hex-height);
      transform-origin: 50% 50%;
      transition: transform 0.15s ease-out;
      width: calc(var(--hex-height) * 180 / 156);
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: calc(var(--hex-height) * 0.2);
      line-height: 1;
      color: rgba(255, 255, 255, 0.45);
      font-weight: bold;
    }
    a:hover img,
    a:hover .patch-contents {
      --hex-scale: 1.1;
    }

    &:nth-child(even) {
      img,
      .patch-contents {
        transform: translateY(
            calc(var(--hex-height) / 2 + var(--gap-vertical) / 2)
          )
          scale(var(--hex-scale));
      }
    }
    &:nth-child(odd) {
      img,
      .patch-contents {
        transform: scale(var(--hex-scale));
      }
    }
  }
}

.telescope {
  height: 500px;
}

.glamor-shots {
  --bg-height: 30rem;

  grid-template-columns: 3fr 2fr 3fr;
  display: grid;

  .column {
    padding: 2rem;
    align-content: center;
    font-size: 18px;
    &.left {
      text-align: right;
    }
    &.right {
      text-align: left;
    }
    img {
      max-width: 80%;
    }
  }
}

.proem {
  --proem-height: 30rem;

  .background {
    background-image:
      url(./styles/proem-side.svg), url(./styles/proem-perspective.svg);
    --gutter-width: calc((100vw - var(--content-width)) / 2);
    --background-left-width: 20rem;
    --background-right-width: 20rem;
    --background-left-origin: calc(
      var(--gutter-width) / 2 - var(--background-left-width) / 2
    );
    --background-right-origin: calc(
      var(--gutter-width) + var(--content-width) + var(--gutter-width) /
        2 - var(--background-right-width) / 2
    );
    background-size: auto 100%;
    background-position:
      var(--background-left-origin) center,
      var(--background-right-origin) center;
    background-repeat: no-repeat, no-repeat;
    height: var(--proem-height);
  }

  .center-content {
    height: var(--proem-height);
  }

  .bigfacts {
    max-width: 30rem;
    font-size: 1.9rem;
    font-weight: bold;
  }
}

.clouds {
  color: #00b7ff;
  aspect-ratio: 8 / 3;
  min-height: 500px;
  // .clouds-still scales 1.2× and translates vertically ±10% for parallax;
  // this clips the overflow at the section's edges so the scaled image
  // doesn't leak into the adjacent stripes. `overflow: hidden` on
  // .clouds-still itself doesn't catch its own transform overflow — only
  // the parent does.
  overflow: hidden;
  // Named view-progress timeline tracked through the vertical (block) axis.
  // .clouds-still references it via `animation-timeline: --clouds-view`. We
  // declare it here rather than relying on the anonymous `view()` function on
  // the subject so the timeline tracks this visible container element (which
  // is in normal flow) rather than the absolutely-positioned .clouds-still.
  view-timeline-name: --clouds-view;
  view-timeline-axis: block;
  --clouds-image: url(/earth.png);
  --clouds-bg-size: cover;
  --clouds-bg-position: 50% 50%;

  @supports (background-image: url(/earth.webp)) {
    --clouds-image: url(/earth.webp);
  }

  background-image: var(--clouds-image);
  background-size: var(--clouds-bg-size);
  background-position: var(--clouds-bg-position);

  .center-content {
    height: 100%;
  }

  // <video class="foreground"> overlays a VP9+alpha time-lapse over the
  // static section background. Single request, browser handles preload.
  video.foreground {
    object-fit: cover;
    object-position: 50% 50%;
    opacity: 1;
  }

  // Single static cloud overlay used as the Safari fallback for the VP9-alpha
  // video. Hidden by default; toggled on inside the @supports block below.
  // Image is a cloud-only WEBP with alpha; .clouds's earth bg shows through
  // where there's no cloud.
  .clouds-still {
    display: none;
    background-image: url(/clouds-fallback.webp);
    background-size: cover;
    background-position: 50% 50%;
  }

  // Safari mis-renders VP9 alpha in <video>: transparent pixels show as
  // opaque black and partial alpha doesn't composite. Detect Safari (the
  // only engine that ships -webkit-named-image()) and swap the video for
  // the still. Pure CSS, no JS / UA sniffing.
  @supports (background: -webkit-named-image(i)) {
    video.foreground {
      display: none;
    }
    .clouds-still {
      display: block;
      mix-blend-mode: screen;
    }
  }

  .background {
    pointer-events: none;
    background-image: var(--clouds-image);
    background-size: var(--clouds-bg-size);
    background-position: var(--clouds-bg-position);
  }

  .bigfacts {
    font-weight: bold;
    font-size: clamp(2.2rem, 4cqi, 4rem);
  }
}

// Parallax keyframes for the Safari .clouds-still. Linear timing + a named
// view-timeline on .clouds means the animation's progress is tied directly
// to the section's progress through the viewport: -10% translateY at entry
// (top edge just appearing at the viewport bottom), 0 when centred, +10%
// at exit (bottom edge just leaving the viewport top). Baseline scale(1.2)
// on .clouds-still keeps the image fully covering the container at both ends.
@keyframes clouds-parallax {
  from {
    transform: translateY(-10%) scale(1.2);
  }
  to {
    transform: translateY(10%) scale(1.2);
  }
}

.wavefront-control {
  .bigfacts {
    font-weight: bold;
    font-size: 1.2rem;
    text-align: left;
  }
  .grid {
    grid-template-rows: 1fr 1fr;
    .bmc2k {
      grid-column: 1 / span 2;
    }
    .ncpc {
      grid-column: 2 / span 2;
      align-content: end;
    }
  }
}

@media (max-width: 768px) {
  .wavefront-control .responsive.grid {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    .bmc2k {
      grid-column: 1 / span 2;
    }
    .ncpc {
      grid-column: 2 / span 2;
      grid-row: 2;
    }
  }
}

.drone {
  min-height: 95vh;
}

* {
  box-sizing: border-box;
}

.overlay {
  display: flex;
  padding: 1rem;
  height: 100%;

  .content {
    width: 50%;
    padding: 1rem;
    margin: 1rem;
    background: rgba(0, 0, 0, 0.2);
    backdrop-filter: blur(10px);

    h2 {
      margin-top: 0;
    }

    h3.subtitle {
      font-size: 1rem;
      font-family: monospace;
      font-weight: inherit;
      margin-top: 0;
    }
  }

  &.right {
    flex-direction: row-reverse;

    &.tilt .content {
      transform: perspective(1000px) rotateX(-10deg) rotateY(-10deg);
    }
  }

  &.left {
    flex-direction: row;

    &.tilt .content {
      transform: perspective(1000px) rotateX(-10deg) rotateY(10deg);
    }
  }
}
.proposals-guidance {
  font-style: italic;
  text-align: center;
  color: #999;
}

.press-list {
  padding: 1.5rem 0 2rem;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;

  a {
    color: var(--accent-contrast-alt);
    &:visited {
      color: var(--accent-contrast-alt);
    }
    &:active {
      color: var(--accent-contrast-alt);
    }
    &:hover {
      color: var(--accent-contrast-alt);
    }
  }

  .press-item {
    background: rgba(255, 255, 255, 0.03);
    overflow: hidden;

    display: grid;
    & > .grid.cols-2 {
      grid-template-columns: 6em 1fr;
    }

    .left-gutter {
      padding: 1rem 1rem 0 0;
    }
    h3 {
      padding: 1rem 0;
    }
    .left-gutter, h3 {
      line-height: 1.8rem;
    }

    .left-gutter {
      background-color: var(--accent-contrast-dim);
      border-right: 2px solid var(--accent-contrast);
      text-align: right;
    }

    h3,
    h4 {
      font-family: "Helvetica Neue";
      font-weight: normal;
      margin: 0 0 0 0;
    }

    .external-links h4 {
      color: #9e5100;
    }
    .body {
      padding-bottom: 1rem;
      padding-right: 1rem;

      h4 {
        font-size: 0.9rem;
        font-weight: bold;
        margin-top: 1rem;
      }

      p {
        margin: 0.25rem 0;
      }

      .link-list {
        list-style: none;
        padding: 0;
        margin: 0.25rem 0;

        li {
          display: inline;
        }

        li + li::before {
          content: " · ";
          white-space: pre;
          color: var(--accent-color);
        }
      }
    }
  }
  .more-publications {
    font-size: 1.2rem;
    font-weight: bold;
    text-align: center;
    padding: 1rem;
    overflow: hidden;
  }
}

.press-item > summary:hover h3 {
  text-decoration: underline;
}
.press-item[open] > summary h3 {
  text-decoration: none;
}
.press-item > summary time::before {
  content: "+ ";
  display: inline-block;
  margin-right: 0.5rem;
}
.press-item[open] > summary time::before {
  content: "− ";
}

.offset-right {
  width: 120%;
}

@media (max-width: 1024px) {
  .glamor-shots {
    grid-template-columns: 1fr;
    --bg-height: auto;

    .column.left {
      display: none;
    }

    .column {
      padding: 1rem;
      text-align: center;
      &.right {
        text-align: center;
      }
      img {
        max-width: 70%;
        max-height: 50vh;
      }
    }
  }

  .telescope,
  .team {
    height: 600px;

    > .width-limiter {
      height: 100%;
      display: flex;
      align-items: flex-end;
    }
  }

  // Team section stacks vertically on mobile: globe on top in its own box,
  // overlay flowing below in normal document order. This overrides the
  // shared .telescope,.team rule above and the global absolute positioning
  // of .background.
  .team {
    height: auto;
    display: flex;
    flex-direction: column;

    > .background {
      position: relative;
      width: 100%;
      height: auto;
      aspect-ratio: 1;
      max-height: 65vh;
    }

    > .width-limiter {
      height: auto;
      display: block;
    }
  }

  .telescope .content h3.subtitle {
    display: none;
  }

  .overlay {
    padding: 0.5rem;
    align-items: flex-end;

    .content {
      width: auto;
      flex: 1;
      margin: 0.5rem;
      padding: 0.75rem;
    }

    &.left.tilt .content,
    &.right.tilt .content {
      transform: none;
    }
  }

  .proem {
    display: flex;
    flex-direction: column;

    > .background {
      position: static;
      width: 100%;
      height: 38vw;
      background-size:
        42% auto,
        42% auto;
      background-position:
        4% center,
        96% center;
    }

    > .center-content {
      height: auto;
      padding: 1rem;
    }

    .bigfacts {
      font-size: 1.2rem;
      max-width: none;
    }
  }

  .patches {
    --hex-width: 12rem;
    --gap-horizontal: 0.25rem;
    --gap-vertical: 0.25rem;
    grid-template-columns:
      repeat(2, calc(var(--hex-width) / 2))
      calc(var(--hex-width) * 2 / 3);
    justify-content: center;
    padding-left: 0.25rem;
    padding-right: 0.25rem;

    .patch:nth-child(even) img,
    .patch:nth-child(even) .patch-contents,
    .patch:nth-child(odd) img,
    .patch:nth-child(odd) .patch-contents {
      transform: scale(var(--hex-scale));
    }

    .patch:nth-child(3n + 2) img,
    .patch:nth-child(3n + 2) .patch-contents {
      transform: translateY(
          calc(var(--hex-height) / 2 + var(--gap-vertical) / 2)
        )
        scale(var(--hex-scale));
    }
  }

  .hex-tessellation::before {
    display: block;
    background-size: 12.5rem 7.18rem;
    background-position: calc((100vw - 20.28rem) / 2) 1rem;
  }

  .hex-tessellation .improving {
    height: 7.18rem;
    padding: 0;

    p {
      font-size: 1.2rem;
    }
  }

  .proposals-guidance {
    p {
      font-size: 1rem;
    }
  }

  // On narrow screens the inline · separators get awkward when long link
  // labels wrap; fall back to a vertical bulleted list so each link gets
  // its own line.
  .press-list .press-item .body .link-list {
    list-style: disc;
    padding-left: 1.25rem;

    li {
      display: list-item;
    }

    li + li::before {
      content: none;
    }
  }

  // Keep the desktop gutter look on mobile, but let the title cell shrink
  // below its content's intrinsic width — grid items default to
  // `min-width: auto`, which is what was forcing a long unbreakable title
  // to grow the card past the viewport edge.
  .press-list .press-item h3 {
    min-width: 0;
    overflow-wrap: anywhere;
  }
}
</style>
