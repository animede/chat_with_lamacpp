import os
import asyncio
import gradio as gr
from openai import AsyncOpenAI

client = AsyncOpenAI(
    base_url="http://localhost:8080/v1",
    api_key="OPENAI_API_KEY",
)

async def generate_text(input_text):
    stream = await client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": input_text}],
        stream=True,
    )
    response = ""
    async for chunk in stream:
        response += chunk.choices[0].delta.content or ""
    response=response.replace("**","")
    return response

def wrap_async_call(input_text):
    return asyncio.run(generate_text(input_text))

interface = gr.Interface(
    fn=wrap_async_call,
    inputs=gr.Textbox(label="Input Text"),
    outputs=gr.Textbox(label="Generated Text"),
    title="OpenAI API Text Generator"
)

interface.launch()

