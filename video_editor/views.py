from django.shortcuts import render, redirect
from .utils import trim_video
from .models import Video
import os
from django.conf import settings
from moviepy import VideoFileClip
from .utils import trim_video

def upload(request):
    if request.method == "POST":
        video_file = request.FILES.get("video")
        start_time = request.POST.get("start_time")
        end_time = request.POST.get("end_time")

        video = Video.objects.create(title=video_file.name, original_video=video_file)
        input_path = video.original_video.path
        processed_videos_path = os.path.join(settings.MEDIA_ROOT, "processed_videos")
        if not os.path.exists(processed_videos_path):
            os.makedirs(processed_videos_path)

        output_path = os.path.join(processed_videos_path,f"trimmed_{video_file.name}")

        try:
            trimmed_video = trim_video(input_path, output_path, start_time, end_time)
            if trimmed_video == "success":
                trimmed_video_url = f"{settings.MEDIA_URL}/processed_videos/trimmed_{video_file.name}"
                video.processed_video = output_path
                video.save()
                return render(request, "video_editor/success.html", {"trimmed_video_url": trimmed_video_url})



            # video_path = input_path
            # clip = (VideoFileClip(video_path).subclipped(start_time, end_time))
            # clip.write_videofile(output_path)
            # trimmed_video_url = f"{settings.MEDIA_URL}/processed_videos/trimmed_{video_file.name}"
            # return render(request, "video_editor/success.html", {"trimmed_video_url": trimmed_video_url})
        except Exception as e:
            return render(request, "video_editor/success.html", {"error": str(e)})

    return render(request, "video_editor/upload.html")

import os
from django.shortcuts import redirect
from django.conf import settings

def undo(request):
    if request.method == "POST":
        # Get the path of the processed video from the form
        processed_video_url = request.POST.get("processed_video_path")
        
        # Convert URL to file path
        processed_video_path = os.path.join(settings.MEDIA_ROOT, os.path.relpath(processed_video_url, settings.MEDIA_URL))
        
        # Delete the processed video file if it exists
        if os.path.exists(processed_video_path):
            os.remove(processed_video_path)
        
        # Redirect to the upload page
        return redirect("upload")
    
    # If not a POST request, redirect to the upload page
    return redirect("upload")
