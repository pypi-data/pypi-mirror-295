
from pydantic import BaseModel
from SimplerLLM.language.llm import LLM,LLMProvider
from SimplerLLM.language.llm_addons import generate_pydantic_json_model_async
from typing import List

from SimplerLLM.tools.web_crawler import crawl_website
from SimplerLLM.prompts.messages_template import MessagesTemplate


openai_instance  = LLM.create(provider=LLMProvider.OPENAI,model_name="gpt-3.5-turbo")
anthropic_instance  = LLM.create(provider=LLMProvider.ANTHROPIC,model_name="claude-3-opus-20240229")
gemini_instance  = LLM.create(provider=LLMProvider.GEMINI,model_name="gemini-pro")

# Create a new message template
template = MessagesTemplate()

# Add messages to the template
#template.add_message("system", "Answer Only in French")


# Add user and assistant messages to the template
template.add_user_message("generate one word")
# template.add_assistant_message("I'm good, thank you! How can I assist you today?")
# template.add_assistant_message("I'm good, thank you! How can I assist you today?")

# Get the messages
template.add_user_message("generate one word")
messages = template.get_messages()


response = gemini_instance.generate_response(messages=messages, system_prompt="you know only arabic, generate everything in ARABIC")
#response = gemini_instance.generate_response(prompt="generate one word", system_prompt="you know only arabic, generate everything in ARABIC")


print(response)


#from SimplerLLM.language.llm_providers.transformers_llm import TransformersModule


# tm = TransformersModule()
#download_path = '/'
# model_name = 'gpt2'

# tm.download_model(model_name, download_path)


import os

# List all files in the download directory
# files_in_directory = os.listdir(download_path)
# print("Files in directory:", files_in_directory)





class BlogTitles(BaseModel):
    titles: List[str]


generate_blog_titles_prompt = """I want you to act as a professional blog titles generator. 
Think of titles that are seo optimized and attention-grabbing at the same time,
and will encourage people to click and read the blog post.
They should also be creative and clever.
Try to come up with titles that are unexpected and surprising.
Do not use titles that are too generic,or titles that have been used too many times before. I want to generate 10 titles maximum.
My blog post is is about {topic}
                                                                                   
"""

# prompt = generate_blog_titles_prompt.format(topic="AI Chatbots")

# response = generate_pydantic_json_model_async(model_class=BlogTitles,prompt=prompt,llm_instance=instance)

# print (response.titles)


import asyncio

# async def main():
#     prompt = generate_blog_titles_prompt.format(topic="AI Chatbots")
#     response = await generate_pydantic_json_model_async(model_class=BlogTitles, prompt=prompt, llm_instance=instance)
#     print(response.titles)

# Assuming this is inside an async function or a coroutine
#await main()
#asyncio.run(main())


# Example usage:
# Crawling example.com up to depth 2, filtering by '/blog' slug
# result = crawl_website("http://learnwithhasan.com", 1)



# for link, (links_beneath, num_links_beneath, unique_links) in result.items():
#     print(f"Link: {link}")
#     print(f"Number of links beneath it: {num_links_beneath}")
#     print(f"Links beneath it: {links_beneath}")
#     print(f"Unique links beneath it: {unique_links}")
#     print()