thonpython
import re
from typing import List

EMAIL_REGEX = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"

def extract_emails_from_text(text: str) -> List[str]:
    """Return all unique emails from text."""
    found = re.findall(EMAIL_REGEX, text)
    return list(set(found))