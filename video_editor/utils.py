from moviepy import VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip
from django.conf import settings
import os

class Editor:
    def __init__(self, video_path, audio_path=None):
        self.original_video = video_path
        self.original_audio = audio_path
        self.temp_clip = None

        # Define temp and output paths
        self.temp_path = os.path.join(settings.MEDIA_ROOT, "temp_videos")
        self.output_path = os.path.join(settings.MEDIA_ROOT, "processed_videos")

        # Ensure the directories exist
        os.makedirs(self.temp_path, exist_ok=True)
        os.makedirs(self.output_path, exist_ok=True)

        # Use base name of the video file for temporary files
        self.alt_name = os.path.basename(self.original_video)

    def trim(self, start=0, end=None):
        """Trim the video from start to end."""
        self.starting_pos = start
        self.ending_pos = end

        # Load and trim the video
        self.temp_clip = VideoFileClip(self.original_video).subclipped(
            self.starting_pos, self.ending_pos
        )

        # Save the trimmed video temporarily
        temp_video_path = os.path.join(self.temp_path, f"temp_{self.alt_name}")
        self.temp_clip.write_videofile(temp_video_path, codec="libx264")

        return True

    def add_audio(self):
        """Add an audio track to the trimmed video."""
        if not self.temp_clip:
            raise ValueError("Trim the video first before adding audio.")
        if not self.original_audio:
            raise ValueError("No audio file provided.")

        # Load audio and attach it to the video
        audio_clip = AudioFileClip(self.original_audio)
        self.temp_clip = self.temp_clip.with_audio(audio_clip)

        # Save the updated video
        final_video_path = os.path.join(self.temp_path, f"temp_{self.alt_name}")
        if os.path.exists(final_video_path):
            os.remove(final_video_path)

        self.temp_clip.write_videofile(
            final_video_path, codec="libx264", audio_codec="aac"
        )

        return True

    def add_text(self, content, horizontal="center", vertical="center", font_size=50, color="white", duration=None):
        """Add text to the trimmed video."""
        if not self.temp_clip:
            raise ValueError("Trim the video first before adding text.")

        font_path = os.path.join(settings.BASE_DIR, "fonts", "LemonJelly.ttf")
        # Create a text clip
        text_clip = TextClip(
            font=font_path,
            text=content,
            font_size=font_size,
            color=color,
        ).with_position(horizontal, vertical).with_duration(duration or self.temp_clip.duration)

        # Combine the text clip with the video
        self.temp_clip = CompositeVideoClip([self.temp_clip, text_clip])

        # Save the updated video
        final_video_path = os.path.join(self.temp_path, f"temp_{self.alt_name}")
        if os.path.exists(final_video_path):
            os.remove(final_video_path)

        self.temp_clip.write_videofile(
            final_video_path, codec="libx264", audio_codec="aac"
        )

        return True

    def save(self, filename=None):
        """Save the final video."""
        if not self.temp_clip:
            raise ValueError("No video to save. Ensure you've trimmed the video.")

        # Define the output filename
        output_filename = filename or f"edited_{self.alt_name}"
        final_output_path = os.path.join(self.output_path, output_filename)

        # Save the video file
        self.temp_clip.write_videofile(
            final_output_path, codec="libx264", audio_codec="aac"
        )

        # Clean up temporary files
        temp_file_path = os.path.join(self.temp_path, f"temp_{self.alt_name}")
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

        # Return the media URL for the saved video
        return f"{settings.MEDIA_URL}processed_videos/{output_filename}"
