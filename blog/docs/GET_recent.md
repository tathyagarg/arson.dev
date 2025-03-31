# GET /api/recent

Get the most recent 5 posts

## Arguments

None

## Response

- `200 OK` on success

## Example Request

```http
GET /api/recent
```

## Example Response

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
    "status": 200,
    "articles": [
        "slug": "example-article",
        "title": "Example Article",
        "created_at": "123456789",
        "banner_url": "https://example.com/banner.jpg",
        "summary": "This is an example article.",
        "tags": [
            {
                "name": "first",
                "color": "#ff0000"
            },
            {
                "name": "post",
                "color": "#00ff00"
            }
        ]
    ]
}
```
