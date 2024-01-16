import requests
import json
from colorama import Fore, Style
import replicate
import os
    

def get_user_input():
    return input("Enter your project description or keywords: ").strip()

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
    os.environ['REPLICATE_API_TOKEN'] = 'r8_OxBlp46BxDtls3mceyPjJ8xucYZEUvT4T9i7n'

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
            "prompt":f"Instructions for Extractor: {pre_prompt} Conversation - Input: '{prompt}' Extractor",
            "system_prompt": f"Strict instructions to be followed: {pre_prompt}",
            "max_lenght": 30,
            "return_logits": False,
        },
    ):
        output += str(event)
    keywords = keywords_to_dict(output)
    return keywords

def construct_query(keywords):
    return ' '.join([f"{keyword} in:{field}" for keyword, field in keywords.items()])

def make_github_request(query):
    url = "https://api.github.com/search/repositories"
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": "Bearer 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", # adding this token was intentional
        "X-GitHub-Api-Version": "2022-11-28"
    }
    response = requests.get(url, headers=headers, params={'q': query})
    return response

def display_repository_info(result):
    for item in result.get('items', []):
        name = item.get('name', 'N/A')
        link = item.get('html_url', 'N/A')
        description = item.get('description', 'No description available')

        print(f"\n{Fore.CYAN}Project Name:{Style.RESET_ALL} {name}")
        print(f"{Fore.GREEN}Link:{Style.RESET_ALL} {link}")
        print(f"{Fore.YELLOW}Description:{Style.RESET_ALL} {description}\n")

def main():
    print(f"{Fore.MAGENTA}                                                                   WELCOME TO BONSAI{Style.RESET_ALL}")

    user_input = get_user_input()
    keywords = generate_keywords(user_input)
    query = construct_query(keywords)

    response = make_github_request(query)

    if response.status_code == 200:
        result = response.json()
        display_repository_info(result)
    else:
        print(f"{Fore.RED}Error:{Style.RESET_ALL} {response.status_code} {response.text}")

if __name__ == "__main__":
    main()
