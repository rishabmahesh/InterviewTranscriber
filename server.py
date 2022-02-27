import json
from flask import Flask, request
from flask_cors import CORS
from nlp_tools import NLP_Tools
from transcribe_audio import Transcriber

app = Flask(__name__)
CORS(app)

@app.route('/sendTranscription', methods=['POST'])
def return_route():
    # get the request
    request_str = request.data.decode('utf-8')

# route : http://127.0.0.1:5000/sendTranscription
# Expected post json:
# {
#     "audio_filename": "File1",
#     "questions" : ["Question1", "Question 2"]
#
# }

    request_json = json.loads(request_str)
    audio_filename = request_json['audio_filename'] #use "audio/Casual_English_Conversation.mp3"
    interview_questions = request_json['questions'] #use ['you need casual english', 'you want to talk to your coworkers ']

    # To download the model
    # curl -LO http://alphacephei.com/vosk/models/vosk-model-en-us-0.22.zip
    # and unzip the file
    model_path = "model/vosk-model-en-us-0.22"
    audio_filename = "audio/Casual_English_Conversation.mp3" #can comment out this line when testing complete

    transcriber = Transcriber(model_path)
    text = transcriber.transcribe(audio_filename)

    punct_model = 'Demo-Europarl-EN.pcl'
    sentence_model = 'all-MiniLM-L6-v2'
    nlp_tool = NLP_Tools(punct_model, sentence_model)

    interview_questions = ['you need casual english', 'you want to talk to your coworkers '] #can comment out this line when testing complete
    q_and_a = nlp_tool.get_questions_and_answers(text, interview_questions)

    # return the points
    to_return = {"transcription": q_and_a}
    print(to_return)
    return json.dumps(to_return)

# to run the server, just run python server.py
if __name__ == '__main__':
    print("Starting the server...")
    app.run(debug=True)