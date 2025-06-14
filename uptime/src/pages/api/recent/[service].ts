import type { APIRoute } from 'astro';
import { db, eq, services, pings } from 'astro:db';

export const GET: APIRoute = async ({ params }) => {
  const { service } = params;

  const servicePingData = await db.select({
    status: pings.status,
    responseTime: pings.responseTime,
    createdAt: pings.createdAt,
  }).from(pings).where(eq(pings.service, service ?? "")).orderBy(pings.createdAt).limit(50).run();

  return new Response(JSON.stringify(servicePingData.rows), { status: 200, headers: { 'Content-Type': 'application/json' } });
}

export async function getStaticPaths() {
  const allServices = await db.select().from(services).run();

  return allServices.rows.map(service => ({
    params: { service: service.slug },
  }));
}
