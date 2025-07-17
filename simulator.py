import random

def simular_examen(preguntas, cantidad):
    return random.sample(preguntas, min(cantidad, len(preguntas)))

def evaluar_simulacion(preguntas_simuladas, respuestas_usuario):
    resultados = []
    for pregunta, respuesta_usuario in zip(preguntas_simuladas, respuestas_usuario):
        esperado = pregunta['respuesta'].strip().lower()
        recibido = respuesta_usuario.strip().lower()
        correcto = esperado == recibido
        resultados.append({"pregunta": pregunta['pregunta'], "esperada": esperado, "usuario": recibido, "correcto": correcto})
    return resultados