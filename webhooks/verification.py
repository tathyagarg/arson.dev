from fastapi import Request

import hashlib
import json
import hmac

GITHUB_PUSH_EVENT = 0


async def validate_github_push_event(listener_data: str, request: Request) -> tuple[dict, bool]:
    if request.headers.get('X-GitHub-Event') != 'push':
        return {"error": "Invalid GitHub event type"}, False

    if (sign := request.headers.get('X-Hub-Signature-256')) is None:
        return {"error": "Missing GitHub signature"}, False

    listener_data_obj: dict = json.loads(listener_data)
    message = await request.body()

    hash_object = hmac.new(listener_data_obj['secret'].encode('utf-8'), msg=message, digestmod=hashlib.sha256)
    expected_signature = 'sha256=' + hash_object.hexdigest()

    if not hmac.compare_digest(expected_signature, sign):
        return {"error": "Invalid GitHub signature"}, False

    return {"message": "GitHub push event validated successfully"}, True


VALIDATORS = [GITHUB_PUSH_EVENT]
