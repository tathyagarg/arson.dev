# POST /api/publish

Publishes a new blog post to the database.

## Arguments

1. `slug` (string): The slug of the blog post.
2. `title` (string): The title of the blog post.
3. `tags` (array of strings): The tags of the blog post.
4. `content` (string): The content of the blog post.
5. `banner_url` (string): The URL of the banner image of the blog post.
6. `summary` (string): The summary of the blog post.
7. `authorization`: The authorization token.

## Responses

1. `201 Created`: The blog post has been successfully published.
2. `422 Unprocessable Entity`: The blog post could not be published due to missing or invalid data.
3. `401 Unauthorized`: The authorization token is invalid or missing.
4. `409 Conflict`: The blog post with the same slug already exists.

## Example Request

```http
POST /api/publish HTTP/1.1
Content-Type: application/json

{
    "slug": "my-first-post",
    "title": "My First Post",
    "tags": ["first", "post"],
    "content": "This is my first post.",
    "banner_url": "https://example.com/banner.jpg",
    "summary": "This is my first post.",
    "authorization": "Password123"
}
```

## Example Response

```http
HTTP/1.1 201 Created
Content-Type: application/json

{
    "status": 201,
    "info": "Blog post created"
}
```
