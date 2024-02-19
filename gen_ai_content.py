# General imports ..
import os
import random
import logging
import urllib3
import warnings
import json
import requests

from tqdm import tqdm
from dotenv import load_dotenv

# langchain imports ..
from langchain.retrievers import WikipediaRetriever
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
import google.generativeai as genai

from urls import base_url, api_url, get_sub_url, get_sub_chap_url, add_ai_url
from logger import setup_logger

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# surpress warnings ..
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
warnings.filterwarnings("ignore", category=UserWarning, module="langchain")

# Setting up logger ..
try:
    # Create 'logs' directory if it doesn't exist
    logs_directory = 'logs'
    if not os.path.exists(logs_directory):
        os.makedirs(logs_directory)

    # Set up logger with the log file inside the 'logs' directory
    log_file_path = os.path.join(logs_directory, 'add_chap_topics.log')
    logger = setup_logger('gen_contents', log_file_path)
    logger.info('Logger is activated for GENERATING Chapter & topics ..')
except Exception as e:
    # Log the exception if there is an error during logger setup
    logger.error(e)

# Languages list ..
lang_list = ["english", "hindi", "bengali", "marathi", "telugu", "tamil", "gujarati", "urdu", "kannada", "malayalam", "oriya", "punjabi", "assamese", "sinhala"]
lang_codes = {'english': 1, 'hindi': 6}

# Setting OpenAi key ..
from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())
openai_key = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_KEY"] = openai_key

# surpress warnings ..
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
warnings.filterwarnings("ignore", category=UserWarning, module="langchain")

# 1. Generate answers ..
def gen_content_with_openai(prompt):
    model_name = "gpt-4-1106-preview"
    temperature = 0.5
    model = OpenAI(model_name=model_name, temperature=temperature)
    output = model(prompt)
    return output

# 2.  Gmini Pro ..
def gen_content_with_gemini_pro(prompt) :
    llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.5)
    out = llm.invoke(prompt)
    return out.content

# Preparing prompt for AI content ..
def gen_text_prompts(topic, subject, chapter, grade, target_language="English"):
    prompts = []
    level_instructions = {
        1: "For Level 1 students, provide a simple and detailed explanation.",
        2: "For Level 2 students, provide a balanced and detailed explanation.",
        3: "For Level 3 students, provide a detailed explanation with increased difficulty.",
        4: "For Level 4 students, provide a concise and challenging explanation."
    }

    for level, instruction in level_instructions.items():
        instructions = (
            f"Generate the explanation in {target_language}.\n\n"
            f"Provide a comprehensive and detailed explanation or answer in {target_language}. "
            "Consider the following structure:\n\n"
            f"{topic} Defined:\n"
            f"Start by defining the topic '{topic}' in detail. Explain any concepts, mathematical relationships, or relevant information related to {subject}.\n\n"
            f"Insert any additional content specific to the topic here.\n"
            f"Examples:\n"
            f"Include sample examples to illustrate key points or demonstrate the procedure.\n"
            f"Insert example content here.\n"
            f"Important Points and Notes:\n"
            f"Highlight any crucial information or notable aspects related to the topic or procedure.\n"
            f"Insert important points and notes here.\n"
            f"Additional Information:\n"
            f"Add any other relevant information, historical context, or interesting facts to enhance the answer.\n\n"
            f"Topic: {topic}\n"
            "When generating the answer, follow the structure provided."
        )
        prompts.append(instructions)
    return prompts

##  Preparing prompt for embedding HTML Tags ..
def gen_html_prompt(paragraph):
    # Define HTML instructions
    html_instructions = {
        "heading": "<h{level}>",
        "paragraph": "<p>",
        "strong": "<strong>",
        "subscript": "<sub>",
        "superscript": "<sup>",
        "mathjax_inline": "$$",
        "mathjax_block": "$$"
    }

    # Construct the prompt with instructions, paragraph, and HTML format instructions
    prompt = (
        f"{html_instructions['paragraph']}Please embed HTML tags as necessary to format the following paragraph:\n\n"
        f"{paragraph}\n\n"
        "You may use the following HTML tags:\n"
        "- <h{{level}}> for headings\n"
        "- <p> for paragraphs\n"
        "- <strong> for bold text\n"
        "- <sub> for subscript\n"
        "- <sup> for superscript\n"
        "- $$ for inline MathJax\n"
        "- $$ for block MathJax\n"
        "- <li> for list items\n"
        "Feel free to use additional HTML tags as needed to enhance the structure of the text."
    )

    return prompt

