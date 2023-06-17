
<p align="center">
  <img src="https://media.giphy.com/media/oepOUjo00amPeTO6ye/giphy.gif" width=600 height=350 alt="animated" />
</p>

# AbleReInvigorated

This project was first introduced at CruzHacks 2023, and now it's heading towards becoming a compelling solution. We created a **question answer chatbot for youtube videos** using semantic search, large language models, and REST API. The name is quite self-explanatory.

The project is **livestreamed** at https://reainvent.com/

## What is it for? 

This solution promotes efficient learning by quickly converting extensive video content to text. It's especially handy for revisiting parts of long lectures, hunting down specific details, or looking up certain policies. Furthermore, it's applicable to any YouTube video with quality transcription and can speed up the process of obtaining key information.

## How does it work? 

This bot leverages `pytube` and `youtube_transcript_api` to extract transcription from a given YouTube URL. A semantic search is then run, using OpenAI's embedding models, to pinpoint the most relevant parts of the video. GPT-DaVinci, OpenAI's largest LLM, forms accurate and comprehensible responses based on this context.

Prompt engineering is used to avoid misinformation, and relevant timestamps are provided for easy reference.

# Running in Development Mode

## Create a virtual environment
1. Navigate to the project directory
2. Create the virtual environment
```console 
python3 -m venv ./venv
```
3. Activate the virtual environment
```console 
/venv/Scripts/activate.bat
```
## Install dependencies
```console 
pip install -r requirements.txt
```
## Start the API
```console 
python3 ./backend/server.py
```
_Note: An OpenAI API key in a .env file within the backend directory is required. And OpenAI APIs are not free to use beyond the free trial. The .env file should contain the line `openai_key = "{API_KEY}"`._
## Start the Website
*When running in development mode, make sure to set this line at the top of App.js so the site can communicate with the API. By default, it is set to "/api"*
```console
const API_ENDPOINT = "";
```
Then, initialise the website.
```console
cd frontend
npm start
```

Proceed to localhost:3000 to access the webserver.

### Note
These instructions are designed for the development mode. The API and frontend can be built for production in several possible ways. Currently, AbleReInvigorated is hosted on a Google Cloud VM, using Gunicorn for the backend, and Nginx for the frontend.