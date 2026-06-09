/// <reference types="vite/client" />

declare module "solar-calculator";

declare module "*.vue" {
  import type { DefineComponent } from "vue";
  const component: DefineComponent<object, object, unknown>;
  export default component;
}
