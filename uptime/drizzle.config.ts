import { defineConfig } from 'drizzle-kit';

const import_ctx = import.meta.env ?? process.env;

export default defineConfig({
  schema: './db/schema.ts',
  out: './drizzle',
  dialect: 'postgresql',
  dbCredentials: {
    host: import_ctx.DB_HOST ?? 'localhost',
    port: parseInt(import_ctx.DB_PORT ?? '5432', 10),
    user: import_ctx.DB_USER ?? 'postgres',
    password: import_ctx.DB_PASSWORD ?? 'password',
    database: import_ctx.DB_NAME ?? 'postgres',
    ssl: false,
  },
});
