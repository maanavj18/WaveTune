# controller.py
import pygame

class MusicController:
    def __init__(self, music_file= "assets/sapne-bande.mp3"):
        pygame.mixer.init()
        pygame.mixer.music.load(music_file)

    def handle_gesture(self, gesture):
        if gesture == "THUMB_UP":
            pygame.mixer.music.play()
        elif gesture == "STOP":
            pygame.mixer.music.stop()
