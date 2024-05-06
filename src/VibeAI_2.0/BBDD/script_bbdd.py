#Importamos las librerias necesarias para ejecutar el script 
from flask import request,Flask
from mysql.connector import connect
app = Flask(__name__)


@app.route('/')
def home():
    return "<h1>HOME</p>"


@app.route('/bbdd', methods=['POST'])
def to_BBDD():
    losdatos = request.get_json()

    nombreusuario = losdatos['username']
    sexo= losdatos['sexo']
    edad= losdatos['edad']
    ocupacion= losdatos['ocupacion']
    text = losdatos['text']
    gender = losdatos['gender']
    ages = losdatos['age']
    music = losdatos['music']
    language = losdatos['language']
    hobbie = losdatos['hobbie']
    recomendacion1 = losdatos['data']['recomendacion1']
    recomendacion2 = losdatos['data']['recomendacion2']
    recomendacion3 = losdatos['data']['recomendacion3']
    opinion1 = losdatos['data']['opcion1']
    opinion2 = losdatos['data']['opcion2']
    opinion3 = losdatos['data']['opcion3']

    # INCORPORAR LA INFO A LA BBDD
    

    # Establecer conexión con SQL
    host ='dbmusic.cb2wgp0ktb7z.us-east-1.rds.amazonaws.com'
    user ='admin'
    password ='thebridge'
    
    # Conexión a la BBDD
    conn = connect(host=host, user=user, password=password)
    cursor = conn.cursor()
    cursor.execute('USE music_rec')

    # Inserción de nuevos usuarios
    cursor.execute(f'INSERT INTO usuarios (nombreusuario) VALUES ("{nombreusuario}")')
    conn.commit()
    
    # Inserción de data usuarios
    cursor.execute(f'INSERT INTO info_usuarios (edad, sexo, ocupacion) VALUES ("{edad}", "{sexo}", "{ocupacion}")')
    conn.commit()
    
    # Inserción de nuevas recomendaciones
    cursor.execute(f'INSERT INTO recomendaciones (text, gender, ages_fwer, music, language, hobbie, recomendacion1, recomendacion2, recomendacion3, opinion1, opinion2, opinion3) VALUES ("{text}","{gender}", "{ages}","{music}", "{language}", "{hobbie}", "{recomendacion1}", "{recomendacion2}", "{recomendacion3}", "{opinion1}", "{opinion2}", "{opinion3}")')
    conn.commit()
 
    conn.close()
    return 'User registered successfully!'





if __name__ == "__main__":
    app.run()


