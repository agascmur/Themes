import re
import base64
import requests
from bs4 import BeautifulSoup

def extract_video_links(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # 1. Extraer enlaces del array "video[]"
    script_tags = soup.find_all('script')
    video_links = []
    
    for script in script_tags:
        if 'var video' in script.text:
            # Buscar las entradas del array video[]
            matches = re.findall(r"video\[\d+\] = '(.*?)';", script.text)
            for match in matches:
                # Extraer src dentro del iframe
                src_match = re.search(r'src="([^"]+)"', match)
                if src_match:
                    video_links.append(src_match.group(1))
    
    # Convertir URLs relativas a absolutas
    absolute_links = [
        f"https://example.com{link}" if link.startswith("/") else link
        for link in video_links
    ]
    
    # 2. Extraer enlaces codificados en "servers"
    servers_links = []
    for script in script_tags:
        servers_match = re.search(r"var servers = (\[.*?\]);", script.text, re.DOTALL)
        if servers_match:
            servers = eval(servers_match.group(1))  # Convertir JSON-like a lista
            for server in servers:
                if 'remote' in server:
                    decoded_link = base64.b64decode(server['remote']).decode('utf-8')
                    servers_links.append(decoded_link)
    
    return absolute_links, servers_links

# Obtener el contenido HTML de la página web
url = 'https://jkanime.net/hyakka-ryouran-samurai-bride/1/'
response = requests.get(url)
html_content = response.text

iframe_links, decoded_links = extract_video_links(html_content)

print("Enlaces de video (iframe):")
print("\n".join(iframe_links))

print("\nEnlaces de descarga (decodificados):")
print("\n".join(decoded_links))
