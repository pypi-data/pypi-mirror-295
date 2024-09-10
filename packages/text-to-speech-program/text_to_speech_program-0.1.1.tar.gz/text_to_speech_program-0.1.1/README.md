# Text to Speech Program

This package provides a text-to-speech server, using `gtts` and `playsound`, and a client program to interact with the server.

## 1. Installing

### 1.1. Install the package pip

To install the package from `pypi`, follow the instructions below:


```bash
pip install text_to_speech_program
```

Execute `which tts-program-server` to see where it was installed, probably in `/home/USERNAME/.local/bin/tts-program-server`.


### 1.2. Add a program to the Linux service

```bash
curl -fsSL https://raw.githubusercontent.com/trucomanx/text_to_speech_program/main/install_linux_service.sh | sh
```

After the last code, the program server starts at with the operating system.
Now the next commands are accepted (Use them if necessary).

#### 1.2.1. Start server service in linux
**You only need to start the server if it has been stopped or is disabled from starting with Linux boot**.

```bash
sudo systemctl start tts-program-server
```

#### 1.2.2. Stop server service in linux

```bash
sudo systemctl stop tts-program-server
```

#### 1.2.3. Disable service at linux startup

```bash
sudo systemctl disable tts-program-server
```

## 2. Using

### 2.1. Start the server
**You only need to start the server if it has been stopped**.
If the program server was not added to the Linux service, then to start the text-to-speech server, use the command below:

```bash
tts-program-server
```

This starts a server that will listen on `http://127.0.0.1:5000` and will be ready to receive text conversion requests.



### 2.2. Start the client

The client can submit conversion text-to-speech tasks or remove pending jobs from the server.

#### 2.2.1. Sending a JSON file:
Adding a text-to-speech task.

```bash
tts-program-client send /caminho/para/arquivo.json
```

JSON file example:

```json
{
    "text": "Some text to convert.\n\n OK",
    "language": "en",
    "split_pattern": [".", "\n\n"],
    "speed":1.25
}
```

#### 2.2.2. Sending a DICT from string:
Adding a text-to-speech task.

```bash
tts-program-client senddict '{ "text": "Some text to convert. OK", "language": "en", "split_pattern": ["."], "speed":1.25 }'
```

#### 2.2.3. Remove a task from the stack using the ID:

```bash
tts-program-client remove <ID>
```

Replace `<ID>` with the unique ID returned when adding a task.


## 3. License

This project is licensed under the GPL license. See the `src/LICENSE` file for more details.
