# Color Sorter
This is a python program that allows you to find solutions for a game in which you sort some colored balls.

## The game
The game this is based on has a few rules. You start with some flasks that contain balls, the balls are all stacked ontop of each other making it a single list from top to bottom. Only the highest ball in these flasks are acessiable and can be attempted to be moved to a different flask. The balls can only be moved to a empty flask or one with the same color below the empty spot.

<img src="./Pictures/Valid moves.png" width="50%" align="right">

Lastly, the amount of balls in the flasks can vary from level to level. I have limited this to a minimum of 1 ball to a max of 20. The same is true for the flasks. The game gives you 2 emtpy flasks each level. All the other flasks given in the level are always completely full.