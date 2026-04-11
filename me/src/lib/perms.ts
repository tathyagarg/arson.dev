export type Role = "admin";
export type Perm = `${string}::${string}`;

export type PermMap = {
  readonly [R in Role]: readonly Perm[];
};

const PERM_MAP: PermMap = {
  "admin": ["post::create", "post::delete", "post::edit", "post::view",
    "unpublished::view", "unpublished::edit", "unpublished::delete", "unpublished::publish"],
}

export function hasPerm(role: Role, perm: Perm): boolean {
  return PERM_MAP[role].includes(perm);
}
