import pygame
import random, os
os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()

class Head(object):

    def __init__(self, posX, posY):
        self.posX = posX
        self.posY = posY

        self.headSurf=  pygame.Surface((30,30))
        self.head = pygame.draw.circle(self.headSurf,(0,255,0),(15,15),15,3)

class Tail(object):

    def __init__(self,posX,posY):
        self.posX = posX
        self.posY = posY
        self.tailSurf = pygame.Surface((30,30))
        self.tailCircle = pygame.draw.circle(self.tailSurf,(0,255,0),(15,15),15)
        
class Food(object):
    
    def __init__(self,(posX,posY),radius):
        self.posX = posX
        self.posY = posY
        self.foodSurf = pygame.Surface((30,30))
        self.foodCircle = pygame.draw.circle(self.foodSurf,(0,0,255),(15,15),radius)

#MAIN WINDOW

def main():
    window = pygame.display.set_mode((600,635))
    pygame.display.set_caption("ASHI SNAKE")
    pygame.mouse.set_visible(False)
    
    choice = 0
    length, speed = (0,0)
    while choice != -1:
        choice = menu(window, length, speed)
        
        if choice == 1:
            length, speed = game(window)
    pygame.quit()
    return 0

def menu(window, length = 0, speed = 0):
    
    #VARIBALES
    FPS = 30            #Frames per second
    choice = 1          #return value of the function
    choosing = True     #keeping the loop running
    
    #TEXT
    font = pygame.font.Font("FreeSansBold.ttf",20)
    textNewGame = font.render("New Game",1,(0,255,0))
    textExit = font.render("Exit",1,(0,255,0))
    textLastTry = font.render("Your last Try:",1,(0,200,0))
    textLengthOfSnake = font.render("Length:",1,(0,200,0))
    textLength = font.render(str(length),1,(0,200,100))
    textSpeedString = font.render("Speed:",1,(0,200,0))
    textSpeed = font.render(str(speed),1,(0,200,100))
    
    
    selectionSurf = pygame.Surface((30,30))
    selectionRect = pygame.draw.circle(selectionSurf,(190,0,0),(15,15),10)
    selectionPosY = 250
    selectionPosX = 10
    
    while choosing:
        window.fill((0,0,0))
        
        #EVENTS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                choice = -1
                choosing = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    choice = -1
                    choosing = False
                elif event.key == pygame.K_DOWN:
                    if choice == 1:
                        choice = -1
                        selectionPosY += 50
                elif event.key == pygame.K_UP:
                    if choice == -1:
                        choice = 1
                        selectionPosY -= 50
                elif event.key == pygame.K_RETURN:
                    choosing = False
        window.blit(textNewGame, (50,250))
        window.blit(textExit,(50,300))
        window.blit(selectionSurf,(selectionPosX, selectionPosY))
        
        if length != 0:
            window.blit(textLastTry,(400,230))
            window.blit(textLengthOfSnake, (400,280))
            window.blit(textLength, (500,280))
            window.blit(textSpeedString, (400,330))
            window.blit(textSpeed, (500,330))
        pygame.display.update()
    
    return choice
        
                    
        


