import httpx
import json

def test_api():
    base_url = "http://127.0.0.1:8000"
    
    # 1. Health check
    print("Testing /api/health...")
    r = httpx.get(f"{base_url}/api/health")
    print(f"Health response ({r.status_code}):", r.json())
    assert r.status_code == 200
    assert r.json()["status"] == "ok"

    # 2. Invalid URL
    print("\nTesting /api/video/info with invalid URL...")
    r = httpx.post(f"{base_url}/api/video/info", json={"url": "http://127.0.0.1:8000/internal"})
    print(f"Invalid URL response ({r.status_code}):", r.json())
    assert r.json()["success"] is False
    assert r.json()["error"]["code"] == "INVALID_URL"

    # 3. Valid public video info
    print("\nTesting /api/video/info with public video (https://www.youtube.com/watch?v=aqz-KE-bpKQ)...")
    r = httpx.post(f"{base_url}/api/video/info", json={"url": "https://www.youtube.com/watch?v=aqz-KE-bpKQ"}, timeout=30.0)
    data = r.json()
    # 4. Test initiating download of a small audio or low-res format
    print("\nTesting /api/video/download (Audio MP3)...")
    dl_req = httpx.post(f"{base_url}/api/video/download", json={
        "url": "https://www.youtube.com/watch?v=aqz-KE-bpKQ",
        "format_id": "audio_mp3"
    }, timeout=30.0)
    dl_data = dl_req.json()
    print("Download start response:", dl_data)
    assert dl_data["success"] is True
    task_id = dl_data["data"]["task_id"]

    # Poll status for up to 10 seconds
    import time
    for i in range(10):
        time.sleep(1)
        st_res = httpx.get(f"{base_url}/api/video/download/status/{task_id}")
        st_data = st_res.json()
        print(f"Status poll [{i+1}]: {st_data['data']['status']} (Progress: {st_data['data']['progress']}%)")
        if st_data["data"]["status"] in ["ready", "failed"]:
            break

    print("\nAll integration API checks passed successfully!")

if __name__ == "__main__":
    test_api()
