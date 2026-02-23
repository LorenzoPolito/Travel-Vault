// @ts-check
import { defineConfig } from "astro/config";

export default defineConfig({
  site: "https://lorenzopolito.github.io",
  base: "/Travel-Vault/",
  output: "static",
  build: {
    assets: "_assets",
  },
  markdown: {
    shikiConfig: {
      theme: "github-dark",
    },
  },
});
