import os
import glob
from main import app, send_data
from flask import Flask, render_template, send_from_directory, request, redirect, url_for, Response, json
from global_def import *
import traceback




def find_maps():
    maps = {}

    #print("type(maps) :", type(maps))
    for fname in glob.glob(mp4_extends):
        if os.path.isfile(fname):
            key = fname
            maps[key] = round(os.path.getsize(fname) / SIZE_MB, 3)
    print("maps :", maps)

    return maps

def get_nest_maps(maps):
    dict_list = []
    for x in maps:
        fl_dic = {}
        try:
            print("x: ", x)
            fl_dic["filename"] = x
            fl_dic["size"] = maps[x]
        except:
            print(traceback.print_exc())
        dict_list.append(fl_dic)
    print("nest_dict :", dict_list)
    return dict_list

@app.route("/")
def index():
    maps = find_maps()
    return render_template("index.html", title=title, files=maps)

@app.route("/upload", methods=['POST', 'GET'])
def upload():
    print("upload")
    if request.method == 'POST':
        for file in request.files.getlist("file"):
            print(file)
            filename = file.filename
            dest = "/".join([FileFolder, filename])
            file.save(dest)

    #return index()
    #maps = find_maps()
    return redirect(url_for('index'))

@app.route('/download/<filename>')
def download(filename):
    fname = filename
    return send_from_directory(FileFolder, fname, as_attachment=True)

@app.route('/play/<filename>')
def play(filename):
    fname = filename
    send_data(play_file=fname)
    return redirect(url_for('index'))


@app.route("/TEST_COLOR/RED", methods=['POST', 'GET'])
def TEST_COLOR_RED():
    return redirect(url_for('index'))

@app.route("/TEST_COLOR/GREEN", methods=['POST', 'GET'])
def TEST_COLOR_GREEN():

    return redirect(url_for('index'))

@app.route("/TEST_COLOR/BLUE", methods=['POST', 'GET'])
def TEST_COLOR_BLUE():

    return redirect(url_for('index'))

@app.route("/TEST_COLOR/WHITE", methods=['POST', 'GET'])
def TEST_COLOR_WHITE():

    return redirect(url_for('index'))

def gen(video):
    """视频流生成函数"""
    while True:
        frame = video.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    """视频流路由(route).放到 img 标签的 src 属性."""
    #return Response(gen(Video_C("./logos.mp4")),
    #                mimetype='multipart/x-mixed-replace; boundary=frame')
    return

@app.route('/get_filelist', methods=['POST', 'GET'])
def get_filelist():
    files_maps = find_maps()
    nest_files_maps = get_nest_maps(files_maps)

    response = app.response_class(
        response=json.dumps(nest_files_maps),
        status=200,
        mimetype='application/json'
    )
    return response

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.
def route_test():
    print("route test!")
