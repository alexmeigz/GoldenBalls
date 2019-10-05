#Golden Balls Game (based off of UK TV Series) using print statements
import random
import math
from collections import namedtuple

Player = namedtuple("Player", "name balls trust voteMult")


def newGame():
    global vallyst
    global activePlayers

    print("New Game Started! \n")

    #import ball values and shuffles them
    file = open("goldenballvalues.txt")
    file.readline()
    file.read(12)
    values = file.read()
    vallyst = values.split(", ")
    random.shuffle(vallyst)
    
    #initialize variables
    user = Player("user", [], 0, 1)
    com1 = Player("com1", [], random.randrange(1, 101), 1)
    com2 = Player("com2", [], random.randrange(1, 101), 1)
    com3 = Player("com3", [], random.randrange(1, 101), 1)
    activePlayers = [user, com1, com2, com3]

    #starts round one
    roundOne()
    
def roundOne():
    global vallyst
    global activePlayers

    print("Round 1 Started! \n")
    
    #randomly selects 12 balls from golden bank + 4 killers
    round1balls = ["KILLER", "KILLER", "KILLER", "KILLER"]
    for i in range(12):
        round1balls.append(vallyst.pop())
    random.shuffle(round1balls)

    #distributes among 4 people
    for i in range(4):
        for player in activePlayers:
            player = player._replace(balls=player.balls.append(round1balls.pop()))
    
    #displays ALL of user's balls + front 2 of each other player
    print("Your Golden Balls are...", activePlayers[0].balls)
    for i in range(1, 4):
        print("The front balls of", activePlayers[i].name, "are...", activePlayers[i].balls[:2])

    
    #calculates likeliness of votes based off visible balls
    votePopulation = 0

    for p in range(4):
        activePlayers[p] = activePlayers[p]._replace(voteMult=1)
        
        for i in range(2):
            if activePlayers[p].balls[i] == "KILLER":
                activePlayers[p] = activePlayers[p]._replace(voteMult=(activePlayers[p].voteMult*100))
            elif int(activePlayers[p].balls[i]) > 10000:
                activePlayers[p] = activePlayers[p]._replace(voteMult=activePlayers[p].voteMult/(int(activePlayers[p].balls[i])/10000))
            elif int(activePlayers[p].balls[i]) < 100:
                activePlayers[p] = activePlayers[p]._replace(voteMult=(activePlayers[p].voteMult*5))
            elif int(activePlayers[p].balls[i]) < 1000:
                activePlayers[p] = activePlayers[p]._replace(voteMult=(activePlayers[p].voteMult*2))

        activePlayers[p] = activePlayers[p]._replace(voteMult=int(round(activePlayers[p].voteMult)))
        votePopulation += activePlayers[p].voteMult

    #takes user input as a vote
    votes = {"user":0, "com1":0, "com2":0, "com3":0}
    
    while True:
        userinput = input("\nWho do you want vote to eliminate? com1, com2, or com3?  ")
        if userinput == "com1":
            votes["com1"] = votes.get("com1")+1
            activePlayers[1] = activePlayers[1]._replace(trust=activePlayers[1].trust / 3)
            activePlayers[2] = activePlayers[2]._replace(trust=activePlayers[2].trust * 1.33)
            activePlayers[3] = activePlayers[3]._replace(trust=activePlayers[3].trust * 1.33)
            break
        elif userinput == "com2":
            votes["com2"] = votes.get("com2")+1
            activePlayers[1] = activePlayers[1]._replace(trust=activePlayers[1].trust * 1.33)
            activePlayers[2] = activePlayers[2]._replace(trust=activePlayers[2].trust / 3)
            activePlayers[3] = activePlayers[3]._replace(trust=activePlayers[3].trust * 1.33)
            break
        elif userinput == "com3":
            votes["com3"] = votes.get("com3")+1
            activePlayers[1] = activePlayers[1]._replace(trust=activePlayers[1].trust * 1.33)
            activePlayers[2] = activePlayers[2]._replace(trust=activePlayers[2].trust * 1.33)
            activePlayers[3] = activePlayers[3]._replace(trust=activePlayers[3].trust / 3)
            break
        else:
            print("Please only  input \"com1\", \"com2\", or \"com3\"")
            
    #generates computer votes using probability
    print()
    i = 1
    while i < 4:
        ownCom = "com" + str(i)
        x = random.randrange(votePopulation) + 1
        
        if x <= activePlayers[0].voteMult:
            votes["user"] = votes.get("user")+1
            print(activePlayers[i].name, "has decided to vote for you!")
            i += 1
        elif activePlayers[0].voteMult < x and x <= activePlayers[0].voteMult + activePlayers[1].voteMult and ownCom != "com1":
            votes["com1"] = votes.get("com1")+1
            print(activePlayers[i].name, "has decided to vote for", activePlayers[1].name + "!")
            i += 1
        elif activePlayers[0].voteMult + activePlayers[1].voteMult < x and x <= activePlayers[0].voteMult + activePlayers[1].voteMult + activePlayers[2].voteMult and ownCom != "com2":
            votes["com2"] = votes.get("com2")+1
            print(activePlayers[i].name, "has decided to vote for", activePlayers[2].name + "!")
            i += 1
        elif activePlayers[0].voteMult + activePlayers[1].voteMult + activePlayers[2].voteMult < x and x <= activePlayers[0].voteMult + activePlayers[1].voteMult + activePlayers[2].voteMult + activePlayers[3].voteMult and ownCom != "com3":
            votes["com3"] = votes.get("com3")+1
            print(activePlayers[i].name, "has decided to vote for", activePlayers[3].name + "!")
            i += 1

    #counts votes
    results = list(votes.items())
    mostVotes = []
    highestVoteCount = 0
    for i in range(4):
        if results[i][1] > highestVoteCount:
            highestVoteCount = results[i][1]
            mostVotes = [results[i][0]]
        elif results[i][1] == highestVoteCount:
            mostVotes.append(results[i][0])
    if len(mostVotes) != 1:
        x = random.randrange(len(mostVotes))
        mostVotes = [mostVotes[x]]
    eliminated = mostVotes[0]

    #eliminates player
    if eliminated == "user":
        print("\nOh no! There was a majority vote to eliminate you! You have been eliminated and your golden balls have been binned!")
        elimIndex = 0
    elif eliminated == "com1":
        print("\nComputer 1's binned balls are...", activePlayers[1].balls)
        elimIndex = 1
    elif eliminated == "com2":
        print("\nComputer 2's binned balls are...", activePlayers[2].balls)
        elimIndex = 2
    else:
        print("\nComputer 3's binned balls are...", activePlayers[3].balls)
        elimIndex = 3

    activePlayers.pop(elimIndex)
    
    #starts round two
    if eliminated != "user":
        roundTwo()
        
            
