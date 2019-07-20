# pythonGames

Messing about with pygame.

## Snake

Snake charicter moves around using the arrow keys. Food appears randomly on the screen. When the head of the snake reaches the food the food is 'eaten' and added on to the body chain. This increases the length of the snake as expected. The game ends when the head of the snake runs in to itsself, or if the walls are ON then the snake can also die by hitting the walls. Before starting the state of the walls can be turned on or off using the space bar.

Issues: The game updates by using pygames  `pygame.time.delay(time ms)' as more food is eaten this delay reduce speeding up the snake. Unfortunatly this also results in the game starting not very responsive. If the delay were to be reduced and the speed to be independednt of the game loop delay then the game would be a lot more responsive and better to play at slower speeds.

## MineSweeper

Classic MineSweeper with three levels (Easy, Medium and Hard). Click on a cell to reveal it. Right click to add a flag to a cell. Right click on a flagged cell to remove the flag. Two grids are used in the game. One containing the mine lcations and the numbers of mines surrounding each location and another containing what is displayed to the player. When a player cell is clicked it is then checked against the same cell in the mine grid to decide on an action. 

ToDo: Add images for flags and for mines. Add congratulations page when complete. Similar to Snake an independednt game timer could be used to improve responsiveness and prevent the time taken for one click running over and causing a double click 9experienced when adding flags as one can be added and then removed very quickly by mistake). 
