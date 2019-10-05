#Golden Balls Game (based off of UK TV Series) using print statements
import random

def newGame():
    global vallyst
    global trust
    global coms
    global activecoms     

    print("New Game Started! \n")

    #import ball values and shuffles them
    file = open("goldenballvalues.txt")
    file.readline()
    file.read(12)
    values = file.read()
    vallyst = values.split(", ")
    random.shuffle(vallyst)
    
    #initialize variables
    trust = [0, 0, 0]
    coms = [[], [], []]
    activecoms = [1, 2, 3]

    #starts round one
    roundOne()
    
def roundOne():
    global vallyst

    #randomly selects 12 balls from golden bank + 4 killers
    round1balls = ["KILLER", "KILLER", "KILLER", "KILLER"]
    for i in range(12):
        round1balls.append(vallyst.pop())
    random.shuffle(round1balls)
    
    user = []
    com1 = []
    com2 = []
    com3 = []

    #distributes among 4 people
    for i in range(4):
        user.append(round1balls.pop())
        com1.append(round1balls.pop())
        com2.append(round1balls.pop())
        com3.append(round1balls.pop())

    #displays ALL of user's balls + front 2 of each other player
    print("Your Golden Balls are...", user)
    print("The front balls of com1 are...", com1[:2])
    print("The front balls of com2 are...", com2[:2])
    print("The front balls of com3 are...", com3[:2], "\n")

    #calculates likeliness of votes based off visible balls
    userVoteMultiplier = 1
    com1VoteMultiplier = 1
    com2VoteMultiplier = 1
    com3VoteMultiplier = 1
    votes = {"user":0, "com1":0, "com2":0, "com3":0}

    for i in range(2):
        if user[i] == "KILLER":
            userVoteMultiplier *= 100
        elif int(user[i]) > 10000:
            userVoteMultiplier /= (int(user[i])/10000)
        elif int(user[i]) < 100:
            userVoteMultiplier *= 5
        elif int(user[i]) < 1000:
            userVoteMultiplier *= 2
            
        if com1[i] == "KILLER":
            com1VoteMultiplier *= 100
        elif int(com1[i]) > 10000:
            com1VoteMultiplier /= (int(com1[i])/10000)
        elif int(com1[i]) < 100:
            com1VoteMultiplier *= 5
        elif int(com1[i]) < 1000:
            com1VoteMultiplier *= 2
            
        if com2[i] == "KILLER":
            com2VoteMultiplier *= 100
        elif int(com2[i]) > 10000:
            com2VoteMultiplier /= (int(com2[i])/10000)
        elif int(com2[i]) < 100:
            com2VoteMultiplier *= 5
        elif int(com2[i]) < 1000:
            com2VoteMultiplier *= 2
            
        if com3[i] == "KILLER":
            com3VoteMultiplier *= 100
        elif int(com3[i]) > 10000:
            com3VoteMultiplier /= (int(com3[i])/10000)
        elif int(com3[i]) < 100:
            com3VoteMultiplier *= 5
        elif int(com3[i]) < 1000:
            com3VoteMultiplier *= 2

    userVoteMultiplier = int(round(userVoteMultiplier))
    com1VoteMultiplier = int(round(com1VoteMultiplier))
    com2VoteMultiplier = int(round(com2VoteMultiplier))
    com3VoteMultiplier = int(round(com3VoteMultiplier))

    voteProbability = userVoteMultiplier + com1VoteMultiplier + com2VoteMultiplier + com3VoteMultiplier

    #generates computer votes using probability
    i = 1
    while i < 4:
        ownCom = "com" + str(i)
        x = random.randrange(voteProbability) + 1

        if x <= userVoteMultiplier:
            votes["user"] = votes.get("user")+1
            i += 1
        elif userVoteMultiplier < x and x <= userVoteMultiplier + com1VoteMultiplier and ownCom != "com1":
            votes["com1"] = votes.get("com1")+1
            i += 1
        elif userVoteMultiplier + com1VoteMultiplier < x and x <= userVoteMultiplier + com1VoteMultiplier + com2VoteMultiplier and ownCom != "com2":
            votes["com2"] = votes.get("com2")+1
            i += 1
        elif userVoteMultiplier + com1VoteMultiplier + com2VoteMultiplier < x and x <= userVoteMultiplier + com1VoteMultiplier + com2VoteMultiplier + com3VoteMultiplier and ownCom != "com3":
            votes["com3"] = votes.get("com3")+1
            i += 1

    #takes user input as a vote
    while True:
        userinput = input("Who do you want vote to eliminate? com1, com2, or com3?  ")
        if userinput == "com1":
            votes["com1"] = votes.get("com1")+1
            break
        elif userinput == "com2":
            votes["com2"] = votes.get("com2")+1       
            break
        elif userinput == "com3":
            votes["com3"] = votes.get("com3")+1
            break
        else:
            print("Please only  input \"com1\", \"com2\", or \"com3\"")

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
        print("Oh no! There was a majority vote to eliminate you! You have been eliminated and your golden balls have been binned!")
    elif eliminated == "com1":
        print("Computer 1's binned balls are...", com1)
        roundTwo(user, com2, com3)
    elif eliminated == "com2":
        print("Computer 2's binned balls are...", com2)
        roundTwo(user, com1, com3)
    else:
        print("Computer 3's binned balls are...", com3)
        roundTwo(user, com1, com2)
            
