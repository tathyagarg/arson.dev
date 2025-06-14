import { db, eq, services } from 'astro:db';
import { config } from '../src/lib/config.ts';

export default async function seed() {
  for (const [name, _service] of Object.entries(config.services)) {
    let service = _service as { name: string; url: string };

    const existingService = await db.select().from(services).where(eq(services.name, service.name));

    if (existingService.length === 0) {
      console.log(`Seeding service: ${service.name} (${service.url})`);

      await db.insert(services).values({
        slug: name,
        name: service.name,
        url: service.url,
      });
    } else {
      console.log(`Service already exists: ${service.name} (${service.url})`);
    }
  }
}
