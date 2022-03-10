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
#     "audio_filename": "File1"
# }

    request_json = json.loads(request_str)
    audio_filename = request_json['audio_filename'] #use "audio/Casual_English_Conversation.mp3"

    # To download the model
    # curl -LO http://alphacephei.com/vosk/models/vosk-model-en-us-0.22.zip
    # and unzip the file
    model_path = "model/vosk-model-en-us-0.22"
    audio_filename = "audio/M_0399_12y4m_1.wav" #can comment out this line when testing complete

    transcriber = Transcriber(model_path)
    text = transcriber.transcribe(audio_filename)

    # return the points
    to_return = {"transcription": text}
    print(to_return)
    return json.dumps(to_return)


@app.route('/analyzeText', methods=['POST'])
def return_route2():

    # route : http://127.0.0.1:5000/analyzeText
    # Expected post json:
    # {
    #     "audio_filename": "File1",
    #     "questions" : ["Question1", "Question 2"]
    # }

    punct_model = 'Demo-Europarl-EN.pcl'
    sentence_model = 'all-MiniLM-L6-v2'
    nlp_tool = NLP_Tools(punct_model, sentence_model)

    request_str = request.data.decode('utf-8')
    request_json = json.loads(request_str)
    audio_filename = request_json['audio_filename'] #use "audio/Casual_English_Conversation.mp3"
    interview_questions = request_json['questions'] #use ['you need casual english', 'you want to talk to your coworkers ']

    #in future, will pull transcribed text from database
    text = 'so tell bit more about the tennis your your during the six week course or something oh am i went to the charles kensington and chelsea fewer age group yeah and and twelve shift and for the youth games to play in and i got free to that and now on saturday mornings ice clerk to nine o\'clock this intensive training every week but not normally play from nine to eleven which are still days interesting ones quite tiring the free outside eleven and what was his youth games if games is kind of and olympics for awful all the bars in london and they do every sport basically a website and is in july about july the tim forgotten would you know where it is an old the main games is the main sports i held at crystal palace but i sent intense can be held somewhere else i\'m not sure locker yeah i i like for kip to certain extent is not going to be a better yeah it\'s not really it\'s not really my favorite game but i plan that not really watching it i want to do a coaching when you go to law and to sunday from your school coaches yours they don\'t know is kind of someone from our school isn\'t is not asian not really a full-time part-time he just teachers cricket high school says kind of school coach but doesn\'t really have school lot of long as you get in the next at all the time an hour for on friday afternoons control and find your home on party i love it when we\'re not playing this friday with the friday after because they\'re testament because customer and rugby is wi-fi yeah it was tend to and again for your school yeah at my school and do we have sort of more than one team of the cold war oh yeah david team for for you for you and in every day of an eighteen minute bt where\'d you go for that you have to grind yeah in twickenham live right next to the stadium if massive school on your schools in twickenham my schools just in non-opec all right by the grind the yeah what\'s called newborn yeah and you say your favorite subject is mouse my science on my second favorite generic sort of to go to what sort of slots are sort of the physics physics probably done during your own website yeah i\'m trying to the moment i\'m perfect can do on the james bond not quite sure yet i\'m still working on my desk though just thinking you\'ve already got here on email yeah rochester too many do get computer science at school yeah i\'m not really oh we do do it but other early march cause i stopped from the kids from a very early age so you\'re not quite a lot and that\'s just a bit boring really because of teaching there yeah they sent me and what about your computer games what was the one you want and the company dan rest of the thought that the wwf smackdown which is what happens in that just a wrestling basically just fly oldest sorry for the is based on the tv program i like that one like wrestling okay let\'s go completely different and your favorite place you\'ve ever been in new york would you like about and i slept with a shopping this nice atmosphere friendly bustling i\'ll say that florida america is on i\'ve been to america twice where else i\'ve been all around the world ready to as far as australia and new zealand japan uncle different based on holiday yeah yeah i\'m not even all the same time way around the world because it for six weeks wow yeah that must be pretty six was that when you went to new yorker floor no i do with florida florida when as a mercy of house in florida who is too important stuff and and my grandad pay for the whole family fifteen guy it\'s massive house that\'s been granted that other separate you did this right oh yeah my mom howard reading nine or i had my nights birthday as we\'re in the trip and the for my birthday when an elephant nice and in north of thailand january britain muslims are talking about nice i see yeah'
    interview_questions = ['so tell bit more about the tennis', 'i held at crystal palace but i sent intense can be held somewhere else ', 'i\'ve been to america twice'] #can comment out this line when testing complete
    q_and_a = nlp_tool.get_questions_and_answers(text, interview_questions)
    ner = nlp_tool.get_ner(text)

    # return the points
    to_return = {"transcription": q_and_a, "ner": ner}
    print(to_return)
    return json.dumps(to_return)

# to run the server, just run python server.py
if __name__ == '__main__':
    print("Starting the server...")
    app.run(debug=True)