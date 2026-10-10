import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET, require_POST

from .ollama_client import OllamaError, chat, listar_modelos

SESSION_HISTORY_KEY = "chatbot_history"
SESSION_MODEL_KEY = "chatbot_model"
MAX_HISTORY = 40


def chat_page(request):
    modelos = []
    erro_modelos = None
    try:
        modelos = listar_modelos()
    except OllamaError as exc:
        erro_modelos = str(exc)

    modelo_atual = request.session.get(SESSION_MODEL_KEY)
    if modelos and (not modelo_atual or modelo_atual not in {m["name"] for m in modelos}):
        modelo_atual = modelos[0]["name"]
        request.session[SESSION_MODEL_KEY] = modelo_atual

    historico = request.session.get(SESSION_HISTORY_KEY, [])

    return render(
        request,
        "chatbot/chat.html",
        {
            "modelos": modelos,
            "modelo_atual": modelo_atual,
            "historico": historico,
            "erro_modelos": erro_modelos,
        },
    )


@require_GET
def api_modelos(request):
    try:
        return JsonResponse({"modelos": listar_modelos()})
    except OllamaError as exc:
        return JsonResponse({"erro": str(exc)}, status=503)


@require_POST
def api_enviar(request):
    try:
        payload = json.loads(request.body.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse({"erro": "JSON inválido."}, status=400)

    mensagem = (payload.get("mensagem") or "").strip()
    modelo = (payload.get("modelo") or "").strip()

    if not mensagem:
        return JsonResponse({"erro": "Digite uma mensagem."}, status=400)
    if not modelo:
        return JsonResponse({"erro": "Selecione um modelo."}, status=400)

    historico = list(request.session.get(SESSION_HISTORY_KEY, []))
    historico.append({"role": "user", "content": mensagem})

    try:
        resposta = chat(modelo, historico)
    except OllamaError as exc:
        historico.pop()
        request.session[SESSION_HISTORY_KEY] = historico
        return JsonResponse({"erro": str(exc)}, status=503)

    historico.append({"role": "assistant", "content": resposta})
    if len(historico) > MAX_HISTORY:
        historico = historico[-MAX_HISTORY:]

    request.session[SESSION_HISTORY_KEY] = historico
    request.session[SESSION_MODEL_KEY] = modelo
    request.session.modified = True

    return JsonResponse(
        {
            "resposta": resposta,
            "modelo": modelo,
            "historico": historico,
        }
    )


@require_POST
def api_limpar(request):
    request.session[SESSION_HISTORY_KEY] = []
    request.session.modified = True
    return JsonResponse({"ok": True})
