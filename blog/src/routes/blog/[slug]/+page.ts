import type { PageLoad } from './$types';
import { error } from '@sveltejs/kit';

export const load: PageLoad = async ({ fetch, params }) => {
  const { slug } = params;
  console.log(slug);

  const res = await fetch(`/api/post?slug=${slug}`);

  if (res.ok) {
    const post = await res.json();

    const { content } = post;
    // const resp = await fetch('https://md.arson.dev/convert', {
    const resp = await fetch('http://localhost:8000/convert', {
      method: 'POST',
      body: content,
    })

    const html = await resp.text()

    const headers = await fetch('http://localhost:8000/headers', {
      method: 'POST',
      body: content,
    });

    const headersText = await headers.json();

    return { html, headers: headersText };
  }

  throw error(404, 'Post not found');
};


