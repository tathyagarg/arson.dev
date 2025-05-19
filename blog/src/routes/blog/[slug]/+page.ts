import type { PageLoad } from './$types';
import { error } from '@sveltejs/kit';

export const load: PageLoad = async ({ fetch, params }) => {
  const { slug } = params;
  console.log(slug);

  const res = await fetch(`/api/post?slug=${slug}`);

  if (res.ok) {
    const post = await res.json();

    const { content } = post;
    const resp = await fetch('https://md.arson.dev/convert', {
      method: 'POST',
      body: content,
    })

    const html = await resp.text()

    return { html };
  }

  throw error(404, 'Post not found');
};


