<<<<<<< HEAD
import pygame
from pygame import event
from pygame import time
import config
from enum import Enum
from direction import Direction
from snake import Snake
import color
from scene import Splash_Scene, Play_Scene

class Snake_Engine:
    def __init__(self):
        
        self._window = pygame.display.set_mode((config.WINDOW_WIDTH, config.WINDOW_HEIGHT))
        self._clock = pygame.time.Clock()  
        

        self._currentScene = 0 #always first spot in scene queue
        self._scene_queue = [Splash_Scene((config.WINDOW_WIDTH, config.WINDOW_HEIGHT)), Play_Scene((config.WINDOW_WIDTH, config.WINDOW_HEIGHT))]
        
        self._uptime = int(0)
        
        self._timerBegun = False
        self._stateFinished = False
        self._isRunning = True
        
    def Reset(self):
        self._window.fill([0,0,0])
        self._scene_queue.clear()
        self._scene_queue = [(Splash_Scene((config.WINDOW_WIDTH, config.WINDOW_HEIGHT))), Play_Scene((config.WINDOW_WIDTH, config.WINDOW_HEIGHT))]
        pygame.display.flip()
    
    def Run(self):
        self._clock.tick()        
        while self._isRunning:
            self._clock.tick(config.GAME_SPEED)
            if not self._isRunning:
                break

            self._uptime = time.get_ticks()

            self._scene_queue[self._currentScene]._process_input()            
            self._stateFinished = self._scene_queue[self._currentScene]._update_state()
            self._scene_queue[self._currentScene]._render_scene(self._window)

            if self._stateFinished:
                self._scene_queue.pop(self._currentScene)
                self._stateFinished = False
                if len(self._scene_queue) == 0:
                    self.Reset()      
=======
import pygame
from pygame import event
from pygame import time
import config
from enum import Enum
from direction import Direction
from snake import Snake
import color
from scene import Splash_Scene, Play_Scene

class Snake_Engine:
    def __init__(self):
        
        self._window = pygame.display.set_mode((config.WINDOW_WIDTH, config.WINDOW_HEIGHT))
        self._clock = pygame.time.Clock()  
        

        self._currentScene = 0 #always first spot in scene queue
        self._scene_queue = [Splash_Scene((config.WINDOW_WIDTH, config.WINDOW_HEIGHT)), Play_Scene((config.WINDOW_WIDTH, config.WINDOW_HEIGHT))]
        
        self._uptime = int(0)
        
        self._timerBegun = False
        self._stateFinished = False
        self._isRunning = True
        
    def Reset(self):
        self._window.fill([0,0,0])
        self._scene_queue.clear()
        self._scene_queue = [(Splash_Scene((config.WINDOW_WIDTH, config.WINDOW_HEIGHT))), Play_Scene((config.WINDOW_WIDTH, config.WINDOW_HEIGHT))]
        pygame.display.flip()
    
    def Run(self):
        self._clock.tick()        
        while self._isRunning:
            self._clock.tick(config.GAME_SPEED)
            if not self._isRunning:
                break

            self._uptime = time.get_ticks()

            self._scene_queue[self._currentScene]._process_input()            
            self._stateFinished = self._scene_queue[self._currentScene]._update_state()
            self._scene_queue[self._currentScene]._render_scene(self._window)

            if self._stateFinished:
                self._scene_queue.pop(self._currentScene)
                self._stateFinished = False
                if len(self._scene_queue) == 0:
                    self.Reset()      
>>>>>>> c9f520ad55e6ee412a7d520b47c535a7311170e7
