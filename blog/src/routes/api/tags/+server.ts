import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

export async function GET(tag) {
  const posts = await prisma.post.findMany({
    where: {
      tags: {
        some: {
          name: tag,
        },
      },
    },
  });

  return new Response(JSON.stringify(posts), {
    status: 200,
    headers: {
      'Content-Type': 'application/json',
    },
  });
}

export async function POST({ request }) {
  const body = await request.json();
  const { name, color } = body;

  const tag = await prisma.tag.create({
    data: {
      name,
      color,
    },
  });

  return new Response(JSON.stringify(tag), {
    status: 201,
    headers: {
      'Content-Type': 'application/json',
    },
  });
}
