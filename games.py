import ipywidgets as widgets
from IPython.display import display
import random
import numpy as np

def computerNextRandom2(humanList, computerList):
    """
    
    Play randomly
    
    """
    a = [x for x in TicTacToeGame.originalList if x not in  (humanList + computerList) ]
    if len(a) == 0:
        return -1
    n = random.choice(a)
    return n

class TicTacToeGame(object):
    
    """
    
    Tic tac toe game.
    
    """
    
    originalList=range(9)
    
    winNumbers=[[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]]
    
    primeList = [2,3,5,7,11,13,17,19,23]
    
    winPrimes = [reduce(lambda x, y: x*y,[primeList[x] for x in w],1) for w in winNumbers]

    
    def __init__(self, computerSymbol="O", humanSymbol="X",computerNext=None):
        
        self.humanList=[]
        self.computerList=[]
        
        self.computerSymbol = computerSymbol
        self.humanSymbol = humanSymbol
 
        self.buttons = [
            widgets.Button(
                description="", 
                height='7em',
                font_size=20,
                disabled= False
            ) for i in range(9)]
        
        for i, b in enumerate(self.buttons):
            b.on_click(self.buttonProg(i))
        
        
        self.startButton = widgets.Button(
            description='Reset_Human_First',
            width=50, 
            height='3em')
        
        self.startButton.on_click(self.startProg)

        if computerNext is not None :
            self.computerNext = computerNext
        else:
            self.computerNext = self.computerNextRandom
        
        self.computerFirstButton = widgets.Button(
            description='Reset_Computer_First',
            width=50, 
            height='3em')
        
        self.computerFirstButton.on_click(self.startComputerFisrt)
        
    def info(self):
        print "Human symbol {}\nComoputer symbol {}".format(humanSymbol,computerSymbol)
        
    def buttonProg(self, n):
        
        """
        
        response to button click.
        
        """
    
        def f(b):
            # print n
            self.humanList.append(n)
            self.buttons[n].description="X"
            self.buttons[n].disabled = True
            if self.isWining(self.humanList):
                print "human wins"
                self.disableAll()
                return 
            a = self.computerNext(self.humanList, self.computerList)
            self.buttons[a].description="O"
            self.buttons[a].disabled = True
            self.computerList.append(a)
            if self.isWining(self.computerList):
                print "computer wins"
                self.disableAll()
                return
            if len(self.humanList + self.computerList) == 9:
                print "tie"
                return
            #print b
        return f
    
    
    def isWining(self, L):
        
        if len(L) < 3:
            return False
        
        p = reduce(lambda x, y: x*y,[TicTacToeGame.primeList[x] for x in L],1)
        
        if 0 in [p % w for w in TicTacToeGame.winPrimes ]:
            return True
        else:
            return False
   
    def disableAll(self):
        for b in self.buttons:
            b.disabled = True
            
    def computerNextRandom(self, humanList, computerList ):
        a = [x for x in TicTacToeGame.originalList if x not in  (self.humanList + self.computerList) ]
        if len(a) == 0:
            return -1
        n = random.choice(a)
        return n
    
    def showBoard(self):
        r1 = widgets.HBox(children=self.buttons[:3])
        r2 = widgets.HBox(children=self.buttons[3:6])
        r3 = widgets.HBox(children=self.buttons[6:9])
        r4 = widgets.HBox(children=[self.startButton, self.computerFirstButton])
        display(widgets.VBox(children=[r1,r2,r3,r4]))
    
    def startProg(self,b):
        self.resetAll()
   
    def startComputerFisrt(self,b):
        
        self.resetAll()
        a = self.computerNext(self.humanList, self.computerList)
        self.buttons[a].description="O"
        self.buttons[a].disabled = True
        self.computerList.append(a)
        
        
    def resetAll(self):

        self.humanList=[]
        self.computerList=[]
        for b in self.buttons:
            b.description = ""
            b.disabled= False
    

class tttAuto (TicTacToeGame):
    
    """
    
    for auto play and data generating.
    
    """
    
    def __init__(self, simulator_0 = None, simulator_1 = None):
        
        #TODO test simulator is valid
        TicTacToeGame.__init__(self)
        
        self.simulator_0 = simulator_0 if simulator_0 else self.computerNextRandom
        self.simulator_1 = simulator_1 if simulator_1 else self.computerNextRandom
        
        self.result = None
        self.data = []
        
    def simulation(self):
        
        self.reset()
        
        while not self.result:
            
            n0 = self.simulator_0(self.humanList,self.computerList)
            self.humanList.append(n0)
            self.data.append(n0)
            if self.isWining(self.humanList):
                self.data.append('0_win')
                self.result = 0
                break
                
            if len(self.humanList + self.computerList) == 9:
                self.data.append('tie')
                self.result = -1
                break                
            
            n1 = self.simulator_1(self.humanList,self.computerList)
            self.computerList.append(n1)
            self.data.append(n1)
            if self.isWining(self.computerList):
                self.data.append('1_win')
                self.result = 1
                break
            
            if len(self.humanList + self.computerList) == 9:
                self.data.append('tie')
                self.result = -1
                break
                
    def reset(self):
        self.result = None
        self.data = []
        self.humanList=[]
        self.computerList=[]   


    