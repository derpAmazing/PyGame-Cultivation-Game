import pygame
import random
import os
from realms import *
import equipment as equipmentList

# Initialize Game
pygame.init()
clock = pygame.time.Clock()

# Display
displayWidth = 1280
displayHeight = 720
mainDisplay = pygame.display.set_mode((displayWidth,displayHeight)) # Probably add 16:9 display modes
pygame.display.set_caption("Cultivation Game") # Make a real title lol

# Assets
dir = os.getcwd()
assets = os.path.join(dir,"assets")
playerPic = pygame.transform.scale(pygame.image.load(os.path.join(assets, "meditating.png")),(300,300))
objects = []

def drawPlayer(x, y):
    playerRect = playerPic.get_rect(center = (x,y))
    mainDisplay.blit(playerPic, playerRect)

def displayText(text, size, color, x, y):
    font = pygame.font.Font(os.path.join(assets,"Lato-Black.ttf"), size)
    textSurface = font.render(text, True, color)
    textRect = textSurface.get_rect(center = (x, y))
    mainDisplay.blit(textSurface, textRect)

# Game Variables
class Player:
    def __init__(self, name):
        self.name = name

        self.baseHP = 100
        self.bonusHP = 0
        self.maxHP = 100
        self.hp = self.maxHP

        self.baseATK = 10
        self.bonusATK = 0
        self.ATK = 10

        self.baseDEF = 5
        self.bonusDEF = 0
        self.DEF = 5

        self.baseSPD = 10
        self.bonusSPD = 0
        self.SPD = 10

        self.money = 0

        self.qi = 0
        self.qiMulti = 1
        self.bonusQiGain = 0
        self.realm = 0
        self.btRequirement = 100
        self.cultivating = False

        self.equipped = {
            "Head" : None,
            "Body" : None,
            "Legs" : None,
            "Weapon" : None,
            "Ring" : None,
            "Necklace" : None
        }
        self.ownedEquipment = {
            "Head" : ["Test Helmet","Test Hat"],
            "Body" : ["Test Chestplate", "Test Robe"],
            "Legs" : ["Test Leggings", "Test Greaves"],
            "Weapon" : ["Test Sword", "Test Dagger"],
            "Ring" : ["Test Power Ring","Test Vitality Ring"],
            "Necklace" : ["Test Defense Necklace","Test Spiritual Necklace"]
        }
    
    def updateStats(self):
        self.maxHP = self.baseHP + self.bonusHP
        self.ATK = self.baseATK + self.bonusATK
        self.DEF = self.baseDEF + self.bonusDEF
        self.SPD = self.baseSPD + self.bonusSPD

    def breakthrough(self): # Work on balancing/scaling
        if self.qi >= self.btRequirement:
            self.realm = self.realm + 1
            self.qi = 0
            self.qiMulti = round(1 * 1.2**(self.realm),1)
            self.btRequirement = round(100 * 1.3**(self.realm),1)
            
            self.baseHP = round(100 * 1.25**(self.realm),1)

            self.baseATK = round(10 * 1.25**(self.realm),1)

            self.baseDEF = round(5 * 1.25**(self.realm),1)

            self.baseSPD = round(10 * 1.25**(self.realm),1)

            self.updateStats()

    def cultivate(self):
        self.cultivating = not self.cultivating

player = Player("")

