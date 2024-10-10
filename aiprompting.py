from openai import OpenAI
import os

def user_input():

    user_input = input("What do you want to learn? ")

    print(f'I want to learn about: {user_input}')

    return user_input

def prompt_ai(language, level, topic):

    client = OpenAI()

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a language instructor."},
            {"role": "system", "content": f'You are teaching the following language: {language}.'},
            {"role": "system", "content": f'The user language level is {level} (using CEFR standards, Basic = 0, A1 = 1, A2 = 2, B1 = 3, B2 = 4, C1 = 5).'},
            {"role": "system", "content": "Generate a 4 paragraph story about the following user topic."},
            {"role": "system", "content": "Add a single * to the start the title of the article."},
            {"role": "system", "content": "Add a single * at the beginning of each paragraph."},

            {
                "role": "user",
                "content": topic
            }
        ]
    )

    return completion.choices[0].message.content

def check_api_key():
    api_key = os.getenv("OPENAI_API_KEY")


    if api_key:
        print("API Key loaded successfully!")
    else:
        print("API Key not found. Please set the environment variable.")