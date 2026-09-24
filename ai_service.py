import ollama
import logging

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

def analyse_avec_ollama(prompt):
    
    try: 
        logger.info("Envoi du rapport à Ollama")
        response = ollama.chat(
            model="qwen3.5:4b",
            messages=[
                {
                    "role": "user",
                    "content": prompt    
                }         
            ]
        )
        logger.info("Réponse reçue d'Ollama")
    except Exception as erreur:
        logger.error(f"Erreur Ollama : {erreur}")
        raise

    return response["message"]["content"]