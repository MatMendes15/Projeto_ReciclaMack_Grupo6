import pygame
from cenas.menu import Menu

def main():
    pygame.init()
    menu = Menu()
    menu.run()

if __name__ == "__main__":
    main()