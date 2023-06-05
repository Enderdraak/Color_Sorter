# Color Sorter
This is a python program that allows you to find solutions for a game in which you sort some colored balls.

## Table of index
 * [The game](#the-game)
 * [The idea](#the-idea)

## The game
<img src="./Pictures/Valid moves.png" width="25%" align="right">
The game this is based on has a few rules. You start with some flasks that contain balls, the balls are all stacked ontop of each other making it a single list from top to bottom. Only the highest ball in these flasks are acessiable and can be attempted to be moved to a different flask. The balls can only be moved to a empty flask or one with the same color below the empty spot. In the picture to the right the only four valid moves in that senario are shown.

Lastly, the amount of balls in the flasks can vary from level to level. I have limited this to a minimum of 1 ball to a max of 20. The same is true for the flasks. The game gives you 2 emtpy flasks each level. All the other flasks given in the level are always completely full.

## The idea
After I got stuck on multiple levels and just could not figure out how I could solve them I figured I should be able to make a python script that can solve it for me. The idea I had was to just brute force it. Starting at the first flask and just attempting all the possible combinations until I found one that solved the puzzle.

## Problems
When I sat down and make the code I came across serveral problems. I have picked 5 of them and highlighted the problem and how I solved them.

### Recursive
The program had orgiginally a recursive function that would try and find the solution. One of the issues that gave was that the when a function was closed some changes in the variables where not undone. This could have been prevented with some extra code but that was not the only issue I found at the time. For some other problem I needed to know all the previous steps that where done towards the solution, this was also not easily done with the recursive function. And to finish I also realised that the way I had set it up did not need or require a recursive function and could also be done with a looping function instead.
```python
def repeating_moves():

    global steps
    steps = [-2,-2]
    Victory = False
    if check_complete() == True:
        Victory = True
        steps = []
    
    while not Victory:
        
        #undo a move
        if steps[-2] == -2:
            steps[-2] += 1
            steps[-1] = -2
        else:   
            del steps[-2:]
            if len(steps) == 0:
                return False
            move(steps[-1], steps[-2], True)
            steps[-2] -= 1
            steps[-1] -= 1
        
        while steps[-2] >= -1 and steps[-2] < map_data("flask")+1 and not Victory:
            steps[-2] += 1
            if not twice_twice(steps):
                if not full_flask(steps):
                        
                    if steps[-1] >= map_data("flask")+1:
                        steps[-1] = -2
                    steps[-1] += 1
                    while steps[-1] >= -1 and steps[-1] < map_data("flask")+1 and not Victory:
                        steps[-1] += 1

                        if not bouncing(steps):
                            if not skipping(steps):

                                #do the move
                                if move(steps[-2], steps[-1]) != False:
                                    if check_complete() == True:
                                        Victory = True
                                        break

                                    #this code should prevent looping
                                    loop = detect_loop(steps)
                                    if  not loop:
                                        steps = steps + [-2,-2]
                                    else:
                                        for x in range(0, loop, 2):
                                            move(steps[-1], steps[-2], True)
                                            del steps[-2:]
                                        move(steps[-1], steps[-2], True)
                                        
    #return the final info
    return steps
```