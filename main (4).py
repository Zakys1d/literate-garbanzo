import pygame #підключення бібліотеки pygame
pygame.init()


back = (50, 45, 50) #створення кольору для головного вікна
mw = pygame.display.set_mode((500, 500)) #створення головного вікна
mw.fill(back) #заповнення головного вікна
clock = pygame.time.Clock() #створення таймера
bd_image = pygame.image.load('wall.png')


class Area(): #клас для створення меж об'єкту
    def __init__(self, x=0, y=0, width=10, height=10, color=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.fill_color = back
        if color:
            self.fill_color = color
    def color(self, new_color):
        self.fill_color = new_color
    def fill(self):
        pygame.draw.rect(mw, self.fill_color, self.rect)
    def collidepoint(self, x, y):
        return self.rect.collidepoint(x, y)      
    def colliderect(self, rect):
        return self.rect.colliderect(rect)
class Label(Area): #клас для створення надписів
    def set_text(self, text, fsize=12, text_color=(0, 0, 0)):
        self.image = pygame.font.SysFont('verdana', fsize).render(text, True, text_color)
    def draw(self, shift_x=0, shift_y=0):
        self.fill()
        mw.blit(self.image, (self.rect.x + shift_x, self.rect.y + shift_y))


class Picture(Area): #клас для прикріплення зображень
    def __init__(self, filename, x=0, y=0, width=10, height=10):
        Area.__init__(self, x=x, y=y, width=width, height=height, color=None)
        self.image = pygame.image.load(filename)

    def draw(self):
        mw.blit(self.image, (self.rect.x, self.rect.y))


class Wall(Area):
    def __init__(self,x=0,y=0,width=0,height=0,color=(22,26,31)):
        super().__init__(x,y,width,height,color)

walls = [Wall(350,250,200,400),
        Wall(275,300,150,400),
        Wall(250,275,50,400),
        Wall(125,250,50,600),
        Wall(0,200,50,450),
        Wall(100,120,75,20),
        Wall(250,0,50,150),
        Wall(375,0,25,250)]


class Label(Area): #клас для створення надписів
    def set_text(self, text, fsize=12, text_color=(0, 0, 0)):
        self.image = pygame.font.SysFont('verdana', fsize).render(text, True, text_color)
    def draw(self, shift_x=0, shift_y=0):
        self.fill()
        mw.blit(self.image, (self.rect.x + shift_x, self.rect.y + shift_y))


class Player(Picture):
    def __init__(self, filename, x=0, y=0, width=10, height=10):
        super().__init__(filename,x,y,width,height)
        self.gravity = 0.5 #гравітація (швидкість падіння вниз)
        self.jump_power = -10 #величина стрибка
        self.vel_y = 0 #швидкість руху в стрибку
    
    def move(self):
        self.vel_y += self.gravity
        self.rect.y += self.vel_y

        for w in walls:
            if self.rect.colliderect(w.rect):
                if self.vel_y > 0:
                    self.rect.bottom = w.rect.top
                    self.vel_y = 0
                    self.can_jump = True
                elif self.vel_y < 0:
                    self.rect.top = w.rect.bottom
                    self.vel_y = 0

    def jump(self):
        if self.can_jump:
            self.vel_y = self.jump_power
            self.can_jump = False

player = Player('cube.png',300,200,50,50) #створення об'єкту
key1 = Player('keya.png',115,40,50,50) #створення об'єкту
door1 = Player('scr.png',420,200,50,50) #створення об'єкту
spike = Player('spike.png',-220,-220,50,50)


move_left = False
move_right = False

game = True
while game: #створення головного циклу
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        if event.type == pygame.KEYDOWN: # якщо натиснута клавіша
            if event.key == pygame.K_d: # якщо клавіша "праворуч"
                move_right = True
            if event.key == pygame.K_a: # якщо клавіша "ліворуч"
                move_left = True

            if event.key == pygame.K_w:
                    
                player.jump()

        elif event.type == pygame.KEYUP: # якщо клавіша відпущена
            if event.key == pygame.K_d: # якщо клавіша "праворуч"
                move_right = False
            if event.key == pygame.K_a: # якщо клавіша "ліворуч"
                move_left = False

    text1 = Label(20,20,20,10,(0,0,0)) # перші 2 цифри це координати
    text1.set_text('Text',60,(255,0,0)) # 60 - це розмір тексту, і далі 2 цифри це колір
    text1.draw(20,20)
    
    player.move()

    if move_right:
        player.rect.x += 3
    if move_left:
        player.rect.x -= 3

    if move_right:
        player.rect.x += 3
        for w in walls:
            if player.rect.colliderect(w.rect):
                player.rect.right = w.rect.left  # змінюємо позицію гравця, щоб він не міг пройти крізь стіну
    if move_left:
        player.rect.x -= 3
        for w in walls:
            if player.rect.colliderect(w.rect):
                player.rect.left = w.rect.right  # змінюємо позицію гравця, щоб він не міг пройти крізь стіну
    
    if player.rect.colliderect(key1.rect):
        walls.pop(7)
        key1.rect.y = -200

    if player.rect.colliderect(spike.rect):
        player.rect.x = 400
        player.rect.y = 300


    mw.blit(bd_image, (0,0)) #заповнення головного вікна
    mw.blit(bd_image, (346.7,0))
    mw.blit(bd_image, (0,348))
    mw.blit(bd_image, (346.8,348))

    #button class

class Button():
	def __init__(self, x, y, image, scale):
		width = image.get_width()
		height = image.get_height()
		self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)
		self.clicked = False

	def draw(self, surface):
		action = False
		#get mouse position
		pos = pygame.mouse.get_pos()

		#check mouseover and clicked conditions
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				self.clicked = True
				action = True

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False

		#draw button on screen
		surface.blit(self.image, (self.rect.x, self.rect.y))

		return action

