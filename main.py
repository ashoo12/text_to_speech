

import time


from flask import Flask,request,render_template,Response
import requests
import random

app=Flask(__name__)
app.app_context().push()

api_key="f63cf263242457f0027a76a619bae5c4"
headers = {
  "Accept": "audio/mpeg",
  "Content-Type": "application/json",
  "xi-api-key": api_key
}

@app.route("/")
def home():
    return render_template("index.html")
text=[]

@app.route('/text_to_speech',methods=['POST','GET'])
def text_to_speech():
    global  text
    voice_ids = []
    voice_url = "https://api.elevenlabs.io/v1/voices"
    voice_response = requests.get(url=voice_url, headers=headers)
    voice_data = voice_response.json()
    print(f"voice_response:{voice_response.status_code}")
    for voice in voice_data["voices"]:
      id = voice["voice_id"]
      voice_ids.append(id)
    voice_id = random.choice(voice_ids)
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

    if request.method == 'POST':
        user_text = request.form.get("user_input")
        text.append(user_text)
        print(text[0])
    data = {
        "text": text[0],
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.5}
    }
    response = requests.post(url, json=data, headers=headers, stream=True)
    print(f"tts:{response.status_code}")
    return Response(response.content, mimetype="audio/mpeg")

    #
    # elif request.method == 'GET':
    #     user_text = request.args.get("user_input")
    #     text=user_text
    # print(text)








if __name__=="__main__":
    app.run(debug=True)

