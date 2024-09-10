#!/usr/bin/python3
import requests
import json
import sys
import os

def send_json_from_dict(server_url,data):
    # Enviar solicitação POST ao servidor
    response = requests.post(f'{server_url}/add_task', json=data)

    if response.status_code == 200:
        print(f"Task sent successfully! ID: {response.json()['id']}")
        return response.json()['id'];
    else:
        print("Error submitting task.")
        return None

def send_json_from_file(server_url,filepath):
    # Verificar se o arquivo existe
    if not os.path.isfile(filepath):
        print(f"File {filepath} not found.")
        return None

    # Carregar o conteúdo do arquivo JSON
    try:
        with open(filepath, 'r') as file:
            data = json.load(file)
    except json.JSONDecodeError:
        print(f"Error reading JSON file {filepath}.")
        return None

    return send_json_from_dict(server_url,data);


def remove_task(server_url,task_id):
    # Enviar solicitação DELETE ao servidor
    response = requests.delete(f'{server_url}/remove_task/{task_id}')

    if response.status_code == 200:
        print(response.json()["message"])
        return response.json()["message"]
    else:
        print("Error removing task:",task_id)
        return None

def main():
    # URL do servidor
    SERVER_URL = 'http://localhost:5000'

    # Verificar o comando recebido
    if len(sys.argv) < 2:
        print("Use: tts-program-client <command> <arguments>")
        print("Commands:")
        print("  send <path_arquive_json>")
        print("  senddict \"{dict_code}\"")
        print("  remove <ID>")
        sys.exit(1)

    command = sys.argv[1]

    if command == "send":
        if len(sys.argv) != 3:
            print("Use: tts-program-client send <path_arquive_json>")
            sys.exit(1)

        filepath = sys.argv[2]
        send_json_from_file(SERVER_URL,filepath)

    elif command == "senddict":
        if len(sys.argv) != 3:
            print("Use: tts-program-client senddict \"{dict_code}\"")
            sys.exit(1)
        
        data_dict = json.loads(sys.argv[2])
        send_json_from_dict(SERVER_URL,data_dict)

    elif command == "remove":
        if len(sys.argv) != 3:
            print("Use: tts-program-client remove <ID>")
            sys.exit(1)

        task_id = sys.argv[2]
        remove_task(SERVER_URL,task_id)

    else:
        print("Command unknown. Use 'send', 'denddict' or 'remove'.")

# Iniciar o servidor Flask
if __name__ == "__main__":
    main();
 
