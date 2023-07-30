agent - entity that perceives its environment and acts upon that environment
state - a configuration of the agent and its environment
initial state - the state in which the agent begins
actions - choices that can be made in a state

Actions(state) returns the set of actions that can be executed in state

transition model - a description of what state results from performing any applicable action in any state

Result(state, action) returns the state resulting from performing action in state s

state space - the set of all states reachable from the initial state by any sequence of actions

goal test - way to determine whether a given state is a goal state

path cost - numerical cost associated with a given path

solution - a sequence of actions that leads from the initial state to a goal state

optimal solution - a solution that has the lowest path cost among all solutions

----------------------------------------------------------------------
----------------------------------------------------------------------

Search Problems
-> Initial State
-> Actions
-> Transition Model
-> Goal Test
-> Path Cost Function

----------------------------------------------------------------------
**node**
a data structure that keeps track of
-> state
-> a parent (node that generated node)
-> an action (action applied to parent to get node)
-> a path cost (from initial state to node)

______________________________________________________________________

**Approach**
* start with a frontier that contains the initial state
* Repeat:
  * If the frontier is empty, then no solution
  * Remove a node from a frontier
  * If node contains goal state, return the solution
  * Expand node, add resulting nodes to the frontier




**Revised Approach**
* start with a frontier that contains the initial state
* start with an empty explored set
* Repeat:
  * If the frontier is empty, then no solution
  * Remove a node from a frontier
  * If node contains goal state, return the solution
  * Add the node to the explored set
  * Expand node, add resulting nodes to the frontier if they aren't already in frontier or they aren't already in the explored set


___________________________________________________________________________

**Depth-First Search**
using Stack
First-in-last-out

* search algorithm that always expands the deepest node in the frontier



**Breadth-First Search**
* search algorithm that always expands the shallowest node in the frontier

using Queue
First-in-first-out



**Two Types of Search**
* Uninformed search -> search strategy that uses no problem-specific knowledge: DFS, BFS
* Informed search -> such strategy that uses problem-specific knowledge to find solutions more efficiently: GBFS, A* search

_________________________________________________________________________________________________
**greedy best-first search**
-> search algorithm that expands the node that is closest to the goal, as estimated by a **heuristic function h(n)**


Heuristic function? Manhattan distance



** A* search **
-> search algorithm that expands node with lowest value of g(n) + h(n)

* g(n) = cost to reach node: ex, steps taken
* h(n) = estimated cost to goal: ex, manhattan steps go toal


A* is optimal if:
  - h(n) is admissible (never overestimates the true cost)
  - h(n) is consistent (for every node n and successor n' with step cost c, h(n) <= h(n') + c)


________________________________________________________________________________________________________________________
**Adversarial Search**

ex, tic tac toe

**Minimax algorithm**

-------------------------------------------------------------------
* set of rules:
O wins = -1 - min player
X wins = 1 - maxp layer
draw = 0

* MAX(X) aims to maximize score
* MIN(O) aims to minimize score
-------------------------------------------------------------------



