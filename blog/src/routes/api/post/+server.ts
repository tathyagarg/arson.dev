import prisma from '$lib/server/prisma';

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
