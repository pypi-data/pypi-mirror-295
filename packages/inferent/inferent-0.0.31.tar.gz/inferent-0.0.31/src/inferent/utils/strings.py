"""String utility functions"""

import string

def ct(s: str) -> str:
    """ct = cleantext

    Takes a utf-8 string and converts to ascii lower case without punctuation
    """
    if not s:
        return ""
    return (
        s.encode("utf-8")
        .decode("ascii", "ignore")
        .translate(str.maketrans("", "", string.punctuation))
        .lower()
        .strip()
    )
