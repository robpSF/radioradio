import streamlit as st
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips
import tempfile
import os

# Streamlit application
st.title('Multiple Images and Audio to Video')

image_files = st.file_uploader("Upload Images", type=["png", "jpg", "jpeg"], accept_multiple_files=True)
audio_file = st.file_uploader("Upload an MP3 Audio File", type=["mp3"])

if image_files and audio_file:
    st.write("Files uploaded successfully!")

    # Save the uploaded audio file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as audio_tmp_file:
        audio_tmp_file.write(audio_file.getvalue())
        audio_path = audio_tmp_file.name
        st.write(f"Audio saved to {audio_path}")
    
    # Load audio
    audio_clip = AudioFileClip(audio_path)
    audio_duration = audio_clip.duration
    
    # Calculate duration per image
    image_duration = audio_duration / len(image_files)
    st.write(f"Each image will be displayed for {image_duration:.2f} seconds.")

    # Save the uploaded images and create image clips
    image_clips = []
    image_paths = []
    for image_file in image_files:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as img_tmp_file:
            img_tmp_file.write(image_file.getvalue())
            image_path = img_tmp_file.name
            st.write(f"Image saved to {image_path}")
            image_paths.append(image_path)

        image_clip = ImageClip(image_path).set_duration(image_duration)
        image_clips.append(image_clip)
    
    # Concatenate image clips
    video = concatenate_videoclips(image_clips)
    video = video.set_audio(audio_clip)
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
    os.remove(audio_path)
    for image_path in image_paths:
        os.remove(image_path)
    os.remove(output_path)
else:
    st.write("Please upload images and an MP3 file.")
