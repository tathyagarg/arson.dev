# GET /api/tag

Gets the color of a specific tag.

## Arguments

1. `name` (string): The name of the tag.

## Responses

1. `200 OK`: The color of the tag has been successfully retrieved.
2. `404 Not Found`: The tag does not exist in the database.

## Example Request

```http
GET /api/tag?name=new-tag HTTP/1.1
```

## Example Response

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
    "status": 200,
    "color": "#ff0000"
}
```
