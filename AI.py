from Player import Player
import random

class AI(Player):
  def __init__(self, name):
    super().__init__(name)

  def getVote(self, playerLyst):
    '''returns the AI's generated vote'''      
    votePopulation = 0
    
    for player in playerLyst:
      votePopulation += player.getMultiplier()

    v = random.randrange(votePopulation) + 1

    if v <= playerLyst[0].getMultiplier():
      return playerLyst[0].getName()
    elif playerLyst[0].getMultiplier() < v and v <= playerLyst[0].getMultiplier() + playerLyst[1].getMultiplier():
      return playerLyst[1].getName()
    else:
      return playerLyst[2].getName()
