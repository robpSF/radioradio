import streamlit as st
from moviepy.editor import ImageClip, AudioFileClip, CompositeVideoClip
from pydub import AudioSegment
import numpy as np
import matplotlib.pyplot as plt
import tempfile
import os
from PIL import Image

# Function to create waveform image
def create_waveform(audio_path, output_path):
    audio = AudioSegment.from_file(audio_path)
    data = np.array(audio.get_array_of_samples())

    fig, ax = plt.subplots()
    ax.plot(data, linewidth=0.5)
    ax.set_xlim(0, len(data))
    ax.set_ylim(-2**15, 2**15)
    ax.axis('off')
    
    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
    fig.savefig(output_path, bbox_inches='tight', pad_inches=0)
    plt.close(fig)

# Streamlit application
st.title('Image and Audio to Video with Waveform')

image_file = st.file_uploader("Upload an Image", type=["png", "jpg", "jpeg"])
audio_file = st.file_uploader("Upload an MP3 Audio File", type=["mp3"])

if image_file and audio_file:
    # Save the uploaded files
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as img_tmp_file:
        img_tmp_file.write(image_file.getvalue())
        image_path = img_tmp_file.name

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as audio_tmp_file:
        audio_tmp_file.write(audio_file.getvalue())
        audio_path = audio_tmp_file.name
    
    waveform_image_path = tempfile.mktemp(suffix=".png")
    create_waveform(audio_path, waveform_image_path)
    
    # Resize waveform image using Pillow
    waveform_image = Image.open(waveform_image_path)
    waveform_image = waveform_image.resize((waveform_image.width, 100), Image.LANCZOS)
    waveform_resized_path = tempfile.mktemp(suffix=".png")
    waveform_image.save(waveform_resized_path)
    
    # Load image and audio
    image_clip = ImageClip(image_path)
    audio_clip = AudioFileClip(audio_path)
    
    # Set the duration of the image clip to match the audio
    image_clip = image_clip.set_duration(audio_clip.duration)
    
    # Create waveform clip
    waveform_clip = ImageClip(waveform_resized_path).set_duration(audio_clip.duration)
    waveform_clip = waveform_clip.set_position(("center", "bottom"))
    
    # Composite video with image and waveform
    video = CompositeVideoClip([image_clip, waveform_clip.set_start(0)])
    video = video.set_audio(audio_clip)
    
    # Save the final video
    output_path = tempfile.mktemp(suffix=".mp4")
    video.write_videofile(output_path, codec="libx264", fps=24, logger=None, verbose=False)
    
    # Provide video file for download
    with open(output_path, "rb") as video_file:
        st.video(video_file.read())
        st.download_button(label="Download Video", data=video_file, file_name="output_video.mp4", mime="video/mp4")

    # Cleanup
    os.remove(image_path)
    os.remove(audio_path)
    os.remove(waveform_image_path)
    os.remove(waveform_resized_path)
    os.remove(output_path)
