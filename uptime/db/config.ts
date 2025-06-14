import { defineDb, defineTable, column, NOW } from 'astro:db';

const services = defineTable({
  columns: {
    id: column.number({ primaryKey: true, autoIncrement: true }),
    slug: column.text({ unique: true }),
    name: column.text({ unique: true }),
    url: column.text({ unique: true }),
    createdAt: column.date({ default: NOW }),
  }
})

const pings = defineTable({
  columns: {
    id: column.number({ primaryKey: true, autoIncrement: true }),
    service: column.text({ references: () => services.columns.slug }),
    status: column.number(),
    responseTime: column.number(),
    createdAt: column.date({ default: NOW }),
  }
});

export default defineDb({
  tables: {
    services,
    pings
  }
});
