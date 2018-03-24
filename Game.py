import pygame,sys,os,math
from pygame.locals import *
from pygame.time import *

screenSizeX = 640
screenSizeY = 480

pygame.init()
mainClock = Clock()
pygame.display.set_caption('Prezes Jumper')
window = pygame.display.set_mode((screenSizeX,screenSizeY))
background = pygame.image.load('background.jpg')
background = pygame.transform.scale(background,(screenSizeX,screenSizeY))
screen = pygame.display.get_surface()
screen.blit(background,(0,0))
pygame.display.flip()
MySprite = pygame.image.load("avatar.bmp")
pygame.display.set_icon(MySprite)
MySprite = pygame.transform.scale(MySprite,(128,128))
myFont = pygame.font.SysFont('monospace', 26)


def input(events):
	for event in events:
		if event.type == QUIT:
			sys.exit(0)
		elif event.type == KEYDOWN:
			if event.key == 27:
				sys.exit(0)
		else:
			print(event)


ground = pygame.image.load('ziemia_t.png')
psox = 0

class IsMoving():
	Left = False
	Right = False
	Up = False
	Down = False
			

class Logic(pygame.sprite.Sprite):
	step = 8
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = ground
		self.rect = self.image.get_rect()
		self.mask = pygame.mask.from_surface(self.image)
		self.x = screenSizeX-150
		self.y = screenSizeY-160
		
	def Move(self,surface):
		#self.x -= Logic.step
		surface.blit(self.image,(self.x,self.y))
	
class Res():
		Result = 0
		Jumpressed = False

Result = Res()
		
Iter = 0

class Player(pygame.sprite.Sprite):
	step = 8
	jump = 45
	startposy = screenSizeY-228
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = MySprite
		self.rect = self.image.get_rect()
		self.mask = pygame.mask.from_surface(self.image)
		self.x = 100
		self.y = Player.startposy
	
	def update(self,surface):
		surface.blit(self.image,(self.x,self.y))
		
	
	def GetKey(self,temp_event):
		for event in temp_event:
			if event.type == KEYDOWN:
				if event.key == ord('w'):
					IsMoving.Up = True
					Iter = 0
					Res.Jumpressed = True
				if event.key == ord('a'):
					IsMoving.Left = True
				if event.key == ord('s'):
					IsMoving.Down = True
				if event.key == ord('d'):
					IsMoving.Right = True
			if event.type == KEYUP:
				#if event.key == ord('w'):
				#	IsMoving.Up = False
				if event.key == ord('a'):
					IsMoving.Left = False
				if event.key == ord('s'):
					IsMoving.Down = False
				if event.key == ord('d'):
					IsMoving.Right = False
		
	def Movement(self):
		if IsMoving.Up == True:
			self.y -= Player.jump
			if Player.jump<0 and Player.jump>-2:
				Player.jump+=abs(Player.jump)/3
			Player.jump -=math.sqrt(abs(Player.jump))
			if self.y>Player.startposy:
				Result.Result += 1
				IsMoving.Up=False
				Res.Jumpressed = False
				self.y=Player.startposy
				Player.jump = 45
		if IsMoving.Left == True and self.x>0:
			self.x -= Player.step
		if IsMoving.Right == True and self.x<screenSizeX-128:
			self.x += Player.step





Character = Player()
Obstacle = Logic()

Highscore = 0

while True:
	screen.blit(background,(0,0))
	
	new_event = pygame.event.get()
	input(new_event)
	
	Character.GetKey(new_event)
	Character.Movement()
	Character.update(screen)
	
	if Res.Jumpressed == False:
		Iter += 1
		if Iter > 30:
			Highscore = max(Result.Result,Highscore)
			Result.Result = 0
			Iter = 0
	
	Chart = myFont.render('Bhops: ' + str(Result.Result),1,(0,0,0))
	screen.blit(Chart,(430,15))
	Chart2 = myFont.render('Best: ' + str(Highscore),1,(0,0,0))
	screen.blit(Chart2,(430,48))
	
	#Obstacle.Move(screen)
	
	#if pygame.sprite.collide_mask(Character,Obstacle):
	#	print('xDDD')
	
	pygame.display.flip()
	mainClock.tick(60)