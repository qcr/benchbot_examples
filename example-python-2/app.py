import os
from benchbot import BenchBot

with BenchBot() as benchbot:
  image = benchbot.getImage()
  benchbot.store('image', image)
  benchbot.send('complete', {'id': 'goal_1a'})

  print 'Finished'
