from playsound import playsound
import time
import pyglet

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
                print'playing sound'
        else:
            if self.player.playing:
                self.player.pause()
                print 'stopping sound'

# make a method that will shuffle up the queue a bit



bird=bird_sounds()
print' will now be playing the alarm'
bird.sees_bird=True
bird.check_bird()
time.sleep(2)
print bird.player.playing
print 'will now stop the player'
time.sleep(1)
bird.sees_bird=False
bird.check_bird()
print bird.player.playing
print 'the ennnnnnnnd.... for now at least'
print 'next step is computer vision'