import ffmpy
import cv2
import os
import glob
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

def find_maps():
    maps = {}
    for fname in glob.glob(mp4_extends):
        if os.path.isfile(fname):
            key = fname  # .decode()
            maps[key] = round(os.path.getsize(fname) / SIZE_MB, 3)

    return maps

def sync_gif_with_mp4(mp4_folder, gif_folder ):
    os.chdir(mp4_folder)
    mp4_file_list = []
    for fname in sorted(glob.glob(mp4_extends)):
        if os.path.isfile(fname):
            mp4_file_list.append(fname)

    os.chdir(gif_folder)
    gif_file_list = []
    for fname in sorted(glob.glob(gif_extends)):
        tmp_mp4_name = fname.replace(".gif", ".mp4")
        found_mp4 = False
        for mp4_name in mp4_file_list:
            if mp4_name == tmp_mp4_name:
                found_mp4 = True
                print(tmp_mp4_name + " gif exists!")

        if found_mp4 is False:
            os.remove(fname)

    os.chdir(mp4_folder)
    print("mp4_file_list :", mp4_file_list)
    # Gen thumbnail at initial
    for i in range(len(mp4_file_list)):
        #gen thumbnail jpg
        #gen_thumbnail_from_video(FileFolder, mp4_file_list[i])
        #gen gif
        gen_gif_from_video(FileFolder, mp4_file_list[i])
    #print("gif_file_list :", gif_file_list)
