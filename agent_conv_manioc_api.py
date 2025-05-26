from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

# Configurer la clé API OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")  # Utiliser la variable d'environnement

# Contexte initial sur le manioc
CONTEXT = """
Tu es un expert en manioc, une plante tropicale également appelée cassava ou yuca. Tu fournis des conseils précis sur sa culture, sa transformation, sa préparation culinaire, ses bienfaits nutritionnels et ses défis. Réponds de manière claire et concise, en te basant sur des informations fiables et adaptées au contexte africain ou tropical.
"""

# Endpoint pour vérifier que le serveur est actif
@app.route('/', methods=['GET'])
def health_check():
    return jsonify({'status': 'Server is running'})

# Endpoint pour obtenir des conseils sur le manioc
@app.route('/manioc_advice', methods=['POST'])
def get_manioc_advice():
    try:
        data = request.get_json()
        print(f"Requête reçue : {data}")  # Log pour déboguer
        user_input = data.get('question', '')
        if not user_input:
            return jsonify({'error': 'Aucune question fournie'}), 400

        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",  # Vous pouvez utiliser "gpt-4" si disponible
            messages=[
                {"role": "system", "content": CONTEXT},
                {"role": "user", "content": user_input}
            ],
            max_tokens=300,
            temperature=0.7
        )
        advice = response.choices[0].message.content
        print(f"Réponse envoyée : {advice}")  # Log pour déboguer
        return jsonify({'advice': advice})
    except Exception as e:
        print(f"Erreur : {str(e)}")  # Log pour déboguer
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv("PORT", 5000)))