def roundTwo():
    #rerandomizes 3 remaining players' balls
    #adds 2 new balls from golden bank + 1 killer
    #displays ALL of user's balls + front 2 of each other player
    #takes user input to remove 1 player from the game
    global vallyst
    global activePlayers

    print("\nRound 2 Started! \n")
    round2balls = ["KILLER"] + [vallyst.pop()] + [vallyst.pop()]

    for i in range(3):
        round2balls += activePlayers[i].balls
        activePlayers[i] = activePlayers[i]._replace(balls=[])
    random.shuffle(round2balls)

    #distributes among 3 people
    for i in range(5):
        for player in activePlayers:
            player = player._replace(balls=player.balls.append(round2balls.pop()))
    
    #displays ALL of user's balls + front 2 of each other player
    print("Your Golden Balls are...", activePlayers[0].balls)
    for i in range(1, 3):
        print("The front balls of", activePlayers[i].name, "are...", activePlayers[i].balls[:2])
        
    #calculates likeliness of votes based off visible balls
    votePopulation = 0

    for p in range(3):
        activePlayers[p] = activePlayers[p]._replace(voteMult=1)
        
        for i in range(2):
            if activePlayers[p].balls[i] == "KILLER":
                activePlayers[p] = activePlayers[p]._replace(voteMult=(activePlayers[p].voteMult*100))
            elif int(activePlayers[p].balls[i]) > 10000:
                activePlayers[p] = activePlayers[p]._replace(voteMult=activePlayers[p].voteMult/(int(activePlayers[p].balls[i])/10000))
            elif int(activePlayers[p].balls[i]) < 100:
                activePlayers[p] = activePlayers[p]._replace(voteMult=(activePlayers[p].voteMult*5))
            elif int(activePlayers[p].balls[i]) < 1000:
                activePlayers[p] = activePlayers[p]._replace(voteMult=(activePlayers[p].voteMult*2))

        activePlayers[p] = activePlayers[p]._replace(voteMult=int(round(activePlayers[p].voteMult)))
        votePopulation += activePlayers[p].voteMult

    #takes user input as a vote
    votes = {"user":0, "com1":0, "com2":0, "com3":0}
        
    while True:
        userinput = input("\nWho do you want vote to eliminate: " + activePlayers[1].name + " or " + activePlayers[2].name + "? ")
        if userinput == "com1" and activePlayers[1].name == "com1":
            votes["com1"] = votes.get("com1")+1
            activePlayers[1] = activePlayers[1]._replace(trust=activePlayers[1].trust / 5)
            activePlayers[2] = activePlayers[2]._replace(trust=activePlayers[2].trust * 1.5)
            break
        elif userinput == "com2" and activePlayers[1].name == "com2":
            votes["com2"] = votes.get("com2")+1
            activePlayers[1] = activePlayers[1]._replace(trust=activePlayers[1].trust / 5)
            activePlayers[2] = activePlayers[2]._replace(trust=activePlayers[2].trust * 1.5)
            break
        elif userinput == "com2" and activePlayers[2].name == "com2":
            votes["com2"] = votes.get("com2")+1
            activePlayers[1] = activePlayers[1]._replace(trust=activePlayers[1].trust * 1.5)
            activePlayers[2] = activePlayers[2]._replace(trust=activePlayers[2].trust / 5)
            break
        elif userinput == "com3" and activePlayers[2].name == "com3":
            votes["com3"] = votes.get("com3")+1
            activePlayers[1] = activePlayers[1]._replace(trust=activePlayers[1].trust * 1.5)
            activePlayers[2] = activePlayers[2]._replace(trust=activePlayers[2].trust / 5)
            break
        else:
            print("Please only  input \"" + activePlayers[1].name + "\" or \"" + activePlayers[2].name +"\"")

    #generates computer votes using probability
    print()
    
    i = 1
    while i < 3:
        ownCom = activePlayers[i].name
        x = random.randrange(votePopulation) + 1
        
        if x <= activePlayers[0].voteMult:
            votes["user"] = votes.get("user")+1
            print(activePlayers[i].name, "has decided to vote for you!")
            i += 1
        elif activePlayers[0].voteMult < x and x <= activePlayers[0].voteMult + activePlayers[1].voteMult and ownCom != activePlayers[1].name:
            votes[activePlayers[1].name] = votes.get(activePlayers[1].name)+1
            print(activePlayers[i].name, "has decided to vote for", activePlayers[1].name + "!")
            i += 1
        elif activePlayers[0].voteMult + activePlayers[1].voteMult < x and x <= activePlayers[0].voteMult + activePlayers[1].voteMult + activePlayers[2].voteMult and ownCom != activePlayers[2].name:
            votes[activePlayers[2].name] = votes.get(activePlayers[2].name)+1
            print(activePlayers[i].name, "has decided to vote for", activePlayers[2].name + "!")
            i += 1

    #counts votes
    results = list(votes.items())
    mostVotes = []
    highestVoteCount = 0
    for i in range(4):
        if results[i][1] > highestVoteCount:
            highestVoteCount = results[i][1]
            mostVotes = [results[i][0]]
        elif results[i][1] == highestVoteCount:
            mostVotes.append(results[i][0])
    if len(mostVotes) != 1:
        x = random.randrange(len(mostVotes))
        mostVotes = [mostVotes[x]]
    eliminated = mostVotes[0]

    #eliminates player
    if eliminated == "user":
        print("\nOh no! There was a majority vote to eliminate you! You have been eliminated and your golden balls have been binned!")
        elimIndex = 0
    elif eliminated == activePlayers[1].name:
        print("\n" + activePlayers[1].name + "'s binned balls are...", activePlayers[1].balls)
        elimIndex = 1
    else:
        print("\n" + activePlayers[2].name + "'s binned balls are...", activePlayers[2].balls)
        elimIndex = 2

    activePlayers.pop(elimIndex)
    
    #starts binOrWin
    if eliminated != "user":
        binOrWin()
    
