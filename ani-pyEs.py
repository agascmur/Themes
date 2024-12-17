import re
import time
import requests
import subprocess
from bs4 import BeautifulSoup
import sys
import json

def get_html_content(referer, url_page, agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0"):

    # Descargar la página web
    headers = {
        "User-Agent": agent,
        "Referer": referer,
    }
    response = requests.get(url_page, headers=headers)

    if response.status_code != 200:
        print(f"Error: No se pudo obtener la página. Código HTTP {response.status_code}")
        exit()
    
    return response.text

def save_html_to_file(html_content, filename="output.html"):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(html_content)
    print(f"El HTML se ha guardado en {filename}")

# Comprobar que se pasaron suficientes argumentos
if len(sys.argv) != 3:
    print("Se deben proporcionar dos parámetros: video_id y episode_id")
    sys.exit(1)

# ================== MAIN ================== #

# Obtener los parámetros del terminal (los índices 1 y 2)
video_id = sys.argv[1]
episode_id = sys.argv[2]
referer = "https://www3.animeflv.net"

# Crear la URL usando los parámetros proporcionados
url_page = f"https://www3.animeflv.net/ver/{video_id}-{episode_id}"

# Imprimir la URL
print("URL generada:", url_page)

# Extraer JSON con enlaces
html_content = get_html_content(referer, url_page)

# Usamos BeautifulSoup para analizar el HTML
soup = BeautifulSoup(html_content, 'html.parser')

# Ahora, busca el script que contiene el objeto 'videos'
script_tags = soup.find_all('script')

# Usamos una expresión regular para encontrar el objeto 'videos'
pattern = r'var videos = ({.*?});'
match = re.search(pattern, html_content)

if match:
    # Convertimos el string JavaScript a un diccionario de Python
    videos_json = match.group(1)
    videos_data = json.loads(videos_json)

    # Ahora 'videos_data' es un diccionario Python que contiene los datos
    print("Videos Scrappeados:")
    print("##############################################################")
    print(videos_data)
    print("##############################################################")
else:
    print("No se encontró la variable 'videos'.")

# Recorrer los videos
for video in videos_data["SUB"]:
    # Obtener la URL del video (usar 'url' si está disponible)
    video_url = video.get('code', None)
    print(video_url)
    
    if video_url:
        print(f"Reproduciendo video: {video['title']} en el servidor {video['server']}")
        print(f"URL: {video_url}")
        
        # Intentar reproducir el video en mpv usando subprocess
        try:
            video_html = get_html_content(video_url, video_url)

            # Llamar a firefox con el enlace del video
            subprocess.run(["firefox", "--private", video_url])
            print(f"Reproducción del video {video['title']} establecida.")
            
        except Exception as e:
            print(f"No se pudo reproducir el video {video['title']}. Error: {e}")
        
        # Preguntar si detener la ejecución tras el video
        user_input = input("¿Quieres dejer de probar servidores de vídeo? (s/n): ")
        if user_input.lower() == 's':
            print("Deteniendo la ejecución.")
            break
    else:
        print(f"URL no disponible para {video['title']} en el servidor {video['server']}")
    
    # Un pequeño retraso entre reproducciones
    time.sleep(1)