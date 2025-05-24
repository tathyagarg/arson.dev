import { PASSPHRASE } from '$env/static/private';
import prisma from '$lib/server/prisma';

export async function GET({ url }) {
  const tag = url.searchParams.get('tag');

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
  const { name, color, passphrase } = body;
  if (passphrase !== PASSPHRASE) {
    return new Response('Invalid passphrase', {
      status: 401,
      headers: {
        'Content-Type': 'application/json',
      },
    });
  }

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
