// @ts-check
import { defineConfig } from 'astro/config';

import tailwindcss from '@tailwindcss/vite';

import db from '@astrojs/db';

import node from '@astrojs/node';

// https://astro.build/config
export default defineConfig({
  vite: {
    plugins: [tailwindcss()]
  },

  integrations: [db()],

  adapter: node({
    mode: 'standalone'
  })
});