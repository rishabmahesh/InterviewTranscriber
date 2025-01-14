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