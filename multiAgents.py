# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

import math
from game import Agent
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState: GameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"

        currentFoodList=newFood.asList()
        newScore=successorGameState.getScore()

        tempGhostDistancesList=[]
        for i in newGhostStates:
            tempGhostPos=i.getPosition()
            tempManhattan=manhattanDistance(newPos,tempGhostPos)
            tempGhostDistancesList.append(tempManhattan)

        #if  newGhostStates:
        #    newScore=newScore +min(tempGhostDistancesList)

        tempFoodDistancesList = []
        for i in currentFoodList:
            tempManhattan = manhattanDistance(newPos, i)
            tempFoodDistancesList.append(tempManhattan)

        if tempFoodDistancesList:
             newScore+= (min(tempGhostDistancesList)-1)/(min(tempFoodDistancesList)+1)

        return newScore

def scoreEvaluationFunction(currentGameState: GameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState: GameState):


        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"

        def performingMinimax(self, gameState, agentIndex, depth):

            if gameState.isWin() or gameState.isLose() or depth == self.depth or gameState.getLegalActions(agentIndex) == 0:
                return self.evaluationFunction(gameState),None

            v = -math.inf
            if agentIndex==0:
                for i in gameState.getLegalActions(agentIndex):

                    newIndex = (agentIndex + 1) % gameState.getNumAgents()
                    tempValue, tempMove = performingMinimax(self, gameState.generateSuccessor(agentIndex, i), newIndex, depth)

                    if tempValue > v:
                        v, maxing = tempValue, i

                if v != -math.inf:
                    return v, maxing

            v = math.inf
            if agentIndex!=0:
                for i in gameState.getLegalActions(agentIndex):
                    if (((agentIndex + 1) % gameState.getNumAgents()) == 0):

                        newIndex = (agentIndex + 1) % gameState.getNumAgents()
                        tempValue, tempMove = performingMinimax(self, gameState.generateSuccessor(agentIndex, i), newIndex, depth+1)
                    else:
                        newIndex = (agentIndex + 1) % gameState.getNumAgents()
                        tempValue, tempMove = performingMinimax(self, gameState.generateSuccessor(agentIndex, i), newIndex, depth)

                    if tempValue < v:
                        v, mining = tempValue, i

                if v != math.inf:
                    return v, mining

        return performingMinimax(self,gameState,0,0)[1]

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def performinAlphaBeta(self, gameState, agentIndex, depth,Alpha,Beta):

            if gameState.isWin() or gameState.isLose() or depth == self.depth or gameState.getLegalActions(agentIndex) == 0:
                return self.evaluationFunction(gameState),None

            v = -math.inf
            if agentIndex==0:

                for i in gameState.getLegalActions(agentIndex):

                    newIndex = (agentIndex + 1) % gameState.getNumAgents()
                    tempValue, tempMove = performinAlphaBeta(self, gameState.generateSuccessor(agentIndex, i), newIndex, depth,Alpha,Beta)

                    if tempValue > v:
                        v, maxing = tempValue, i

                    if v>Beta:
                        return v,maxing
                    Alpha=max(Alpha,v)


                if v != -math.inf:
                    return v, maxing

            v = math.inf
            if agentIndex!=0:
                for i in gameState.getLegalActions(agentIndex):
                    if (((agentIndex + 1) % gameState.getNumAgents()) == 0):

                        newIndex = (agentIndex + 1) % gameState.getNumAgents()
                        tempValue, tempMove = performinAlphaBeta(self, gameState.generateSuccessor(agentIndex, i), newIndex, depth + 1,Alpha,Beta)
                    else:
                        newIndex = (agentIndex + 1) % gameState.getNumAgents()
                        tempValue, tempMove = performinAlphaBeta(self, gameState.generateSuccessor(agentIndex, i), newIndex, depth, Alpha, Beta)

                    if tempValue < v:
                        v, mining = tempValue, i

                    if v<Alpha:
                        return v,mining
                    Beta=min(Beta,v)

                if v != math.inf:
                    return v, mining

        return performinAlphaBeta(self,gameState,0,0,Alpha=-math.inf,Beta=math.inf)[1]

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"

        def performingExpectimax(self, gameState, agentIndex, depth):

            if gameState.isWin() or gameState.isLose() or depth == self.depth or gameState.getLegalActions(agentIndex) == 0:
                return self.evaluationFunction(gameState),None

            v = -math.inf
            if agentIndex==0:
                for i in gameState.getLegalActions(agentIndex):

                    newIndex = (agentIndex + 1) % gameState.getNumAgents()
                    tempValue, tempMove = performingExpectimax(self, gameState.generateSuccessor(agentIndex, i), newIndex, depth)

                    if tempValue > v:
                        v, maxing = tempValue, i

                if v != -math.inf:
                    return v, maxing

            v = math.inf
            if agentIndex!=0:

                listingWeightedPossibilities=[]

                for i in gameState.getLegalActions(agentIndex):
                    if (((agentIndex + 1) % gameState.getNumAgents()) == 0):

                        newIndex = (agentIndex + 1) % gameState.getNumAgents()
                        tempValue, tempMove = performingExpectimax(self, gameState.generateSuccessor(agentIndex, i), newIndex, depth+1)
                    else:
                        newIndex = (agentIndex + 1) % gameState.getNumAgents()
                        tempValue, tempMove = performingExpectimax(self, gameState.generateSuccessor(agentIndex, i), newIndex, depth)

                    listingWeightedPossibilities.append(tempValue*(1/len(gameState.getLegalActions(agentIndex))))

                expectedValue=0
                for i in listingWeightedPossibilities:
                    expectedValue+=i

                return expectedValue,None

        return performingExpectimax(self, gameState, 0, 0)[1]

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>

    It basically evaluates current pacman's position, closest food position, closest ghost position and current scared ghost positions.
    In order to obtain feasible score, i tried to manipulate these variables in some sense.

    Firstly, its adding more or less score corresponding to distance between closest food position and pacman's position.
    Secondly, its adding much much more score corresponding to distance between scared ghosts position and pacman's position.
    And lastly, its substracting more or less score corresponding to distance between closest ghost position and pacman's position.
    Distances are all take a seat on denominator because in every situation when its close it gain or lose more score and in the reverse sense also.
    All these distances are multiplying with weights and become useful scores.
    """
    "*** YOUR CODE HERE ***"
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newScore = currentGameState.getScore()
    treshold = 5

    currentFoodList = newFood.asList()
    tempFoodDistancesList = []

    for i in currentFoodList:
        tempManhattan = manhattanDistance(newPos, i)
        tempFoodDistancesList.append(tempManhattan)

    if tempFoodDistancesList != []:
        closestfoodDistance=min(tempFoodDistancesList)
        if tempFoodDistancesList != None:
            newScore += treshold / closestfoodDistance  # Adding weighted closestfooddistance, get close get more score

    tempGhostDistancesList = []
    for i in newGhostStates:
        if i.scaredTimer>0 and manhattanDistance(newPos, i.getPosition())!=0:
            tempGhostPos = i.getPosition()
            tempManhattan = manhattanDistance(newPos, tempGhostPos)
            newScore += ((treshold) ** 2) / tempManhattan # Adding weighted closestScaredGhostDistance, get close get more score BUT WITH INCREASED WEIGHT
        else:
            tempGhostPos = i.getPosition()
            tempManhattan = manhattanDistance(newPos, tempGhostPos)
            tempGhostDistancesList.append(tempManhattan)

    if tempGhostDistancesList!=[]:
        closestGhostDistance=min(tempGhostDistancesList)
        if closestGhostDistance>0:
            newScore -= treshold / closestGhostDistance # Substract weighted closestghostdistance, get close get less score

    return newScore

    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
