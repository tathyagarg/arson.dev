from datetime import datetime

DISCORD_FIELD_FIELDS = {
    'name': lambda x: isinstance(x, str) and 0 < len(x) <= 256,
    'value': lambda x: isinstance(x, str) and 0 < len(x) <= 1024,
    'inline': lambda x: isinstance(x, bool),
}
DISCORD_FIELD_REQUIRED_FIELDS = ['name', 'value']

def verify_iso8601(date_string):
    try:
        datetime.fromisoformat(date_string)
        return True
    except ValueError:
        return False

def verify_discord_field(data) -> bool:
    if not isinstance(data, dict):
        return False

    for field in DISCORD_FIELD_REQUIRED_FIELDS:
        if field not in data:
            return False
        
        if DISCORD_FIELD_FIELDS[field](data[field]) is False:
            return False

    for field in data:
        if field in DISCORD_FIELD_REQUIRED_FIELDS:
            continue
        if field not in DISCORD_FIELD_FIELDS:
            return False
        if DISCORD_FIELD_FIELDS[field](data[field]) is False:
            return False

    return True

DISCORD_EMBED_FIELDS = {
    'title': lambda x: isinstance(x, str),
    'description': lambda x: isinstance(x, str),
    'url': lambda x: isinstance(x, str),
    'timestamp': lambda x: isinstance(x, str) and verify_iso8601(x),
    'color': lambda x: isinstance(x, int) and 0 <= x <= 0xFFFFFF,
    'footer': lambda x: True,
    'image': lambda x: True,
    'thumbnail': lambda x: True,
    'author': lambda x: True,
    'fields': lambda x: isinstance(x, list) and len(x) <= 25 and all(
        verify_discord_field(field)
        for field in x
    ),
}

def verify_discord_embed(data) -> bool:
    if not isinstance(data, dict):
        return False

    for field in DISCORD_EMBED_FIELDS:
        if field not in data:
            continue
        if DISCORD_EMBED_FIELDS[field](data[field]) is False:
            return False

    return True


DISCORD_REQUIRED_FIELDS = {
    'content': lambda x: isinstance(x, str),
    'embeds': lambda x: isinstance(x, list) and \
        len(x) in range(11) and \
        all(verify_discord_embed(e) for e in x),
}  # any one of these fields is required
DISCORD_OPTIONAL_FIELDS = ['username', 'avatar_url', 'tts', 'allowed_mentions', 'components']

def check_discord_payload_data(payload_data):
    if not isinstance(payload_data, dict):
        return False

    for field in DISCORD_REQUIRED_FIELDS:
        if field in payload_data:
            break
    else:
        return False


CHECK_PAYLOAD_DATA = {
    'discord': check_discord_payload_data,
    # 'slack': check_slack_payload_data,
    # 'email': check_email_payload_data,
    # 'webhook': check_webhook_payload_data,
}

