from math import fabs
import pygame
from pygame import event
from pygame import time
import config
from enum import Enum

class Direction(Enum):
    NONE = 0,
    UP = 1,
    DOWN = 2,
    LEFT = 3,
    RIGHT = 4





class Snake_Engine:
    def __init__(self):
        self._window = pygame.display.set_mode((config.WINDOW_WIDTH, config.WINDOW_HEIGHT))
        self._clock = pygame.time.Clock()
        self._GRID_LAYER = pygame.Surface((config.BG_WIDTH,config.BG_HEIGHT))
        self._SNAKE_LAYER = pygame.Surface((config.PLAYER_WIDTH, config.PLAYER_HEIGHT))
        self._SCORE_PANEL_LAYER = pygame.Surface((config.WINDOW_WIDTH, config.BG_HEIGHT ))
        self._SPLASH_LAYER = pygame.Surface((config.WINDOW_WIDTH, config.WINDOW_HEIGHT))
        self.apple = None # coord to hold where apple is at once it is known
        self._isRunning = True
        self._TIMED_POINT_INCREASE = pygame.USEREVENT + 1
        self._TIMED_POINT_INCREASE_EVENT = event.Event(self._TIMED_POINT_INCREASE)
        self._currentDir = Direction.NONE
        self._pendingGrowth = False
        self._hitDetected = False
        self._points = 0
        self._pointTimerExpired = False
        self._uptime = int(0)
        self._gameover = False
        self._waitingOnSplash = True
        self._score_text = config.SCORE_FONT.render("Points: {}".format(self._points), True, config.FADED_SCHOOLBUS)
        self._score_text_rect = self._score_text.get_rect()
        self._hasBegun = False
        self._timerBegun = False
        

        self._score_text_rect.topleft = (config.WINDOW_WIDTH * .05, config.WINDOW_HEIGHT * .90)
        
        
        if config.DEBUG_MODE_ON:
            self.snake = [config.DEFAULT_HEAD_COORD, \
                         [config.DEFAULT_HEAD_COORD[0] + 1, config.DEFAULT_HEAD_COORD[1]], \
                         [config.DEFAULT_HEAD_COORD[0] + 2, config.DEFAULT_HEAD_COORD[1]], \
                         [config.DEFAULT_HEAD_COORD[0] + 3, config.DEFAULT_HEAD_COORD[1]], \
                         [config.DEFAULT_HEAD_COORD[0] + 4, config.DEFAULT_HEAD_COORD[1]], \
                         [config.DEFAULT_HEAD_COORD[0] + 4, config.DEFAULT_HEAD_COORD[1]+1], \
                         [config.DEFAULT_HEAD_COORD[0] + 4, config.DEFAULT_HEAD_COORD[1]+2] ]
            self.pixelPos = []
        else:
            self.snake = [config.DEFAULT_HEAD_COORD]

    def Reset(self):
        pass
    
    
    
    def Run(self):
        self._clock.tick()
        self._initSplash(self._SPLASH_LAYER)
        while self._waitingOnSplash:
            self._splashScreen()

        #The following 2 declarations initialize the surface named GRID_LAYER
        self._initFilledBG(config.ZORA_SKIN, self._GRID_LAYER)
        self._initGridOverlay(config.DARK_BLUE, self._GRID_LAYER)


        while not self._gameover:
            if not self._isRunning:
                break

            self._clock.tick(config.GAME_SPEED)
            self._uptime = time.get_ticks()

            if self._hasBegun and not self._timerBegun:
                time.set_timer(self._TIMED_POINT_INCREASE_EVENT, 3000)
                self._timerBegun = True
                
            self._processevents()
            
            self._updateState()
            self._render()

            if config.DEBUG_MODE_ON:
                
                self._DB_CONSOLE_UPDATE()
        
        while self._gameover and self._isRunning:
            #This is where I could restart the game or reset the gamestate to start over
            self._processevents()
     
    def _processevents(self):

        if not self._waitingOnSplash:
            # The following keypress code allows for more responsive keys than with the event system
            keys = pygame.key.get_pressed()
            
            # The extra conditional logic is to combat a glitch that allows you to do a 180 via multi key processing between frames
            if keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT] and not keys[pygame.K_UP] and not keys[pygame.K_DOWN]:
                self._LeftPressed()
                if not self._hasBegun:
                    self._hasBegun = True
            if keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT] and not keys[pygame.K_UP] and not keys[pygame.K_DOWN]:
                self._RightPressed()
                if not self._hasBegun:
                    self._hasBegun = True
            if keys[pygame.K_UP] and not keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT] and not keys[pygame.K_DOWN]:
                self._UpPressed()
                if not self._hasBegun:
                    self._hasBegun = True
            if keys[pygame.K_DOWN] and not keys[pygame.K_RIGHT] and not keys[pygame.K_UP] and not keys[pygame.K_LEFT]:
                self._DownPressed()
                if not self._hasBegun:
                    self._hasBegun = True


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._isRunning = False
                break
            if not self._waitingOnSplash and self._hasBegun:
                if event.type == self._TIMED_POINT_INCREASE_EVENT.type:
                    self._pointTimerExpired = True
            
            if self._waitingOnSplash:
                if event.type == pygame.KEYUP:
                    self._waitingOnSplash = False

        

    def _updateState(self):
        if not self._waitingOnSplash:
            if self._isRunning:            
                
                if self.apple == None:
                    self.apple = self._spawnApple()

                if self._checkAppleCollision():
                    self._collectApple()

                selfHit = self._checkForSelfBodyHit()

                if (self.snake[0][0] <= 0 and self._currentDir == Direction.LEFT) or \
                (self.snake[0][0] >= config.CELLS_ACROSS - 1 and self._currentDir == Direction.RIGHT) or \
                (self.snake[0][1] <= 0 and self._currentDir == Direction.UP) or \
                (self.snake[0][1] >= config.CELLS_DOWN -1 and self._currentDir == Direction.DOWN) or \
                (selfHit == True):

                    self._hitDetected = True
                else:    
                    if self._currentDir == Direction.UP:
                        self._MoveSnakeUp()
                    elif self._currentDir == Direction.DOWN:
                        self._MoveSnakeDown()
                    elif self._currentDir == Direction.LEFT:
                        self._MoveSnakeLeft()
                    elif self._currentDir == Direction.RIGHT:
                        self._MoveSnakeRight()
                    elif self._currentDir == Direction.NONE:
                        pass
                
                if self._hitDetected:
                    time.set_timer(self._TIMED_POINT_INCREASE_EVENT, 0)
                    self._gameover = True
                
                if self._pointTimerExpired and not self._hitDetected:
                    if config.DEBUG_MODE_ON:
                        config.EVENT_CALL_COUNTER += 1
                    self._points += 1
                    self._pointTimerExpired = False

    def _render(self):
        if self._waitingOnSplash:
            self._window.blit(self._SPLASH_LAYER, (0,0))
            
            pygame.display.flip()
        else:
            self._window.blit(self._GRID_LAYER, (0,0))
            self._drawSnake()
            if self.apple != None:
                if len(self.apple) > 0:
                    self._drawApple()
            
            self._initScorePanel(self._SCORE_PANEL_LAYER)
            
            self._window.blit(self._SCORE_PANEL_LAYER, (0, config.BG_HEIGHT))
            self._score_text = config.SCORE_FONT.render("Points: {}".format(self._points), True, config.FADED_SCHOOLBUS)
            self._window.blit(self._score_text, self._score_text_rect)

            
            pygame.display.flip()

    def _DB_CONSOLE_UPDATE(self):
        config.DB_CLEAR()
        print("pos: {} , {}".format(self.snake[0][0], self.snake[0][1]))
        self.pixelPos = self._CoordToPixel(self.snake[0]) 
        print("Pixel Pos: {}, {}".format(self.pixelPos[0], self.pixelPos[1]))
        print("len: {}".format(len(self.snake)))
        config.DRAW_DEBUG_MSG(self._window)
        print("Score Events Called: {}".format(config.EVENT_CALL_COUNTER))
        print("Points: {}".format(self._points))
        print("Hit Detected: {}".format(self._hitDetected))
        if self.apple != None:
            if len(self.apple) > 0:
                print("Apple Coord: {},{}".format(self.apple[0], self.apple[1]))
        print("Pending Growth?: {}".format(self._pendingGrowth))

        upt = config.convertMillis(self._uptime)
        
        
        print("Uptime: {}:{}:{}".format(int(upt[0]), int(upt[1]), int(upt[2])))

    def _initFilledBG(self, rgb, surface):
        rectColor = []
        if config.DEBUG_MODE_ON:
            rectColor = config.DB_GREEN
        else:
            rectColor = rgb

        pygame.draw.rect(surface, rectColor, [0, 0, config.BG_WIDTH, config.BG_HEIGHT], 0)

    def _initGridOverlay(self,rgb, surface):
        rectColor = []
        if config.DEBUG_MODE_ON:
            rectColor = config.DB_SNOT
        else:
            rectColor = rgb

        for i in range(config.CELLS_ACROSS):
            for j in range(config.CELLS_DOWN):
                x = i * config.CELL_WIDTH
                y = j * config.CELL_HEIGHT
                pygame.draw.rect(surface, rectColor, [x + config.GRID_CELL_OFFSET_X, y + config.GRID_CELL_OFFSET_Y, config.GRID_CELL_WIDTH, config.GRID_CELL_HEIGHT], 0)

    def _initSplash(self,surface):
         pygame.draw.rect(surface, config.ZORA_SKIN, [0, 0, config.WINDOW_WIDTH, config.WINDOW_HEIGHT], 0)
         surface.blit(config.LOGO, config.LOGO_RECT)

    def _initScorePanel(self, surface):
        pygame.draw.rect(surface, config.DARK_BLUE, [0, 0, config.WINDOW_WIDTH, config.WINDOW_HEIGHT - config.BG_HEIGHT])

    def _drawSnake(self):
        rectColor = []
        if config.DEBUG_MODE_ON:
            rectColor = config.DB_BLUE
        else:
            rectColor = config.SALMON

        for i in range(len(self.snake)):
            pixPos = self._CoordToPixel(self.snake[i])            
            pygame.draw.rect(self._window, rectColor, [pixPos[0], pixPos[1], config.PLAYER_WIDTH, config.PLAYER_HEIGHT], 0)

    def _drawApple(self):
        rectColor = []
        if config.DEBUG_MODE_ON:
            rectColor = config.DB_ORANGE
        else:
            rectColor = config.FADED_SCHOOLBUS

        pixPos = self._CoordToPixel(self.apple)            
        pygame.draw.rect(self._window, rectColor, [pixPos[0], pixPos[1], config.GRID_CELL_WIDTH, config.GRID_CELL_HEIGHT], 0)

    def _CoordToPixel(self, coord:list[int]):
        x = coord[0] * config.CELL_WIDTH
        y = coord[1] * config.CELL_HEIGHT
        return [x,y]
    def _UpPressed(self):
        if self._currentDir != Direction.DOWN:
            self._currentDir = Direction.UP
    def _DownPressed(self):
        if self._currentDir != Direction.UP:
            self._currentDir = Direction.DOWN
    def _LeftPressed(self):
        if self._currentDir != Direction.RIGHT:
            self._currentDir = Direction.LEFT
    def _RightPressed(self):
       if self._currentDir != Direction.LEFT:
            self._currentDir = Direction.RIGHT
    def _MoveSnakeUp(self):
        self.snake.insert(0, (self.snake[0][0], self.snake[0][1] - 1))
        if self._pendingGrowth == False:
            self.snake.pop()
        else:
            self._toggleGrow()
    def _MoveSnakeDown(self):
        self.snake.insert(0, (self.snake[0][0], self.snake[0][1] + 1))
        if self._pendingGrowth == False:
            self.snake.pop()
        else:
            self._toggleGrow()
    def _MoveSnakeLeft(self):
        self.snake.insert(0, (self.snake[0][0] - 1, self.snake[0][1]))
        if self._pendingGrowth == False:
            self.snake.pop()
        else:
            self._toggleGrow()
    def _MoveSnakeRight(self):
        self.snake.insert(0, (self.snake[0][0] + 1, self.snake[0][1]))
        if self._pendingGrowth == False:
            self.snake.pop()
        else:
            self._toggleGrow()
    def _checkForSelfBodyHit(self) -> bool:
        ''' Check if given list contains any duplicates '''
        if len(self.snake) >= 5:
            i = 1
            while i < len(self.snake):
                if self.snake[0][0] == self.snake[i][0] and self.snake[0][1] == self.snake[i][1]:
                    return True                
                i += 1
            return False

    def _spawnApple(self) -> list[int]:
        "Finds an open grid space at random and returns the coordinate"
        genAgain = True
        newCoord = None
        while genAgain:
            newCoord = config.Generate_Random_Coord()
            if newCoord in self.snake:
                genAgain = True
            else:
                genAgain = False
        return newCoord

    def _collectApple(self):
        "Consumes the current apple so to say and triggers a new spawn and a point increment"
        self._points += 10
        self.apple.clear()
        self.apple = None
        self._toggleGrow()
        
    def _checkAppleCollision(self)->bool:
        if self.apple != None:
            if len(self.apple) > 0:
                for elem in self.snake:
                    if elem[0] == self.apple[0] and elem[1] == self.apple[1]:
                        return True
                
            return False

    def _toggleGrow(self):
        if self._pendingGrowth:
            self._pendingGrowth = False
        else:
            self._pendingGrowth = True

    def _splashScreen(self):
        
        self._processevents()
        self._updateState()
        self._render()

