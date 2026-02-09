import requests
import glob
import os

# --- SETTINGS ---
BASE_URL = "http://localhost:8000"
USERNAME = "joshua.penafiel"
PASSWORD = "1"
IMAGE_PATH = "/home/joshua/odm_data_aukerman/images/*.JPG"
PROJECT_NAME = "My Python Project"

# 1. GET TOKEN
auth_res = requests.post(f"{BASE_URL}/api/token-auth/", data={
    "username": USERNAME, 
    "password": PASSWORD
})
token = auth_res.json().get('token')
headers = {'Authorization': f'JWT {token}'}

# 2. CREATE PROJECT
proj_res = requests.post(f"{BASE_URL}/api/projects/", headers=headers, data={
    "name": PROJECT_NAME
}).json()
project_id = proj_res['id']

# 3. PREPARE IMAGES
image_files = glob.glob(IMAGE_PATH)
files_payload = []
for path in image_files:
    # WebODM requires a list of tuples for multiple files
    files_payload.append(('images', (os.path.basename(path), open(path, 'rb'), 'image/jpeg')))

# 4. UPLOAD & START TASK
# 'options' must be a JSON string
options = '[{"name": "dsm", "value": true}]'
task_res = requests.post(
    f"{BASE_URL}/api/projects/{project_id}/tasks/",
    headers=headers,
    files=files_payload,
    data={"options": options}
).json()

print(f"Success! Task {task_res['id']} started in project {project_id}.")
