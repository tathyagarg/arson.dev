import { db, eq, pings, desc } from 'astro:db';

export const prerender = false;

export async function GET({ params }) {
  console.log(`Received request for service: ${params.service}`);

  const { service } = params;

  console.log(`Fetching ping data for service: ${service}`);

  const servicePingData = await db.select({
    status: pings.status,
    responseTime: pings.responseTime,
    createdAt: pings.createdAt,
  }).from(pings).where(eq(pings.service, service ?? "")).orderBy(desc(pings.createdAt)).limit(50).run();

  console.log(`Fetched ${servicePingData.rows.length} ping records for service: ${service}`);

  return new Response(JSON.stringify({
    pings: servicePingData.rows.reverse(),
    average: servicePingData.rows.reduce((acc, ping) => acc + (ping.responseTime as number), 0) / servicePingData.rows.length || 0,
  }), { status: 200, headers: { 'Content-Type': 'application/json' } });
}
