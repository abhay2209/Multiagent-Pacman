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

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
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

    def evaluationFunction(self, currentGameState, action):
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
        #print(successorGameState)
        newPos = successorGameState.getPacmanPosition()
        #print(newPos)
        newFood = successorGameState.getFood()
        #print(newFood)
        newGhostStates = successorGameState.getGhostStates()
        #print(newGhostStates)
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        
        "*** YOUR CODE HERE ***"
        totalScore=successorGameState.getScore()
        # Higher score if food is close

        #Had to use asList, to get a list of food locations, so i can carry my operations in a loop
        foodLocation=newFood.asList()
        for each in foodLocation:
          #distance of x+y from each food loaction to newPos
		      foodDistance = util.manhattanDistance(each,newPos)
          #if not zero, 1/dis is larger if distacne is less, that means higher score
		      if foodDistance!=0:
        		totalScore=totalScore+(1.0/foodDistance)
        #same logic goes for ghosts but we need to maintain a least difference of 1.
        for ghost in newGhostStates:
		      ghostPos=ghost.getPosition()
		      ghostDistance = util.manhattanDistance(ghostPos,newPos)
		      if ghostDistance>1:	
			      totalScore=totalScore+(1.0/ghostDistance)
        return totalScore
		
	
	      


def scoreEvaluationFunction(currentGameState):
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

    def getAction(self, gameState):
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
        """
        "*** YOUR CODE HERE ***"
        def minimax(agent, depth, gameState):
            #return if we win or lose and check for depth
            if gameState.isWin() or gameState.isLose() or depth == self.depth: 
                return self.evaluationFunction(gameState)
            #as agent =0 is pacman, we maximize for it.    
            if agent == 0:  
                #I set the agent to 1 which are the ghosts 
                return max(minimax(1, depth, gameState.generateSuccessor(agent, nextState)) for nextState in gameState.getLegalActions(agent))
            #And we will minimize it for the ghosts
            else:  
                #We check if we have add all for all the ghosts at that depth
                totalAgent = agent + 1  
                if gameState.getNumAgents() == totalAgent:
                    totalAgent = 0 # setting it back for pacman when we have checked for all the ghosts
                    depth+=1
                #This continues until we have all ghosts calculated for and that is when I increase the depth
                return min(minimax(totalAgent, depth, gameState.generateSuccessor(agent, nextState)) for nextState in gameState.getLegalActions(agent))

        #Now we calculate it for our agent at depth 0 for maximum, after we start from the least value possible.
        maximum = float("-inf")
        for State in gameState.getLegalActions(0):
            utility = minimax(1, 0, gameState.generateSuccessor(0, State))
            if utility > maximum:
                maximum = utility
                actionState = State

        return actionState
       

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        return self.alphaBetaPruner(gameState, 0, 0, float("-inf"),float("inf"))

    def alphaBetaPruner (self, gameState, agentIndex, depth, alpha, beta):

        if agentIndex >= gameState.getNumAgents():
            agentIndex = 0
            depth += 1

        if gameState.isWin() or gameState.isLose() or depth == self.depth:
            return self.evaluationFunction(gameState)

        if agentIndex == self.index:
            return self.max_value(gameState, agentIndex, depth, alpha, beta)
        else:
            return self.min_value(gameState, agentIndex, depth, alpha, beta)

        

    def max_value(self, gameState, agentIndex, depth, alpha, beta):
      #Initialize v as -infinity
      v = float("-inf")
      #calculating legal actions to get successor state
      for legalActions in gameState.getLegalActions(agentIndex):
        if legalActions == Directions.STOP:
          continue
        #Getting successor states
        successorState = gameState.generateSuccessor(agentIndex, legalActions)
        current = self.alphaBetaPruner(successorState, agentIndex+1, depth, alpha, beta)
        #v=max value
        if current > v:
          v = current
          actionValue = legalActions
        #As from piaza we keep looping around until we ind a value more than a particular beta or we run out of succesor states
        if v > beta:
          return v

        alpha = max(alpha, v)

      if depth == 0:
        return actionValue
      else:
        return v

    def min_value(self, gameState, agentIndex, depth, alpha, beta):
       #Initialize v as +infinity
      v = float("inf")
      #calculating legal actions to get successor state
      for legalActions in gameState.getLegalActions(agentIndex):
        if legalActions == Directions.STOP:
          continue
        #Getting successor states
        successorState = gameState.generateSuccessor(agentIndex, legalActions)
        current = self.alphaBetaPruner(successorState, agentIndex+1, depth, alpha, beta)
        #v=min value
        if current < v:
          v = current
          actionValue = legalActions
        #As from piaza we keep looping around until we ind a value less than a particular alpha or we run out of succesor states
        if v < alpha:
          return v
        beta = min (beta,v)
      return v


  
      

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        def expectimax(agent, depth, gameState):
            #return if we win or lose and check for depth
            if gameState.isWin() or gameState.isLose() or depth == self.depth: 
                return self.evaluationFunction(gameState)
            #as agent =0 is pacman, we maximize for it.    
            if agent == 0:  
                #I set the agent to 1 which are the ghosts 
                return max(expectimax(1, depth, gameState.generateSuccessor(agent, nextState)) for nextState in gameState.getLegalActions(agent))
            #And we will minimize it for the ghosts
            else:  
                #We check if we have add all for all the ghosts at that depth
                totalAgent = agent + 1  
                if gameState.getNumAgents() == totalAgent:
                    totalAgent = 0 # setting it back for pacman when we have checked for all the ghosts
                    depth+=1
                #This continues until we have all ghosts calculated for and that is when I increase the depth
                return sum(expectimax(totalAgent, depth, gameState.generateSuccessor(agent, newState)) for newState in gameState.getLegalActions(agent)) / float(len(gameState.getLegalActions(agent)))


        #Now we calculate it for our agent at depth 0 for maximum, after we start from the least value possible.
        maximum = float("-inf")
        for State in gameState.getLegalActions(0):
            utility = expectimax(1, 0, gameState.generateSuccessor(0, State))
            if utility > maximum:
                maximum = utility
                actionState = State

        return actionState

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    newPos = currentGameState.getPacmanPosition()
    #print(newPos)
    newFood = currentGameState.getFood()
    #print(newFood)
    newGhostStates = currentGameState.getGhostStates()
    #print(newGhostStates)
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    #assigning a weight to everything, food and ghost has same weight and ofc weight of a scared ghost will be more
    foodWeight = 1.0
    ghostWeight = 1.0
    scaredGhostWeight = 2.0

    #From this total score I will subtract or add according to movement I want to follow
    totalScore = currentGameState.getScore()

    for ghost in newGhostStates:
        distance = manhattanDistance(newPos, newGhostStates[0].getPosition())
        if distance > 0:
            #if the ghost is scared, eat it
            if ghost.scaredTimer > 0:  
                totalScore += scaredGhostWeight/distance
            # if it is not scared, go away    
            else:
                totalScore -= ghostWeight/distance
    

    # Now we find distacne to the closest food
    distancesToFood = [manhattanDistance(newPos, x) for x in newFood.asList()]
    if len(distancesToFood):
        totalScore += foodWeight / min(distancesToFood)

    return totalScore

# Abbreviation
better = betterEvaluationFunction