def binOrWin():

    #user alternates between binning and picking balls to win
    global pot

    print("\nBin or Win Started! \n")

    #rerandomizes 2 remaining players' balls and adds 1 killer
    round3balls = ["KILLER"]
    for i in range(2):
        round3balls += activePlayers[i].balls
        activePlayers[i] = activePlayers[i]._replace(balls=[])
    random.shuffle(round3balls)

    notPicked = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11"]
    winBalls = 0
    pot = 0
    binTracker = True

    while winBalls != 5:
        if binTracker:
            userinput = input("\nPick a Golden Ball from 1 to 11 that you HAVE NOT PICKED to BIN: ")
            if userinput in notPicked:
                binTracker = False
                notPicked.remove(userinput)
                print("You binned a golden ball with a value of... ", round3balls[int(userinput)-1])
            else:
                print("Please pick a ball that you haven't picked using a numerical value from 1 to 11")
        else:
             userinput = input("\nPick a Golden Ball from 1 to 11 that you HAVE NOT PICKED to WIN: ")
             if userinput in notPicked:
                binTracker = True
                notPicked.remove(userinput)
                winBalls += 1
                if round3balls[int(userinput)-1] == "KILLER":
                    pot /= 10
                    print("Oh no! You have picked a killer! Your pot value has been reduced by a factor of 10 :(")
                else:
                    pot += int(round3balls[int(userinput)-1])
                    print("You added a golden ball with a value of... ", round3balls[int(userinput)-1], "to the pot")
             else:
                print("Please pick a ball that you haven't picked using a numerical value from 1 to 11")            

    print("\nThe last golden ball you have binned has the value of... ", round3balls[int(notPicked[0])-1])
    print("Your final pot contains... $", round(pot, 2))
    splitOrSteal()
    

