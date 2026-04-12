export type Role = "admin" | "user";
export type Perm = number;

export type PermMap = {
  readonly [R in Role]: Perm;
};

export const PostCreate = 0x1;
export const PostDelete = 0x2;
export const PostEdit = 0x4;
export const PostView = 0x8;
export const PostUnpublish = 0x10;
export const UnpublishedView = 0x20;
export const UnpublishedEdit = 0x40;
export const UnpublishedDelete = 0x80;
export const UnpublishedPublish = 0x100;
export const CommentCreate = 0x200;
export const CommentDelete = 0x2400;
export const CommentEdit = 0x800;
export const CommentView = 0x1000;
export const CommentOwnedDelete = 0x2000;

const PERM_MAP: PermMap = {
  "admin": PostCreate | PostDelete | PostEdit | PostView | PostUnpublish |
    UnpublishedView | UnpublishedEdit | UnpublishedDelete | UnpublishedPublish |
    CommentCreate | CommentDelete | CommentEdit | CommentView,
  "user": PostView | CommentCreate | CommentOwnedDelete | CommentEdit | CommentView,
}

export function hasPerm(role: Role, perm: Perm): boolean {
  return PERM_MAP[role] & perm ? true : false;
}
