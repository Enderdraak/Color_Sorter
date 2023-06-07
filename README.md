# Color Sorter
This is a python program that allows you to find solutions for a game in which you sort some colored balls.

## Table of index
 * [The game](#the-game)
 * [The idea](#the-idea)
 * [Problems](#problems)
  * [Recursive](#recursive)
  * [Loops](#loops)
  * [Bouncing](#bouncing)

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
### Loops
The program had the tendency to figure out a series of steps that could be repeated indefinitly without changing anything. This is not something that is desireable. I had to write a piece of code that would figure out when a loop like that happened and then return a number of the amount of steps to undo.
The code looks for the biggest loop possible. Meaning that if you give it a loop that has been repeated four times it will tell you the loop is 2x loop lengths long. Which results in two of the loops remaining. This will not cause any problems because it checks every step for loops, so it will find the first loop that gets made.

```python
def detect_loop(steps):

    #detect if a series of steps get repeated and detect the size of that loop
    biggest_loop = False
    for i in range(2,int((len(steps)+2)/2),2):
        test_steps = steps[:i*-1]
        if test_steps[i*-1:] == steps[i*-1:] and i > 2:
            detection_list = [[0 for j in range(map_data("flasks")+2)],[0 for j in range(map_data("flasks")+2)]]
            for k in range(0,i,2):
                detection_list[0][steps[(k+1)*-1]] += 1
                detection_list[1][steps[(k+2)*-1]] += 1
            if detection_list[0] == detection_list[1]:
                biggest_loop = i
    return biggest_loop
```
### Bouncing
Bouncing is the act of moving the ball back where it came from. The computer would sometimes get stuck moving a single red ball from flask A to B, a blue one from C to D and then move the red one back. Doing every single step towards solving with the swapping of the red ball inbetween, since this just about did not loop but was quite useless.
The code I wrote looks into all the previous steps and find the last most step in which one, or both, the flasks has been used to move with (both to and from). If they have been touched it looks to see it the current move undos the move that was done back then. Should the move indeed undo that move it is not allowed. Any other move is allowed. Like moving all the red balls from flask A to B.

```python
def bouncing(steps):
        
    #put in the test to check for bouncing. It can redo moves, but it can not undo moves if both piles have not been changed since then.
    bouncing = 0
    for action in range(2,len(steps),2):
        test_step = [steps[(action+2)*-1], steps[(action+1)*-1]]
        if test_step[0] == steps[-1] or test_step[0] == steps[-2]:
            bouncing = 1
        if test_step[1] == steps[-1] or test_step[1] == steps[-2]:
            bouncing = 1
        if test_step[0] == steps[-1] and test_step[1] == steps[-2]:
            bouncing = 2
        if bouncing != 0:
            break
    if bouncing <= 1:
        return False
    return True
```
