export type Role = "admin" | "user";
export type Perm = `${string}::${string}`;

export type PermMap = {
  readonly [R in Role]: readonly Perm[];
};

const PERM_MAP: PermMap = {
  "admin": ["post::create", "post::delete", "post::edit", "post::view", "post::unpublish",
    "unpublished::view", "unpublished::edit", "unpublished::delete", "unpublished::publish"],
  "user": ["post::view"],
}

export function hasPerm(role: Role, perm: Perm): boolean {
  return PERM_MAP[role].includes(perm);
}
