import requests

def usar_ollama(prompt, modelo="llama3"):
    try:
        url = "http://localhost:11434/api/generate"
        payload = {
            "model": modelo,
            "prompt": prompt,
            "stream": False
        }
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            return response.json().get("response", "").strip()
        else:
            return f"[Error {response.status_code}] No se pudo obtener respuesta."
    except Exception as e:
        return f"[Error] {str(e)}"

def responder_preguntas(preguntas, modelo="llama3"):
    resultados = []
    for item in preguntas:
        pregunta = item.get("pregunta")
        if not item.get("respuesta"):
            respuesta = usar_ollama(pregunta, modelo)
        else:
            respuesta = item["respuesta"]
        resultados.append({
            "pregunta": pregunta,
            "respuesta": respuesta
        })
    return resultados
