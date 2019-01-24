import os
from benchbot import BenchBot
from yolo import Detector

#path = os.path.dirname(os.path.abspath(__file__))
detector = Detector()

with Benchbot() as benchbot:

	locations = benchbot.get('locations')

	for location in locations:
		benchbot.send('goto', {'id': location})
		image = benchbot.getImage()
	
		benchbot.store(location + '-image', image)

		detections = detector.detect(image)

    if 'bottle' in [item[0] for item in detections]:
      benchbot.send('complete', {'id': 'item_at', 'location': location})
      break
