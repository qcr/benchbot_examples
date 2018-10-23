from benchbot import BenchBot
from random import choice
import json
import math
from util import PriorityQueue, memoize

class NavigationProblem:
	def __init__(self, gridmap, position, heading, goal, tolerance=0.3):
		self.gridmap = gridmap
		self.initial_state = self.to_state(position, heading['z'])
		self.goal_state = goal
		self.tolerance = tolerance

	def actions(self, s):
		return ['forward', 'left', 'right']

	def result(self, s, a):
		if a == 'forward':
			x, y = self.gridmap.toMetric(s[0], s[1])
			e_x, e_y = self.gridmap.toGrid(x + 0.5 * math.cos(s[2]), y + 0.5 * math.sin(s[2]))
			return (e_x, e_y, s[2])
		else:
			heading = s[2] + (0.523599 if a == 'left' else -0.523599)
			if heading > math.pi:
				heading = heading - math.pi * 2
			if heading < -math.pi:
				heading = heading + math.pi * 2
			
			return (s[0], s[1], round(heading, 2))

	def is_goal(self, s):
		return self.distance(s) < self.tolerance

	def path_cost(self, c, s1, a, s2):
		return c + max(1, self.gridmap.getFromGrid(s2[0], s2[1]))

	def distance(self, s):
		x, y = self.gridmap.toMetric(s[0], s[1])
		return ((x - self.goal_state[0]) ** 2 + (y - self.goal_state[1]) ** 2) ** 0.5

	@staticmethod
	def to_state(position, heading):
		return tuple(list(gridmap.toGrid(position['x'], position['y'])) +  [round(heading, 2)])

	def __str__(self):
		return str(self.initial_state)

class Node(object):
	def __init__(self, state, parent=None, action=None, path_cost=0):
		self.state = state
		self.parent = parent
		self.action = action
		self.path_cost = path_cost

		self.depth = self.parent.depth + 1 if self.parent else 0

	def expand(self, problem):
		return [self.child_node(problem, action)
                for action in problem.actions(self.state)]

	def child_node(self, problem, action):
		child_state = problem.result(self.state, action)
		return Node(child_state, self, action, problem.path_cost(self.path_cost, self.state, action, child_state))

	def solution(self):
		return [node.action for node in self.path()[1:]]
 
	def path(self):
		node, path_back = self, []
		while node:
			path_back.append(node)
			node = node.parent
		return list(reversed(path_back))

	def __eq__(self, other):
		return isinstance(other, Node) and self.state == other.state

	def __hash__(self):
		return hash(self.state)

def astar(problem, h=None):
	h = memoize(h or problem.h)

	frontier = PriorityQueue(lambda n: h(n) + n.path_cost)
	frontier.append(Node(p.initial_state))
	
	explored = set()

	while frontier:
		node = frontier.pop()
		if p.is_goal(node.state):
			return node
			
		explored.add(node.state)

		frontier.extend(child for child in node.expand(p)
						if child.state not in explored
						and child not in frontier)

	return None

benchbot = BenchBot() # Create a benchbot instance

while True:
	gridmap = benchbot.getGridMap()

	p = NavigationProblem(gridmap, benchbot.get('pose'), benchbot.get('heading'), [2, 4])
	if p.distance(p.initial_state) < 0.3:
		break

	node = astar(p, lambda n: p.distance(n.state))

	if node:
		print node.solution()
		benchbot.send(node.solution().pop(0))

print benchbot.send('complete', {'id': 'find-items-in-kitchen', 'marker': 'april_23', 'items': {'cup': 2, 'duck': 1}})
