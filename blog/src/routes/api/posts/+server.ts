import { PASSPHRASE } from '$env/static/private';
import prisma from '$lib/server/prisma';

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
  const { title, slug, content, excerpt, tagNames, passphrase } = body;

  if (passphrase !== PASSPHRASE) {
    return new Response('Invalid passphrase', {
      status: 403,
      headers: {
        'Content-Type': 'application/json',
      },
    });
  }

  const tags = await prisma.tag.findMany({
    where: {
      name: {
        in: tagNames,
      },
    },
  })

  const post = await prisma.post.create({
    data: {
      slug,
      title,
      content,
      excerpt,
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
