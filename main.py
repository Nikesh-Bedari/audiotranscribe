import requests
import sys
from api_secrets import API_KEY_ASSEMBLYAI



upload_endpoint = "https://api.assemblyai.com/v2/upload"
transcript_endpoint = "https://api.assemblyai.com/v2/transcript"
file_path = sys.argv[1] #run the main.py file from terminal and pass the filename at the end of it e.g = $python main.py file.wav
headers = {'authorization': API_KEY_ASSEMBLYAI} #keep a variable of api key in a seperate file and import and use it.

def upload(file_path):
    def read_file(file_path, chunk_size=5242880):
        with open(file_path, 'rb') as _file:
            while True:
                data = _file.read(chunk_size)
                if not data:
                    break
                yield data
    upload_response = requests.post(upload_endpoint, headers=headers, data=read_file(file_path))
    audio_url = upload_response.json()['upload_url']
    return audio_url


def transcribe(audio_url):
    json = {"audio_url": audio_url}
    transcript_response = requests.post(transcript_endpoint, json=json, headers=headers)
    task_id = transcript_response.json()['id']
    return task_id

def poll():
    while True:
        poll_endpoint = transcript_endpoint + '/' + task_id
        poll_response = requests.get(poll_endpoint, headers=headers)

        if poll_response.json()['status'] == "completed":
            return poll_response.json()
        elif poll_response.json()['status'] == "error":
            return "error"

def save_text(poll_response):
    text_filename = file_path + ".txt"
    with open(text_filename,"w") as empty_textfile:
        word_list = poll_response['text'].split()
        for i in word_list:
            empty_textfile.write(f"{i: <10}\n")
    

audio_url = upload(file_path)
task_id = transcribe(audio_url)
poll_response = poll()
save_text(poll_response)



