import os
import sys
import django

# Setup django environment
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.test import Client
from django.urls import reverse

def debug_download():
    client = Client()
    print("Testing POST /api/video/download/ with a short video...")
    res = client.post(
        reverse('video_download'),
        data={"url": "https://www.youtube.com/watch?v=jNQXAC9IVRw", "quality": "best"},
        content_type="application/json"
    )
    print("Status code:", res.status_code)
    if res.status_code != 200:
        print("Response content:", res.content.decode('utf-8', errors='ignore'))
    else:
        print("Success! Content-Type:", res.get('Content-Type'))
        print("Content-Disposition:", res.get('Content-Disposition'))
        # Consume stream
        content = b''.join(res.streaming_content)
        print("Streamed bytes:", len(content))

if __name__ == "__main__":
    debug_download()
