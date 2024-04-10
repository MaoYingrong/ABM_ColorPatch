"""
handles the definition of the canvas parameters and
the drawing of the model representation on the canvas
"""
# import webbrowser

import mesa

from .model import ColorPatches

_COLORS = [
    "Aqua",
    "Blue",
    "Fuchsia",
    "Gray",
    "Green",
    "Lime",
    "Maroon",
    "Navy",
    "Olive",
    "Orange",
    "Purple",
    "Red",
    "Silver",
    "Teal",
    "White",
    "Yellow",
]


grid_rows = 50
grid_cols = 25
cell_size = 10
canvas_width = grid_rows * cell_size
canvas_height = grid_cols * cell_size


def get_state_count(model):
    """
    Display the number of agents in state 2
    """
    new_dic = {}
    for k, v in model.state_count.items():
        new_dic[_COLORS[k]] = v

    return str(new_dic)
    # for k, v in model.state_count.items():
    #     words = "the number of agents having opinion %s is : %d " % (k, v)
    #     total += words
    #     total += "\n"
    # return total



def color_patch_draw(cell):
    """
    This function is registered with the visualization server to be called
    each tick to indicate how to draw the cell in its current state.

    :param cell:  the cell in the simulation

    :return: the portrayal dictionary.
    """
    if cell is None:
        raise AssertionError
    portrayal = {"Shape": "rect", "w": 1, "h": 1, "Filled": "true", "Layer": 0}
    portrayal["x"] = cell.get_row()
    portrayal["y"] = cell.get_col()
    portrayal["Color"] = _COLORS[cell.get_state()]
    return portrayal


canvas_element = mesa.visualization.CanvasGrid(
    color_patch_draw, grid_rows, grid_cols, canvas_width, canvas_height
)

model_params = {
    "width": grid_rows,
    "height": grid_cols,
    "num_op": mesa.visualization.Slider(
        name="number of opinions", value=16, min_value=1, max_value=16, step=1
    ),
    "prob_op": mesa.visualization.Slider(
        name="probability of opinion change", value=1.0, min_value=0.0, max_value=1.0, step=0.01,
    ),
    "radius": mesa.visualization.Slider(
        name="radius of opinion polling", value=1, min_value=1, max_value=5, step=1
    ),
}

server = mesa.visualization.ModularServer(
    model_cls=ColorPatches,
    visualization_elements=[canvas_element, get_state_count],
    name="Color Patches",
    model_params=model_params,
)

# webbrowser.open('http://127.0.0.1:8521')  # TODO: make this configurable
