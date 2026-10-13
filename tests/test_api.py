import pytest
from fastapi.testclient import TestClient
from backend import main
from backend.chat import ModelError, construire_messages

@pytest.fixture
def client(monkeypatch):
    main.conversations.clear()
    def fake(message, history):
        answer = f"{len(history)} messages précédents"
        return answer, [*history, {"role":"user", "content":message}, {"role":"assistant", "content":answer}]
    monkeypatch.setattr(main, "repondre", fake)
    with TestClient(main.app) as c:
        yield c

def test_health(client):
    assert client.get("/health").json()["status"] == "ok"

@pytest.mark.parametrize("message", ["", "   ", "x"*4001])
def test_invalid_messages(client, message):
    assert client.post("/chat", json={"message":message}).status_code == 422
    assert not main.conversations

def test_context_isolation_reset(client):
    a = client.post("/chat", json={"message":"Bonjour"}).json()
    b = client.post("/chat", json={"message":"Autre conversation"}).json()
    assert a["conversation_id"] != b["conversation_id"]
    follow = client.post("/chat", json={"message":"Et ensuite ?", "conversation_id":a["conversation_id"]}).json()
    assert follow["answer"] == "2 messages précédents"
    assert len(main.conversations[b["conversation_id"]]) == 2
    assert client.delete("/chat/"+a["conversation_id"]).status_code == 204
    assert a["conversation_id"] not in main.conversations
    assert client.post("/chat", json={"message":"Suite", "conversation_id":a["conversation_id"]}).status_code == 404

@pytest.mark.parametrize("status", [429, 502, 503, 504])
def test_error_does_not_modify_history(client, monkeypatch, status):
    cid = client.post("/chat", json={"message":"Bonjour"}).json()["conversation_id"]
    old = list(main.conversations[cid])
    def fail(*args): raise ModelError("Erreur test", status)
    monkeypatch.setattr(main, "repondre", fail)
    result = client.post("/chat", json={"message":"Suite", "conversation_id":cid})
    assert result.status_code == status
    assert main.conversations[cid] == old

def test_cors(client):
    r = client.options("/chat", headers={"Origin":"http://localhost:5173", "Access-Control-Request-Method":"POST"})
    assert r.headers["access-control-allow-origin"] == "http://localhost:5173"

def test_prompt_keeps_roles_and_input():
    history = [{"role":"user", "content":"notes = [1,2]"}, {"role":"assistant", "content":"OK"}]
    msgs = construire_messages("Et ensuite ?", history)
    assert msgs[0]["role"] == "system"
    assert msgs[1:3] == history
    assert len(history) == 2
    assert msgs[-1]["content"] == "Et ensuite ?"
