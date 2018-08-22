from benchbot import BenchBot
from random import choice
import json

benchbot = BenchBot() # Create a benchbot instance

routes = benchbot.get() # Get a list of available routes
commands = benchbot.get('command') # Get a list of possible actions for the command route
print 'Available:', commands

while not benchbot.isDone():
    response = benchbot.send('command', {'action': choice(commands)})

    if (response['result'] == 0):
        print 'Command issued successfully'
    else:
        print response['error']

print 'Goal reached!'