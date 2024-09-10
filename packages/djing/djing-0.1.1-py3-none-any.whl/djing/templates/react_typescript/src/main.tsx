import "./index.css";

import { createInertiaApp } from "@inertiajs/react";
import { createRoot } from "react-dom/client";
import MainLayout from "./Layout/MainLayout";

document.addEventListener("DOMContentLoaded", () => {
  createInertiaApp({
    resolve: async (name) => {
      const pages = import.meta.glob("./Pages/**/*.tsx");

      let page: any = pages[`./Pages/${name}.tsx`];

      const module = await page();

      const Component = module.default;

      Component.layout =
        Component.layout || ((page: any) => <MainLayout>{page}</MainLayout>);

      return module;
    },
    setup({ el, App, props }) {
      createRoot(el).render(<App {...props} />);
    },
  });
});
