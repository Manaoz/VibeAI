#Importamos las librerias necesarias para ejecutar el script 
import openai
from flask import Flask, request


app = Flask(__name__)
app.config['DEBUG'] = True
openai.api_key = ""


@app.route('/recomendaciones', methods=['POST'])

#Función para pasar los archivos tipo json a python

def json_to_python():
    #Hacemos request del json que utilizaremos para introducir un prompt a ChatGPT
    data = request.get_json()
    
    #Extraemos los datos del json para alimentar al prompt correctamente
    artista1 = data['grupo1']
    artista2 = data['grupo2']
    similaridad = data['similarity']


    #Asignamos el motor para procesar la peticion
    model_engine = "text-davinci-002"
    
    #Definimos el prompt a hacerle a la API especificando que queremos como salida
    prompts = (f"Hazme una lista seguida con el nombre de 3 grupos/artistas segun genero musical,estilo musical,sus canciones y popularidad, época, país de origen,si son bandas o solistas, similares a ambos {artista1} y {artista2},pero no incluyas nunca estos en la lista, es decir NO REPITAS LOS NOMBRES DE {artista1} ni a {artista2},e incluye el porcentaje de similitud que tu creas que tienen con  {artista1} y {artista2} comparando segun el genero musical,estilo musical,sus canciones y popularidad,siendo mayor al {similaridad}%. El output siempre debe aparecer en el siguiente formato de ejemplo ='Artista/grupo 1','Artista/grupo 2','Artista/grupo 3','similitud del Artista/grupo 1 ejemplo= %''similitud del Artista/grupo 2 ejemplo= %','similitud del Artista/grupo 3 %'. La salida deberia quedar como el siguiente ejemplo: Artista/grupo 1,Artista/grupo 2,Artista/grupo 3,int %,int %,int %. todo DEBE QUEDAR en la misma linea sin saltos, no quiero que me devuelvas nada que no se ajuste a ese formato que te he mostrado, todo debe estar en una sola linea")    
    #Corremos la funcion para hacer request, definiendo parametros ajustados a lo que deseamos 
    completions = openai.Completion.create(engine = model_engine,
                                        prompt = prompts,
                                        max_tokens = 80,
                                        n = 1,
                                        stop= None,
                                        temperature = 0.1,
                                        top_p = 0.8
                                        )
    
    # Eliminamos los caracteres de nueva línea que no son necesarios en la respuesta
    response = completions.choices[0].text
    response = response.replace("'","")
    response = response.replace(", ",",")
    response = response.replace(":","")
    response = response.replace("Lista: ","")
    response = response.replace(".","")
    response = response.replace("%","")
    
    
    return (response)


if __name__ == "__main__":
    app.run(port=5000)
