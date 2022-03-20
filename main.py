import random
import requests # to get image from the web
import shutil
from images_db_new import urls
from PIL import Image
import os, sys
from datetime import datetime
from PIL import Image
import string
from moviepy.editor import *
import time
import os 
import subprocess
from os.path import exists
import schedule
from time import sleep
from flask import Flask
import shutil
from threading import Thread
from flask import send_file, send_from_directory, safe_join, abort

app = Flask(__name__)
# ========================= ONLY FOR META3 (INSPIRA) =====================

dir_path = os.path.dirname(os.path.realpath(__file__))
fps = 24


def id_generator(size=20, chars=string.ascii_uppercase + string.digits):
  return ''.join(random.choice(chars) for _ in range(size))

def deleteDownloads():
    dir = os.path.join(dir_path, "downloaded")
    for files in os.listdir(dir):
        path = os.path.join(dir, files)
        try:
            shutil.rmtree(path)
        except OSError:
            os.remove(path)

def deletegen():
    dir = os.path.join(dir_path, "gen")
    for files in os.listdir(dir):
        path = os.path.join(dir, files)
        try:
            shutil.rmtree(path)
        except OSError:
            os.remove(path)

def deleteResized():
    dir = os.path.join(dir_path, "resized")
    for files in os.listdir(dir):
        path = os.path.join(dir, files)
        try:
            shutil.rmtree(path)
        except OSError:
            os.remove(path)

def deleteVid():
    dir = os.path.join(dir_path, "outputs")
    for files in os.listdir(dir):
        path = os.path.join(dir, files)
        try:
            shutil.rmtree(path)
        except OSError:
            os.remove(path)

def getImage():
	pics = []
	for _ in range(3):
		x = random.choice(urls)
		pics.append(x)
	return pics

def resizer(f):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    fz = os.path.join(dir_path, "resized")
    now = datetime.now().strftime('%Y%m%d-%H%M%S-%f')
    im = Image.open(f)
    new_img = im.resize((720,im.height))
    x, y = im.size
    # size = max(720, x, y)
    fill_color=(0, 0, 0, 0)
    new_im = Image.new('RGBA', (720, 1280), fill_color)
    # new_im.paste(im, (int((size - x) / 2), int((size - y) / 2)))
    size_h = int((1280 - y)/2)
    size_w = int(0)
    new_im.paste(new_img, (size_w, size_h))
    new_im.convert('RGB').save(os.path.join(fz ,'111111' + now + '.jpg'), 'JPEG')

def downloadImg():
    imgs = getImage()
    heads = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
    # imgs = ["89994Xinspirational-quote-life-unknown-author-pretty-monarch-butterfly-perched-flower-43678437.jpg", "D3IK1Linspirational-quote-happiness-c-e-jerningham-two-adorable-poodles-enjoying-life-to-fullest-43678289.jpg","SE8AJ8inspirational-phrases-be-positive-believe-yourself-enjoy-life-motivational-notes-papers-48980497.jpg" ]
    for i in imgs:
        dir_path = os.path.dirname(os.path.realpath(__file__))
        image_url = i
        filename = id_generator() + ".jpg"
        fz = os.path.join(dir_path, "downloaded")
        r = requests.get(image_url,headers=heads, stream = True)
        if r.status_code == 200:
            r.raw.decode_content = True
            with open(filename,'wb') as f:
                shutil.copyfileobj(r.raw, f)

            shutil.move(str(filename), fz)
            print('Image sucessfully Downloaded: ', id_generator() + filename)

            tp = os.path.join(fz, filename)
            resizer(tp)
        else:
            print('Image Couldn\'t be retreived')
    deleteDownloads()

def getRandomItems(list, n):
    import random
    import math
    random_items = []
    for i in range(n):
        random_items.append(list[int(math.floor(random.random() * len(list)))])
    return random_items

def getRandomImg():
    import os 
    dir_path = os.path.dirname(os.path.realpath(__file__))
    files = []
    fz = os.path.join(dir_path, "resized")
    for file in os.listdir(os.path.join(dir_path, "resized")):
        if file.endswith(".png") or file.endswith(".jpg"):
            files.append(os.path.join(fz, file))
            # print(os.path.join(file))
    return files

def generateVedio():
    #deleteVid()
    dest = os.path.join(dir_path, "outputs")
    images_list = getRandomImg()

    clips = [ImageClip(m).set_duration(5)
            for m in images_list]

    file_name = id_generator()

    ms = ['music1.mp3', 'music2.mp3', 'music3.mp3', 'music4.mp3', 'music5.mp3', 'music6.mp3']
    music = os.path.join(dir_path, random.choice(ms))
    audioclip = AudioFileClip(music).set_duration(15)
    target = os.path.join(dest, f"{file_name}.mp4")
    concat_clip = concatenate_videoclips(clips, method="compose").set_audio(audioclip)
    # concat_clip.write_videofile(target, fps=fps, codec="mpeg4")
    concat_clip.write_videofile(target, fps=fps)
    deleteResized()

def bulkGenerate():
    for i in range(4):
        downloadImg()
        generateVedio()
    print("Short generted!")
    dir_path = os.path.dirname(os.path.realpath(__file__))
    out_ = os.path.join(dir_path, "gen/short")
    dir_ = os.path.join(dir_path, "outputs")
    deletegen()
    shutil.make_archive(out_ , 'zip', dir_)
    print(os.path.isfile(os.path.join("out_", ".zip")))
    print("files compressed")
    
    
@app.route('/')
def hello_world():
  def fsz():
  	bulkGenerate()
  thread = Thread(target=fsz)
  thread.start()
  return "File getting generated!"
  

  
@app.route('/v')
def home():
  #def fsz():
  #	bulkGenerate()
  #thread = Thread(target=fsz)
  #thread.start()
  #print("thread started")
  
  dir_path = os.path.dirname(os.path.realpath(__file__))
  file_ = os.path.join(dir_path, "gen/short.zip")
  files_dir = os.path.join(dir_path, "gen")
  
  try:
    return send_file(file_,  attachment_filename="short.zip")
  except Exception as e:
    return str(e)
  

if __name__ == "__main__":
    app.run(debug=True)
