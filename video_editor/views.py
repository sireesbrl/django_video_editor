from django.shortcuts import render
from .utils import trim_video
from .models import Video
import os
from django.conf import settings
from moviepy import VideoFileClip

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
            video_path = input_path
            clip = (VideoFileClip(video_path).subclipped(start_time, end_time))
            clip.write_videofile(output_path)
            video.processed_video = output_path
            video.save()

            trimmed_video_url = f"{settings.MEDIA_URL}/processed_videos/trimmed_{video_file.name}"
            return render(request, "video_editor/success.html", {"trimmed_video_url": trimmed_video_url})
        except Exception as e:
            return render(request, "video_editor/success.html", {"error": str(e)})

    return render(request, "video_editor/upload.html")
