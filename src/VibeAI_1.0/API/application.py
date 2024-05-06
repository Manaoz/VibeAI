from flask import Flask,jsonify, request
import openai
import json


application = Flask(__name__)

@application.route('/')
def home():
    return "<h1>HOME</p>"

@application.route('/recomendacion', methods = ['POST'])
def get_recommendation():
    openai.api_key = ""
    #Hacemos request del json que utilizaremos para introducir un prompt a ChatGPT
    data = request.get_json()
    #Extraemos los datos del json para alimentar al prompt correctamente
    artista1 = data['grupo1']
    artista2 = data['grupo2']
    #Asignamos el motor para procesar la peticion
    model_engine = "text-davinci-002"
    #Definimos el prompt a hacerle a la API especificando que queremos como salida
    prompts = (f"Recomiendame 3 nombres de grupos similares a {artista1} o {artista2} excluyendo a los mencionados en formato json donde solo aparezcan los nombres de los grupos recomendadospor ejemplo: {'grupo1','grupo2','grupo3'}")
    # prompts = (f"Me gusta {grupos} recomienda tres artistas diferentes a los ya mencionados que me puedan gustar en formato json")
    # prompts = (f"Give me a list of 3 music groups similar to the groups in this {grupos}, the response must be in json format")
    #Corremos la funcion para hacer request, definiendo parametros ajustados a lo que deseamos
    completions = openai.Completion.create(engine = model_engine,
                                        prompt = prompts,
                                        max_tokens = 1024,
                                        n = 1,
                                        stop= None,
                                        temperature = 0.5
                                        )
    resultado = completions.choices[0].text
    return resultado

# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()

