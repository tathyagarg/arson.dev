import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

export async function GET() {
  const posts = await prisma.post.findMany({
    include: {
      tags: true,
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
  const { title, content, tagNames } = body;

  const tags = await prisma.tag.findMany({
    where: {
      name: {
        in: tagNames,
      },
    },
  })

  const post = await prisma.post.create({
    data: {
      title,
      content,
      tags: {
        connect: tags
      }
    },
  });

  return new Response(JSON.stringify(post), {
    status: 201,
    headers: {
      'Content-Type': 'application/json',
    },
  });
}
