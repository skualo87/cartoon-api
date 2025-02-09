from fastapi import FastAPI
import openai
import os

app = FastAPI()

# Usa la tua chiave API di OpenAI salvata come variabile d'ambiente
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.get("/")
def read_root():
    return {"message": "API FastAPI è online su Render!"}

@app.get("/generate_script/")
def generate_script(prompt: str):
    response = openai.Completion.create(
        model="gpt-4",
        prompt=prompt,
        max_tokens=300
    )
    return {"script": response.choices[0].text.strip()}
