import { hasPerm, type Role } from "$lib/perms";
import { prisma } from "$lib/server/prisma"
import type { PageServerLoad } from "./$types";

export const prerender = false;

export const load: PageServerLoad = async ({ locals }) => {
  console.log("Loading posts for user:", locals.user);
  const role = locals.user?.role || "user";

  let includeUnpublished = hasPerm(role as Role, "unpublished::view");

  const posts = await prisma.post.findMany({
    orderBy: {
      createdAt: "desc",
    },
    include: { content: false },
    where: {
      published: includeUnpublished ? undefined : true,
    },
  });

  return {
    posts,
    role,
  }
}
