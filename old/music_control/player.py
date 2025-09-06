# controller.py
import pygame

class MusicController:
    def __init__(self, music_file= "assets/sapne-bande.mp3"):
        pygame.mixer.init()
        pygame.mixer.music.load(music_file)

    def startstop(self, fingers):    
        if fingers == 5:
            pygame.mixer.music.play()
        elif fingers == 0:
            pygame.mixer.music.stop()
