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

referer = "https://www3.animeflv.net"

def get_html_content(url_page, agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0"):
    headers = {
        "User-Agent": agent,
        "Referer": referer,
    }
    response = requests.get(url_page, headers=headers)
    
    '''
    if response.status_code != 200:
        print(f"Error: No se pudo obtener la página. Código HTTP {response.status_code}")
        exit()
    '''
    return response.text

def save_html_to_file(html_content, filename="output.html"):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(html_content)
    print(f"El HTML se ha guardado en {filename}")

def view_video_link_on_browser(video_link):
    try:
        video_html = get_html_content(video_link)

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
    
def scrap_video_link(name_id, episode_id):
    # Crear la URL usando los parámetros proporcionados | adaptada a animeflv
    url_page = f"https://www3.animeflv.net/ver/{name_id}-{episode_id}"
    print("URL generada:", url_page)

    # Extraer JSON con enlaces, la clave aquí es que todos los videos se encuentran dentro de el tag script
    # Y siguen el pattern: var videos = {"key": "value", "key2": "value2"}; | r'var videos = ({.*?});'
    html_content = get_html_content(url_page)
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
        if soup.find_all(class_="Page404"):
            print("La página asociada a este anime no existe, error 404 not found.")
            return 404
        return 1

    for video in videos_data["SUB"]:
        video_url = video.get('code', None)
        print(video_url)
        
        if video_url:
            print(f"Reproduciendo video: {video['title']} en el servidor {video['server']}")
            print(f"URL: {video_url}")
            
            view_video_link_on_browser(video_url)
            
            user_input = input("Quieres acceder al siguiente servidor (s/n): ")
            if user_input.lower() == 'n':
                print("Deteniendo la ejecución.")
                break
        else:
            print(f"URL no disponible para {video['title']} en el servidor {video['server']}")
        
        time.sleep(1)

def search_anime_name(name):
    search_link=f"https://www3.animeflv.net/browse?q={name}"
    html_content=get_html_content(search_link)
    soup = BeautifulSoup(html_content, 'html.parser')

    # Buscar todos los elementos <a> con href que contengan '/anime/', si sale duplicado se guarda un unico elemento
    unique_links = []
    for a in soup.find_all('a', href=True):
        if '/anime/' in a['href']:
            anime_name = a['href'].replace('/anime/', '')
            if anime_name not in unique_links:
                unique_links.append(anime_name)
    
    num = 1         
    for anime_ref in unique_links:
        print(f"{num}. {anime_ref}")
        num += 1
    
    anime_num=input("Cual te interesa ver? (Introduce su numero) ")
    try:
        anime_index = int(anime_num) - 1  # Restar 1 porque las listas comienzan en 0
        if 0 <= anime_index < len(unique_links):  # Validar que está en rango
            selected_anime = unique_links[anime_index]
            print(f"Has seleccionado: {selected_anime}")
        else:
            print("Número fuera de rango. Por favor, inténtalo de nuevo.")
    except ValueError:
        print("Entrada inválida. Por favor, introduce un número.")
    
    return selected_anime

######################################## MAIN ########################################
def main():
    '''
    if len(sys.argv) != 3:
        print("Se deben proporcionar dos parámetros: name_id y episode_id")
        sys.exit(1)
        
    name_id = sys.argv[1]
    episode_id = sys.argv[2]
    name = sys.argv[1]
    '''
    
    #TBD main loop - debe acabar controlando todo el flujo del programa , se rompe con una interrupcion ctrl+c, ctrl+z
    
    # Solo un arg para el nombre -> devuelve name_id
    anime_name = input("Que anime quieres buscar? ")    
    name_id = search_anime_name(anime_name)
    # Consulta el numero de capitulo a ver -> devuelve episode_id
    episode_id = input("Que capítulo quieres ver? ")
    scrap_video_link(name_id, episode_id)

if __name__ == "__main__":
    main()