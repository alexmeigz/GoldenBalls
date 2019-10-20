import random

class TheVote:
    def __init__(self):
        pass

    def findMajority(self, voteLyst):
        '''returns eliminated person based on votes'''
        votes = {}
        highestVotes = []
        highestVoteCount = 0
        for vote in voteLyst:
            votes[vote] = votes.get(vote, 0) + 1
            if votes[vote] > highestVoteCount:
                highestVotes = [vote]
                highestVoteCount = votes[vote]
            elif votes[vote] == highestVoteCount:
                highestVotes.append(vote)
        if len(highestVotes) == 1:
            #non-tie case
            return highestVotes[0]
        else:
            #tie case
            return self.tieBreaker(highestVotes)

    def tieBreaker(self, voteLyst):
        '''in the event of a tie, one of the tied people are randomly eliminated'''
        return random.choice(voteLyst)
  
