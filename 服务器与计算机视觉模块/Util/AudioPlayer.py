#encoding=utf-8
from playsound import playsound
from subprocess import call
#import os
#MODEL_DIR = os.path.realpath(__file__).rsplit('\\', 3)[0] + '\\'


def play_audio(audio_name):
    try:
        # global MODEL_DIR
        # if MODEL_DIR is None:
        #     MODEL_DIR = os.path.realpath(__file__)
        #     MODEL_DIR = MODEL_DIR.rsplit('\\', 3)[0] + '\\'
        # windows
        playsound(audio_name)
        #Linux
        # call('mpg321 ' + audio_name, shell=True)
    except KeyboardInterrupt as e:
        print(e)
    finally:
        pass



if __name__ == '__main__':
    play_audio('Audios\\no_face_detected.mp3')
