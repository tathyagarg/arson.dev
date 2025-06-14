import { db, eq, services, pings } from 'astro:db';

export const prerender = false;

export async function GET({ params }) {
  console.log(`Received request for service: ${params.service}`);

  const { service } = params;

  console.log(`Fetching ping data for service: ${service}`);

  const servicePingData = await db.select({
    status: pings.status,
    responseTime: pings.responseTime,
    createdAt: pings.createdAt,
  }).from(pings).where(eq(pings.service, service ?? "")).orderBy(pings.createdAt).limit(50).run();

  console.log(`Fetched ${servicePingData.rows.length} ping records for service: ${service}`);

  return new Response(JSON.stringify(servicePingData.rows), { status: 200, headers: { 'Content-Type': 'application/json' } });
}
