# -*- coding: utf-8 -*-
# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def genericSearchAlgorithm(problem, open_type, PriorityQueue=False, heuristic=nullHeuristic):
    """
    通过配置不同的参数(搜索算法要解决的问题对象,采用的数据结构,是否使用优先队列[即,是否每条路径具有不同的代价],启发式函数)
    可实现DFS(深度搜索),BFS(广度搜索),UCS(代价一致),A*算法(代价一致+启发式函数)搜索
    param1: problem (搜索算法要解决的问题对象)
    param2: open_type (搜索算法中的open表采用的数据结构)
    param3: PriorityQueue (bool值,默认False,是否采用优先队列数据结构,用于代价一致搜索和A*搜索算法)
    param4: heuristic (启发式函数,默认为nullHeuristic[返回值为0,相当于没有该函数],用于A*算法)
    节点(node)：
        对于DFS和BFS,open表中的每个节点(node)均是(state, actions)的二元组,其中state为状态,即为吃豆人所在的坐标(coord),
        actions为从初始结点到达本状态所要执行的操作序列["South","North",....]
        对于UCS和A*,open表中的每个节点(node)均是((state, actions),cost)的二元组,其中state为状态,即为吃豆人所在的坐标(coord),
        actions为从初始结点到达本状态所要执行的操作序列["South","North",....],cost为从初始结点到当前结点的代价(对于UCS)或
        从初始结点到当前结点的代价+启发式函数值(对于A*)

    return值: actions列表,即,吃豆人吃到豆子所执行的一个action序列
    """
    openTable = open_type()  # open_type为util中的一个数据结构(Stack、Queue、PriorityQueue)类
    # 将其实例化,创建open表
    if PriorityQueue:  # 判断是否使用优先队列,如果是,则push二元组((state, actions),cost)
        openTable.push((problem.getStartState(), []),
                       heuristic(problem.getStartState(), problem))
    else:
        openTable.push((problem.getStartState(), []))
    closed = []  # 初始化closed表为空表
    while True:
        if openTable.isEmpty():  # 如果open表为空，则搜索问题无解
            return []
        coord, actions = openTable.pop()  # 从open表中pop出一个节点
        if problem.isGoalState(coord):  # 如果当前结点是目标状态,则搜索成功,返回操作序列actions
            return actions
        if coord not in closed:  # 若当前结点不在closed表中
            closed.append(coord)  # 将当前结点加入closed表,coord=(x,y)
            for successor_coord, action, step_cost in \
                    problem.getSuccessors(coord):
                # 遍历当前结点的后继节点
                if PriorityQueue:
                    """
                    若使用优先队列，则在push时要给出优先级信息,为从起始节点通过actions到达当前结点的代价加
                    以当前结点为参数的启发式函数的值,即((state, actions),cost)
                    """
                    openTable.push((successor_coord, actions + [action]),
                                   problem.getCostOfActions(actions + [action]) +
                                   heuristic(successor_coord, problem))
                else:
                    openTable.push((successor_coord, actions + [action]))


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    """
    深度优先搜索算法
    实例化类GenericSearch为dfs,使用util.py中定义的
    数据结构栈Stack来作为open表的数据结构
    param: problem 搜索算法要解决的问题对象
    return值: actions列表,即,吃豆人吃到豆子所执行的一个action序列
    """
    return genericSearchAlgorithm(problem, util.Stack)


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    """
    广度优先搜索算法
    实例化类GenericSearch为bfs,使用util.py中定义的
    数据结构队列Queue来作为open表的数据结构
    param: problem 搜索算法要解决的问题对象
    return值: actions列表,即,吃豆人吃到豆子所执行的一个action序列
    """
    return genericSearchAlgorithm(problem, util.Queue)


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    """
    代价一致搜索算法
    实例化类GenericSearch为ucs,使用util.py中定义的
    数据结构优先队列PriorityQueue来作为open表的数据结构
    param: problem 搜索算法要解决的问题对象
    return值: actions列表,即,吃豆人吃到豆子所执行的一个action序列
    """
    return genericSearchAlgorithm(problem, util.PriorityQueue, True)


def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    """
    A*算法
    实例化类GenericSearch为astar,使用util.py中定义的
    数据结构优先队列PriorityQueue来作为open表的数据结构
    同时指定启发式函数heuristic,使用该启发式函数来估算当前结点到目标结点的代价
    param1: problem 搜索算法要解决的问题对象
    param2: heuristic 启发式函数对象
    return值: actions列表,即,吃豆人吃到豆子所执行的一个action序列
    """
    return genericSearchAlgorithm(problem, util.PriorityQueue, True, heuristic)


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
