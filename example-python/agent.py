from benchbot import BenchBot
from random import choice
import cv2
import json

class Agent(BenchBot):
    def __init__(self):
        BenchBot.__init__(self)
        self.actions = self.get('command')

    def chooseAction(self, image):
        return choice(self.actions)

    def doAction(self, action):
        return self.send('command', {'action': action})
        
    def run(self):
        while not self.isDone():
            img = self.getImage()
            
            cv2.imshow('Image', img)
            cv2.waitKey(30)
        
            action = self.chooseAction(img)
            result = self.doAction(action)

            if (result['result'] == 0):
                print 'Command issued successfully'
            else:
                print result['error']

agent = Agent() 
agent.run()
