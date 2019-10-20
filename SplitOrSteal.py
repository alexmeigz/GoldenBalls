class SplitOrSteal:
    def __init__(self):
        pass

    def makeDecision(self, user, com):
        '''returns a list of proportions each player wins from the pot
        based on their decisions; index 0 = user; index 1 = computer'''
        if user == "SPLIT":
            if com == "SPLIT":
                return [0.5, 0.5]
            elif com == "STEAL":
                return [0, 1]
            elif com == "COUNTER":
                return [1, 0]
        elif user == "STEAL":
            if com == "SPLIT":
                return [1, 0]
            elif com == "STEAL":
                return [0, 0]
            elif com == "COUNTER":
                return [0, 1]
        elif user == "COUNTER":
            if com == "SPLIT":
                return [0, 1]
            elif com == "STEAL":
                return [1, 0]
            elif com == "COUNTER":
                return [0.25, 0.25]
        return -1
