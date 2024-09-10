#!/usr/bin/python3

from flask import Flask, request, jsonify
from gtts import gTTS
import os
import uuid
import threading
from queue import LifoQueue
import time
import tempfile

from . import play_audio

app = Flask(__name__)

# Pilha para armazenar as tarefas
task_stack = LifoQueue()

def split_text(input_text,pattern_list):
    text=str(input_text);
    for pattern in pattern_list:
        text = text.replace(pattern, '&');
    sentences = [sentence.strip() for sentence in text.split('&') if sentence]
    return sentences

    
def play_text(text,language,speed=1.25):
    if text.strip():
        # Converter o texto em fala usando gTTS
        tts = gTTS(text=text, lang=language)
        tmp_filename = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        tts.save(tmp_filename.name)

        # Reproduzir o áudio
        play_audio.ajustar_velocidade(tmp_filename.name, speed);

        # Remover o arquivo de áudio após reprodução
        os.remove(tmp_filename.name)

# Função assíncrona para processar a pilha
def process_tasks():
    while True:
        if not task_stack.empty():
            task = task_stack.get()
            task_id, task_data = task
            
            text          = task_data["text"];
            language      = task_data["language"];
            split_pattern = task_data["split_pattern"];
            speed         = task_data["speed"];

            # Processar o texto (dividir de acordo com o padrão se necessário)
            sentences=split_text(text,split_pattern);
                        
            for m in range(len(sentences)):
                #print(sentences[m])
                play_text(sentences[m],language,speed);
        
        time.sleep(1)

# Rota para receber os dados do cliente
@app.route('/add_task', methods=['POST'])
def add_task():
    data = request.json
    task_id = str(uuid.uuid4())
    task_stack.put((task_id, data))
    return jsonify({"id": task_id})

# Rota para remover um item da pilha por ID
@app.route('/remove_task/<task_id>', methods=['DELETE'])
def remove_task(task_id):
    temp_stack = []
    
    # Desempilhar para verificar se o ID está na pilha
    while not task_stack.empty():
        task = task_stack.get()
        if task[0] != task_id:
            temp_stack.append(task)
    
    # Reempilhar os itens que não foram removidos
    for task in temp_stack:
        task_stack.put(task)
    
    return jsonify({"message": f"Tasks with ID {task_id} removed."})

# Iniciar a thread para processar a pilha de forma assíncrona
task_processor_thread = threading.Thread(target=process_tasks, daemon=True)
task_processor_thread.start()

def main():
    app.run(debug=True);

# Iniciar o servidor Flask
if __name__ == "__main__":
    main();

