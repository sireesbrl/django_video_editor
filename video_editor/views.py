from .utils import Editor
from .models import Video
from django.shortcuts import render, redirect
from django.http import HttpResponseBadRequest
import os
from django.conf import settings

def upload(request):
    """Handle video upload, trimming, optional audio addition, and text overlay."""
    if request.method == "POST":
        # Retrieve uploaded files and input details
        video_file = request.FILES.get("video")
        audio_file = request.FILES.get("audio")  # Optional audio upload
        start_time = request.POST.get("start_time")
        end_time = request.POST.get("end_time")
        text_content = request.POST.get("text_content")  # Optional text
        text_position = request.POST.get("text_position")  # Optional text position
        text_color = request.POST.get("text_color")  # Optional text color

        # Validate required fields
        if not video_file:
            return HttpResponseBadRequest("No video file provided.")
        if not start_time or not end_time:
            return HttpResponseBadRequest("Start and end times are required.")

        # Save the uploaded video (and optionally audio) to the database
        video = Video.objects.create(title=video_file.name, original_video=video_file)
        if audio_file:
            video.original_audio = audio_file
            video.save()

        # Initialize the editor
        try:
            editor = Editor(video.original_video.path, audio_path=video.original_audio.path if audio_file else None)

            # Perform trimming
            trimmed_video_url = editor.trim(start=float(start_time), end=float(end_time))

            # Add audio if provided
            if audio_file:
                editor.add_audio()

            # Add text if provided
            if text_content:
                video.text_content = text_content
                video.text_position = text_position
                video.save()
                try:
                    x, y = text_position.split(",")
                    editor.add_text(content=text_content, horizontal=x, vertical=y, color=text_color)
                except Exception as e:
                    editor.add_text(content=text_content, color=text_color)

            # Save the final video
            final_video_url = editor.save()
            video.processed_video = final_video_url
            video.save()

            return render(request, "video_editor/upload.html", {
                "processed_video_url": final_video_url,
                "processed": True,
            })

        except Exception as e:
            return render(request, "video_editor/error.html", {"error_message": str(e)})

    # Render the upload page for GET requests
    return render(request, "video_editor/upload.html")

def undo(request):
    """Handle undo by deleting the processed video."""
    if request.method == "POST":
        # Get the processed video path from the form
        processed_video_url = request.POST.get("processed_video_path")
        if not processed_video_url:
            return HttpResponseBadRequest("No processed video path provided.")

        # Construct the full file path
        processed_video_path = os.path.join(
            settings.MEDIA_ROOT, os.path.relpath(processed_video_url, settings.MEDIA_URL)
        )

        try:
            # Delete the processed video file if it exists
            if os.path.exists(processed_video_path):
                os.remove(processed_video_path)
            else:
                return HttpResponseBadRequest("Processed video file does not exist.")

            # Redirect back to the upload page
            return redirect("upload")

        except Exception as e:
            return render(request, "video_editor/error.html", {"error_message": str(e)})

    return redirect("upload")
