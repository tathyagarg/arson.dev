import { db } from '../../../../db/client.ts'
import { pings } from '../../../../db/schema.ts';
import { eq, desc } from 'drizzle-orm';

export const prerender = false;

export async function GET({ params }: { params: { service: string } }) {
  console.log(`Received request for service: ${params.service}`);

  const { service } = params;

  console.log(`Fetching ping data for service: ${service}`);

  const servicePingData = await db.select({
    status: pings.status,
    responseTime: pings.responseTime,
    createdAt: pings.createdAt,
  }).from(pings).where(eq(pings.service, service ?? "")).orderBy(desc(pings.createdAt)).limit(50);

  console.log(`Fetched ${servicePingData.length} ping records for service: ${service}`);

  return new Response(JSON.stringify({
    pings: servicePingData.reverse(),
    average: servicePingData.reduce((acc, ping) => acc + (ping.responseTime as number), 0) / servicePingData.length || 0,
  }), { status: 200, headers: { 'Content-Type': 'application/json' } });
}
