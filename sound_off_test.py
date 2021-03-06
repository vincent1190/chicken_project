from keras.preprocessing.image import img_to_array
from keras.models import load_model
from threading import Thread 
from imutils.video import VideoStream
import time
import pyglet
import numpy as np 
import imutils
import time
import cv2
import os

'''
make sure too add in parse arg functions
'''


class bird_sounds:
    def __init__(self):
        # initilizing the class
        pyglet.options['audio']=('directsound','openal','pulse')
        self.source=pyglet.media.load('chicken_alarm.wav')# will later edit this to include a list of sounds
        self.player=pyglet.media.Player()
        self.player.queue(self.source)

    def check_bird(self):
        if self.sees_bird:
            if self.player.playing:
                pass
            else:
                self.player.play()
                print('playing sound')
        else:
            if self.player.playing:
                self.player.pause()
                print( 'stopping sound')


class chicken_vision:
    def __init__(self):

        # initialize the bird_sound class
        self.bird=bird_sounds()
        self.bird.sees_bird=False

        # initialize the total number of frames that *consecutively* contain
        # a chicken along with threshold required to trigger the alarm
        self.TOTAL_CONSEC = 0
        self.TOTAL_THRESH = 20

        # loading the trained CNN
        print("[INFO] loading model...")
        # self.model=load_model("chicken_not_chicken.model")
        self.model=load_model("D:\Scripts\chicken_project\models\chicken_model.model")

        # initialize the video stream and allow the camera sensor to warm up
        # print("[INFO] starting video stream...")
        # self.path=r"D:\Scripts\chicken_project\chicken_video.mp4"
        # self.vs = VideoStream(src=self.path).start()
        # vs = VideoStream(usePiCamera=True).start()
        time.sleep(2.0)

    def video_loop(self):

        print("[INFO] starting video stream...")

        # video file path
        self.path=r"D:\Scripts\chicken_project\chicken_video.mp4"

        # video stream usage which is faster but need it to be slower for testing
        # self.vs = VideoStream(src=self.path).start()
        # self.vs = VideoStream(src=0).start()
        # loop over the frames from the video stream


        # using this instead of videostream for now to test videos
        self.cap=cv2.VideoCapture(self.path)
        print (self.cap.isOpened())
        while(self.cap.isOpened()):

        # remove comment when not testing and ready to use with webcam
        # while True:

            # grab the frame from the threaded video stream and resize it
            # to have a max width of 400 pixels
            # make sure to remove this after testing is done
            # self.frame=self.vs.read()

            ret,self.frame=self.cap.read()

            self.frame=imutils.resize(self.frame, width=400)


            # prepare the image to be classified by the deep learning network
            self.image=cv2.resize(self.frame,(64,64))

            self.image=self.image.astype("float")/255.0
            self.image=img_to_array(self.image)
            self.image=np.expand_dims(self.image, axis=0)

            # classify the input image and initialize the label
            # and probablility of the prediction
            (self.notChicken,self.chicken)=self.model.predict(self.image)[0]
            self.label="Not_Chicken"
            self.proba=self.notChicken

            # check to see if santa was detected using our CNN
            if self.chicken>self.notChicken:
                # update the label and the prediction probablility
                self.label="Chicken"
                self.proba=self.chicken

                # incremeent the total number of consecutive frames
                # that contain the chicken
                self.TOTAL_CONSEC+=1
                if self.TOTAL_CONSEC>=self.TOTAL_THRESH:
                    self.bird.sees_bird=True
                    self.bird.check_bird()
            # if bird are not in the picture reset TOTAL_CONSEC
            else:
                self.TOTAL_CONSEC=0
                self.bird.sees_bird=False
                self.bird.check_bird()

            # build the label and draw it on the fram
            self.labeL="{}: {:.2f}%".format(self.label,self.proba*100)
            self.frame=cv2.putText(self.frame,self.label,(10,25),
                cv2.FONT_HERSHEY_SIMPLEX,0.7, (0, 255, 0), 2)
            time.sleep(.00001)

            # show the output frame
            cv2.imshow("Frame",self.frame)
            if cv2.waitKey(1) & 0xff==ord('q'):
                break

        # do a bit of cleanup
        print("[INFO] cleaning up...")
        cv2.destroyAllWindows()
        self.vs.stop()

            
                
def main():
    chick=chicken_vision()
    chick.video_loop()




if __name__=="__main__":
    main()





# make a method that will shuffle up the queue a bit




# print(' will now be playing the alarm')
# bird.sees_bird=True
# bird.check_bird()
# time.sleep(2)
# print( bird.player.playing)
# print( 'will now stop the player')
# time.sleep(1)
# bird.sees_bird=False
# bird.check_bird()
# print( bird.player.playing)
# print( 'the ennnnnnnnd.... for now at least')
# print( 'next step is computer vision')