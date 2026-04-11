import { prisma } from "$lib/server/prisma"
import bcrypt from "bcryptjs";
import type { PageServerLoad } from "../$types";
import { hasPerm, type Role } from "$lib/perms";

export const load: PageServerLoad = async ({ params, locals }) => {
  let role = locals.user?.role || "user";

  let data = await prisma.post.findUnique({
    where: {
      hash: params.hash,
    },
  });

  if (!data) {
    return {
      status: 404,
      error: new Error("Post not found"),
    }
  }

  if (!data.published && !hasPerm(role as Role, "unpublished::view")) {
    return {
      status: 403,
      error: new Error("You do not have permission to view this post"),
    }
  }

  if (!hasPerm(role as Role, "post::view")) {
    return {
      status: 403,
      error: new Error("You do not have permission to view this post"),
    }
  }

  return {
    post: data,
  }
}
