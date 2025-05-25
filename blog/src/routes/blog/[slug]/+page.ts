import type { PageLoad } from './$types';
import { error } from '@sveltejs/kit';

import { PUBLIC_ENV } from '$env/static/public';

const MD_API_URL = PUBLIC_ENV === 'production' ? 'https://md.arson.dev' : 'http://localhost:8000';

export const load: PageLoad = async ({ fetch, params }) => {
  const { slug } = params;

  const res = await fetch(`/api/posts?slug=${slug}`);

  if (res.ok) {
    const post = await res.json();

    const { title, content } = post;
    const resp = await fetch(`${MD_API_URL}/convert`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ markdown: content }),
    })

    const html = await resp.text()

    const headingsData = await fetch(`${MD_API_URL}/headings`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ markdown: content }),
    });

    const headings = await headingsData.json();

    return { html, headings, title };
  }

  throw error(404, 'Post not found');
};


