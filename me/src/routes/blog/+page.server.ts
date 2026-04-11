import { hasPerm, type Role } from "$lib/perms";
import { prisma } from "$lib/server/prisma"
import type { PageServerLoad } from "./$types";

export const load: PageServerLoad = async ({ locals }) => {
  console.log("Loading posts for user:", locals.user);
  const user = locals.user!;

  let includeUnpublished = hasPerm(user.role as Role, "unpublished::view");

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
    role: user.role,
  }
}
