"""
The model - a 2D lattice where agents live and have an opinion
"""

from collections import Counter

import mesa


class ColorCell(mesa.Agent):
    """
    Represents a cell's opinion (visualized by a color)
    """

    OPINIONS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

    def __init__(self, pos, model, initial_state):
        """
        Create a cell, in the given state, at the given row, col position.
        """
        super().__init__(pos, model)
        self._row = pos[0]
        self._col = pos[1]
        self._state = initial_state
        self._next_state = None

    def get_col(self):
        """Return the col location of this cell."""
        return self._col

    def get_row(self):
        """Return the row location of this cell."""
        return self._row

    def get_state(self):
        """Return the current state (OPINION) of this cell."""
        return self._state

    def step(self):
        """
        Determines the agent opinion for the next step by polling its neighbors
        The opinion is determined by the majority of the 8 neighbors' opinion
        A choice is made at random in case of a tie
        The next state is stored until all cells have been polled
        """
        if self.model.init_state:
            try:
                self.model.state_count[self._state] += 1
            except KeyError:
                self.model.state_count[self._state] = 1
            self.model.init_state = False

        _neighbor_iter = self.model.grid.iter_neighbors\
            (pos=(self._row, self._col), moore=True, include_center=False, radius=self.model.radius)
        neighbors_opinion = Counter(n.get_state() for n in _neighbor_iter)
        # Following is a a tuple (attribute, occurrences)
        polled_opinions = neighbors_opinion.most_common()
        tied_opinions = []
        for neighbor in polled_opinions:
            if neighbor[1] == polled_opinions[0][1]:
                tied_opinions.append(neighbor)

        if self.model.random.random() < self.model.prob_op:
            self._next_state = self.random.choice(tied_opinions)[0]
        else:
            self._next_state = self._state
        
        try:
            self.model.state_count[self._state] += 1
        except KeyError:
            self.model.state_count[self._state] = 1

    def advance(self):
        """
        Set the state of the agent to the next state
        """
        self._state = self._next_state



class ColorPatches(mesa.Model):
    """
    represents a 2D lattice where agents live
    """

    def __init__(self, width=20, height=20, num_op=16, prob_op=0, radius=1):
        """
        Create a 2D lattice with strict borders where agents live
        The agents next state is first determined before updating the grid
        """
        super().__init__()
        self._grid = mesa.space.SingleGrid(width, height, torus=False)
        self.state_count = {}
        self.schedule = mesa.time.SimultaneousActivation(self)
        self.prob_op = prob_op
        self.radius = radius
        self.init_state = True

        self.datacollector = mesa.datacollection.DataCollector(
            model_reporters={"state_count": "state_count"}
        )

        # self._grid.coord_iter()
        #  --> should really not return content + col + row
        #  -->but only col & row
        # for (contents, col, row) in self._grid.coord_iter():
        # replaced content with _ to appease linter
        for _, (row, col) in self._grid.coord_iter():
            cell = ColorCell(
                (row, col), self, ColorCell.OPINIONS[self.random.randrange(0, num_op)]
            )
            self._grid.place_agent(cell, (row, col))
            self.schedule.add(cell)
        
        if self.init_state:
            self.state_count = {}
            self.schedule.step()
            self.init_state = False

        self.datacollector.collect(self)
        self.running = True

    def step(self):
        """
        Advance the model one step.
        """
        self.state_count = {}
        self.schedule.step()

        self.datacollector.collect(self)

    # the following is a temporary fix for the framework classes accessing
    # model attributes directly
    # I don't think it should
    #   --> it imposes upon the model builder to use the attributes names that
    #       the framework expects.
    #
    # Traceback included in docstrings

    @property
    def grid(self):
        """
        /mesa/visualization/modules/CanvasGridVisualization.py
        is directly accessing Model.grid
             76     def render(self, model):
             77         grid_state = defaultdict(list)
        ---> 78         for y in range(model.grid.height):
             79             for x in range(model.grid.width):
             80                 cell_objects = model.grid.get_cell_list_contents([(x, y)])

        AttributeError: 'ColorPatches' object has no attribute 'grid'
        """
        return self._grid
