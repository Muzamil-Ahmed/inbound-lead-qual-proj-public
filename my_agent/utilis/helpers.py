import re
from typing import Optional


# Helper function to check if a given url is valid
def is_valid_url(url: Optional[str]) -> bool:
    """Checks if a given string is a valid URL."""
    if not url or not isinstance(url, str):
        return False
    # Simple regex for URL validation.
    regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)'  # domain
        r'(:\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return re.match(regex, url) is not None