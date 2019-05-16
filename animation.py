#!/usr/bin/env python

import pygame
import os

_image_library = {}
def get_image(path):
    global _image_library
    image = _image_library.get(path)
    if image == None:
        canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
        image = pygame.image.load(canonicalized_path)
        _image_library[path] = image
    return image
 
class knight(pygame.sprite.Sprite):
 
    def __init__(self, frames, fps=15):
        pygame.sprite.Sprite.__init__(self)
        self.upframes       = frames[0]       # save the images in here
        self.leftframes     = frames[1]
        self.downframes     = frames[2]
        self.rightframes    = frames[3]
        self.frames         = self.downframes
        self.current = 0       # idx of current image of the animation
        self.image = self.upframes[0]  # just to prevent some errors
        self.rect = self.image.get_rect()    # same here
        self.oldImage = self.image
        self.oldRect = self.rect
        self.dirty = False
        self.pos = [0,0]

        # stuff for animation timing
        self._next_update = 0
        self._period = fps/1000.
        self._start_time = 0
        self._paused_time = 0
        self._pause_start = 0
        self._frames_len = len(self.frames)

         
    def update(self, key, t, background):
        dirtyRect = None
        self.dirty = False
        if keys[pygame.K_UP] and self.pos[1] > 0:
            self.frames = self.upframes
            self.pos[1] -= 2
        elif keys[pygame.K_LEFT] and self.pos[0] > 0:
            self.frames = self.leftframes
            self.pos[0] -= 2
        elif keys[pygame.K_DOWN] and self.pos[1] < 300-64:
            self.frames = self.downframes
            self.pos[1] += 2
        elif keys[pygame.K_RIGHT] and self.pos[0] < 400-64:
            self.frames = self.rightframes
            self.pos[0] += 2
        if keys[pygame.K_UP] or keys[pygame.K_LEFT] or keys[pygame.K_DOWN] or keys[pygame.K_RIGHT]:
            self.current = int(t*self._period)
            self.current %= self._frames_len

            oldRect = self.rect

            self.image = self.frames[self.current] # new sprite image for next frame
            self.rect = screen.blit(self.image,self.pos) # corresponding rect
            self.dirty = True
            
            if self.rect.colliderect(oldRect): # if the new sprite frame doesn't move far enough

                dirtyRect = self.rect.union(oldRect) # get the overall size of the dirty rectangle

                new_surf = pygame.Surface((dirtyRect[2],dirtyRect[3])) # create a new surface for creating this dirty image
                back_surf = background.subsurface((self.pos[0],self.pos[1],dirtyRect[2],dirtyRect[3])) # find the background's image in that area
                back_rect = back_surf.get_rect() # get the background's rect for that area
                new_surf.blit(back_surf,(0,0))
                new_surf.blit(self.image,(0,0))
                dirtyRect = screen.blit(new_surf,tuple(self.pos))

        return dirtyRect
    
    def blit(self, screen):
        print('rect',self.rect)
        print('screen',screen)
        print('pos',self.pos)
        print(self.rect.colliderect(self.oldRect))
        print(self.rect.union(self.oldRect))
        print('screenblit',screen.blit(self.image,tuple(self.pos)))


        


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((400,300))
    background = get_image('megaman.jpg')
    screen.blit(background,(0,0))
    pygame.display.flip()
    # screen.fill((255,255,255))
    done = False
    clock = pygame.time.Clock()

    usprites = ['new_sprites-' + str(i) + '.png' for i in range(0, 9)]
    lsprites = ['new_sprites-' + str(i) + '.png' for i in range(9, 18)]
    dsprites = ['new_sprites-' + str(i) + '.png' for i in range(18, 27)]
    rsprites = ['new_sprites-' + str(i) + '.png' for i in range(27, 36)]
    sprites = [usprites,lsprites,dsprites,rsprites]
    frames = []
    for i,row in enumerate(sprites):
        frames.append([])
        for sprite in row:
            frames[i].append(get_image(sprite))
    dude = knight(frames)

    while not done:
        rect = []
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        
        keys = pygame.key.get_pressed()
        pos = dude.update(keys, pygame.time.get_ticks(), background)
        if dude.dirty:
            pygame.display.update(pos)
        clock.tick(60)