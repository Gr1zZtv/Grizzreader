from datetime import datetime
import os
from threading import Thread
from flask import Flask, jsonify
from TikTokLive import TikTokLiveClient
from TikTokLive.types.events import CommentEvent, ConnectEvent

# Define the path to the HTML file and CSS file
html_file_path = os.path.join(os.getcwd(), "index.html")
css_file_path = os.path.join(os.getcwd(), "style.css")

# Instantiate the Flask app
app = Flask(__name__)

# Define a new route that returns the chat messages as JSON
@app.route('/chat')
def get_chat():
    # Read the chat messages from the HTML file
    with open(html_file_path, 'r', encoding='utf-8') as f:
        chat_messages = f.read()

    # Return the chat messages as JSON
    return jsonify({'chat': chat_messages})

# Start the Flask app in a separate thread
def run_flask_app():
    app.run()

flask_thread = Thread(target=run_flask_app)
flask_thread.start()

# Instantiate the client with the user's username
client = TikTokLiveClient(unique_id="@7yla")

# Define how you want to handle specific events via decorator
@client.on("connect")
async def on_connect(_: ConnectEvent):
    print("Connected to Room ID:", client.room_id)

    # Create the HTML file with initial content when connected
    with open(html_file_path, "w") as f:
        f.write("<!DOCTYPE html>\n")
        f.write("<html>\n")
        f.write("<head>\n")
        f.write("<meta charset='UTF-8'>\n")
        f.write("<meta http-equiv='refresh' content='5'>\n")
        f.write(f"<link rel='stylesheet' type='text/css' href='{css_file_path}'>\n")
        f.write("<title>TikTok Live Chat</title>\n")
        f.write("</head>\n")
        f.write("<body>\n")
        f.write("<h1>TikTok Live Chat</h1>\n")
        f.write("</body>\n")
        f.write("</html>\n")

# Define handling an event via "callback"
@client.on("comment")
async def on_comment(event: CommentEvent):
    print(f"{event.user.nickname} -> {event.comment}")

    # Update the HTML file with the new message
    with open(html_file_path, "a", encoding="utf-8") as f:
        f.write(f"<p><span class='user-nickname'>{event.user.nickname}:</span> {event.comment.encode('ascii', 'ignore').decode('ascii')}</p>\n")

if __name__ == '__main__':
    # Add the listener for comment event
    client.add_listener("comment", on_comment)

    # Start the client and block the main thread
    # await client.start() to run non-blocking
    client.run()

