// Islands entrypoint. App.vue's body is treated as static SSR'd HTML — we never
// call `createApp(App).mount(#app)` on the client, so the bulk of the landing
// page costs zero JS. Only components marked `data-island="..."` in the SSR
// output get hydrated, and their bundles (notably three.js for StarGlobe /
// TelescopeModel) are pulled in lazily via dynamic import + IntersectionObserver.
//
// To add a new island: register it in `islands` below and render a placeholder
// in App.vue like `<div data-island="my-thing" data-prop-foo="bar"></div>`.
// `data-prop-*` attributes are forwarded as props to the mounted component.

import { createApp, type Component } from "vue";
// Side-effect import: ensures App.vue's <style> block stays in the client CSS
// bundle even though we never instantiate it on the client in production.
import "./App.vue";

type IslandLoader = () => Promise<{ default: Component }>;

const islands: Record<string, IslandLoader> = {
  "star-globe": () => import("./components/StarGlobe.vue"),
  "telescope-model": () => import("./components/TelescopeModel.vue"),
};

function collectProps(el: HTMLElement): Record<string, string> {
  const props: Record<string, string> = {};
  const PREFIX = "data-prop-";
  for (const attr of Array.from(el.attributes)) {
    if (attr.name.startsWith(PREFIX)) {
      props[attr.name.slice(PREFIX.length)] = attr.value;
    }
  }
  return props;
}

function observeIslands() {
  const observer = new IntersectionObserver(
    (entries) => {
      for (const entry of entries) {
        if (!entry.isIntersecting) continue;
        const el = entry.target as HTMLElement;
        const name = el.dataset.island;
        const loader = name && islands[name];
        if (!loader) continue;
        observer.unobserve(el);
        loader().then((mod) => {
          createApp(mod.default, collectProps(el)).mount(el);
        });
      }
    },
    { rootMargin: "200px" },
  );
  document
    .querySelectorAll<HTMLElement>("[data-island]")
    .forEach((el) => observer.observe(el));
}

async function bootstrap() {
  if (import.meta.env.DEV) {
    // Dev (vite dev server) skips the prerender step, so #app is empty and
    // the islands have nothing to attach to. Mount App.vue eagerly here so
    // `npm run dev` behaves like a normal SPA with HMR; in production this
    // branch is tree-shaken away by Vite's DEV constant inlining.
    const App = (await import("./App.vue")).default;
    createApp(App).mount("#app");
  }
  observeIslands();
}

bootstrap();
