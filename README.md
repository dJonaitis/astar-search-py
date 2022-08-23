# astar-search-py
The A* pathfinding algorithm visualised using pygame, built entirely in Python.



## Usage:
1. Ensure you have prerequisite dependencies (colorspy, pygame)
2. Run ``main.py`` and the window will open.
3. Your first two left clicks will indicate the start, end points.
4. Any further left clicks will draw walls.
5. Right clicking will turn the node into an empty one.
6. Hit ENTER to start once start and end points have been placed.
7. The shortest path will be outlined in blue.
8. Hit BACKSPACE to reset the grid.

## Colors:
- **Yellow** is the starting point.
- **Pink** is the end point.
- **Black** are the walls through which a path cannot be made.
- **Red** are the closed nodes that have already been checked.
- **Green** are open nodes.
- **White** are the nodes through which a path can be made.
- **Blue** is the shortest path, and will appear once it is finished.
