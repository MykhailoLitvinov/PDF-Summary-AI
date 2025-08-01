import logging
import os
from typing import Optional

import openai
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)


class OpenAIService:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key not found. Set OPENAI_API_KEY")

        self.client = openai.OpenAI(api_key=self.api_key)

    def generate_summary(self, text: str, images: list[dict]) -> str:
        """Generate a summary of the document"""
        try:
            developer_prompt = """
            You are expert at summarization of the pdf file content. 
            Your goal is to provide a concise and informative summary of the document based on the text, tables and images input.
            """
            content = [
                {"type": "text", "text": f"Document to summarize:\n\n{text}"},
                *(
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{image["base64"]}"}}
                    for image in images
                ),
            ]
            messages = [
                {"role": "developer", "content": developer_prompt},
                {"role": "user", "content": content},
            ]

            response = self.client.chat.completions.create(
                model="gpt-4o-2024-11-20",
                messages=messages,
                max_tokens=1000,
                temperature=0.1,
            )

            summary = response.choices[0].message.content.strip()

            return summary

        except openai.RateLimitError:
            logger.error("Rate limit exceeded for OpenAI API")
            raise Exception("Rate limit exceeded for OpenAI. Please try again later.")

        except openai.APIError as e:
            logger.error(f"OpenAI API error: {str(e)}")
            raise Exception(f"OpenAI service error: {str(e)}")

        except Exception as e:
            logger.error(f"Unexpected error while generating summary: {str(e)}")
            raise Exception(f"Summary generation error: {str(e)}")
