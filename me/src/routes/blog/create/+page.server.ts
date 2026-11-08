import { prisma } from "$lib/server/prisma";
import { redirect, type Actions } from "@sveltejs/kit";
import type { PageServerLoad } from "../$types";
import { hasPerm, PostCreate } from "$lib/perms";

import { load } from "cheerio";
import hljs from "highlight.js/lib/common";

export const prerender = false;

export const load: PageServerLoad = async ({ locals }) => {
  const role = locals.user?.role || "user";

  if (!hasPerm(role, PostCreate)) {
    return redirect(308, "/blog?err=403");
  }

  return {};
};

export const actions = {
  default: async ({ locals, request }) => {
    const user = locals.user;

    if (!user) {
      return {
        status: 403,
        error: new Error("You must be logged in to create a post"),
      };
    }

    if (!hasPerm(user.role, PostCreate)) {
      return {
        status: 403,
        error: new Error("You do not have permission to create a post"),
      };
    }

    const data = await request.formData();

    const title = data.get("title");
    const content = data.get("content");
    const published = data.get("published") === "on";

    if (typeof title !== "string" || typeof content !== "string") {
      return {
        status: 400,
        error: new Error("Invalid title or content"),
      };
    }

    // Parse the submitted HTML
    const $ = load(content, {}, false);

    // Highlight all code blocks
    $("pre code").each((_, element) => {
      const code = $(element);

      const className = code.attr("class") ?? "";

      const languageMatch = className.match(
        /\blanguage-([\w+-]+)\b/
      );

      if (!languageMatch) {
        return;
      }

      const language = languageMatch[1];

      // Avoid errors for unsupported languages
      if (!hljs.getLanguage(language)) {
        return;
      }

      const source = code.text();

      const highlighted = hljs.highlight(source, {
        language,
      });

      // Replace the original code with highlighted HTML
      code.html(highlighted.value);
    });

    const highlightedContent = $.html();

    await prisma.post.create({
      data: {
        title,
        content: highlightedContent,
        published,
        publishedAt: published ? new Date() : null,
      },
    });

    return { success: true };
  },
} satisfies Actions;
