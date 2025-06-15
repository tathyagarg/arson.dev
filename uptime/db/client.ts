import { drizzle } from 'drizzle-orm/node-postgres';
import { Pool } from "pg";

const pool = new Pool({
  host: import.meta.env.DB_HOST ?? 'localhost',
  port: parseInt(import.meta.env.DB_PORT ?? '5432', 10),
  user: import.meta.env.DB_USER ?? 'postgres',
  password: import.meta.env.DB_PASSWORD ?? 'password',
  database: import.meta.env.DB_NAME ?? 'postgres',
})

export const db = drizzle(pool);
