# features/extractor.py
import re
import tldextract
from urllib.parse import urlparse
import socket

class FeatureExtractor:
    def __init__(self, url: str):
        self.url = str(url).strip()
        # Default to HTTPS if no scheme is given
        if not self.url.startswith(("http://", "https://")):
            self.normalized = "https://" + self.url
        else:
            self.normalized = self.url

        self.parsed = urlparse(self.normalized)
        self.extracted = tldextract.extract(self.normalized)
        self.domain = self.extracted.registered_domain or ""
        self.subdomain = self.extracted.subdomain or ""

    # --- URL-based features (1 = phishing, 0 = legit) ---
    def having_ip(self):
        return 1 if re.search(r'(\d{1,3}\.){3}\d{1,3}', self.url) else 0

    def url_length(self):
        # keep raw length, not binary
        return len(self.url)

    def shortening_service(self):
        return 1 if re.search(
            r"bit\.ly|goo\.gl|tinyurl|ow\.ly|t\.co|is\.gd|adf\.ly",
            self.url,
            re.IGNORECASE,
        ) else 0

    def having_at_symbol(self):
        return 1 if "@" in self.url else 0

    def double_slash_redirect(self):
        return 1 if self.url.find("//", 8) != -1 else 0

    def prefix_suffix(self):
        return 1 if "-" in self.domain else 0

    def having_sub_domain(self):
        # ignore "www" (common legit subdomain)
        if not self.subdomain or self.subdomain == "www":
            return 0
        return 1

    def https_token(self):
        host = self.parsed.netloc.lower().split(":")[0]
        return 1 if "https" in host else 0

    def port(self):
        try:
            p = self.parsed.port
            return 1 if (p is not None and p not in (80, 443)) else 0
        except Exception:
            return 0

    def ssl_final_state(self):
        # HTTPS = safe (0), HTTP = phishing (1)
        return 0 if self.parsed.scheme == "https" else 1

    def dns_record(self):
        if not self.domain:
            return 1  # no domain = suspicious
        try:
            socket.setdefaulttimeout(2.0)
            socket.getaddrinfo(self.domain, None)
            return 0  # resolves → legit
        except Exception:
            return 1  # no DNS → phishing

    def get_features(self):
        """
        Returns dict with features (1 = phishing, 0 = legit).
        Feature set matches the training CSV.
        """
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
            "ssl_certificate": 0,  # placeholder for compatibility
        }


