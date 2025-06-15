import { drizzle } from 'drizzle-orm/node-postgres';
import { Pool } from "pg";

const import_context = import.meta.env ?? process.env;

const pool = new Pool({
  host: import_context.DB_HOST ?? 'localhost',
  port: parseInt(import_context.DB_PORT ?? '5432', 10),
  user: import_context.DB_USER ?? 'postgres',
  password: import_context.DB_PASSWORD ?? 'password',
  database: import_context.DB_NAME ?? 'postgres',
})

export const db = drizzle(pool);
