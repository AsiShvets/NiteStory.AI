import requests

url = "https://solid-space-doodle-jx449j5rq9q3qx7x-8000.app.github.dev/api/image-to-text"
files = {'file': open('boy_dog.jpg', 'rb')}
response = requests.post(url, files=files)

print("Status Code:", response.status_code)
print("Response Text:", response.text)  # Print raw response before parsing JSON
