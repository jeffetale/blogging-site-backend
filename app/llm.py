import os
from openai import OpenAI
from bs4 import BeautifulSoup

from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("LLM_API_KEY"),
    base_url="https://api.aimlapi.com",
)


def summarize_content(html_content: str) -> str:
    soup = BeautifulSoup(html_content, "html.parser")
    text_content = soup.get_text(separator=" ", strip=True)

    response = client.chat.completions.create(
        model="meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that summarizes blog content in about 100 words. Go straight to the point and just give me the output. That is ready to be pulled from the backed to the front end where the user will see the surmarised content. Dont use words like 'Here is a 100-word summary of the blog post' e.t.c to tell me the summary. Just return the reply of the content",
            },
            {
                "role": "user",
                "content": f"{text_content}",
            },
        ],
    )

    return response.choices[0].message.content.strip()
