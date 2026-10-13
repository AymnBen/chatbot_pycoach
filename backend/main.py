"""API locale de TP. Historique en mémoire : lancer avec un seul worker."""
from threading import Lock
from uuid import UUID, uuid4
from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, ConfigDict
from backend.config import ORIGINS
from backend.chat import repondre, ModelError

app = FastAPI(title="PyCoach", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=ORIGINS,
                   allow_methods=["GET", "POST", "DELETE"], allow_headers=["Content-Type"])
# Le verrou rend atomiques les mises à jour et les réinitialisations du petit TP.
# Il sérialise les requêtes ; une version de production utiliserait des verrous par conversation.
lock = Lock()
conversations = {}

class ChatInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
    message: str = Field(min_length=1, max_length=4000)
    conversation_id: UUID | None = None

class ChatOutput(BaseModel):
    conversation_id: UUID
    answer: str

@app.get("/health")
def health():
    return {"status": "ok", "chatbot": "PyCoach"}

@app.post("/chat", response_model=ChatOutput)
def chat(payload: ChatInput):
    with lock:
        cid = str(payload.conversation_id) if payload.conversation_id else str(uuid4())
        if payload.conversation_id and cid not in conversations:
            raise HTTPException(404, "Conversation introuvable. Commence une nouvelle conversation.")
        history = conversations.get(cid, [])
        try:
            answer, updated = repondre(payload.message, history)
        except ValueError as exc:
            raise HTTPException(422, str(exc)) from None
        except ModelError as exc:
            raise HTTPException(exc.status, str(exc)) from None
        # Ne mémoriser un échange qu'après une réponse réussie.
        conversations[cid] = updated
        return {"conversation_id": cid, "answer": answer}

@app.delete("/chat/{conversation_id}", status_code=204)
def reset(conversation_id: UUID):
    with lock:
        conversations.pop(str(conversation_id), None)
    return Response(status_code=204)
