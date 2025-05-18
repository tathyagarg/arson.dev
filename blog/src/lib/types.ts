export type Tag = {
  name: string,
  color: string,
}

export type Post = {
  title: string,
  slug: string,

  content: string,
  excerpt: string,

  tags: Tag[],

  createdAt: string,
  thumbnail: string,
}
