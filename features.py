# features/extractor.py
import re
import tldextract
from urllib.parse import urlparse
import socket

class FeatureExtractor:
    def __init__(self, url):
        self.url = str(url).strip()
        # ensure a scheme so urlparse and tldextract behave consistently
        if not self.url.startswith(("http://", "https://")):
            self.normalized = "http://" + self.url
        else:
            self.normalized = self.url
        self.parsed = urlparse(self.normalized)
        self.extracted = tldextract.extract(self.normalized)
        self.domain = self.extracted.registered_domain or ""
        self.subdomain = self.extracted.subdomain or ""

    # URL-based features (kept same names as your original code)
    def having_ip(self):
        return 1 if re.search(r'(\d{1,3}\.){3}\d{1,3}', self.url) else 0

    def url_length(self):
        return len(self.url)

    def shortening_service(self):
        return 1 if re.search(r"bit\.ly|goo\.gl|tinyurl|ow\.ly|t\.co|is\.gd|adf\.ly", self.url, re.IGNORECASE) else 0

    def having_at_symbol(self):
        return 1 if "@" in self.url else 0

    def double_slash_redirect(self):
        # count '//' occurrences (scheme 'http://' counts as 1)
        return 1 if self.url.count("//") > 1 else 0

    def prefix_suffix(self):
        return 1 if "-" in self.domain else 0

    def having_sub_domain(self):
        return len([p for p in self.subdomain.split('.') if p]) if self.subdomain else 0

    def https_token(self):
        # token 'https' inside hostname/subdomain (suspicious)
        host = self.parsed.netloc.lower().split(':')[0]
        return 1 if 'https' in host else 0

    def port(self):
        try:
            p = self.parsed.port
            return 1 if (p is not None and p not in (80, 443)) else 0
        except Exception:
            return 0

    def ssl_final_state(self):
        return 1 if self.parsed.scheme == "https" else 0

    def dns_record(self):
        # quick DNS check (may be slow); returns 1 if resolves, 0 otherwise
        if not self.domain:
            return 0
        try:
            socket.setdefaulttimeout(2.0)
            socket.getaddrinfo(self.domain, None)
            return 1
        except Exception:
            return 0

    def get_features(self):
        # Return dict with exactly the features your model expects (plus url if desired)
        return {
            "url": self.url,
            "having_ip": self.having_ip(),
            "url_length": self.url_length(),
            "shortening_service": self.shortening_service(),
            "having_at_symbol": self.having_at_symbol(),
            "double_slash_redirect": self.double_slash_redirect(),
            "prefix_suffix": self.prefix_suffix(),
            "having_sub_domain": self.having_sub_domain(),
            "https_token": self.https_token(),
            "port": self.port(),
            "ssl_final_state": self.ssl_final_state(),
            "dns_record": self.dns_record(),
            # keep ssl_certificate placeholder to match training pipeline if used
            "ssl_certificate": 1
        }
