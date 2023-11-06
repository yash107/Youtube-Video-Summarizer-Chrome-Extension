from flask import Flask, request
from youtube_transcript_api import YouTubeTranscriptApi
from transformers import pipeline

app = Flask(__name__)

@app.get('/summary')
def summary_api():
    url = request.args.get('url', '')
    # for the url of the video
    video_id = url.split('=')[1]
    # to get only the part that is before the =
    summary = get_summary(get_transcript(video_id))
    # final summary output 
    return summary, 200

def get_transcript(video_id):
    transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
    # get the transcript of the entire video from the api call 
    transcript = ' '.join([d['text'] for d in transcript_list])
    return transcript

def get_summary(transcript):
    summariser = pipeline('summarization')
    #pipeline module is used in which summarization model is used to summarize the transcript that was generated 
    summary = ''
    for i in range(0, (len(transcript)//1000)+1):
        summary_text = summariser(transcript[i*1000:(i+1)*1000])[0]['summary_text']
        summary = summary + summary_text + ' '
    return summary
    

if __name__ == '__main__':
    app.run()