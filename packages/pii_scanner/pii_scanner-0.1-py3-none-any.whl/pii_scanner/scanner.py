import re
from .patterns import PII_PATTERNS

class PIIScanner:
    def __init__(self):
        self.patterns = PII_PATTERNS

    def scan_text(self, text):
        results = {}
        for pii_type, pattern in self.patterns.items():
            matches = re.findall(pattern, text)
            if matches:
                results[pii_type] = matches
        return results
