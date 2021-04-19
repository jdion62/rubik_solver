from typing import List
from typing import Optional

import rubik

############################################################################
#Invarient Documentation:
#
#Our invarient is that the list frontier is full of elements we have yet to
# visit, but are near points that we have visited so long as it's empty, we
# have not visited all nodes. We know that this relates to the depth as, if
# we have not yet found the solution, we know the problem is longer than the
# depth of the current point we are visiting (point curr). My program uses
# depth to mean something slightly different in order to cut down on math
# operations
#
#On Initialization of the loop, this holds true as we have not visited any
# nodes so any nodes that are in frontier are unvisited and the starting
# node is the only one queued to be visited due to it's depth (0)
#
#During Maintenence of the loop, this is provably true as the way we visit
# the node is by popping it out of the frontier list, later during the
# maintenence we add any nodes that we can "see" from our curr nude to
# frontier which cues them to be visited, though the problem seems to grow,
# we are actually shrinking the problem as we stop looking at irrelevant
# information as we know that the solution can not be shorter than the
# current depth that we are at
#
#During termination of the loop, we have found the shortest possible path
# and the frontier list is now filled with nodes that we have not visited
# and are close to the solved state, we have no need to visit these nodes
# so we never do as we break out of the loop. We will have our answer as we
# either have found the shortest answer at our current depth or frontier is
# emoty and we have completely traversed the tree and found no possible
# solution on any existing depth
#
############################################################################
def shortest_path(
        start: rubik.Position,
        end: rubik.Position,
) -> Optional[List[rubik.Permutation]]:
    """
    Using 2-way BFS, finds the shortest path from start to end.
    Returns a list of Permutations representing that shortest path.
    If there is no path to be found, return None instead of a list.

    You can use the rubik.quarter_twists move 6-tuple.
    Each move can be applied using rubik.perm_apply.
    """
    #initialize a frontier to store nodes that still need to be explored
    frontier = [start]

    #make a dictionary saving the stored points and pairing them with the move that got us to it
    moves = {start: None}
    
    #initialize some variables for use later in order to presentt the answer
    solved = False
    path = []
    depth = 0

    #while fronier has elements (starts with "start") and we haven't reached an aswer already, depth is just to control runtime
    while frontier and not solved and depth <= 1000000:
            #grab the first element remaining in the frontier
            curr = frontier.pop(0)
            depth += 1

            #if we find our end point, we're done, mark as solved and break out of the loop
            if(curr == end):
                    solved = True
                    break

            #check the 6 possible moves from the current position
            for i in range(6):
                    temp = rubik.perm_apply(rubik.quarter_twists[i], curr)

                    #check if we've seen this cube state already, if not store reverse of move
                    if temp not in moves:
                            frontier.append(temp)
                            if(i%2 == 0):
                                    moves[temp] = i+1
                            else:
                                    moves[temp] = i-1
    #check if we have a solved cube
    if solved:
        #im is the "important" point that we are working backwards from, i is the move
        im = end
        i = moves[im]
        #while we are not at the start
        while i != None:
                #save move and update i and im
                temp = 0
                if(i%2 == 0):
                        temp = i+1
                else:
                        temp = i-1
                path.append(rubik.quarter_twists[temp])
                im = rubik.perm_apply(rubik.quarter_twists[i], im)
                i = moves[im]
        #reverse since we were appending the earlier moves last
        path.reverse()
        return path
    else:
        #we were given an unsolvable cube
        return None

#       raise NotImplementedError
