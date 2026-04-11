import { prisma } from '$lib/server/prisma';
import type { Handle } from '@sveltejs/kit';

export const handle: Handle = async ({ event, resolve }) => {
  console.log("YOOYOYO");
  const sessionId = event.cookies.get("sessionId");

  if (sessionId) {
    // @ts-expect-error
    const session = await prisma.session.findUnique({
      where: { id: sessionId },
      include: { user: true }
    });

    if (session && session.expiresAt > new Date()) {
      event.locals.user = session.user;
    } else {
      event.locals.user = null;
    }
  } else {
    event.locals.user = null;
  }

  const result = await resolve(event);
  return result;
};
