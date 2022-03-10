import json
from pydub import AudioSegment
from vosk import Model, KaldiRecognizer
import wave
import audioop

class Transcriber:

    def __init__(self, model_path):
        """
        Parameters:
          language : the language for the sentence segmenter
          model : model for the sentence transformer
        """
        self.model = Model(model_path)

    # download required:  brew install ffmpeg
    def mp3_to_wav(self, source):
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

    def transcribe(self, audio_filename):
        if audio_filename.__contains__("mp3"):
            audio_filename = self.mp3_to_wav(audio_filename)
        wf = wave.open(audio_filename, "rb")

        rec = KaldiRecognizer(self.model, wf.getframerate())
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

        # convert list of JSON dictionaries to string
        text = ''
        for sentence in results:
            text = text + sentence["text"] + ' '

        wf.close()  # close audiofile

        return text

if __name__ == '__main__':
    # model_path = "model/vosk-model-en-us-0.22"
    # audio_filename = "audio/M_0399_12y4m_1.wav" #can comment out this line when testing complete
    #
    # transcriber = Transcriber(model_path)
    # text = transcriber.transcribe(audio_filename)
    # print(text)
    import spacy
    #nlp = spacy.load('en_core_web_trf')
    nlp = spacy.load('en_core_web_lg')

    doc = nlp('i had practice today from nine to eleven o\'clock. on monday i went to his house at noon. on tuesday i went to his house at one in the afternoon.')
    for ent in doc.ents:
        #gets index in doc
        print(ent.text, ent.start_char, ent.end_char)
        #gets index in sentence
        print(ent.text, ent.start_char-ent.sent.start_char, ent.end_char-ent.sent.start_char, ent.label_)