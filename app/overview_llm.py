import os
import time
import json
from openai import OpenAI
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from tenacity import retry, stop_after_attempt, wait_exponential

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def short_summarized_content(html_content: str) -> str:
    soup = BeautifulSoup(html_content, "html.parser")
    text_content = soup.get_text(separator=" ", strip=True)
    try:
        print("Sending request to OpenRouter API for short summary...")
        response = client.chat.completions.create(
            extra_headers={
                "HTTP-Referer": os.getenv(
                    "MY_SITE_URL", "https://your-default-site.com"
                ),
                "X-Title": os.getenv("MY_APP_NAME", "Your Default App Name"),
            },
            model="nousresearch/hermes-3-llama-3.1-405b:free",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that summarizes content in only one or two sentences. Go straight to the point and just give me the output. That is ready to be pulled from the backed to the front end where the user will see the summarised content. Don't use words like 'Here is a 2-sentence summary of the blog post' etc. to tell me the summary. Just return the reply of the content:",
                },
                {
                    "role": "user",
                    "content": f"{text_content}",
                },
            ],
        )
        print("Received response from OpenRouter API for short summary:")
        print(json.dumps(response.model_dump(), indent=2))

        summary = response.choices[0].message.content.strip()
        print(f"Generated short summary:\n{summary}")
        return summary
    except Exception as e:
        print(f"Error in short_summarized_content: {str(e)}")
        raise
