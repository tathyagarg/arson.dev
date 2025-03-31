# GET /api/blog/{slug}

Gets a specific blog post from the database.

## Arguments

1. `slug` (string): The slug of the blog post.

## Responses

1. `200 OK`: The blog post has been successfully retrieved.

## Example Request

```http
GET /api/blog/my-first-post HTTP/1.1
```

## Example Response

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
    "status": 200,
    "blog": {
        "title": "My First Post",
        "content": "This is my first post.",
        "created_at": "123456789",
    }
}
```
