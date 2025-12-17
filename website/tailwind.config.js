import type { Config } from 'tailwindcss';

export default {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
    "./docs/**/*.{md,mdx}",
    "./blog/**/*.{md,mdx}",
    "./pages/**/*.{js,jsx,ts,tsx}",
    "./node_modules/@docusaurus/core/lib/**/*.js",
    "./node_modules/@docusaurus/theme-classic/lib/**/*.js",
    "./node_modules/@docusaurus/theme-live-codeblock/lib/**/*.js",
    "./node_modules/@docusaurus/theme-search-algolia/lib/**/*.js",
    "./node_modules/@docusaurus/preset-classic/lib/**/*.js",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
  corePlugins: {
    preflight: true,
  },
} satisfies Config;