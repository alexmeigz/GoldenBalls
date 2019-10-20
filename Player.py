import random

class Player:

  def __init__(self, name):
    #TODO: Implement Trust
    self.trust = random.randrange(1, 101)
    self.name = name
    self.balls = []
    self.voteMultiplier = 1

  def receiveBall(self, ball):
    '''adds to player's balls'''
    self.balls.append(ball)

  def showBalls(self):
    '''reveals player's balls'''
    return self.balls

  def showFrontBalls(self):
    '''reveals player's front 2 balls'''
    return self.balls[:2]

  def returnBalls(self):
    '''returns the players balls and removes them from player's possession'''
    balls = self.balls
    self.balls = []
    return balls
    
  def getName(self):
    '''returns player's name'''
    return self.name

  def resetMultiplier(self):
    '''resets the player's multiplier'''
    self.voteMultiplier = 1

  def calculateMultiplier(self, ballLyst):
    '''recalculates the player's multiplier'''
    for val in ballLyst:
      if val == "KILLER":
        self.voteMultiplier *= 150
      elif int(val) > 10000:
        self.voteMultiplier /= (int(val)/10000)
      elif int(val) <= 100:
        self.voteMultiplier *= (5 + 50/int(val))
      elif int(val) <= 1000:
        self.voteMultiplier *= (1 + 500/int(val))
    self.voteMultiplier = int(round(self.voteMultiplier))

  def getMultiplier(self):
    '''returns the player's multiplier'''
    return self.voteMultiplier
      
  
