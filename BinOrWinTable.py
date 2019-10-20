import random

class BinOrWinTable:
    #balls: dictionary of tuples with key as ball number
    balls = {}
    pot = 0

    def __init__(self):
        pass

    def addBalls(self, valLyst):
       '''adds balls to the table'''
       assert(len(valLyst) == 11), "ERROR: Must input exactly 11 Ball Values"
       random.shuffle(valLyst)
       for i in range(11):
           self.balls[i+1] = valLyst[i]

    def getRemainingBalls(self):
      '''returns unchosen ball numbers in a string'''
      returnStr = ""
      for element in list(self.balls.keys()):
          returnStr = returnStr + str(element) + " "
      return returnStr

    def binBall(self, n):
      '''returns (str) value of binned ball; -1 if unsuccessful'''
      return self.balls.pop(n, "-1")

    def winBall(self, n):
      '''returns (str) value of win ball; -1 if unsuccessful'''
      val = self.balls.pop(n, "-1")
      if val != "-1":
        if val == "KILLER":
            self.pot /= 10
        else:
            self.pot += int(val)
      return val
     
    def getPot(self):
      '''returns the pot (float) value'''
      return self.pot

    
        
    
