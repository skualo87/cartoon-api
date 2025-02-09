from fastapi import FastAPI, HTTPException
import openai
import os

app = FastAPI()

# Recupera la chiave API da Render (variabile d'ambiente)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.get("/")
def read_root():
    return {"message": "API FastAPI è online su Render!"}

@app.get("/generate_script/")
def generate_script(prompt: str):
    if not openai.api_key:
        raise HTTPException(status_code=500, detail="Chiave API OpenAI non trovata. Verifica le variabili d'ambiente.")

    if not prompt or prompt.strip() == "":
        raise HTTPException(status_code=400, detail="Il parametro 'prompt' è obbligatorio.")

    try:
        response = openai.Completion.create(
            model="gpt-4",
            prompt=prompt,
            max_tokens=300
        )
        return {"script": response.choices[0].text.strip()}

    except openai.error.AuthenticationError:
        raise HTTPException(status_code=401, detail="Errore di autenticazione con OpenAI. Controlla la chiave API.")

    except openai.error.RateLimitError:
        raise HTTPException(status_code=429, detail="Hai superato il limite di utilizzo dell'API OpenAI.")

    except openai.error.OpenAIError as e:
        raise HTTPException(status_code=500, detail=f"Errore OpenAI: {str(e)}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Errore generico: {str(e)}")
