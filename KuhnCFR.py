from KuhnPoker import *
from treelib import Node, Tree
from CfrNode import CfrNode
from GameTree import GameTree

class CFRtrainer:
    def __init__(self):
        self.playerOneTree = GameTree()
        self.playerTwoTree = GameTree()
        self.kuhn = KuhnPoker()

    def HasChild(self, parentId, childTag, tree):
        if(self.GetChildByTag(parentId, childTag, tree)):
            return True

        return False

    def GetChildByTag(self, parentId, childTag, tree):
        for childId in  tree.children(parentId):
            childNode = tree[childId]
            if(childNode.tag == childTag):
                return childNode

        return None

    def CFR(self, p0, p1):
        curPlayer = self.kuhn.GetCurrentPlayer()
        curPlayerProb = p0 if curPlayer == Players.one else p1
        tree = self.playerOneTree if curPlayer == Players.one else self.playerTwoTree

        if(self.kuhn.IsTerminateState()):
            return self.kuhn.GetPayoff(curPlayer)

        # lastMove = self.kuhn.infoSet[self.currentMoveId - 2]
        #
        # if(lastMove >= 0):

        # card = self.kuhn.GetPlayerCard(curPlayer)
        #
        # infoset = str(card) + " | " + str(self.kuhn.infoSet)
        #
        # if(previousInfoset not in tree):
        #     previousInfoset = 'root'


        # lastNodeId = self.playerOneLastNode if curPlayer == Players.one else self.playerTwoLastNode
        # lastMoveId = self.kuhn.currentMoveId - 1
        #
        # if(lastMoveId < 0):
        #     nodeId = lastNodeId
        # else:
        #     lastMove = self.kuhn.infoSet[lastMoveId]
        #
        #     if(self.HasChild(lastNodeId, lastMove, tree)):
        #         nodeId = self.GetChildByTag(lastNodeId, lastMove, tree).identifier
        #     else:
        #         nodeId = tree.create_node(tag=lastMove, data=CfrNode(), parent=lastNodeId).identifier
        #
        #     if(curPlayer == Players.one):
        #         self.playerOneLastNode = nodeId
        #     else:
        #         self.playerTwoLastNode = nodeId

        # infoset = self.kuhn.GetInfoset(curPlayer)
        #
        # if (infoset in tree):
        #     gameNode = tree[infoset]
        # else:
        #     gameNode = tree.AddCFRNode(infoset, self.kuhn, curPlayer)
            #node = tree.create_node(tag=lastMove, data=CfrNode(), parent=lastNodeId).identifier

        # cfrNode = gameNode.data
        #'2 | [0 0 0]'

        cfrNode = tree.GetOrCreateCFRNode(self.kuhn, curPlayer)
        strategy = cfrNode.GetStrategy(curPlayerProb)
        util = [0.0] * NUM_ACTIONS
        nodeUtil = 0

        for action in range(NUM_ACTIONS):
            infosetBackup = self.kuhn.SaveInfoSet()
            curMove = Moves(MovesToOneHot[action + 1])
            self.kuhn.MakeMove(curMove)

            if(curPlayer == Players.one):
                util[action] = -self.CFR(p0 * strategy[action], p1)
            else:
                util[action] = -self.CFR(p0, p1 * strategy[action])

            nodeUtil += strategy[action] * util[action]

            self.kuhn.RestoreInfoSet(infosetBackup)

        for action in range(NUM_ACTIONS):
            regret = util[action] - nodeUtil
            opProb = p1 if curPlayer == Players.one else p0
            cfrNode.regretSum[action] += opProb * regret
            if(cfrNode.infoset == '2 | [0 0 0]'):
                print(cfrNode.infoset)

        return nodeUtil

    def Train(self):
        util = 0
        cnt = 0

        # self.playerOneTree.GetOrCreateCFRNode(self.kuhn, Players.one)
        # self.playerTwoTree.GetOrCreateCFRNode(self.kuhn, Players.one)

        # while (self.kuhn.NewRound() != 1):
        #     util += self.CFR(1, 1)
        #     cnt += 1
        #     if(cnt % 10 == 0):
        #         print(util / cnt)

        for i in range(500):
            self.kuhn.NewRound()
            util += self.CFR(1, 1)
            cnt += 1
            if(cnt % 10 == 0):
                print(util / cnt)


trainer = CFRtrainer()
for i in range(1):
    trainer.Train()

print("Player one avg strategy:")
trainer.playerOneTree.PrintAvgStrategy()
print("Player one best resp strategy:")
trainer.playerOneTree.PrintBestResp()

print("----------------------")
print("Player two avg strategy:")
trainer.playerTwoTree.PrintAvgStrategy()
print("Player two best resp strategy:")
trainer.playerTwoTree.PrintBestResp()



print("done")

