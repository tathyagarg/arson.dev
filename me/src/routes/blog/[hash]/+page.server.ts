import { prisma } from "$lib/server/prisma"
import bcrypt from "bcryptjs";
import type { PageServerLoad } from "../$types";
import { hasPerm, type Role } from "$lib/perms";

export const load: PageServerLoad = async ({ params, cookies }) => {
  // get user data
  let role = "user";

  if (cookies.get("arsonist__pass")) {
    let username = cookies.get("arsonist__username");
    let pass = cookies.get("arsonist__pass") ?? "";

    const user = await prisma.user.findFirst({
      where: {
        username: username,
      },
    });

    if (!user) {
      return;
    }

    const isValid = await bcrypt.compare(pass, user.password);

    if (!isValid) {
      return;
    }

    role = user.role;
  }

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
