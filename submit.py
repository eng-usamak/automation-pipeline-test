import json
import hmac
import hashlib
import requests
from datetime import datetime, timezone

NAME = "Usama Islam"
EMAIL = "islamusama10@gmail.com"
RESUME_LINK = "https://drive.google.com/file/d/1jtAR9nQJT2GNGdrabNwFZ8Bvty_G-nKg/view"
REPOSITORY_LINK = "https://github.com/eng-usamak/automation-pipeline-test"
ACTION_RUN_LINK = "https://github.com/eng-usamak/automation-pipeline-test/actions/runs/25128149104"
SIGNING_SECRET = b"hello-there-from-b12"
URL = "https://b12.io/apply/submission"

timestamp = datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")

payload = {
    "action_run_link": ACTION_RUN_LINK,
    "email": EMAIL,
    "name": NAME,
    "repository_link": REPOSITORY_LINK,
    "resume_link": RESUME_LINK,
    "timestamp": timestamp,
}

body = json.dumps(payload, separators=(",", ":"), sort_keys=True).encode("utf-8")

digest = hmac.new(SIGNING_SECRET, body, hashlib.sha256).hexdigest()
signature = f"sha256={digest}"

headers = {
    "Content-Type": "application/json",
    "X-Signature-256": signature,
}

response = requests.post(URL, data=body, headers=headers)

if response.status_code == 200:
    print(response.json()["receipt"])
else:
    print("Error:", response.status_code, response.text)