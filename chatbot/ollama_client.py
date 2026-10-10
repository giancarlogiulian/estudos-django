import json
import urllib.error
import urllib.request

from django.conf import settings


class OllamaError(Exception):
    """Erro ao falar com a API do Ollama."""


def _base_url() -> str:
    return getattr(settings, "OLLAMA_BASE_URL", "http://127.0.0.1:11434").rstrip("/")


def _request(path: str, payload: dict | None = None, timeout: int = 300) -> dict:
    url = f"{_base_url()}{path}"
    data = None
    headers = {"Accept": "application/json"}

    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"

    req = urllib.request.Request(url, data=data, headers=headers, method="POST" if data else "GET")

    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            body = response.read().decode("utf-8")
            return json.loads(body) if body else {}
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="ignore")
        raise OllamaError(f"Ollama HTTP {exc.code}: {detail or exc.reason}") from exc
    except urllib.error.URLError as exc:
        raise OllamaError(
            "Não foi possível conectar ao Ollama. "
            "Confirme se o serviço está rodando (ollama serve)."
        ) from exc
    except TimeoutError as exc:
        raise OllamaError("A resposta do Ollama demorou demais (timeout).") from exc


def listar_modelos() -> list[dict]:
    data = _request("/api/tags", timeout=10)
    modelos = []
    for item in data.get("models", []):
        nome = item.get("name") or item.get("model")
        if not nome:
            continue
        detalhes = item.get("details") or {}
        modelos.append(
            {
                "name": nome,
                "size": item.get("size"),
                "parameter_size": detalhes.get("parameter_size"),
                "family": detalhes.get("family"),
            }
        )
    return sorted(modelos, key=lambda m: m["name"])


def chat(model: str, messages: list[dict]) -> str:
    data = _request(
        "/api/chat",
        payload={
            "model": model,
            "messages": messages,
            "stream": False,
        },
        timeout=getattr(settings, "OLLAMA_TIMEOUT", 300),
    )
    message = data.get("message") or {}
    content = message.get("content", "").strip()
    if not content:
        raise OllamaError("O Ollama retornou uma resposta vazia.")
    return content
