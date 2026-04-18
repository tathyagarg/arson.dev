import { db } from '../../../../db/client'
import { pings } from '../../../../db/schema';
import { eq, desc } from 'drizzle-orm';

export const prerender = false;

export async function GET({ params }: { params: { service: string } }) {
  const { service } = params;

  const servicePingData = await db.select({
    status: pings.status,
    responseTime: pings.responseTime,
    createdAt: pings.createdAt,
  }).from(pings).where(eq(pings.service, service ?? "")).orderBy(desc(pings.createdAt)).limit(50);

  return new Response(JSON.stringify({
    pings: servicePingData.reverse(),
    average: servicePingData.reduce((acc, ping) => acc + (ping.responseTime as number), 0) / servicePingData.length || 0,
  }), { status: 200, headers: { 'Content-Type': 'application/json' } });
}