class textEntry:
    def __init__(self, text, textsize, x, y, minWidth, height, function, charLimit=None):
        self.rect = pygame.Rect(x, y, minWidth, height)
        self.minWidth = minWidth
        self.color = (0,50,100)
        self.text = text
        self.font = pygame.font.Font(os.path.join(assets,"Lato-Black.ttf"), textsize)
        self.textSurface = self.font.render(text, True, self.color)
        self.active = False
        self.function = function
        self.charLimit = charLimit

    def eventHandler(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            if self.active:
                self.color = (255,0,0)
            else: 
                self.color = (0,50,100)
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    self.function()
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif self.charLimit != None:
                    if not len(self.text) >= self.charLimit:
                        self.text += event.unicode
                else:
                    self.text += event.unicode
                self.textSurface = self.font.render(self.text, True, self.color)

    def update(self):
        width = max(self.minWidth, self.textSurface.get_width()+15)
        self.rect.w = width

    def draw(self, screen):
        screen.blit(self.textSurface, (self.rect.x+5, self.rect.y+5))
        pygame.draw.rect(screen, self.color, self.rect, 2)

def button(x,y,width,height,normalColor,hoverColor,text,textsize,function=None,arguments=None):
    global buttonState
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+width > mouse[0] > x and y+height > mouse[1] > y:
        pygame.draw.rect(mainDisplay, hoverColor,(x,y,width,height))

        if click[0] == 1 and arguments != None and not buttonState:
            buttonState = True
            function(arguments)    
        elif click[0] == 1 and arguments == None and not buttonState:
            buttonState = True
            function()
        else:
            buttonState = False
    else:
        pygame.draw.rect(mainDisplay, normalColor,(x,y,width,height))

    font = pygame.font.Font(os.path.join(assets,"Lato-Black.ttf"), textsize)
    textSurface = font.render(text,True,(0,0,0))
    textRect = textSurface.get_rect()
    textRect.center = ( (x+(width/2)), (y+(height/2)) )
    mainDisplay.blit(textSurface, textRect)

# Game
def intro():
    intro = True
    def exitIntro():
        player.name = nameEntry.text
        mainGame()

    nameEntry = textEntry("", 30, displayWidth*0.31, displayHeight*0.80, 480, 50, exitIntro, 25)
    while intro == True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            nameEntry.eventHandler(event)
        
        mainDisplay.fill((255,255,255))
        displayText("You wake up.", 30, (100,0,0), displayWidth*0.5, displayHeight*0.2)
        displayText("You look around, finding that you are in a small, wooden hut. Strangely, you are unable to remember anything about your past.", 20, (0,0,0), displayWidth*0.5, displayHeight*0.3)
        displayText("You don't know how you got here or where you were a few minutes ago, but you do know your goal:", 20, (0,0,0), displayWidth*0.5, displayHeight*0.33)
        displayText("Cultivate.", 30, (0,0,100), displayWidth*0.5, displayHeight*0.4)
        displayText("Amongst your fragmented memories you do find one thing though...", 20, (0,0,0), displayWidth*0.5, displayHeight*0.5)
        displayText("What is your name?", 35, (0,0,0), displayWidth*0.5, displayHeight*0.6)
        nameEntry.update()
        nameEntry.draw(mainDisplay)
        if not len(nameEntry.text) == 0:
            displayText("Press Enter to continue...", 30, (0,0,0), displayWidth*0.5, displayHeight*0.9)
        
        if len(nameEntry.text) >= 25:
            displayText("Your name can only be 25 characters long", 10, (255,0,0), displayWidth*0.5, displayHeight*0.78)

        pygame.display.update()
        clock.tick(30)

def explorationScreen():
    print('hi')

def equipClick(type):
    equipmentScreen(type)

def mainGame():
    main = True
    currentRealmName = None
    qiCycles = 0
    recoveryCycles = 0
        
    while main:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        for obj in objects:
            obj.handler()

        mainDisplay.fill((255,255,255))
        drawPlayer(displayWidth*0.5, displayHeight*0.5)
        displayText(player.name, 40, (0,0,0), displayWidth*0.505, displayHeight*0.25)
        displayText("Qi: " + str(player.qi), 30, (0,0,0), displayWidth * 0.5, displayHeight * 0.8)
        displayText(realms[player.realm], 30, (0,0,0), displayWidth*0.5, displayHeight*0.7)
        pygame.draw.rect(mainDisplay, (0,0,0), [displayWidth * 0.30, displayHeight * 0.34, 76.8, 76.8], 3)
        button(displayWidth*0.3,displayHeight*0.34,76.8,76.8,(255,255,25),(0,100,200),"Head",15,equipClick,"Head")

        pygame.draw.rect(mainDisplay, (0,0,0), [displayWidth * 0.30, displayHeight * 0.44, 76.8, 76.8], 3)
        button(displayWidth*0.3,displayHeight*0.44,76.8,76.8,(255,255,25),(0,100,200),"Body",15,equipClick,"Body")

        pygame.draw.rect(mainDisplay, (0,0,0), [displayWidth * 0.30, displayHeight * 0.54, 76.8, 76.8], 3)
        button(displayWidth*0.3,displayHeight*0.54,76.8,76.8,(255,255,25),(0,100,200),"Boots",15,equipClick,"Legs")

        pygame.draw.rect(mainDisplay, (0,0,0), [displayWidth * 0.65, displayHeight * 0.34, 76.8, 76.8], 3)
        button(displayWidth*0.65,displayHeight*0.34,76.8,76.8,(255,255,25),(0,100,200),"Weapon",15,equipClick,"Weapon")

        pygame.draw.rect(mainDisplay, (0,0,0), [displayWidth * 0.65, displayHeight * 0.44, 76.8, 76.8], 3)
        button(displayWidth*0.65,displayHeight*0.44,76.8,76.8,(255,255,25),(0,100,200),"Accessory",15,equipClick,"Ring")

        pygame.draw.rect(mainDisplay, (0,0,0), [displayWidth * 0.65, displayHeight * 0.54, 76.8, 76.8], 3)
        button(displayWidth*0.65,displayHeight*0.54,76.8,76.8,(255,255,25),(0,100,200),"Accessory",15,equipClick,"Necklace")

        pygame.draw.rect(mainDisplay, (0,0,0), [displayWidth*0.01,displayHeight*0.25,180,360],3)
        displayText("Statistics",25,(0,0,0),90+displayWidth*0.01,displayHeight*0.28)
        displayText("HP: " + str(player.hp) + "/" + str(player.maxHP),15,(0,0,0),90+displayWidth*0.01,displayHeight*0.32)
        displayText("ATK: " + str(player.ATK),15,(0,0,0),90+displayWidth*0.01,displayHeight*0.34)
        displayText("DEF: " + str(player.DEF),15,(0,0,0),90+displayWidth*0.01,displayHeight*0.36)
        displayText("SPD: " + str(player.SPD),15,(0,0,0),90+displayWidth*0.01,displayHeight*0.38)
        displayText("Money: " + str(player.money) + " Taels",15,(0,0,0),90+displayWidth*0.01,displayHeight*0.40)
        displayText("Qi Boost: " + str(player.bonusQiGain) + "%",15,(0,0,0),90+displayWidth*0.01,displayHeight*0.42)

        # Breakthrough/Cultivate Button
        if player.qi < player.btRequirement:
            button(490,displayHeight*0.9,300,76.8,(255,255,25),(0,100,200),"Cultivate",40,player.cultivate)
        else:
            button(490,displayHeight*0.9,300,76.8,(255,255,25),(0,100,200),"Breakthrough",40,player.breakthrough)

        button(980, displayHeight * 0.2, 300, 76.8, (255, 255, 25), (0, 100, 200), "Explore", 40, explorationScreen)

        # Cultivate Qi loop
        if player.cultivating == True and (player.qi <= player.btRequirement) and qiCycles >= 3:
            qiCycles = 0
            player.qi = min(round(player.qi + ((1 + (player.bonusQiGain/100)) * (1 * player.qiMulti)),1),player.btRequirement)

        # Health Recovery Loop
        if player.hp < player.maxHP and recoveryCycles >= 30:
            recoveryCycles = 0
            player.hp = min(round(player.hp + player.maxHP*0.01,1),player.maxHP)

        pygame.display.update()
        clock.tick(30)
        player.updateStats()
        qiCycles = qiCycles + 1
        recoveryCycles = recoveryCycles + 1

def selectEquipment(equipmentOption):
    global selectedEquipment
    selectedEquipment = equipmentOption

selectEquipment("None")

def updateEquipBonusStats(type):
    # Remove previous equipment bonuses
    if player.equipped[type] is not None:
        previousEquipment = player.equipped[type]
        player.bonusHP -= equipmentList.equipment[type][previousEquipment]["bonusHP"]
        player.bonusATK -= equipmentList.equipment[type][previousEquipment]["bonusATK"]
        player.bonusDEF -= equipmentList.equipment[type][previousEquipment]["bonusDEF"]
        player.bonusSPD -= equipmentList.equipment[type][previousEquipment]["bonusSPD"]
        player.bonusQiGain -= equipmentList.equipment[type][previousEquipment]["bonusQiGain"]

        # Add new equip bonuses
    if selectedEquipment is not None:
        player.bonusHP += equipmentList.equipment[type][selectedEquipment]["bonusHP"]
        player.bonusATK += equipmentList.equipment[type][selectedEquipment]["bonusATK"]
        player.bonusDEF += equipmentList.equipment[type][selectedEquipment]["bonusDEF"]
        player.bonusSPD += equipmentList.equipment[type][selectedEquipment]["bonusSPD"]
        player.bonusQiGain += equipmentList.equipment[type][selectedEquipment]["bonusQiGain"] 

def equipSelectedEquipment(type):
    if selectedEquipment is not None:
        print("Equipping:", selectedEquipment)
        updateEquipBonusStats(type)
        player.equipped[type] = selectedEquipment

def equipmentScreen(type):
    equipmentPopup = True
    selectEquipment("None")

    while equipmentPopup:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if displayWidth * 0.9 + 30 > event.pos[0] > displayWidth * 0.9 and displayHeight * 0.1 + 30 > event.pos[1] > displayHeight * 0.1:
                    equipmentPopup = False

        mainDisplay.fill((255, 255, 255))
        displayText(type, 30, (0, 0, 0), displayWidth * 0.5, displayHeight * 0.1)

        equipDrawnY = displayHeight * 0.2
        for gear in player.ownedEquipment[type]:
            button(460, equipDrawnY, 360, 50, (255, 255, 25), (0, 100, 200), gear, 20, selectEquipment, gear)
            equipDrawnY += 60

        if selectedEquipment != "None":
            displayText("Selected: " + selectedEquipment, 20, (0, 0, 0), displayWidth * 0.2, displayHeight * 0.3)
            pygame.draw.rect(mainDisplay,(0,0,0),[displayWidth*0.08,displayHeight*0.25,300,300],3)
            button(displayWidth*0.15, displayHeight * 0.59, 120, 40, (0, 255, 0), (0, 200, 0), "Equip", 20, equipSelectedEquipment,type)
            equipStatsTextY = displayHeight*0.35
            for stat, bonus in equipmentList.equipment[type][selectedEquipment].items():
                if bonus != 0:
                    if stat == "bonusQiGain":
                        displayText("Qi Boost: " + str(bonus) + "%",15,(0,0,0), displayWidth*0.2, equipStatsTextY)
                    else:
                        displayText(stat[5::] + ": " + str(bonus),15,(0,0,0), displayWidth*0.2, equipStatsTextY)
                    equipStatsTextY += 20

        if player.equipped[type] != None:
            displayText("Equipped: " + player.equipped[type], 20, (0, 0, 0), displayWidth * 0.8, displayHeight * 0.3)
            pygame.draw.rect(mainDisplay,(0,0,0),[877.6,displayHeight*0.25,300,300],3)
            equipStatsTextY = displayHeight*0.35
            for stat, bonus in equipmentList.equipment[type][player.equipped[type]].items():
                if bonus != 0:
                    if stat == "bonusQiGain":
                        displayText("Qi Boost: " + str(bonus) + "%",15,(0,0,0), displayWidth*0.8, equipStatsTextY)
                    else:
                        displayText(stat[5::] + ": " + str(bonus),15,(0,0,0), displayWidth*0.8, equipStatsTextY)
                    equipStatsTextY += 20

        # Close button
        pygame.draw.rect(mainDisplay, (255, 0, 0), [displayWidth * 0.9, displayHeight * 0.1, 30, 30])
        pygame.draw.line(mainDisplay, (255, 255, 255), (displayWidth * 0.9, displayHeight * 0.1), (displayWidth * 0.9 + 30, displayHeight * 0.1 + 30), 5)
        pygame.draw.line(mainDisplay, (255, 255, 255), (displayWidth * 0.9, displayHeight * 0.1 + 30), (displayWidth * 0.9 + 30, displayHeight * 0.1), 5)

        pygame.display.update()
        clock.tick(30)
        player.updateStats()

if __name__ == "__main__":
    intro()

pygame.quit()
quit()