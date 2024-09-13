import re
from urllib.parse import urlparse
from uuid import UUID


def extract_uuid_from_url(url: str) -> UUID | None:
    try:
        parsed_url = urlparse(url)
        path = parsed_url.path
        uuid_pattern = r'([a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})$'
        match = re.search(uuid_pattern, path)
        if not match:
            return None

        return UUID(match.group(1))
    except Exception:
        return None
