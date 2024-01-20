from flask import Flask, request, jsonify
import requests
import json
from colorama import Fore, Style
import replicate
import os
import re
from flask_cors import CORS
from difflib import SequenceMatcher

# flask
app = Flask(__name__)
CORS(app)

app.config['ENV'] = 'production'
app.config['DEBUG'] = False


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
    first_key = next(iter(keywords))
    hell.append(first_key)
    return keywords
hell=[]

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


# Github
@app.route("/github")
def git():
    user_input = request.args.get('user_input')
    print(f"http://127.0.0.1:5000/github?user_input={user_input}")

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


#Product Hunt
@app.route("/producthunt")
def product():
    user_input=hell[0]

    def search_product_hunt_for_keywords(words):
        API_URL = "https://api.producthunt.com/v2/api/graphql"
        API_TOKEN = "ff_NiFAD0WKqGnk8l_GIQVRCgVetuULSznJE38kKpYQ"

        # Graph QL query
        graphql_query = f"""
        query {{
            posts(topic:"{words}") {{
                edges {{
                    node {{
                        name
                        website
                        description
                    }}
                }}
            }}
        }}
        """

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {API_TOKEN}"
        }

        response = requests.post(API_URL, headers=headers, data=json.dumps({"query": graphql_query}))

        if response.status_code == 200:
            return response.json()
        else:
            print(f"{Fore.RED}Product Hunt Error:{Style.RESET_ALL} {response.status_code} {response.text}")
            return None
    pro=[]
    def display_product_hunt_info(product_hunt_results):
        for post in product_hunt_results.get('data', {}).get('posts', {}).get('edges', []):
            name = post.get('node', {}).get('name', 'N/A')
            website = post.get('node', {}).get('website', 'N/A')
            description = post.get('node', {}).get('description', 'No description available')
            pro.append(name)
            pro.append(website)
            pro.append(description)

    def find_most_similar_word(word, word_list):
        max_similarity = 0
        most_similar_word = None

        for other_word in word_list:
            similarity_ratio = SequenceMatcher(None, word, other_word).ratio()

            # Update the most similar word if a higher similarity ratio is found
            if similarity_ratio > max_similarity:
                max_similarity = similarity_ratio
                most_similar_word = other_word

        return most_similar_word, max_similarity

    word_to_compare = user_input
    word_list = [
        "productivity", "tech", "developer-tools", "marketing", "artificial-intelligence", "user-experience",
        "design-tools", "internet-of-things", "wearables", "home", "analytics", "growth-hacking", "photography",
        "books", "web-app", "bots", "ios", "mac", "games", "api-1", "social-media", "task-management",
        "health-fitness", "education", "slack", "prototyping", "product-hunt", "open-source", "writing", "android",
        "music", "chrome-extensions", "messaging", "social-network", "venture-capital", "virtual-reality", "fintech",
        "touch-bar-apps", "augmented-reality", "streaming-services", "github", "travel", "software-engineering",
        "e-commerce", "crypto", "branding", "news", "saas", "email", "seo", "email-marketing", "calendar",
        "global-nomad", "freelance", "linkedin", "advertising", "coffee", "investing", "crowdfunding", "gifs",
        "twitter",
        "spotify", "startup-books", "imessage-apps", "instagram", "drones", "design-books", "wordpress", "sales",
        "a-b-testing", "snapchat", "art", "typography", "sketch", "medium", "search", "amazon", "text-editors",
        "youtube",
        "virtual-assistants", "apple", "reddit", "hiring", "biohacking", "movies", "photoshop", "languages", "fashion",
        "payments", "maps", "climate-tech", "windows", "meditation", "menu-bar-apps", "customer-communication",
        "newsletters", "video-streaming", "time-tracking", "emoji", "funny", "hardware", "privacy",
        "facebook-messenger",
        "sports", "robots", "spreadsheets", "wi-fi", "icons", "3d-printer", "cooking", "public-relations", "free-games",
        "space", "alexa-skills", "website-builder", "pokemon", "notes", "home-automation", "beauty", "linux",
        "outdoors",
        "ipad", "vacation", "web-design", "on-demand", "startup-lessons", "storage", "delivery", "indie-games", "web3",
        "anonymous", "wallpaper", "meetings", "events", "business", "strategy-games", "apple-watch", "cars",
        "ux-design",
        "legal", "backpacks", "customer-success", "ridesharing", "tv", "transportation", "blockchain", "dating",
        "ebook-reader", "board-games", "soundcloud", "pc", "telegram", "side-project", "browser-extensions",
        "cryptocurrency", "drinking", "development", "no-code", "science-books", "social-media-marketing", "couples",
        "dogs", "pets", "apple-tv", "finance", "data-analytics", "standing-desks", "emulators", "puzzle-games",
        "charity-giving", "health", "parenting", "accessories", "politics", "safari-extensions", "ad-blockers",
        "comics-graphic-novels", "kids", "money", "adventure-games", "jewelry", "graphics-design", "batteries", "cats",
        "growth-hacks", "design", "oculus-rift", "card-games", "art-books", "sneakers-shoes", "remote-work", "gear-vr",
        "history-books", "open-world-games", "football", "weather", "retro-games", "biking", "star-wars",
        "moving-storage", "wine", "action-games", "data-science", "adult-coloring-books", "playstation", "party",
        "marketing-automation", "medical", "crafting-games", "quantified-self", "sci-fi-games", "data-visualization",
        "novels", "rpgs", "cookbooks", "social-impact", "simulation-games", "affiliate-marketing", "graphic-design",
        "arkit", "djing", "online-learning", "business-intelligence", "fantasy-games", "maker-tools", "soccer",
        "word-games", "alarms", "funny-games", "fashion-books", "custom-keyboards", "food-drink", "community",
        "platformers", "nft", "sports-games", "tech-news", "yoga-books", "tabletop-games", "xbox", "personal-finance",
        "basketball", "celebrities", "digital-art", "playstation-vr", "work-in-progress", "notion", "animation",
        "security", "surfing", "cannabis", "audio", "horror-games", "computers", "swimming", "data", "mmos",
        "design-resources", "photo-video", "beauty-fashion", "influencer-marketing", "nintendo", "database",
        "historical-games", "crime-books", "driving-games", "3d-modeling", "entertainment", "human-resources",
        "first-person-shooter", "design-templates", "bitcoin", "isometric-games", "consulting", "skateboarding",
        "development-language", "horror-books", "video", "fighting-games", "golf", "thriller-books", "donald-trump",
        "logo-design", "tennis", "tower-defense-games", "illustration", "diversity-inclusion", "career",
        "social-networking", "femtech", "zombie-games", "accounting", "crm", "monetization", "business-travel",
        "kanye-west", "lifestyle", "htc-vive", "banking", "boxing", "science", "photo-editing", "shopping", "defi",
        "fitness", "health-news", "dj-khaled", "fundraising", "home-improvement", "baseball", "clothing", "hacking",
        "interior-design", "coding-books", "drake", "construction", "wii-u", "business-books", "operations", "drawing",
        "home-services", "marketing-attribution", "electronic-music", "vita", "ethereum", "home-office",
        "event-marketing",
        "change-management", "dao", "spirituality", "nutrition", "diy", "crafting", "food-delivery", "furniture",
        "graphics",
        "video-art", "dapp", "nature-outdoors", "budgeting", "statistical-analysis", "painting", "wireframing",
        "live-music",
        "comedy", "electric-cars", "lgbtq", "cell-phone", "nature", "family", "kids-parenting", "aquarium", "cosmetics",
        "calligraphy", "physics", "hotels", "mixed-reality", "marketing-calendar", "credit-card", "encryption",
        "printing",
        "camping", "classical-music", "password-manager", "political-news", "sdk", "live-events", "school",
        "video-cameras",
        "farming", "chat-rooms", "vpn", "memes", "running", "plants", "home-security", "extended-reality", "hiking",
        "coloring",
        "weightlifting", "local-news", "pop-culture", "inclusivity", "appliances", "streetwear", "modeling",
        "edge-extensions",
        "concerts", "survival", "motorcycles", "webcam", "personal-shopper", "hip-hop", "dieting", "toys", "babies",
        "radio",
        "alcohol", "tablet", "dslrs", "sporting-events", "intimacy", "sensors", "textbooks", "climbing", "ticketing",
        "gps",
        "concert", "theater", "dining", "neighborhood", "college-sports", "military", "home-theater", "racing",
        "tuning",
        "snow-sports", "toddlers", "pregnancy", "psychedelics"
    ]

    most_similar_word, similarity_ratio = find_most_similar_word(word_to_compare, word_list)
    product_hunt_results = search_product_hunt_for_keywords(most_similar_word)

    if product_hunt_results:
        display_product_hunt_info(product_hunt_results)
    else:
        print(f"{Fore.RED}Product Hunt Error:{Style.RESET_ALL} Unable to retrieve data from Product Hunt")


    prod=[]
    def ListTD(L):
        x = len(L)
        for i in range(0, x, 3):
            r = {"Description": L[i + 2], "Website": L[i + 1], "Name": L[i]}
            prod.append(r)

    ListTD(pro)
    return prod

#Summary
@app.route("/summary")
def summary():
    return "Ujjwal"

#Runner
if __name__ == "__main__":
    print("http://127.0.0.1:5000/github")
    print("http://127.0.0.1:5000/producthunt")
    print("http://127.0.0.1:5000/summary")
    app.run(debug=True)

