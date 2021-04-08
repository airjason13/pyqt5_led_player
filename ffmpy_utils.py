import ffmpy
import cv2

def get_video_duration(video_path):
    print(video_path)
    video = cv2.VideoCapture(video_path)

    #duration = video.get(cv2.CAP_PROP_POS_MSEC)
    frame_count = video.get(cv2.CAP_PROP_FRAME_COUNT)
    fps = video.get(cv2.CAP_PROP_FPS)
    duration_ms = frame_count/fps
    #print(duration_ms)
    #print(frame_count)
    return duration_ms


def get_thumbnail_from_video(video_path):
    thumbnail_path = video_path.replace(".mp4", ".jpg")
    duration_ms = get_video_duration(video_path)
    ff = ffmpy.FFmpeg(
        inputs={video_path: None},
        outputs={thumbnail_path: ['-ss', '00:00:10.000', '-vframes', '1']}
    )
    """ff = ffmpy.FFmpeg(
        inputs={video_path: None},
        outputs={thumbnail_path: ['-ss', duration_ms, '-vframes', '1']}
    )"""
    ff.run()
    return thumbnail_path