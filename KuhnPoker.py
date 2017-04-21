from enum import Enum
from queue import *
import numpy as np
import itertools

class Players(Enum):
    one = 1
    two = 2

class Moves(Enum):
    uplayed = 0
    pas = 1
    bet = 11

#list(map(int, Color))
MovesToOneHot = {0: 0, 1: 1, 2: 11}
CardsToOneHot = {1: 0, 2: 1, 3: 11}


NUM_ACTIONS = 2

class Results(Enum):
    toHighCard = 0
    toPlayer1 = 1
    toPlayer2 = 2

CARDS = [1, 2, 3]

def NextPlayer(currentPlayer):
    if(currentPlayer == Players.one):
        return Players.two

    return Players.one

class KuhnPoker:
    @staticmethod
    def JoinMoves(moves):
        res = np.array_str(moves)
        return res

    @staticmethod
    def GetInfoSet(moves):
        infoSet = KuhnPoker.JoinMoves(moves)
        return infoSet

    def AddToPayoffTable(self, result, moves):
        infoSet = KuhnPoker.GetInfoSet(np.array([move.value for move in moves]))
        self.payoffTable[infoSet] = result

    def InitPayoffTable(self):
        self.AddToPayoffTable([Results.toHighCard, 1], [Moves.pas, Moves.pas, Moves.uplayed])
        self.AddToPayoffTable([Results.toPlayer2, 1],  [Moves.pas, Moves.bet, Moves.pas])
        self.AddToPayoffTable([Results.toHighCard, 2], [Moves.pas, Moves.bet, Moves.bet])
        self.AddToPayoffTable([Results.toPlayer1, 1],  [Moves.bet, Moves.pas, Moves.uplayed])
        self.AddToPayoffTable([Results.toHighCard, 2], [Moves.bet, Moves.bet, Moves.uplayed])

    def InitInfoSet(self):
        self.infoSet =  np.array([Moves.uplayed.value, Moves.uplayed.value, Moves.uplayed.value])
        self.currentMoveId = 0

    def __init__(self):
        self.PayoffCount = 0
        self.payoffTable = {}
        self.InitPayoffTable()
        self.InitInfoSet()

        self.cardsPermutations = []
        for deck in itertools.permutations(CARDS):
            self.cardsPermutations.append(deck)

        self.permutationIndex = 0
        self.cards = None

    # def GetFullInfoSet(self, player):
    #     card = self.GetPlayerCard(player)
    #     for i in range(self.C)
    #
    # def GetPrettyInfoset(self):
    #     target = self.infoSet
    #     for action in Moves:
    #         target = target.replace(action.value, action)
    #
    #     return target

    def _getInfoset(self, infoset, curPlayer):
        card = self.GetPlayerCard(curPlayer)
        infosetString = str(card) + " | " + str(infoset)
        return infosetString


    def GetInfoset(self, curPlayer):
        return self._getInfoset(self.infoSet, curPlayer)

    def GetPrettyLastMove(self, curPlayer):
        if(self.currentMoveId == 0 and curPlayer == Players.one):
            return str(self.GetPlayerCard(curPlayer))

        lastMove = self.infoSet[self.currentMoveId - 1]
        return str(Moves(lastMove).name)

    def PrintInfoset(self):
        infoset = Moves(self.infoSet[0]).name + ";" + Moves(self.infoSet[1]).name + ";" + Moves(self.infoSet[2]).name
        return infoset

    def GetPrevInfoset(self, curPlayer):
        if(cself.ards)

        prevInfoset = self.infoSet.copy()

        if(self.currentMoveId == 0):
            return str(self.GetPlayerCard(curPlayer))

        if(self.currentMoveId >= 1):
            prevInfoset[0] = Moves.uplayed.value

        if (self.currentMoveId == 2):
            prevInfoset[1] = Moves.uplayed.value

        return self._getInfoset(prevInfoset, curPlayer)

    def GetPlayerCard(self, player):
        if (player == Players.one):
            return self.cards[0]
        else:
            return self.cards[1]

    def SaveInfoSet(self):
        infosetBackup = self.infoSet.copy()
        pokerEngineMoveId = self.currentMoveId
        return infosetBackup, pokerEngineMoveId

    def RestoreInfoSet(self, backupTuple):
        self.infoSet = backupTuple[0].copy()
        self.currentMoveId = backupTuple[1]

    def GetPlayerOneCard(self):
        return self.cards[0]

    def GetCurrentPlayer(self):
        playerId = (self.currentMoveId % 2) + 1
        return Players(playerId)

    def GetPlayerTwoCard(self):
        return self.cards[1]

    def IsTerminateState(self):
        return self.GetStringInfoset() in self.payoffTable

    def GetStringInfoset(self):
        return np.array_str(self.infoSet)

    def GetPayoff(self, player):
        self.PayoffCount += 1

        cardOne = self.GetPlayerOneCard()
        cardTwo = self.GetPlayerTwoCard()

        if(cardOne == cardTwo):
            raise ValueError("The same cards")

        result = self.payoffTable[self.GetStringInfoset()]

        winner = result[0]
        reward = result[1]

        if(player == Players.two):
            reward = reward * (-1);

        if(winner == Results.toPlayer1):
            return reward
        elif(winner == Results.toPlayer2):
            return -reward
        else:
            if(cardOne > cardTwo):
                return reward
            else:
                return -reward

    def _nexDeck(self):
        for deck in itertools.permutations(CARDS):
            yield deck

    def NewRound(self):
        retValue = 0


        # if(self.permutationIndex >= len(self.cardsPermutations)):
        #     self.permutationIndex = 0
        #     retValue = 1
        #
        # self.cards = self.cardsPermutations[self.permutationIndex]
        # self.permutationIndex += 1
        self.cards = self.cardsPermutations[len(self.cardsPermutations) - 1] #ToDO: REMOVE!!!!!! Temp!!!!!!
        self.InitInfoSet()
        return retValue


    def MakeMove(self, move):
        self.MakeOneHotMove(move.value)

    def MakeOneHotMove(self, adHocMove):
        if(self.currentMoveId >= len(self.infoSet)):
            ValueError("To much moves!")

        self.infoSet[self.currentMoveId] = adHocMove
        self.currentMoveId += 1



