#-------------------------------------------------------------------------------
# Name:        module3
# Purpose:
#
# Author:      Babu
#
# Created:     29/08/2012
# Copyright:   (c) Babu 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------


import cv2,cv,pygame,time,random,numpy as np,speech
'''
sword
enemy
image processing
gamebody

'''
class image_pro():

      def __init__(self):
        #cv2.namedWindow("image1",1)
    	#cv2.namedWindow("image2",1)
    	self.vid= cv2.VideoCapture(0)
        self.lowerb=np.array([0,180,30])
        self.upperb=np.array([70,255,120])
        self.kernel = np.ones((5,5),'uint8')
        self.kernel1 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))

      '''add a filter that reduce the size of the image'''
      '''also make it a bit blur to give an effect '''
      def image_filter(self,im1):
        im4=cv2.blur(im1,(8,8))
        #im1=cv2.cvtColor(im4,cv2.COLOR_BGR2HSV)
        im=cv2.cvtColor(im4,cv2.COLOR_BGR2RGB)
        im1=cv2.cvtColor(im,cv2.COLOR_RGB2HSV)
        im2=cv2.inRange(im1,self.lowerb,self.upperb)
        im3=cv2.erode(im2,self.kernel)
        im2=cv2.dilate(im3,self.kernel)
        im3 = cv2.morphologyEx(im2,cv2.MORPH_OPEN,self.kernel)
        im2 = cv2.morphologyEx(im3,cv2.MORPH_CLOSE,self.kernel)
        #cv2.imshow("image3",im2)
        return im2

      def image_core(self):
        #time1 = time.time()
        val,im = self.vid.read()
        #cv2.imshow("image2",im)
        posX,posY=0,0
        if val:
            im2=self.image_filter(im)
            #r,im1=cv2.threshold(im2,90,255,1)
            contours,hierarchy = cv2.findContours(im2,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
            print contours
            for h,cnt in enumerate(contours):
               area = cv2.contourArea(cnt)#error in opencv think of changing version to 2.4.2 (dang) suggest using linux
               if area > 1000:
                posX = int((cv2.moments(cnt)['m10']) / (cv2.moments(cnt)['m00']))
                posY = int((cv2.moments(cnt)['m01']) / (cv2.moments(cnt)['m00']))
                '''moments = cv2.moments(cnt)
                moment00 = moments['m00']
                moment10=moments['m10']
                moment01=moments['m01']
                posX = int(moment10/moment00)
                posY = int(moment01/moment00)'''
                cv2.circle(im,(int((posX)),int((posY))),40,(0,0,255),2,1)
                cv2.circle(im,(int((posX+5)),int((posY+5))),40,(0,0,255),2,1)
                cv2.circle(im,(int((posX-5)),int((posY-5))),40,(0,0,255),2,1)
                cv2.circle(im,(int((posX+5)),int((posY-5))),40,(0,0,255),2,1)
                cv2.circle(im,(int((posX-5)),int((posY+5))),40,(0,0,255),2,1)
               else:
                posX,posY=0,0
            im1=cv.fromarray(im)
            #cv2.imshow("image1",im)
            cv2.waitKey(10)
            #time2 = time.time()
            #print ((time2-time1)*1000.0)
            return im1,posX,posY

class Sword(pygame.sprite.Sprite):

    def __init__(self, color, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([width, height])
        white= ( 255, 255, 255)
        self.image.fill(white)
        self.image.set_colorkey(white)
        pygame.draw.ellipse(self.image,color,[0,0,width,height])
        self.rect = self.image.get_rect()

class enemy(pygame.sprite.Sprite):# for the dragons blitting

    def __init__(self, color, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([width, height])
        self.image.fill(white)
        self.image.set_colorkey(white)
        pygame.draw.ellipse(self.image,color,[0,0,width,height])
        self.rect = self.image.get_rect()

class game_body(Sword,enemy,pygame.sprite.Sprite):

    def __init__(self):
        pygame.init()
        self.h=480
        self.w=640
        black= (   0,   0,   0)
        white= ( 255, 255, 255)
        red  = ( 255,   0,   0)
        self.window=pygame.display.set_mode((self.w,self.h))
        self.surface = pygame.Surface([self.w,self.h])
        self.surface.fill(white)
        self.window.blit(self.surface,(0,0))
        pygame.display.set_caption("SWORDS")
        self.screen=pygame.display.get_surface()
        if self.screen == None:
           print 'NO DISPLAY IS SET'
        self.all_sprites_list = pygame.sprite.RenderPlain()
        self.player1 = Sword(red, 20, 15)
        self.player2 = Sword(red, 20, 15)
        self.player3 = Sword(red, 20, 15)
        self.player4 = Sword(red, 20, 15)
        self.player5 = Sword(red, 20, 15)
        self.all_sprites_list.add(self.player1)
        self.all_sprites_list .add(self.player2)
        self.all_sprites_list.add(self.player3)
        self.all_sprites_list.add(self.player4)
        self.all_sprites_list.add(self.player5)
        self.i=0
        self.x=0
        self.y=0
        self.t=0
        self.score=0
    '''improve front cover '''
    def gui_start(self):
        f_cover=pygame.image.load('troll7.jpg')
        self.surface.fill((0,0,0))
        self.window.blit(f_cover,((self.w/2-220,25)))
        font = pygame.font.Font(None,80)
        text = font.render('SWORDS', True,(0,122,255))
        self.window.blit(text,(self.w/2-140,20))
        pygame.display.update()
        #font = pygame.font.Font(None,20)
        #text = font.render('This is a simple game using image processing designed by using Pygame and OpenCV.', True,(0,0,0))
        #self.window.blit(text,(10,50))
        pygame.display.update()
        font = pygame.font.Font(None,60)
        text = font.render('Press Any Key To Begin', True,(0,122,255))
        self.window.blit(text,(self.w/2-280,self.h-60))
        pygame.display.update()

    def gui_end(self):
        self.surface.fill((255,255,255))
        self.window.blit(self.surface,(0,0))
        f_cover=pygame.image.load('troll4.jpg')
        self.surface.fill((0,0,0))
        pygame.display.update()
        self.window.blit(f_cover,((10,10)))
        font = pygame.font.Font(None,55)
        text = font.render('The Game Ends', True, (0,0,0))
        self.window.blit(text,(self.w/2+10,self.h/2-150))
        pygame.display.update()
        score='Your Score is '+str(self.score)
        text = font.render(score, True,(0,0,0))
        self.window.blit(text,(self.w/2+25,self.h/2+100))
        pygame.display.update()
        pygame.time.delay(1000)
# an images comes in the middle

    def start(self):
        pygame.display.update()
        event = pygame.event.poll()
        if event.type == pygame.KEYDOWN:
              start=1
              return start

    def end(self):
        event = pygame.event.poll()
        if event.type == pygame.KEYDOWN:
           if event.key ==pygame.K_ESCAPE:
              return 0
           else:
                return 1
        else:
             return 1

    def draw_circle(self,i,x,y,t):
        if t==1:
           pygame.draw.circle(self.window,(255,0,0),(x,y),i,1)
           pygame.display.update()

    def sword_center_draw(self,im1,posX,posY):
        pg_img = pygame.image.frombuffer(im1.tostring(), cv.GetSize(im1),"RGB")
        if posX == 0:
            self.window.blit(pg_img, (0,0))
            pygame.display.update()
            return
        self.player1.rect.x=posX
        self.player1.rect.y=posY
        self.player2.rect.x=posX+5
        self.player2.rect.y=posY+5
        self.player3.rect.x=posX-5
        self.player3.rect.y=posY-5

        self.player4.rect.x=posX-5
        self.player4.rect.y=posY+5

        self.player5.rect.x=posX+5
        self.player5.rect.y=posY-5

        self.window.blit(pg_img, (0,0))
        pygame.display.update()
        self.all_sprites_list.draw(self.window)
        pygame.display.update()


    def game_core(self,posX,posY):


        self.draw_circle(self.i,self.x,self.y,self.t)
        self.i=self.i+2
        x,y=self.x,self.y
        if self.i>50:
           self.x,self.y,self.i,self.t=random.randint(50,580),random.randint(50,430),3,1
        if (x+30 > posX > x-30 and y+30 > posY > y-30 ) or (x+30 > posX+5 > x-30 and y+30 > posY+5 > y-30 ) or (x+30 > posX-5 > x-30 and y+30 > posY-5 > y-30 )or (x+30 > posX+5 > x-30 and y+30 > posY-5 > y-30 )or (x+30 > posX-5 > x-30 and y+30 > posY+5 > y-30 ):
                      #count=0
                      #while count > 10 :
                      for c in xrange(0,5):
                          pygame.draw.circle(self.window,(0,255,0),(x,y),self.i,0)
                          pygame.display.update()
                      #self.window.blit(pg_img, (0,0))
                      #pygame.display.update()
                      self.x,self.y,self.i,self.t=random.randint(50,580),random.randint(50,430),3,1
                      print 'collision'
                      #if self.i>5:
                      self.score=self.score+1
                      print 'score=',self.score
        return self.score


def main():
    image=image_pro()
    game=game_body()
    game.gui_start()
    start,end,score=0,1,0
    speech.say("Welcome to swords")
    speech.say("press any key to begin")
    while end:
          start,end=game.start(),game.end()
          #start=game.start()
          #print end
          while start:
              #profile.run('main()')
              time1 = time.time()
              im,posX,posY=image.image_core()
              game.sword_center_draw(im,posX,posY)
              score=game.game_core(posX,posY)
              time2 = time.time()
              #print ((time2-time1)*1000.0),'sec'
              end=game.end()
              start=end
    ''' option for retry'''
    game.gui_end()
    speech.say("final score is "+str(score))
    cv2.destroyAllWindows()
    pygame.quit ()

if __name__ == '__main__':
    main()
