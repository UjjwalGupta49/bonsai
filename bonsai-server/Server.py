from flask import Flask, request, jsonify
import requests
import json
from colorama import Fore, Style
import replicate
import os
import re
from flask_cors import CORS

# flask
app = Flask(__name__)
CORS(app)

app.config['ENV'] = 'production'
app.config['DEBUG'] = False


# Github
@app.route("/github")
def home():
    user_input = request.args.get('user_input')
    print(f"http://127.0.0.1:5000/github?user_input={user_input}")

    def keywords_to_dict(output):
        start = output.find('{{') + 2  # +2 to skip the '{{'
        end = output.find('}}', start)

        # Extract the substring
        dict_str = output[start:end].strip()

        # Convert the string to a dictionary
        # Using json.loads after replacing single quotes with double quotes
        try:
            extracted_dict = json.loads(f"{{{dict_str}}}")
        except json.JSONDecodeError as e:
            print("Error in converting to dictionary:", e)
            extracted_dict = {}
        return extracted_dict

    def llama_setup():
        os.environ['REPLICATE_API_TOKEN'] = 'r8_L6937wBVLpE8jZyi1nqG2u1z1qOoNfT06xVJG'

    def generate_keywords(user_input):
        llama_setup()
        pre_prompt = '''
        You are a helpful assistant, your job is to extract technology keywords from a given text. You are given a list of technologies and a text. Your task is to extract all the technologies mentioned in the text and return a python dictionary of specified keywords in the text. You will be provided with examples and sample cases of how this data extraction would work.
        You will read the given input from the user and return a python dictionary in specified format. In this converstation you will act as 'Extractor' and the user prompts will be given as 'Input'. In this conversation you can not ask the user for follow up questions and only respond with the extracted python dictionary.

        here are some examplesof how you will act and respond:

        example 1: 
        {
        Input: "find projects that use AI using tensorflow medical imaging", Extractor: "{{"tensorflow": "topics", "healthcare": "topics", "ai": "topics", "AI healthcare": "readme", "medical imaging": "readme"}}"
        }
        example 2: 
        {
        Input: "find projects that use AI for house price predection", Extractor: "{{"ai": "topics", "house price predection": "readme", "price predection": "readme"}}"
        }
        example 3: 
        {
        Input: "find projects that implement AI using pythorch for heart disease detection", Extractor: "{{"ai": "topics", "pytorch": "topics", "hear disease detection": "readme", "heart disease AI": "readme"}}"
        }
        example 4: 
        {
        Input: "give me projects that create tokens on solana blockchain using rust", Extractor: "{{"solana": "topics", "blockchain": "topics", "solana tokens": "readme", "solana blockchain tokens": "readme", "solana rust tokens": "readme", "solana tokens": "description"}}"
        }
        example 5: 
        {
        Input: "data science projects using python", Extractor: "{{"data science": "topics", "data science": "readme", "data science python": "data science": "description"}}"
        }

        Extractor should end the conversation after giving it's response for the python dictionary.
        do not ask for follow up questions and only respond with the extracted python dictionary.
        '''
        prompt = user_input
        output = ""
        # The meta/llama-2-7b model can stream output as it's running.
        for event in replicate.stream(
                "meta/llama-2-7b",
                input={
                    "debug": False,
                    "temprature": 0.01,
                    "prompt": f"Instructions for Extractor: {pre_prompt} Conversation - Input: '{prompt}' Extractor",
                    "system_prompt": f"Strict instructions to be followed: {pre_prompt}",
                    "max_lenght": 30,
                    "return_logits": False,
                },
        ):
            output += str(event)
        keywords = keywords_to_dict(output)
        return keywords

    def construct_query(keywords):
        print(keywords)
        return ' '.join([f"{keyword} in:{field}" for keyword, field in keywords.items()])

    def make_github_request(query):
        url = "https://api.github.com/search/repositories"
        headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": "Bearer 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",
            "X-GitHub-Api-Version": "2022-11-28"
        }
        response = requests.get(url, headers=headers, params={'q': query})
        return response

    x = []

    def display_repository_info(result):
        for item in result.get('items', []):
            name = item.get('name', 'N/A')
            link = item.get('html_url', 'N/A')
            description = item.get('description', 'No description available')
            pattern = re.compile(r'https://github\.com/([^/]+)/')
            match = pattern.search(link)
            username = match.group(1)
            crl = f"https://api.github.com/repos/{username}/{name}/issues"
            response = requests.get(crl)
            total_issues = 0
            if response.status_code == 200:
                issues = response.json()
                total_issues += len(issues)

            x.append(name)
            x.append(link)
            x.append(description)
            x.append(total_issues)

    def main(user_input):
        keywords = generate_keywords(user_input)
        query = construct_query(keywords)

        response = make_github_request(query)

        if response.status_code == 200:
            result = response.json()
            display_repository_info(result)
        else:
            print(f"{Fore.RED}Error:{Style.RESET_ALL} {response.status_code} {response.text}")

    if request.method == "GET":
        try:
            main(user_input)
        except Exception as e:
            return jsonify({"error": str(e)})
    D = []

    def L2D(L):
        x = len(L)
        for i in range(0, x, 4):
            r = {"Issue": L[i + 3], "Description": L[i + 2], "Link": L[i + 1], "Project Name": L[i]}
            D.append(r)

    L2D(x)
    sorted_projects = sorted(D, key=lambda x: x["Issue"], reverse=True)
    return jsonify(sorted_projects)


if __name__ == "__main__":
    print("http://127.0.0.1:5000/github")
    app.run(debug=True)

