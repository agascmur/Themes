# Dependencias
- **Firefox**: Asegúrate de tener Firefox instalado en tu sistema para poder reproducir los videos.
- **Python**: Debes tener Python instalado.
## Install
```bash
# Crea entorno virtual
python -m venv venv

# Activa en linux
source venv/bin/activate
# Activa en Windows
.\venv\Scripts\activate
# Instala dependencias
pip install -r requirements.txt

# Actualizar requirements.txt
pip freeze > requirements.txt
```

# Uso
Ejecuta el script en la terminal con los siguientes parámetros:
```bash
python ani-pyEs.py $NombreAnime $NumeroCapitulo
```

# DISCLAIMER
En estos momentos es solo una versión incial que requiere trabajo para poder encontrar los capítulos como es debido. Solo lo he testeado con un par de animes.
