# scalableRandomMazeGenerator

This is a Maze generator and race game.

It uses a non-traditional maze generating algorithm that I made, which makes a random line from one side of the map to the other, then slowly branches out with a tree-like pattern. Although less optimal, it produces a nice, unpredictable maze, unlike the recursive division method. 

Scalable from a 2x2 to 200x200 maze, using boolean adjacency matrices to store values of connecting paths. 

Turned into an endless two player racing game, making use of recursive design and procedural generation.

A similar algorithm is used in UpChuck for its map generation. 
