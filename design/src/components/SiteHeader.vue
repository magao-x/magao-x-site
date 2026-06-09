<script setup lang="ts"></script>

<template>
  <div class="full-width">
    <div class="background bg-grid">
      <div class="grid-fade"></div>
      <div class="grid-lines"></div>
    </div>
    <header class="width-limiter">
      <div id="logo">
        <a href="/"
          ><img src="../styles/magao-x-logo-white.svg" /><span>MagAO-X</span></a
        >
      </div>
      <div>Extreme adaptive optics at visible wavelengths</div>
    </header>
    <nav class="width-limiter">
      <ul>
        <li><a class="hover-underline" href="/#press">Press</a></li>
        <li><a class="hover-underline" href="/publications.html">Publications</a></li>
        <li>
          <a class="hover-underline" href="/#capabilities">Capabilities</a>
        </li>
        <li><a class="hover-underline" href="/#team">Team</a></li>
        <li>
          <a class="hover-underline external" href="https://magao-x.org/docs/handbook/" target="_blank"
            >Handbook</a
          >
        </li>
        <li>
          <a class="hover-underline external" href="https://xwcl.science/blog/#content" target="_blank">Blog</a>
        </li>
      </ul>
    </nav>
  </div>
</template>

<style lang="scss">
header {
  text-align: center;
  padding-top: 1rem;
  padding-bottom: 1rem;

  div {
    font-family: monospace;
    margin: 0;
    padding: 0;
    font-size: 1rem;
  }
}

#logo {
  a {
    display: inline-block;
    margin: 0 auto;
  }
  img {
    height: 6rem;
    filter: drop-shadow(0 0 13px #0a90ffff);
    transition: filter 0.3s ease-in-out;
  }

  a:hover img {
    filter: drop-shadow(0 0 13px rgb(145, 206, 255));
  }

  span {
    position: absolute;
    left: -999em;
  }
}

$body-bg: #222;
$grid-color: rgba(#00e1ff, 0.3);
$grid-height: 600px;

.bg-grid {
  width: 100%;
  height: 100%;
  overflow: hidden;
  perspective: ($grid-height * 0.75);

  .grid-fade {
    width: 100%;
    height: 100%;
    position: absolute;
    z-index: 1;
    background: radial-gradient(
      ellipse at 50% 50%,
      rgba($body-bg, 0%) 0%,
      rgba($body-bg, 100%) 80%
    );
  }

  .grid-lines {
    width: 100%;
    height: 200%;
    background-image:
      linear-gradient(to right, $grid-color 1px, transparent 0),
      linear-gradient(to bottom, $grid-color 1px, transparent 0);
    background-size: 45px 30px;
    background-position: center center;
    background-repeat: repeat;
    transform-origin: 100% 0 0;
    transform: rotateX(70deg);
  }
}

nav {
  font-family: Baumans;
  padding-bottom: 1rem;
  transform-style: preserve-3d;

  ul {
    list-style-type: none;
    margin: 0;
    margin-top: 1rem;
    padding: 0;
    display: flex;
  }

  li {
    margin: 0 auto;

    a {
      font-weight: bold;
      font-size: 1.7rem;
      text-decoration: none;
    }
  }
}

@media (max-width: 1024px) {
  #logo img {
    max-width: 66vw;
  }
  nav > ul {
    display: block;
    text-align: center;
    & > li {
      display: inline-block;
      margin: 0 1rem;
      .hover-underline {
        font-size: 1em;
      }
    }
  }
}
</style>
