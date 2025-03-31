# POST /api/tag

Creates a new tag in the database.

## Arguments

1. `name` (string): The name of the tag.
2. `color` (string): The color of the tag.
3. `authorization`: The authorization token.

## Responses

1. `201 Created`: The tag has been successfully created.
2. `422 Unprocessable Entity`: The tag could not be created due to missing or invalid data.
3. `401 Unauthorized`: The authorization token is invalid or missing.
4. `200 OK`: The tag with the same name already exists.

## Example Request

```http
POST /api/tag HTTP/1.1
Content-Type: application/json

{
    "name": "new-tag",
    "color": "#ff0000",
    "authorization": "Password123"
}
```

## Example Response

```http
HTTP/1.1 201 Created
Content-Type: application/json

{
    "status": 201,
    "info": "Tag created"
}
```
