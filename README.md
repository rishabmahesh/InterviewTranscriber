# InterviewTranscriber

This tool will achieve the following tasks: transcribe an audio file to text, create sentence segments from the transcription,
identify the interview questions and corresponding answers, and identify key elements of the answers. 

The following downloads are required: ffmpeg

Additional steps are needed to integrate Punctuator:
- Download the model from https://drive.google.com/drive/u/1/folders/0B7BsN5f2F1fZQnFsbzJ3TWxxMms?resourcekey=0-6yhuY9FOeITBBWWNdyG2aw
    - I used the Demo-Europarl-en.pcl
- in the punctuator folder, edit punc.py line 171 to include the file path for the model
