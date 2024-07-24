import streamlit as st
from moviepy.editor import ImageClip, AudioFileClip
import tempfile
import os

# Streamlit application
st.title('Image and Audio to Video')

image_file = st.file_uploader("Upload an Image", type=["png", "jpg", "jpeg"])
audio_file = st.file_uploader("Upload an MP3 Audio File", type=["mp3"])

if image_file and audio_file:
    st.write("Files uploaded successfully!")
    
    # Save the uploaded files
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as img_tmp_file:
        img_tmp_file.write(image_file.getvalue())
        image_path = img_tmp_file.name
        st.write(f"Image saved to {image_path}")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as audio_tmp_file:
        audio_tmp_file.write(audio_file.getvalue())
        audio_path = audio_tmp_file.name
        st.write(f"Audio saved to {audio_path}")
    
    # Load image and audio
    image_clip = ImageClip(image_path)
    audio_clip = AudioFileClip(audio_path)
    
    # Set the duration of the image clip to match the audio
    image_clip = image_clip.set_duration(audio_clip.duration)
    
    # Set the audio of the image clip
    video = image_clip.set_audio(audio_clip)
    st.write("Video composition completed.")
    
    # Save the final video
    output_path = tempfile.mktemp(suffix=".mp4")
    video.write_videofile(output_path, codec="libx264", fps=24, logger=None, verbose=False)
    st.write(f"Video saved to {output_path}")
    
    # Provide video file for download
    with open(output_path, "rb") as video_file:
        st.video(video_file.read())
        st.download_button(label="Download Video", data=video_file, file_name="output_video.mp4", mime="video/mp4")

    # Cleanup
    os.remove(image_path)
    os.remove(audio_path)
    os.remove(output_path)
else:
    st.write("Please upload both an image and an MP3 file.")
