import { pgTable, serial, text, integer, timestamp } from 'drizzle-orm/pg-core';

export const services = pgTable('services', {
  id: serial('id').primaryKey(),
  slug: text('slug').notNull().unique(),
  name: text('name').notNull(),
  url: text('url').notNull(),
  createdAt: timestamp('created_at', { withTimezone: true }).defaultNow(),
})

export const pings = pgTable('pings', {
  id: serial('id').primaryKey(),
  service: text('service')
    .notNull()
    .references(() => services.slug, { onDelete: 'cascade' }),
  status: integer('status').notNull(),
  responseTime: integer('response_time').notNull(),
  createdAt: timestamp('created_at', { withTimezone: true }).defaultNow(),
});
