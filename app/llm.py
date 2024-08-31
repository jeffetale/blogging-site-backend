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

    # Generate summary using OpenAI's API
    response = client.chat.completions.create(
        model="meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that summarizes content in about 50 words.",
            },
            {
                "role": "user",
                "content": f"Summarize the following content in about 50 words:\n\n{text_content}",
            },
        ],
    )

    return response.choices[0].message.content.strip()