def splitOrSteal():
    #takes user input split or steal
    #computer makes a decision
    global activePlayers
    global pot

    #calculates computer's chance of splitting vs stealing based on trust and money amount
    potchance = (98.9053 * math.exp(-0.000018554*pot) - 0.174823)
    trustchance = (-112.141 * math.exp(-0.0113712*activePlayers[1].trust) + 111.51) / 100
    chance = int(round(trustchance * potchance))

    #using adjusted trust to determine computer's decision of split or steal
    if random.randrange(100) < chance:
        comDecision = "SPLIT"
    else:
        comDecision = "STEAL"

    outputStr = "Are you going to SPLIT or STEAL the plot of $" + str(pot) + " with the computer? "
    while True:
        userDecision = input(outputStr)
        if userDecision.upper() == comDecision and comDecision == "SPLIT":
            print("\nCongratulations! You and the computer both have split the pot of $", pot, " and you have each won $", round(pot/2, 2), " each!", sep="")
            break
        elif userDecision.upper() == comDecision and comDecision == "STEAL":
            print("\nOh no! You and the computer both have chosen to steal! As such you both walk away with nothing!")
            break
        elif userDecision.upper() == "SPLIT":
            print("\nOh no! You have chosen to split while the computer has chosen to steal! The computer wins the entire pot of $" + str(pot) + ". Better luck next time!")
            break
        elif userDecision.upper() == "STEAL":
            print("\nWow, sneaky! You have chosen to steal while the computer has chosen to split! You win the entire pot of $" + str(pot) + ". Congratulations!")
            break
        else:
            print("Please only input the phrases \"SPLIT\" or \"STEAL\"")

newGame()
