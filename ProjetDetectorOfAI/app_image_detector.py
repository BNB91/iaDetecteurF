from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

# Remplacez ces valeurs par les vôtres issues de votre projet Custom Vision
project_id = "b36e6bc8-4bf2-475d-83b5-fa258dd11f33"
iteration_id = "7d8f9887-79eb-4270-8440-ea2e1607993b"
prediction_url = f"https://iadetectorcustomvision-prediction.cognitiveservices.azure.com/customvision/v3.0/Prediction/b36e6bc8-4bf2-475d-83b5-fa258dd11f33/classify/iterations/Iteration10/image"

# Remplacez également la clé de prédiction dans les en-têtes
prediction_key = "92b5dffe118c407983eef1aa2afc31be"
headers = {'Content-Type': 'application/octet-stream', 'Prediction-Key': prediction_key}

@app.route('/')
def index():
    # Initialiser la variable prediction à une valeur par défaut
    prediction = None
    return render_template('index.html', prediction=prediction)

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return render_template('index.html', error='Aucun fichier trouvé.')

    file = request.files['file']

    if file.filename == '':
        return render_template('index.html', error='Aucun fichier sélectionné.')

    # Préparez l'image pour la prédiction
    file_content = file.read()

    # Envoyez la requête POST
    response = requests.post(prediction_url, data=file_content, headers=headers)

    # Récupérez la prédiction du modèle
    prediction = response.json()['predictions'][0]['tagName']

    return render_template('index.html', prediction=prediction)

if __name__ == '__main__':
    app.run(debug=True)