// Pre-render the app into static HTML.
// run `npm run generate` and then `dist/static` can be served as a static site.
//
// Emits two files:
//   - index.html: full landing page with App.vue pre-rendered into the body
//   - base.html:  shell rendering of Base.vue (header + footer only) with a
//                 `{% block content %}{% endblock %}` slot fallback baked into
//                 the body. Downstream Jinja2 templates extend this directly.

import fs from "node:fs";
import path from "node:path";
import url from "node:url";

const __dirname = path.dirname(url.fileURLToPath(import.meta.url));

const toAbsolute = (p) => path.resolve(__dirname, p);

const manifest = JSON.parse(
  fs.readFileSync(toAbsolute("dist/static/.vite/ssr-manifest.json"), "utf-8"),
);
const indexShell = fs.readFileSync(
  toAbsolute("dist/static/index.html"),
  "utf-8",
);
// base.html is consumed as a Jinja2 parent template by static pages that don't
// need Vue at all. If we leave the entrypoint script in, it would mount <App/>
// onto #app at load time and clobber whatever block content was injected.
const baseShell = indexShell.replace(
  /\s*<script\s+type="module"[^>]*src="\/index\.js"[^>]*><\/script>/,
  "",
);
const { render } = await import("./dist/server/entry-server.js");

const writeOut = async (filename, route, shell, { withPreloads = true } = {}) => {
  const [appHtml, preloadLinks] = await render(route, manifest);
  const html = shell
    .replace(`<!--preload-links-->`, withPreloads ? preloadLinks : "")
    .replace(`<!--app-html-->`, appHtml);
  const filePath = `dist/static/${filename}`;
  fs.writeFileSync(toAbsolute(filePath), html);
  console.log("pre-rendered:", filePath);
};

await writeOut("index.html", "/", indexShell);
await writeOut("base.html", "/base", baseShell, { withPreloads: false });

// done, delete .vite directory including ssr manifest
fs.rmSync(toAbsolute("dist/static/.vite"), { recursive: true });
