"""
Yin Zhao
Oct 2014
"""
from __future__ import absolute_import
from engines import Engine
from copy import deepcopy
import random
#import timeit

"""maximum searching depth"""
global POSITIVE_INFINITY
POSITIVE_INFINITY = 50000
global NEGATIVE_INFINITY
NEGATIVE_INFINITY = -50000


class StudentEngine(Engine):

    def __init__(self):
        self.alpha_beta = False
	#self.num_nodes = 1
	#self.nodes_last = 0
	#self.known_boards = []
	#self.duplicates= []
	#self.branch=1
	#self.branchls=[]

    def get_move(self, board, color, move_num=None,
                 time_remaining=None, time_opponent=None):
	#start = timeit.default_timer()
	if time_remaining <= 15:
	    minimax_depth=1
	    ab_depth=1
	elif time_remaining <=20:
	    minimax_depth=3
	    ab_depth=3
	else:
	    minimax_depth=3
	    ab_depth=4
	if self.alpha_beta:
    	    bestmove = self.get_alpha_beta(board,color,ab_depth,NEGATIVE_INFINITY,POSITIVE_INFINITY)[1]
        else:
            bestmove= self.get_minimax(board, color, minimax_depth)[1]
	#end = timeit.default_timer()
	#print "run time: "
	#print end - start
	#print "number of nodes generated: "
	#print self.num_nodes
	#print "number of duplicates: "
	#print len(self.duplicates)
	#print "branching factor: "
	#print sum(self.branchls)/self.branch
	#print self.nodes_last
	
	return bestmove
	
    def get_minimax(self, board, color, depth):
        if depth ==0:
	    return [self.evaluate(board,color),None]
	moves = board.get_legal_moves(color)
	bestscore = NEGATIVE_INFINITY
	bestmove=None
	if moves:
	    bestmove=moves[0]
	    for i in range(len(moves)):
		newboard=deepcopy(board)
		newboard.execute_move(moves[i],color)
		gettry=self.get_minimax(newboard,color*-1,depth-1)
		tryscore = gettry[0]*-1
		
		if tryscore>bestscore:
		    bestscore=tryscore
		    bestmove=moves[i]

	    #self.nodes_last=len(moves)
	    #self.num_nodes=self.num_nodes+self.nodes_last
	    #self.branch=self.branch+1
	    #self.branchls.append(self.nodes_last)

	return [bestscore,bestmove]

    def get_alpha_beta(self, board, color, depth, alpha, beta):
  	if depth==0:
	    return [self.evaluate(board,color),None]
	moves = board.get_legal_moves(color)
	bestmove = None
	if moves:
	    bestmove = moves[0]
	while moves:
	    newboard = deepcopy(board)
	    newboard.execute_move(moves[0],color)
	    amove=self.get_alpha_beta(newboard,color*-1,depth-1,beta*-1,alpha*-1)
	    value = amove[0]*-1
	    
	    if value>alpha:
		alpha=value
		bestmove=moves[0]
	    moves.pop(0)
	    if beta <= alpha:
		return [alpha,bestmove]
	    
	return [alpha,bestmove]

	    #self.nodes_last=len(moves)
	    #self.num_nodes+=self.nodes_last
	    #self.branch=self.branch+1
	    #self.branchls.append(self.nodes_last)


    def evaluate(self, board, color):

        # create a deepcopy of the board to preserve the state of the actual board
        """ Calculate evaluated value by weight """
	#boardstr = ""
	#for x in range (7):
	#    for y in range (7):
	#	if board[x][y]==1:
	#	    boardstr=boardstr+"W"
	#	else:
	#	    boardstr=boardstr+"B"
		
	#if boardstr in self.known_boards:
	#    if boardstr not in self.duplicates:
	#	self.duplicates.append(boardstr)
	#else:
	#    self.known_boards.append(boardstr)
        value = (board[0][0]+board[0][7]+board[7][0]+board[7][7])*25
	value = value -(board[1][0]+board[0][1]+board[1][7]+board[7][1]+board[6][0]+board[0][6]+board[6][7]+board[7][6])*4
	value = value +(board[2][0]+board[0][2]+board[2][7]+board[7][2]+board[5][0]+board[0][5]+board[5][7]+board[7][5])*8
	value = value -(board[1][1]+board[6][1]+board[1][6]+board[6][6])*2
	value = value +(board[0][3]+board[0][4]+board[7][3]+board[7][4]+board[3][0]+board[4][0]+board[3][7]+board[4][7])*3
	for i in range(4):
	    value =value -2*(board[1][i+2]+board[6][i+2]+board[i+2][1]+board[i+2][6])
	    for j in range(4):
		value += board[i+2][j+2]

        #if evaluating black value, flip sign
        if color == -1:
            value = value*-1

        # subtract opponent's mobility

	opmobility = len(board.get_legal_moves(color*-1))
	value = value-opmobility
        return value


    def _get_cost(self, board, color, move):
        """ Return the difference in number of pieces after the given move 
        is executed. """
        
        # Create a deepcopy of the board to preserve the state of the actual board
        newboard = deepcopy(board)
        newboard.execute_move(move, color)

        # Count the # of pieces of each color on the board
        num_pieces_op = len(newboard.get_squares(color*-1))
        num_pieces_me = len(newboard.get_squares(color))

        # Return the difference in number of pieces
        return num_pieces_me - num_pieces_op
        
engine = StudentEngine

