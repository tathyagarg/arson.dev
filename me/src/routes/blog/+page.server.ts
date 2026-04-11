import { prisma } from "$lib/server/prisma"
import type { Cookies } from "@sveltejs/kit";
import bcrypt from "bcryptjs";

export const load = async ({ cookies }: { cookies: Cookies }) => {
  console.log(await bcrypt.hash('tattuuu', 10));

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

    console.log("User", user)
    role = user.role;
  }

  const posts = await prisma.post.findMany({
    orderBy: {
      createdAt: "desc",
    },
    include: { content: false }
  });

  return {
    posts,
    role: role ?? "user",
  }
}