def game(window):

    #GRID, TRACKS WHICH TILE IS OCCUPIED (0 = free, 1 = blocked, 2 = Food)
    grid = [[0 for i in xrange(20)] for i in xrange(20)]
    
    #LIST OF FREE TILES
    freeTiles = []
    for i in xrange(20):
        for j in xrange(20):
            freeTiles.append((i,j))
    
    #VARIABLES
    running = True
    fpsClock = pygame.time.Clock()
    bigFoodVanishClock = pygame.time.Clock()
    FPS = 5
    direction = 1 # -2:Down, -1:Up, 1: Right, 2:Left
    foodOnGrid = False
    hasEaten = False
    isPaused = False
    bigFoodVanishCounter = 0
    bigFoodVanishCounting = False
    length = 4
    bigFoodCounter = 0
    directionList = [1]
    score = 0
    
    #TEXT
    font = pygame.font.Font("FreeSansBold.ttf",20)
    textLengthOfSnake = font.render("Length of snake:", 1, (0,200,0))
    textLengthOfSnakePos = (0,610)
    textScore = font.render(str(length), 1, (0,200,100))
    textScorePos = (textLengthOfSnake.get_size()[0]+10,610)
    textSpeed = font.render(str(FPS), 1, (0,200,100))
    textSpeedPos = (window.get_size()[0]-textSpeed.get_size()[0]-12,610)
    textSpeedString = font.render("Speed:",1,(0,200,0))
    textSpeedStringPos = (window.get_size()[0]-textSpeedString.get_size()[0]-textSpeed.get_size()[0]-20,610)
    textPause = font.render("PAUSE: Press 'P' to continue or 'ESC' to quit", 1, (255,0,0))
    stringBigFoodTimer = ""
    textBigFoodTimer = font.render(stringBigFoodTimer,1,(255,0,0))
    textBigFoodTimerPos = (250,610)
    
    #HEAD OF THE SNAKE, CONTROLABLE
    head = Head(10,10)
    grid[head.posX][head.posY] = 1
    
    tailList = []

    tailList.append(Tail(9,10))
    tailList.append(Tail(8,10))
    tailList.append(Tail(7,10))

    
    del freeTiles[freeTiles.index((9,10))]
    del freeTiles[freeTiles.index((8,10))]
    del freeTiles[freeTiles.index((7,10))]

    
    for tail in tailList:
        grid[tail.posX][tail.posY] = 1
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                        running = False
                elif event.key == pygame.K_p:
                    if isPaused:
                        isPaused = False
                    else:
                        isPaused = True
                elif (event.key == pygame.K_DOWN or event.key == pygame.K_s) and not isPaused:
                    if directionList[-1] > 0:
                        directionList.append(-2)
                elif (event.key == pygame.K_UP or event.key == pygame.K_w) and not isPaused:
                    if directionList[-1] > 0:
                        directionList.append(-1)
                elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and not isPaused:
                    if directionList[-1] < 0:
                        directionList.append(1)
                elif (event.key == pygame.K_LEFT or event.key == pygame.K_a) and not isPaused:
                    if directionList[-1] < 0:
                        directionList.append(2)
                elif event.key == pygame.K_l:
                    FPS = 1
        window.fill((0,0,0))
    
    
    
        ############
        #GAME LOGIC#
        ############
        if not isPaused: #only update if game is not paused
            
            if len(directionList) > 1:
                directionList.pop(0)
            
            direction = directionList[0]
            
            #TAIL FOLLOWING THE HEAD
            for i in xrange(len(tailList)-1,-1,-1):
                if i == 0:
                    tailList[i].posX = head.posX
                    tailList[i].posY = head.posY
                else:
                    if i == len(tailList)-1:
                        if hasEaten:
                            tailList.append(Tail(tailList[i].posX, tailList[i].posY))
                            hasEaten = False
                            foodOnGrid = False
                            length += 1
                            bigFoodCounter += 1
                        else:
                            grid[tailList[i].posX][tailList[i].posY] = 0
                            freeTiles.append((tailList[i].posX, tailList[i].posY))
                    tailList[i].posX = tailList[i-1].posX
                    tailList[i].posY = tailList[i-1].posY
        
            #MOVEMENT
            if direction == -2: #MOVING DOWN
                if head.posY == 19:
                    if grid[head.posX][0] == 1:
                        running = False
                        break
                    else:
                        if grid[head.posX][0] == 2:
                            hasEaten = True
                        grid[head.posX][0] = 1
                        del freeTiles[freeTiles.index((head.posX,0))]
                        head.posY = 0
                else:
                    if grid[head.posX][head.posY + 1] == 1:
                        running = False
                        break
                    else:
                        if grid[head.posX][head.posY + 1] == 2:
                            hasEaten = True
                        grid[head.posX][head.posY + 1] = 1
                        del freeTiles[freeTiles.index((head.posX,head.posY + 1))]
                        head.posY += 1
            elif direction == -1: #MOVING UP
                if head.posY == 0:
                    if grid[head.posX][19] == 1:
                        running = False
                        break
                    else:
                        if grid[head.posX][19] == 2:
                            hasEaten = True
                        grid[head.posX][19] = 1
                        del freeTiles[freeTiles.index((head.posX,19))]
                        head.posY = 19
                else:
                    if grid[head.posX][head.posY - 1] == 1:
                        running = False
                        break
                    else:
                        if grid[head.posX][head.posY - 1] == 2:
                            hasEaten = True
                        grid[head.posX][head.posY - 1] = 1
                        del freeTiles[freeTiles.index((head.posX, head.posY - 1))]
                        head.posY -= 1
            elif direction == 1: #MOVING RIGHT
                if head.posX == 19:
                    if grid[0][head.posY] == 1:
                        running = False
                        break
                    else:
                        if grid[0][head.posY] == 2:
                            hasEaten = True
                        grid[0][head.posY] = 1
                        del freeTiles[freeTiles.index((0, head.posY))]
                        head.posX = 0
                else:
                    if grid[head.posX + 1][head.posY] == 1:
                        running = False
                        break
                    else:
                        if grid[head.posX + 1][head.posY] == 2:
                            hasEaten = True
                        grid[head.posX + 1][head.posY] = 1
                        del freeTiles[freeTiles.index((head.posX + 1, head.posY))]
                        head.posX += 1
            elif direction == 2: #MOVING LEFT
                if head.posX == 0:
                    if grid[19][head.posY] == 1:
                        running = False
                        break
                    else:
                        if grid[19][head.posY] == 2:
                            hasEaten = True
                        grid[19][head.posY] = 1
                        del freeTiles[freeTiles.index((19, head.posY))]
                        head.posX = 19
                else:
                    if grid[head.posX - 1][head.posY] == 1:
                        running = False
                        break
                    else:
                        if grid[head.posX - 1][head.posY] == 2:
                            hasEaten = True
                        grid[head.posX - 1][head.posY] = 1
                        del freeTiles[freeTiles.index((head.posX - 1, head.posY))]
                        head.posX -= 1
            
            #UPDATE SCORE IF SNAKE HAS EATEN
            if hasEaten:
                score += FPS
                print score
            
            #FOOD
            if bigFoodVanishCounting:
                bigFoodVanishClock.tick()
                bigFoodVanishCounter += bigFoodVanishClock.get_time()
                print bigFoodVanishCounter
            
            if bigFoodVanishCounting and bigFoodVanishCounter > 5000:
                grid[foodPos[0]][foodPos[1]] = 0
                foodOnGrid = False
                bigFoodVanishCounter = 0
                bigFoodVanishCounting = False
                bigFoodCounter = 0
            
            if not foodOnGrid:
                foodPos = random.choice(freeTiles)
                grid[foodPos[0]][foodPos[1]] = 2
                if bigFoodCounter == 5:
                    FPS += 1
                    bigFoodCounter = 0
                    food = Food(foodPos, 5)
                    foodOnGrid = True
                    bigFoodVanishCounter = 0
                    bigFoodVanishCounting = False
                    bigFoodCounter = 0
                elif bigFoodCounter == 4:
                    bigFoodVanishCounting = True
                    food = Food(foodPos, 10)
                    foodOnGrid = True
                    bigFoodVanishClock.tick()
                else:
                    food = Food(foodPos,5)
                    foodOnGrid = True
            
            #SOMEONE ACTUALLY WINNING THIS GAME
            if length == 400:
                print "You won"
                running = False
            
        
        
        #########
        #DRAWING#
        #########
        
        #for tiles in freeTiles:
         #   pygame.draw.rect(window, (255,0,0),(tiles[0]*30+10,tiles[1]*30+10,10,10))
        
        pygame.draw.line(window,(255,0,0),(0,600),(600,600))
        textScore = font.render(str(length), 1, (0,200,100))
        textSpeed = font.render(str(FPS), 1, (0,200,100))
        
        for tail in tailList:
            window.blit(tail.tailSurf,(tail.posX*30,tail.posY*30))
        window.blit(tailList[-1].tailSurf, (tailList[-1].posX*30, tailList[-1].posY*30))
        if foodOnGrid:
            window.blit(food.foodSurf, (food.posX*30, food.posY*30))
            
        window.blit(head.headSurf,(head.posX*30,head.posY*30))
        window.blit(textLengthOfSnake, textLengthOfSnakePos)
        window.blit(textScore, textScorePos)
        window.blit(textSpeedString, textSpeedStringPos)
        window.blit(textSpeed, textSpeedPos)
        if isPaused:
            window.blit(textPause, (300 - textPause.get_size()[0] / 2, 300))
        if bigFoodVanishCounting:
            stringBigFoodTimer = str((5000-bigFoodVanishCounter)/1000)
            textBigFoodTimer = font.render(stringBigFoodTimer,1,(255,0,0))
            window.blit(textBigFoodTimer, textBigFoodTimerPos)
        pygame.display.update()
        fpsClock.tick(FPS)
    
    return (length, FPS)


if __name__ == "__main__":
    main()
