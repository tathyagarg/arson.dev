import { db, services, pings } from 'astro:db';
import { config } from '../../lib/config.ts';
import type { APIContext } from 'astro';

export const prerender = false;

type ServiceData = {
  slug: string;
  url: string;
  name: string;
}

let allServices: ServiceData[] = [];
let lastFetchTime = 0;

const TTL_MINUTES = config.servicesCacheTTL || 60;
const TTL = TTL_MINUTES * 60 * 1000;

async function fetchServices() {
  const now = Date.now();

  if (allServices.length === 0 || (now - lastFetchTime) > TTL) {
    allServices = await db.select().from(services);
    lastFetchTime = now;
  }

  return allServices;
}

export async function GET(context: APIContext) {
  console.log(context.request.headers)
  if (context.request.headers.get('Authorization') !== import.meta.env.SERVICE_PING_SECRET) {
    return new Response('Unauthorized', { status: 401 });
  }

  const servicesList = await fetchServices();

  for (const service of servicesList) {
    let start = Date.now();
    let status;

    try {
      const response = await fetch(service.url, { method: 'HEAD', cache: 'no-cache' });
      status = response.status;
    } catch (error) {
      status = 400;
    }
    const responseTime = Date.now() - start;

    await db.insert(pings).values({
      service: service.slug,
      responseTime,
      status,
      createdAt: new Date(),
    })
  }

  return new Response(JSON.stringify(servicesList), { status: 200 });
}
