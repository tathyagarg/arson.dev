import prisma from '$lib/server/prisma';

export async function GET() {
  const posts = await prisma.post.findMany({
    include: {
      tags: true,
    },
    orderBy: {
      createdAt: 'desc',
    },
    take: 6,
  });

  return new Response(JSON.stringify(posts), {
    status: 200,
    headers: {
      'Content-Type': 'application/json',
    },
  });
}
