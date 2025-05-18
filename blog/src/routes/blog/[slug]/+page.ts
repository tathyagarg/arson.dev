import type { PageLoad } from './$types';
import { error } from '@sveltejs/kit';

export const load: PageLoad = async ({ fetch, params }) => {
  const { slug } = params;
  console.log(slug);

  const res = await fetch(`/api/post?slug=${slug}`);

  if (res.ok) {
    const post = await res.json();
    return { post };
  }

  throw error(404, 'Post not found');
};


