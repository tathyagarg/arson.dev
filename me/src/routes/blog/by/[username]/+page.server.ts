import { prisma } from "$lib/server/prisma";
import type { PageServerLoad } from "./$types";

export const prerender = false;

export const load: PageServerLoad = async ({ params }) => {
  const username = params.username;

  const user = await prisma.user.findUnique({
    where: {
      username,
    },
    select: {
      uuid: true,
    },
  });

  const posts = await prisma.post.findMany({
    where: {
      // @ts-expect-error
      authorId: user?.id,
      published: true,
    },
    orderBy: {
      createdAt: "desc",
    },
    include: {
      // @ts-expect-error
      content: false,
    }
  });

  return {
    posts,
    username,
  }
}
