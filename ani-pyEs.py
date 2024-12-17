import re
import time
import requests
import subprocess
from bs4 import BeautifulSoup
import sys
import json
import webbrowser
import os
import platform

def get_html_content(referer, url_page, agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0"):
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

def view_video_link_on_browser(video_link, referer):
    try:
        video_html = get_html_content(referer, video_link)

        firefox_path = None
        if platform.system() == "Linux":
            firefox_path = "/usr/bin/firefox"
        elif platform.system() == "Windows":
            firefox_path = "C:/Program Files/Mozilla Firefox/firefox.exe"

        if firefox_path and os.path.isfile(firefox_path):
            webbrowser.register('firefox', None, webbrowser.BackgroundBrowser(firefox_path))
            browser = webbrowser.get('firefox')
        else:
            browser = webbrowser.get()

        browser.open(video_link)
        print(f"Reproducción del video establecida para el enlace: {video_link}.")
    except Exception as e:
        print(f"No se pudo reproducir el video en {video_link}. Error: {e}")
    
def scrap_video_link(name_id, episode_id, referer):
    # Crear la URL usando los parámetros proporcionados | adaptada a animeflv
    url_page = f"https://www3.animeflv.net/ver/{name_id}-{episode_id}"
    print("URL generada:", url_page)

    # Extraer JSON con enlaces, la clave aquí es que todos los videos se encuentran dentro de el tag script
    # Y siguen el pattern: var videos = {"key": "value", "key2": "value2"}; | r'var videos = ({.*?});'
    html_content = get_html_content(referer, url_page)
    soup = BeautifulSoup(html_content, 'html.parser')
    script_tags = soup.find_all('script')
    pattern = r'var videos = ({.*?});'
    match = re.search(pattern, html_content)

    if match:
        videos_json = match.group(1)
        videos_data = json.loads(videos_json)
        print("Videos Scrappeados:")
        print("##############################################################")
        print(videos_data)
        print("##############################################################")
    else:
        print("No se encontró la variable 'videos'.")

    for video in videos_data["SUB"]:
        video_url = video.get('code', None)
        print(video_url)
        
        if video_url:
            print(f"Reproduciendo video: {video['title']} en el servidor {video['server']}")
            print(f"URL: {video_url}")
            
            view_video_link_on_browser(video_url, referer)
            
            user_input = input("¿Quieres dejer de probar servidores de vídeo? (s/n): ")
            if user_input.lower() == 's':
                print("Deteniendo la ejecución.")
                break
        else:
            print(f"URL no disponible para {video['title']} en el servidor {video['server']}")
        
        time.sleep(1)

def search_anime_ids(name):
    
    return("Berserk")

######################################## MAIN ########################################
def main():
    if len(sys.argv) != 3:
        print("Se deben proporcionar dos parámetros: name_id y episode_id")
        sys.exit(1)
        
    #name_id = sys.argv[1]
    episode_id = sys.argv[2]
    name = sys.argv[1]
    referer = "https://www3.animeflv.net"

    # TBD - Solo un arg para el nombre -> devuelve name_id
    name_id = search_anime_ids(name)
    # TBD - Consulta el numero de capitulo a ver -> devuelve episode_id
    
    scrap_video_link(name_id, episode_id, referer)

if __name__ == "__main__":
    main()