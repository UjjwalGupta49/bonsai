import requests
import json
'''
{"topics":["AI  healthcare", "healthcare", "Machine Learning", "Medical imaging", "Convolutional Neural networks"], "language": "Python"}

'''
# Parameters for the request
url = "https://api.github.com/search/repositories"
#query = "tensorflow in:topics healthcare in:topics ai in:topics AI healthcare in:readme medical imaging in:readme convolutional Neural networks in:readme"  # Example query
'''
keywords = {
    "tensorflow": "topics",
    "healthcare": "topics",
    "ai": "topics",
    "AI healthcare": "readme",
    "medical imaging": "readme",
    "convolutional Neural networks": "readme"
}
'''
keywords = {
    "AI": "topics",
    "tensorflow": "topics",
    "object detection": "readme"
}
# Construct the query by joining each keyword with its field
query_parts = [f"{keyword} in:{field}" for keyword, field in keywords.items()]
query = ' '.join(query_parts)
headers = {
    "Accept": "application/vnd.github+json",
    "Authorization": "Bearer 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",
    "X-GitHub-Api-Version": "2022-11-28"
}

# Making the GET request
response = requests.get(url, headers=headers, params={'q': query})

# Check if the request was successful
if response.status_code == 200:
    # Convert the response to JSON and save it to a file
    result = response.json()
    with open('./response.json', 'w') as file:
        json.dump(result, file, indent=4)
    print("Response data saved to 'response.json'")
else:
    print("Error:", response.status_code, response.text)
