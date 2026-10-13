"""Logique partagée par le notebook et l'API ; aucun secret envoyé au navigateur."""
import os
from openai import OpenAI, APIError, APITimeoutError, AuthenticationError, RateLimitError
from backend.config import BASE_URL, MODEL, TIMEOUT
from backend.prompts import PROMPTS

class ModelError(Exception):
    def __init__(self, message, status=502):
        super().__init__(message)
        self.status = status


def construire_messages(message, historique, version="v2"):
    message = message.strip()
    if not message:
        raise ValueError("Le message ne doit pas être vide.")
    if len(message) > 4000:
        raise ValueError("Le message dépasse 4 000 caractères.")
    if len(historique) >= 40:
        raise ValueError("Limite de 20 échanges atteinte : commence une nouvelle conversation.")
    return [{"role": "system", "content": PROMPTS[version]}, *historique,
            {"role": "user", "content": message}]


def repondre(message, historique, version="v2"):
    """Retourne (réponse, nouvel historique). L'ancien historique n'est pas modifié."""
    messages = construire_messages(message, historique, version)
    key = os.getenv("GROQ_API_KEY", "").strip()
    if not key:
        raise ModelError("Clé Groq absente. Configure le fichier .env puis redémarre.", 503)
    try:
        with OpenAI(api_key=key, base_url=BASE_URL, timeout=TIMEOUT, max_retries=0) as client:
            result = client.chat.completions.create(
                model=MODEL, messages=messages, temperature=0.2, max_completion_tokens=2048
            )
        answer = result.choices[0].message.content
        if not answer or not answer.strip():
            raise ModelError("Le modèle a renvoyé une réponse vide. Réessaie.")
    except APITimeoutError:
        raise ModelError("Le modèle met trop de temps à répondre. Réessaie.", 504) from None
    except AuthenticationError:
        raise ModelError("Clé Groq refusée. Vérifie le fichier .env.", 503) from None
    except RateLimitError:
        raise ModelError("Quota ou limite Groq atteint. Réessaie plus tard.", 429) from None
    except APIError:
        raise ModelError("Le fournisseur du modèle est indisponible ou a refusé la requête.", 502) from None
    return answer, [*historique, {"role": "user", "content": message.strip()},
                    {"role": "assistant", "content": answer}]
