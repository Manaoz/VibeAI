import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import openai
from flask import Flask,jsonify, request
from getpass import getpass
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import openai



# Crear una aplicacion Flask y activamos DEBUG
app = Flask(__name__)



# Establecer la clave API de OpenAI
openai.api_key = "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"

# Spotify id de cliente, secreto y URI de redireccion
client_id = "cee22b31b99d413ebf63703888f54b3b"
client_secret = "67adf8a717e047e8a72d2f920fb3a930"

client_credentials_manager = SpotifyClientCredentials(client_id,client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


@app.route('/')
def home():
    return "<h1>HOME</p>"

# Configurar el endpoint '/recomendaciones' que solo responde a las solicitudes POST
@app.route('/recomendacion', methods = ['POST'])
#Función para pasar los archivos tipo json a python

def json_to_python():
    #Hacemos request del json que utilizaremos para introducir un prompt a ChatGPT
    data = request.get_json()
    
    #Extraemos los datos del json para alimentar al prompt correctamente
    text = data['text']
    gender = data['gender']
    ages = data['ages']
    music = data['music']
    hobbie = data['hobbie']
    language = data['language']

     #Corremos la funcion para hacer request, definiendo parametros ajustados a lo que deseamos 
    Prompts = (f"Quiero que me des el titulo de tres canciones diferentes con sus artistas o grupos que esté en idioma {language}, con su cantante o grupo, que esté relacionado  o evoque con el siguiente texto: '{text}'. Recuerda que la cancion deberia estar en Spotify. Ademas de basarte en el texto '{text}' para relacionar una cancion existente y que sea en idioma {language}, ten en cuenta que es para mis stories de instagram y las caracteristicas de mis seguidores son los siguientes: son de género {gender}, con edades entre {ages}, que les gusta el estilo musical {music},y mi instagram se basa en actividad de {hobbie}. Basándote en el siguiente texto: ' {text} ', y en las características de mis seguidores que te he dicho,tienes que devolverme el titulo de una cancion, la cual su letra debe estar en idioma {language} y sea estilo musical de {music},junto a su cantante, el formato tiene que ser: titulo de la cancion, grupo/cantante de esa cancion, recuerda que la letra de la canción debe estar en idioma {language} y debe pertenecer a la clasificacion musical de {music}")
    while True:
    # Realizar la petición a OpenAI
        model_engine = "text-davinci-003"

        completions = openai.Completion.create(engine = model_engine,
                                        prompt = Prompts,
                                        max_tokens = 64,
                                        n = 3,
                                        stop= None,
                                        temperature = 0.7,
                                        frequency_penalty = 0.8,
                                        presence_penalty = 0.5,
                                        top_p = 1
                                        )

        # Obtener la respuesta
        song = completions["choices"][0]["text"]
        song1 = completions["choices"][1]["text"]
        song2 = completions["choices"][2]["text"]
        # Buscar en Spotify
        result = sp.search(q=song, type='track')
        result1 = sp.search(q=song1, type='track')
        result2 = sp.search(q=song2, type='track')
        # Buscar en Spotify
        # Comprobar si se encontró una coincidencia
        if result["tracks"]["total"] > 0:
            # Obtener el título y el artista para la recomendacion 1
            title = result["tracks"]["items"][0]["name"]
            artist = result["tracks"]["items"][0]["artists"][0]["name"]
            uri = result["tracks"]["items"][0]["artists"][0]["id"]
            # Quitamos el caracter ',' para que no de errores
            title.replace(',','')
            # Obtener el título y el artista para la recomendacion 2
            title1 = result1["tracks"]["items"][0]["name"]
            artist1 = result1["tracks"]["items"][0]["artists"][0]["name"]
            uri1 = result1["tracks"]["items"][0]["artists"][0]["id"]

            title1.replace(',','')
            # Obtener el título y el artista para la recomendacion 3
            title2 = result2["tracks"]["items"][0]["name"]
            artist2 = result2["tracks"]["items"][0]["artists"][0]["name"]
            uri2 = result2["tracks"]["items"][0]["artists"][0]["id"]

            title2.replace(',','')
            break
        else:
            # Volver a realizar el prompt
            Prompts = "No se ha encontrado esa cancion, dame otro nombre de una cancion y cantante que sean en idioma {language} y que se considere como genero musical de {music},recuerda que tiene que tiene que ser una recomendación basada en este texto '{text}',y basado también en el perfil de los seguidores de instagram que tienen edades entre {ages} y el canal de Instagram está dedicado a {hobbie}"
    return(
    {
        "data": [
            {
                "recomendacion1": f"{title},{artist}",
                "uri": f"{uri}"
            },
            {
                "recomendacion2": f"{title1},{artist1}",
                "uri": f"{uri1}"
            },
            {
                "recomendacion3": f"{title2},{artist2}",
                "uri": f"{uri2}"
            }
        ]
    }
)



if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    app.run(debug=True)
