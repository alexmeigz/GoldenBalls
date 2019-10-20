#Golden Balls Game (based off of UK TV Series) using print statements

from GoldenBank import GoldenBank
from DistributionPanel import DistributionPanel
from AI import AI
from User import User
from BinOrWinTable import BinOrWinTable
from SplitOrSteal import SplitOrSteal
from TheVote import TheVote
import random

class GoldenBalls:
  def __init__(self):
    self.goldenBank = GoldenBank("goldenballvalues.txt")
    self.distributionPanel = DistributionPanel()
    self.playerLyst = [User("user"), AI("com1"), AI("com2"), AI("com3")]
    self.binOrWinTable = BinOrWinTable()
    self.splitOrSteal = SplitOrSteal()
    self.theVote = TheVote()

  def newGame(self):
    self.goldenBank.reset()
    self.goldenBank.randomize()
    self.distributionPanel.reset()

  def roundOne(self):

    print("Round 1 Started! \n")
    
    #adds 12 balls to the distribution panel and 4 killers
    self.addMoneyBallsToDistPanel(12)
    self.addKillersToDistPanel(4)
    self.distributeToPlayers()
    self.displayToUser()

    eliminated = self.theVote.findMajority(self.getVotes())
    self.eliminate(eliminated)
    
    if eliminated != "user":
      self.roundTwo()
    
  def roundTwo(self):
    
    print("Round 2 Started! \n")

    self.returnToDistPanel()
    self.addMoneyBallsToDistPanel(2)
    self.addKillersToDistPanel(1)
    self.distributeToPlayers()
    self.displayToUser()

    eliminated = self.theVote.findMajority(self.getVotes())
    self.eliminate(eliminated)
    
    if eliminated != "user":
      self.binOrWin()

  def binOrWin(self):
    '''binOrWin phase of the game'''
    print("Bin or Win Started! \n")
    self.returnToDistPanel()
    self.addKillersToDistPanel(1)
    self.binOrWinTable.addBalls(self.distributionPanel.returnBalls())

    #user alternates in picking balls to bin and win
    for i in range(5):
      while True:
        try:
          userinput = int(input("Pick a Golden Ball from 1 to 11 that you HAVE NOT PICKED to BIN: "))
        except:
          print("Please only enter integer values between 1 and 11")
        else:
          binnedVal = self.binOrWinTable.binBall(int(userinput))
          if binnedVal != "-1":
            if binnedVal == "KILLER":
              print("Congratulations! You have binned a KILLER ball!")
            else:
              print("You binned a golden ball with a value of... ", binnedVal)
            break
          else:
            print("Please pick a ball number you haven't picked yet: ")
            print(self.binOrWinTable.getRemainingBalls())
      while True:
        try:
          userinput = int(input("Pick a Golden Ball from 1 to 11 that you HAVE NOT PICKED to WIN: "))
        except:
          print("Please only enter integer values between 1 and 11")
        else:
          winVal = self.binOrWinTable.winBall(int(userinput))
          if winVal != "-1":
            if winVal == "KILLER":
              print("Oh no! You have picked a KILLER ball! Your pot value has been reduced by a factor of 10 :(")
            else:
              print("You added a golden ball with a value of... ", winVal, "to the pot!")
            break
          else:
            print("Please pick a ball number you haven't picked yet: ")
            print(self.binOrWinTable.getRemainingBalls())
    #bin the last ball
    lastBallNum = self.binOrWinTable.getRemainingBalls().strip()
    print("The last ball, ball #", lastBallNum, ", has also been binned: ", sep="")
    binnedVal = self.binOrWinTable.binBall(int(lastBallNum))
    if binnedVal == "KILLER":
      print("Congratulations! You have binned a KILLER ball!")
    else:
      print("You binned a golden ball with a value of... ", binnedVal, "\n")

    print("Your final pot contains... ${:.2f}".format(self.binOrWinTable.getPot()))
    #starts the splitOrSteal round
    self.finalRound()

  def finalRound(self):
    #implement userDecision and comDecision
    while True:
      userDecision = input('''Are you going to SPLIT, STEAL, or COUNTER the \
pot of ${:.2f} with the computer? '''.format(self.binOrWinTable.getPot()))
      
      if userDecision.upper() in "STEAL SPLIT COUNTER":
        break
      else:
        print("Please only enter the phrases \"SPLIT\", \"STEAL\", or \"COUNTER\"")

    #todo: implement trust factor
    comDecision = random.choice(["SPLIT", "STEAL", "COUNTER"])
    print("The computer has decided to...", comDecision)
    
    proportions = self.splitOrSteal.makeDecision(userDecision.upper(), comDecision)

    #todo: edit messages
    print("You have won ${:.2f}!".format(proportions[0] * self.binOrWinTable.getPot()))
    print("The computer has won ${:.2f}!".format(proportions[1] * self.binOrWinTable.getPot()))

  def returnToDistPanel(self):
    '''adds players' balls back to the distribution panel'''
    for player in self.playerLyst:
      for ball in player.returnBalls():
        self.distributionPanel.addBall(ball)

  def distributeToPlayers(self):
    '''randomize and distribute balls to players'''
    self.distributionPanel.randomize()
    self.distributionPanel.distribute(self.playerLyst)
    self.recalculateMultiplier()

  def recalculateMultiplier(self):
    '''recalculates the voting multiplier for AI to use in probability'''
    for player in self.playerLyst:
      player.resetMultiplier()
      #TODO: implement feature to input people's own revelation of their back balls
      player.calculateMultiplier(player.showFrontBalls())

  def addMoneyBallsToDistPanel(self, n):
    '''adds n money balls to distribution panel'''
    for i in range(n):
      self.distributionPanel.addBall(self.goldenBank.generateBall())
      
  def addKillersToDistPanel(self, n):
    '''adds n killer balls to distribution panel'''
    for i in range(n):
      self.distributionPanel.addKiller()

  def displayToUser(self):
    '''displays ALL of user's balls + front 2 of each other player'''
    print("Your Golden Balls are...", self.playerLyst[0].showBalls())
    for player in self.playerLyst[1:]:
        print("The front balls of", player.getName(), "are...", player.showFrontBalls())
    print()
    
  def getPlayerNames(self):
    '''returns string of player names'''
    playerNames = ""
    for player in self.playerLyst[1:]:
      playerNames = playerNames + player.getName() + " "
    return playerNames

  def getUserVote(self):
    '''takes user input and returns their valid vote'''
    playerNames = self.getPlayerNames()
    while True:
      userinput = input("Who do you want vote to eliminate? \n")
      if userinput.lower() in playerNames:
        return userinput.lower()
      else:
        print("Please only input one of the following names: " + playerNames)

  def eliminate(self, eliminated):
    for i in range(len(self.playerLyst)):
      if eliminated == self.playerLyst[i].getName():
        print(self.playerLyst[i].getName(), "has been eliminated!")
        print(self.playerLyst[i].getName() + "'s binned balls are " + str(self.playerLyst[i].showBalls()) + "\n")
        self.playerLyst.pop(i)
        return

  def getVotes(self):
    voteLyst = [self.getUserVote()]
    for i in range(1, len(self.playerLyst[1:])+1):
      compVote = self.playerLyst[i].getVote(self.playerLyst[:i] + self.playerLyst[i+1:])
      print(self.playerLyst[i].getName(), "has voted for", compVote + "!")
      voteLyst.append(compVote)
    print()
    return voteLyst
      
if __name__ == "__main__":
  while True:
    userinput = input("Press 'N' to start a new game! Press 'X' to stop playing...\n")
    if userinput == 'X':
      break
    elif userinput == 'N':
      goldenBallsGame = GoldenBalls()
      goldenBallsGame.newGame()
      goldenBallsGame.roundOne()
  
