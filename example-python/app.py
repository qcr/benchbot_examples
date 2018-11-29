import os
from benchbot import BenchBot
from yolo import Detector

path = os.path.dirname(os.path.abspath(__file__))

benchbot = BenchBot()
detector = Detector(path + '/yolo')

solution = {}

while True:
    location = benchbot.get('location')    
    image = benchbot.getImage()

    detections = detector.detect(image)

    solution[location['location_id']] = [item[0] for item in detections]
    
    result = benchbot.send('next')
    
    if result['result'] != 0:
        break

print benchbot.send('complete', {
  'id': 'main', 
  'data': solution
})
print 'Solution:', solution