def roundTwo(user, comA, comB):
    #rerandomizes 3 remaining players' balls
    #adds 2 new balls from golden bank + 1 killer
    #displays ALL of user's balls + front 2 of each other player
    #takes user input to remove 1 player from the game
    global vallyst
    
    round2balls = user + comA + comB + ["KILLER"] + [vallyst.pop()] + [vallyst.pop()]
    random.shuffle(round2balls)

    user = []
    comA = []
    comB = []

    userVoteMultiplier = 1
    comAVoteMultiplier = 1
    comBVoteMultiplier = 1
    com3VoteMultiplier = 1
    votes = {"user":0, "comA":0, "comB":0}
    
    for i in range(5):
        user.append(round2balls.pop())
        comA.append(round2balls.pop())
        comB.append(round2balls.pop())
        
    print("\nYour Golden Balls are...", user)
    print("The front balls of comA are...", comA[:2])
    print("The front balls of comB are...", comB[:2], "\n")

    for i in range(2):
        if user[i] == "KILLER":
            userVoteMultiplier *= 100
        elif int(user[i]) > 10000:
            userVoteMultiplier /= (int(user[i])/10000)
        elif int(user[i]) < 100:
            userVoteMultiplier *= 5
        elif int(user[i]) < 1000:
            userVoteMultiplier *= 2
            
        if comA[i] == "KILLER":
            comAVoteMultiplier *= 100
        elif int(comA[i]) > 10000:
            comAVoteMultiplier /= (int(comA[i])/10000)
        elif int(comA[i]) < 100:
            comAVoteMultiplier *= 5
        elif int(comA[i]) < 1000:
            comAVoteMultiplier *= 2
            
        if comB[i] == "KILLER":
            comBVoteMultiplier *= 100
        elif int(comB[i]) > 10000:
            comBVoteMultiplier /= (int(comB[i])/10000)
        elif int(comB[i]) < 100:
            comBVoteMultiplier *= 5
        elif int(comB[i]) < 1000:
            comBVoteMultiplier *= 2
            

    userVoteMultiplier = int(round(userVoteMultiplier))
    comAVoteMultiplier = int(round(comAVoteMultiplier))
    comBVoteMultiplier = int(round(comBVoteMultiplier))

    voteProbability = userVoteMultiplier + comAVoteMultiplier + comBVoteMultiplier

    #computer votes - generic probability
    i = 1
    while i < 3:
        ownCom = "com"
        if i == 1:
            ownCom += "A"
        else:
            ownCom += "B"
            
        x = random.randrange(voteProbability) + 1

        if x <= userVoteMultiplier:
            votes["user"] = votes.get("user")+1
            i += 1
        elif userVoteMultiplier < x and x <= userVoteMultiplier + comAVoteMultiplier and ownCom != "comA":
            votes["comA"] = votes.get("comA")+1
            i += 1
        elif ownCom != "comB":
            votes["comB"] = votes.get("comB")+1
            i += 1
    
    while True:
        userinput = input("Who do you want vote to eliminate? comA or comB?  ")
        if userinput == "comA":
            votes["comA"] = votes.get("comA")+1
            break
        elif userinput == "comB":
            votes["comB"] = votes.get("comB")+1
            break
        else:
            print("Please only  input \"comA\" or \"comB\"")    
    

    #vote count
    results = list(votes.items())
    mostVotes = []
    highestVoteCount = 0
    for i in range(3):
        if results[i][1] > highestVoteCount:
            highestVoteCount = results[i][1]
            mostVotes = [results[i][0]]
        elif results[i][1] == highestVoteCount:
            mostVotes.append(results[i][0])
    if len(mostVotes) != 1:
        x = random.randrange(len(mostVotes))
        mostVotes = [mostVotes[x]]
    eliminated = mostVotes[0]

    if eliminated == "user":
        print("Oh no! There was a majority vote to eliminate you! You have been eliminated and your golden balls have been binned!")
    elif eliminated == "comA":
        print("Computer A's binned balls are...", comA)
        binOrWin(user, comB)
    else:
        print("Computer B's binned balls are...", comB)
        binOrWin(user, comA)
        
def binOrWin(user, com):
    #rerandomizes 2 remaining players' balls
    #adds 1 killer
    #user alternates between binning and picking balls to win
    global pot
    round3balls = user + com + ["KILLER"]
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
    print("Your final pot contains... $", round(pot, 2), "\n")
    splitOrSteal()

def splitOrSteal():
    #takes user input split or steal
    #computer makes a decision
    global deceitpoints
    global trustpoints
    
    if random.randrange(2) < 1:
        comDecision = "SPLIT"
    else:
        comDecision = "STEAL"

    outputStr = "Are you going to SPLIT or STEAL the plot of $" + str(pot) + " with the computer? "
    while True:
        userDecision = input(outputStr)
        if userDecision.upper() == comDecision and comDecision == "SPLIT":
            print("Congratulations! You and the computer both have split the pot of $", pot, " and you have each won $", round(pot/2, 2), " each!", sep="")
            break
        elif userDecision.upper() == comDecision and comDecision == "STEAL":
            print("Oh no! You and the computer both have chosen to steal! As such you both walk away with nothing!")
            break
        elif userDecision.upper() == "SPLIT":
            print("Oh no! You have chosen to split while the computer has chosen to steal! The computer wins the entire pot of $" + str(pot) + ". Better luck next time!")
            break
        elif userDecision.upper() == "STEAL":
            print("Wow, sneaky! You have chosen to steal while the computer has chosen to split! You win the entire pot of $" + str(pot) + ". Congratulations!")
            break
        else:
            print("Please only input the phrases \"SPLIT\" or \"STEAL\"")

newGame()
