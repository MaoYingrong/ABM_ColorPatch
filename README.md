# ABM_ColorPatch
This is a revised version of ABM Color Patch model from mesa_examples [Color Patch model](https://github.com/projectmesa/mesa-examples/tree/main/examples/color_patches).  

This model simulates the process of opinion diffusion—how individuals’ opinions are influenced by those of their neighbors, how opinion groups emerge, and how “minority groups” disappear.   

It’s a cellular automaton model where each agent lives in a cell on a 2D grid, and never moves. An agent’s state represents its “opinion” and is shown by the color of the cell the agent lives in. Each color represents an opinion. At each time step, an agent’s opinion is influenced by that of its neighbors. If it decides to adapt its thinking to that of its neighbors, the cell color changes.  


## Files

* ``color_patches/model.py``: Defines the cell and model classes. The cell class governs each cell's behavior. The model class itself controls the lattice on which the cells live and interact.
* ``color_patches/server.py``: Defines an interactive visualization.
* ``run.py``: Launches an interactive visualization





