# GET /api/tags

Gets all tags in the database.

## Arguments

None.

## Responses

1. `200 OK`: The tags have been successfully retrieved.

## Example Request

```http
GET /api/tags HTTP/1.1
```

## Example Response

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
    "status": 200,
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
}
```
