import pygame , sys
from pygame.locals import *
import numpy as np
from keras.models import load_model
import cv2

WINDOWSIZEX = 640
WINDOWSIZEY = 480  
pygame.init()
model = load_model


DISPLAY_SURFACE = pygame.display.set_mode((WINDOWSIZEX, WINDOWSIZEY))
BOUNDRY = 5

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)

FONT = pygame.font.SysFont('Comic Sans Ms', 18)

IMAGESAVE = False

MODEL = load_model("bestmodel.h5")

LABELS = {1:"one" , 2:"two", 3:"three", 4:"four", 5:"five", 6:"six" , 7:"seven", 8:"eight", 9:"nine", 0:"zero"}
num_xcord = []
num_ycord = []

iswriting = False
image_cnt = 1

PREDICT = True

while True:
    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == MOUSEMOTION and iswriting:
            xcord, ycord = event.pos
            pygame.draw.circle(DISPLAY_SURFACE, WHITE , (xcord,ycord), 4 , 0)
            
            num_xcord.append(xcord)
            num_ycord.append(ycord)
            
        if event.type == MOUSEBUTTONDOWN:     # when we are done with writing then we have to capture what we have writtne so far
            iswriting = True
            
            
        if event.type == MOUSEBUTTONUP:
            iswriting = False
            num_xcord = sorted(num_xcord)
            num_ycord = sorted(num_ycord)
            
            rect_min_x, rect_max_x = (max(num_xcord[0]-BOUNDRY,0) , min(WINDOWSIZEX, num_xcord[-1]+BOUNDRY))
            rect_min_y, rect_max_y = (max(num_ycord[0]-BOUNDRY,0) , min(WINDOWSIZEX, num_ycord[-1]+BOUNDRY))
            
            
            num_xcord = []
            num_ycord = []
            
            
            img_arr = np.array(pygame.PixelArray(DISPLAY_SURFACE))[rect_min_x:rect_max_x, rect_min_y:rect_max_y].T.astype(np.float32)
            
            if IMAGESAVE:
                cv2.imwrite("image.png")
                image_cnt+=1
            
            if PREDICT:
                
                image = cv2.resize(img_arr, (28,28))
                image = np.pad(image, (10,10),'constant', constant_values=0)
                image = cv2.resize(image,(28,28))/255
                
                label = str(LABELS[np.argmax(MODEL.predict(image.reshape(1,28,28,1)))])
                
                textsurface = FONT.render(label, True, RED, WHITE)
                textrecobj = testing.get_rect
                
                textrecobj.left , textrecobj.bottom = rect_min_x, rect_max_y
                
                DISPLAY_SURFACE.blit(textsurface, textrecobj)
                
            if event.type == KEYDOWN:
                if event.unicode == "n":
                    DISPLAY_SURFACE.fill(BLACK)
            
    pygame.display.update()    
            
                                                   

         
            
         







