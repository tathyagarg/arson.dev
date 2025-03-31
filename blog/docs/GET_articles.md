# GET /api/articles

Gets all articles in the database.

## Arguments

None.

## Responses

1. `200 OK`: The articles have been successfully retrieved.

## Example Request

```http
GET /api/articles HTTP/1.1
```

## Example Response

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
    "status": 200,
    "articles": [
        {
            "title": "My First Post",
            "content": "This is my first post.",
            "created_at": "123456789",
        },
        {
            "title": "My Second Post",
            "content": "This is my second post.",
            "created_at": "123456789",
        }
    ]
}
```
