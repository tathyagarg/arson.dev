import { prisma } from "$lib/server/prisma";
import type { Actions } from "@sveltejs/kit";
import bcrypt from "bcryptjs";

export const prerender = false;

export const actions = {
  default: async ({ cookies, request }) => {
    const data = await request.formData();

    const username = data.get("username");
    const password = data.get("password");

    console.log("Received login attempt:", { username, password });

    if (typeof username !== "string" || typeof password !== "string") {
      return { success: false, error: "Invalid form data" };
    }

    const user = await prisma.user.findUnique({ where: { username } });
    if (!user) {
      return { success: false, error: "Invalid username or password" };
    }

    const isValidPassword = await bcrypt.compare(password, user.password);
    if (!isValidPassword) {
      return { success: false, error: "Invalid username or password" };
    }

    const session = await prisma.session.create({
      data: {
        userId: user.uuid,
        expiresAt: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000), // 7 days
      },
    });

    cookies.set("sessionId", session.id, {
      path: "/",
      httpOnly: true,
      secure: process.env.NODE_ENV === "production",
      sameSite: "lax",
      maxAge: 7 * 24 * 60 * 60, // 7 days
    });

    return { success: true };
  }
} satisfies Actions;
