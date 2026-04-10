
import { VERCEL_GIT_COMMIT_SHA } from "$env/static/private";

export const prerender = true;

export const load = () => {
  return {
    commitSha: VERCEL_GIT_COMMIT_SHA
  };
}