pygame.display.set_caption("Main Menu")

#game variables
game_paused = False
menu_state = "main"

resume_img = pygame.image.load("images/button_resume.png").convert_alpha()
options_img = pygame.image.load("images/button_options.png").convert_alpha()
quit_img = pygame.image.load("images/button_quit.png").convert_alpha()
video_img = pygame.image.load('images/button_video.png').convert_alpha()
audio_img = pygame.image.load('images/button_audio.png').convert_alpha()
keys_img = pygame.image.load('images/button_keys.png').convert_alpha()
back_img = pygame.image.load('images/button_back.png').convert_alpha()

#create button instances
resume_button = Button(304, 125, resume_img, 1)
options_button = Button(297, 250, options_img, 1)
quit_button = Button(336, 375, quit_img, 1)
video_button = Button(226, 75, video_img, 1)
audio_button = Button(225, 200, audio_img, 1)
keys_button = Button(246, 325, keys_img, 1)
back_button = Button(332, 450, back_img, 1)

def draw_text(text, font, text_col, x, y):
  img = font.render(text, True, text_col)
  mw.blit(img, (x, y))

#game loop
run = True
while run:

  mw.fill((52, 78, 91))

  #check if game is paused
  if game_paused == True:
    #check menu state
    if menu_state == "main":
      #draw pause screen buttons
      if resume_button.draw(mw):
        game_paused = False
      if options_button.draw(mw):
        menu_state = "options"
      if quit_button.draw(mw):
        run = False
    #check if the options menu is open
    if menu_state == "options":
      #draw the different options buttons
      if audio_button.draw(mw):
        print("Audio Settings")
      if keys_button.draw(mw):
        print("Change Key Bindings")
      if back_button.draw(mw):
        menu_state = "main"
  else:
    draw_text("Press SPACE to pause", 160, 250)

  #event handler
  for event in pygame.event.get():
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_SPACE:
        game_paused = True
    if event.type == pygame.QUIT:
      run = False


    player.fill()
    player.draw()
    key1.fill()
    key1.draw()
    door1.fill()
    door1.draw()
    spike.fill()
    spike.draw()
    
    
    if player.rect.colliderect(door1.rect):
        walls = [Wall(0,0,25,1000),
        Wall(0,400,1000,1000),
        Wall(475,0,1000,1000),
        Wall(0,320,100,25),
        Wall(175,170,150,25),
        Wall(175,250,150,25),
        Wall(400,320,100,25),
        Wall(380,120,100,25),
        Wall(380,0,25,120),]
        door1.rect.y=75 
        door1.rect.x=410
        key1.rect.y=50
        key1.rect.x=25
        spike.rect.y=375
        spike.rect.x=225




    for w in walls:
        w.fill()
       # door2.fill() 
       # door2.draw()
    
    pygame.display.update() #оновлення кадрів
    clock.tick(60) # фпс