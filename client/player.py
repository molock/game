import os
import pygame
import view
import math
import pymunk
from pymunk import Vec2d


#from vector import Vector
#from projectile import *
#from force import *
#import copy
#import math
#PI = 3.141592653589793238462643383

class Player(pygame.sprite.Sprite):
	
	speed = 50

	def __init__(self, position, seconds):
		pygame.sprite.Sprite.__init__(self)
		imgPath = os.path.dirname(os.path.dirname( os.path.realpath( __file__ ) ) ) + "/images/ship.gif"
		self.image = pygame.image.load(imgPath)
		self.rect = self.image.get_rect()
		self.rect.center = self.worldPos = position
		self.lastDirectionChange = seconds()
		self.direction = [0,-1]
		self.seconds = seconds
		self.observers = []

		self.mass = 500
		self.width = self.height = 30
		self.inertia = pymunk.moment_for_box(500, self.width, self.height) #mass, width, height
		self.elasticity = 1.0
		self.body = pymunk.Body(self.mass,  self.inertia) #Mass, Moment of inertia
		self.shape = pymunk.Poly.create_box(self.body, (self.width, self.height))
		self.body.position = pymunk.Vec2d(position[0], position[1])

	#center the player when resolution is set/changed
	def center(self, resolution):
		self.rect.center = (resolution[0]/2, resolution[1]/2)

	def getPosition(self):
		return list(self.worldPos)

	def addObserver(self, observer):
		#Add the given object to the list of those notified about state changes in this player.
		self.observers.append(observer)

	def setDirection(self, dir):
		self.direction = dir
		for observer in self.observers:
			observer.directionChanged(self)

	def update(self):
		self.updatePos()

	def updatePos(self):
		#self.worldPos[0] += self.direction[0] * self.speed
		#self.worldPos[1] += self.direction[1] * self.speed
		
		self.body.velocity = (self.direction[0] * self.speed, self.direction[1] * self.speed)
		
		#Below lines are temporary to show movement until environment is added
		pos = self.body.position
		#print self.direction, pos
		pos = Vec2d(pos.x, pos.y)
		angle = math.degrees(self.body.angle)
		print angle
		self.image = pygame.transform.rotate(self.image, angle)
		self.rect.center = (pos.x, pos.y)
		
		for observer in self.observers:
			observer.posChanged(self)

			
	def fireProj(self, pos):
		proj = Projectile(self.rect.center, self.worldPos, pos, 0, self.seconds)
		self.manager.addProjectile(proj)
		#for observer in self.observers:
			#observer.createProjectile(proj)