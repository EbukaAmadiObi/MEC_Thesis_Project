"""Test for MEC based MEC client"""

import requests

"""# POST request
image = "ebukaamadiobi/knn-model"
name = "test"
response = requests.post(f"http://127.0.0.1:8000/create-container/?image={image}&name={name}")
print(response.json())"""

response = requests.post(f"http://127.0.0.1:8000/list-containers/")
print(response.json())