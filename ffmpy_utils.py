import ffmpy
import cv2
import os
from global_def import *

def get_video_duration(video_path):
    print(video_path)
    video = cv2.VideoCapture(video_path)

    #duration = video.get(cv2.CAP_PROP_POS_MSEC)
    frame_count = video.get(cv2.CAP_PROP_FRAME_COUNT)
    fps = video.get(cv2.CAP_PROP_FPS)
    duration_ms = frame_count/fps
    print(duration_ms)
    #print(frame_count)
    return duration_ms


def gen_thumbnail_from_video(file_folder, video_path):
    thumbnail_path = file_folder + ThumbnailFileFolder + video_path.replace(".mp4", ".jpg")
    if os.path.isfile(thumbnail_path) is False:
        duration_ms = get_video_duration(video_path)
        print(type(duration_ms))
        duration_ms -= 1
        str_ms = str(duration_ms)
        print("str_ms :", str_ms)
        ff = ffmpy.FFmpeg(
            inputs={video_path: None},
            outputs={thumbnail_path: ['-ss', str_ms, '-vframes', '1']}
        )
        """ff = ffmpy.FFmpeg(
            inputs={video_path: None},
            outputs={thumbnail_path: ['-ss', '00:00:10.000', '-vframes', '1']}
        )"""

        ff.run()
    return thumbnail_path

def gen_gif_from_video(file_folder, video_path):
    thumbnail_path = file_folder + ThumbnailFileFolder + video_path.replace(".mp4", ".gif")
    if os.path.isfile(thumbnail_path) is False:
        duration_ms = get_video_duration(video_path)
        print(type(duration_ms))
        #duration_ms -= 1
        str_ms = str(duration_ms)
        print("str_ms :", str_ms)
        ff = ffmpy.FFmpeg(
            inputs={video_path: None},
            outputs={thumbnail_path: None}
        )

        ff.run()
    return thumbnail_path