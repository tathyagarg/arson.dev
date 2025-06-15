import { services } from './schema.ts';
import { db } from './client.ts';
import { config } from '../src/lib/config.ts';

for (const [name, _service] of Object.entries(config.services) as [string, { name: string; url: string }][]) {
  console.log(`Seeding service: ${name} (${_service.name}) at ${_service.url}`);
  const service = {
    slug: name,
    name: _service.name,
    url: _service.url,
  };

  await db.insert(services).values(service).onConflictDoNothing();
}
