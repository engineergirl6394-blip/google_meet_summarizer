from moviepy import VideoFileClip
import whisper
import os
import torch


# For pdf
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4

print("Current Directory:", os.getcwd())

# Step 1: Load video
video_file = "meeting.mp4"   # Change if your file name is different
print(f"Checking for video file: {video_file}")

if not os.path.exists(video_file):
    print("ERROR: Video file not found!")
    exit()

print("Video found. Loading...")
video = VideoFileClip(video_file)

# Step 2: Extract audio
print("Extracting audio...")
audio_path = "audio.wav"
video.audio.write_audiofile(audio_path)
print(f"Audio extracted to: {audio_path}")

# Step 3: Transcribe with Whisper
print("Loading Whisper model...")
model = whisper.load_model("tiny")
print("Whisper model loaded.")

print("Transcribing audio...")
result = model.transcribe(audio_path)
print("Transcription complete.")
speaker_text = result["text"]
# Step 4: Output transcription
output_file = "transcription.txt"
with open(output_file, "w", encoding="utf-8") as f:
    f.write(speaker_text)

print(f"Transcription saved to: {output_file}")

#Step 5 : Pdf generator
pdf_file = "transcription.pdf"


# Create PDF
styles = getSampleStyleSheet()
style = styles['Normal']
style.fontName = "Times-Roman"
style.fontSize = 12
style.leading = 15   # Line spacing

doc = SimpleDocTemplate(pdf_file, pagesize=A4)

# Convert full text into a paragraph (auto wrap)
story = []
story.append(Paragraph(speaker_text.replace("\n","<br/>"), style))

# Build PDF
doc.build(story)

print("PDF saved as:",pdf_file)