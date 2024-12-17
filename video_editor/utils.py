from moviepy import VideoFileClip

def trim_video(video_path, start_time, end_time):
    clip = (VideoFileClip(video_path)
            .subclipped(start_time, end_time)
    )

    clip.write_videofile(f"trimmed_video.mp4")

    return True