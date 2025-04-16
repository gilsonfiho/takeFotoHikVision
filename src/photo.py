# Autor: Gilson Almeida
# Script para captura e Armazenamento de Imagens da Câmera HikVision

import requests
import os
import time

# Configurações da câmera
camera_ip = ''
username = 'admin'
password = ''

# Diretório onde as fotos serão salvas
save_directory = '/img/'

# Criar o diretório se não existir
if not os.path.exists(save_directory):
    os.makedirs(save_directory)

# Criar uma sessão
session = requests.Session()
session.auth = (username, password)

# Função para capturar foto


def capture_photo():
    url = f'http://{camera_ip}/ISAPI/Streaming/channels/101/picture'
    response = session.get(url, stream=True)
    if response.status_code == 200:
        # Adiciona os milissegundos
        timestamp = time.strftime("%Y%m%d-%H%M%S-%f")[:-3]
        filename = os.path.join(save_directory, f'photo_{timestamp}.jpg')
        with open(filename, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print(f'Foto capturada e salva: {filename}')
    else:
        print('Falha ao capturar foto', response.status_code, response.text)


# Intervalo entre capturas de foto (em segundos)
interval = 0.5

# Loop para capturar fotos periodicamente
try:
    while True:
        capture_photo()
        time.sleep(interval)
except KeyboardInterrupt:
    print('Captura de fotos interrompida pelo usuário')
