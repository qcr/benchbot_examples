import os
from benchbot import BenchBot
from yolo import Detector

detector = Detector()

with BenchBot() as benchbot:
  locations = benchbot.get('locations')
  locations.sort()

  for location in locations:
    benchbot.send('goto', {'location_id': location})
    
    image = benchbot.getImage()
    
    #benchbot.store(location, image)
    detections = detector.detect(image)
    #benchbot.store(location+'-detections', detector.draw(image, detections))

    found = filter(lambda detection: detection[0] == 'bottle', detections)

    if found:
      break

  benchbot.complete('main', {'data': location if found else ''})
  print 'Found at:', location if found else ''
