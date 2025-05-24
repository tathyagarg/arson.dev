import { PASSPHRASE } from '$env/static/private';
import prisma, { PostRequest } from '$lib/server/prisma';

export async function GET(event) {
  const params = event.url.searchParams;
  const slug = params.get('slug');

  if (!slug) {
    return new Response('Slug is required', { status: 400 });
  }

  try {
    const post = await prisma.post.findUnique({
      where: { slug },
    });

    if (!post) {
      return new Response('Post not found', { status: 404 });
    }

    return new Response(JSON.stringify(post), {
      headers: { 'Content-Type': 'application/json' },
    });
  } catch (error) {
    console.error('Error fetching post:', error);
    return new Response('Internal Server Error', { status: 500 });
  } finally {
    await prisma.$disconnect();
  }
}

export async function POST({ request }) {
  const body = await request.json();
  const { passphrase, ...postData } = body;

  if (passphrase !== PASSPHRASE) {
    return new Response('Invalid passphrase', {
      status: 401,
      headers: {
        'Content-Type': 'application/json',
      },
    });
  }

  const tags = await prisma.tag.findMany({
    where: {
      name: {
        in: postData.tagNames,
      },
    },
  })

  let { tagNames, ...createData } = postData;

  const post = await prisma.post.create({
    data: {
      ...createData,
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
