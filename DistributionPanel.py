import random

class DistributionPanel:
  def __init__(self):
    '''0 argument constructor'''
    self.value_lyst = []

  def randomize(self):
    '''randomizes the golden bank'''
    random.shuffle(self.value_lyst)

  def generateBall(self):
    '''generates a ball from the distribution panel'''
    return self.value_lyst.pop()

  def returnBalls(self):
    '''returns all balls in the distribution panel'''
    balls = self.value_lyst
    self.value_lyst = []
    return balls
    
  def addBall(self, ball):
    '''adds a ball back to the distribution panel'''
    self.value_lyst.append(ball)

  def addKiller(self):
    '''adds a killer ball'''
    self.addBall("KILLER")

  def checkEmpty(self):
    '''returns True if there are no balls in the distribution panel'''
    return len(self.value_lyst) == 0

  def reset(self):
    '''clears the distribution panel of all balls'''
    self.value_lyst = []

  def distribute(self, playerLyst):
    '''distributes balls evenly to the players in the lyst'''
    while(self.value_lyst != []):
      for player in playerLyst:
        player.receiveBall(self.value_lyst.pop())

    
    
