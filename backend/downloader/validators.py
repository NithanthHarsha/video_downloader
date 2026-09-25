import ipaddress
import re
import socket
from urllib.parse import urlparse
from typing import Tuple, Optional

# Regex for valid HTTP/HTTPS URLs
VALID_URL_REGEX = re.compile(
    r'^(https?:\/\/)?' # http:// or https://
    r'(([a-zA-Z0-9_-]+\.)+[a-zA-Z]{2,})' # domain
    r'(:\d+)?' # optional port
    r'(\/[a-zA-Z0-9_\-\.~%!$&\'()*+,;=:@/]*)*' # path
    r'(\?[a-zA-Z0-9_\-\.~%!$&\'()*+,;=:@/?]*)?' # query string
    r'(#[a-zA-Z0-9_\-\.~%!$&\'()*+,;=:@/?]*)?$', # fragment
    re.IGNORECASE
)

# Blocked loopback, internal, link-local, cloud metadata ranges
BLOCKED_IP_NETWORKS = [
    ipaddress.ip_network("127.0.0.0/8"),       # Loopback
    ipaddress.ip_network("10.0.0.0/8"),        # Private Class A
    ipaddress.ip_network("172.16.0.0/12"),     # Private Class B
    ipaddress.ip_network("192.168.0.0/16"),    # Private Class C
    ipaddress.ip_network("169.254.0.0/16"),    # Link-local / Cloud metadata (AWS, GCP, Azure)
    ipaddress.ip_network("0.0.0.0/8"),         # Broadcast/this host
    ipaddress.ip_network("::1/128"),           # IPv6 loopback
    ipaddress.ip_network("fc00::/7"),          # IPv6 Unique Local
    ipaddress.ip_network("fe80::/10"),         # IPv6 Link-local
]

BLOCKED_HOSTNAMES = {
    "localhost",
    "metadata.google.internal",
    "169.254.169.254",
    "instance-data",
}

def validate_video_url(url: str) -> Tuple[bool, Optional[str]]:
    """
    Validates that a URL is a valid, publicly routable HTTP/HTTPS URL
    and prevents SSRF (Server-Side Request Forgery) attacks.
    """
    if not url or not isinstance(url, str):
        return False, "URL cannot be empty."

    url = url.strip()
    if len(url) > 2048:
        return False, "URL is too long."

    if not (url.startswith("http://") or url.startswith("https://")):
        return False, "URL must start with http:// or https://"

    if not VALID_URL_REGEX.match(url):
        return False, "Invalid URL structure."

    try:
        parsed = urlparse(url)
        hostname = parsed.hostname
        if not hostname:
            return False, "Invalid URL host."

        hostname_lower = hostname.lower()

        # Check blocked hostnames
        if hostname_lower in BLOCKED_HOSTNAMES:
            return False, "Access to local or private networks is strictly prohibited."

        # Check direct IP addresses
        try:
            ip = ipaddress.ip_address(hostname)
            for blocked_net in BLOCKED_IP_NETWORKS:
                if ip in blocked_net:
                    return False, "Access to private or local network IP addresses is prohibited."
        except ValueError:
            # Resolved IP SSRF check
            try:
                resolved_ips = socket.getaddrinfo(hostname, None)
                for res in resolved_ips:
                    sockaddr = res[4]
                    ip_str = sockaddr[0]
                    ip = ipaddress.ip_address(ip_str)
                    for blocked_net in BLOCKED_IP_NETWORKS:
                        if ip in blocked_net:
                            return False, "Resolved domain points to an internal or restricted network address."
            except (socket.gaierror, ValueError):
                pass

        return True, None

    except Exception as e:
        return False, f"URL validation failed: {str(e)}"
