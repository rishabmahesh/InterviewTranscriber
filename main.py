from pydub import AudioSegment
from vosk import Model, KaldiRecognizer, SetLogLevel
import wave
import audioop
import json
import nlp_tools

# download required:  brew install ffmpeg
def mp3_to_wav(source):
    stereoWav = source[0:len(source)-4] + "_stereo.wav"
    monoWav = source[0:len(source)-4] + "_mono.wav"
    # convert mp3 to wav
    sound = AudioSegment.from_mp3(source)
    sound.export(stereoWav, format="wav")

    # read input file and write mono output file
    try:
        # open the input and output files
        inFile = wave.open(stereoWav,'rb')
        outFile = wave.open(monoWav,'wb')
        # force mono
        outFile.setnchannels(1)
        # set output file like the input file
        outFile.setsampwidth(inFile.getsampwidth())
        outFile.setframerate(inFile.getframerate())
        # read
        soundBytes = inFile.readframes(inFile.getnframes())
        print("frames read: {} length: {}".format(inFile.getnframes(),len(soundBytes)))
        # convert to mono and write file
        monoSoundBytes = audioop.tomono(soundBytes, inFile.getsampwidth(), 1, 1)
        outFile.writeframes(monoSoundBytes)

    except Exception as e:
        print(e)

    finally:
        inFile.close()
        outFile.close()
    return monoWav

# To download the model
# curl -LO http://alphacephei.com/vosk/models/vosk-model-en-us-0.22.zip
# and unzip the file
model_path = "model/vosk-model-en-us-0.22"
audio_filename = "audio/Casual_English_Conversation.mp3"

model = Model(model_path)
if audio_filename.__contains__("mp3"):
    audio_filename = mp3_to_wav(audio_filename)
wf = wave.open(audio_filename, "rb")

rec = KaldiRecognizer(model, wf.getframerate())
rec.SetWords(True)

# get the list of JSON dictionaries
results = []
# recognize speech using vosk model
while True:
    data = wf.readframes(500)
    if len(data) == 0:
        break
    if rec.AcceptWaveform(data):
        part_result = json.loads(rec.Result())
        results.append(part_result)
part_result = json.loads(rec.FinalResult())
results.append(part_result)

# convert list of JSON dictionaries to list of 'Word' objects
list_of_words = []
list_of_text = []
for sentence in results:
    # if len(sentence) == 1:
    #     # sometimes there are bugs in recognition
    #     # and it returns an empty dictionary
    #     # {'text': ''}
    #     continue
    # for obj in sentence["result"]:
    #     w = Word(obj)  # create custom Word object
    #     list_of_words.append(w)  # and add it to list
    list_of_text.append(sentence["text"])  # and add it to list

wf.close()  # close audiofile

text = ''
# output to the screen
for sent in list_of_text:
    text = text + sent + ' '
    print(sent)


sentences = nlp_tools.sentence_segment(text)
question_indices = nlp_tools.get_list_question_indices(sentences, ['you need casual english', 'you want to talk to your coworkers '])
answer_lists = nlp_tools.get_list_answer_indices(sentences, question_indices)
q_and_a = {}
print(question_indices)
for i in range(len(question_indices)):
    q_and_a_pair = {}
    q_and_a_pair['question'] = sentences[question_indices[i]]
    q_and_a_pair['answer'] = answer_lists[i]
    q_and_a[i] = q_and_a_pair
print(q_and_a)