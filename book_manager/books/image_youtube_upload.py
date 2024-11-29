import os
import pickle
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from mutagen.mp3 import MP3
from PIL import Image, ImageDraw, ImageFont
import moviepy.editor as mp
from googleapiclient.http import MediaFileUpload



#   pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client mutagen Pillow moviepy
#   pip install pydub mutagen Pillow
#   pip install mutagen Pillow moviepy





# Function to authenticate to YouTube API
def authenticate_youtube_api(credentials_file):
    """Authenticate to the YouTube API."""
    scopes = ["https://www.googleapis.com/auth/youtube.upload"]

    # Check if we have a valid token already
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)
    else:
        # If not, we need to authenticate using OAuth 2.0
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            credentials_file, scopes)
        creds = flow.run_local_server(port=0)

        # Save the credentials for the next time
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)
    
    # Build the YouTube API client
    youtube = googleapiclient.discovery.build("youtube", "v3", credentials=creds)
    return youtube


# Function to read audio metadata (name, title, and link)
def get_audio_metadata(file_path):
    audio = MP3(file_path)
    name = audio.get("TIT2", "Unknown Name")
    title = audio.get("TIT1", "Unknown Title")
    link = audio.get("URL", "Unknown Link")
    return name, title, link


# Function to insert metadata into an image
def insert_metadata_into_image(image_path, metadata, output_path):
    img = Image.open(image_path)
    draw = ImageDraw.Draw(img)
    
    # Specify the font and size
    font = ImageFont.truetype("arial.ttf", 40)

    name, title, link = metadata

    # Define positions for the metadata text
    name_position = (100, 100)
    title_position = (100, 150)
    link_position = (100, 200)

    # Insert metadata into the image
    draw.text(name_position, f"Name: {name}", font=font, fill="black")
    draw.text(title_position, f"Title: {title}", font=font, fill="black")
    draw.text(link_position, f"Link: {link}", font=font, fill="black")
    
    # Save the edited image
    img.save(output_path)


# Function to convert audio to video with image as background
def audio_to_video(audio_file, image_file, output_video):
    audio_clip = mp.AudioFileClip(audio_file)
    image_clip = mp.ImageClip(image_file)

    # Set the duration of the image to match the audio duration
    image_clip = image_clip.set_duration(audio_clip.duration)
    image_clip = image_clip.resize(height=720)  # Adjust to your preferred resolution
    image_clip = image_clip.set_fps(24)

    video = image_clip.set_audio(audio_clip)

    # Write the video to the output file
    video.write_videofile(output_video, codec="libx264", audio_codec="aac")


# Function to upload the video to YouTube
def upload_video_to_youtube(youtube, video_file, title, description):
    try:
        request_body = {
            "snippet": {
                "title": title,
                "description": description,
                "tags": ["music", "audio", "video"]
            },
            "status": {
                "privacyStatus": "public"
            }
        }

        video_file = os.path.abspath(video_file)
        media_file = MediaFileUpload(video_file, mimetype="video/mp4")

        video_request = youtube.videos().insert(
            part="snippet,status",
            body=request_body,
            media_body=media_file
        )

        # Upload the video
        video_request.upload()
        print(f"Video uploaded successfully with title: {title}")
    except Exception as e:
        print(f"An error occurred: {e}")


# Main function to create the video and upload it to YouTube
def create_video_from_audio_and_upload(audio_file, image_template, credentials_file, output_video):
    # Step 1: Get metadata from the audio file
    metadata = get_audio_metadata(audio_file)
    title = metadata[1]  # Title from audio metadata
    description = f"Audio Title: {metadata[1]}\nAudio Link: {metadata[2]}"  # Description from audio metadata
    
    # Step 2: Create the image with metadata
    image_output = "generated_image.jpg"
    insert_metadata_into_image(image_template, metadata, image_output)
    
    # Step 3: Convert the audio and image into a video
    audio_to_video(audio_file, image_output, output_video)
    
    # Step 4: Authenticate to YouTube API
    youtube = authenticate_youtube_api(credentials_file)
    
    # Step 5: Upload the video to YouTube
    upload_video_to_youtube(youtube, output_video, title, description)


# Example usage:
audio_file_path = "path_to_audio_file.mp3"  # Path to your audio file
image_template_path = "path_to_image_template.jpg"  # Path to your image template
output_video_path = "output_video.mp4"  # Path for saving the generated video
credentials_file_path = "credentials.json"  # Path to your OAuth credentials JSON file

# Run the function to create and upload the video
create_video_from_audio_and_upload(audio_file_path, image_template_path, credentials_file_path, output_video_path)
