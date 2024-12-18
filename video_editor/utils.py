from moviepy import VideoFileClip

def trim_video(video_path, output_path, start_time, end_time):
    clip = (VideoFileClip(video_path)
            .subclipped(start_time, end_time)
    )

    trimmed_video = clip.write_videofile(output_path)

    return "success"