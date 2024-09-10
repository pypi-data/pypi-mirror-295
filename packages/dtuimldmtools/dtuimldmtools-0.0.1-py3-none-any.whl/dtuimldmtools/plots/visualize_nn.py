import numpy as np
from matplotlib import pyplot as plt


def draw_neural_net(
    weights, biases, tf, attribute_names=None, figsize=(12, 12), fontsizes=(15, 12)
):
    """
    Draw a neural network diagram using matplotlib based on the network weights,
    biases, and used transfer-functions.

    :usage:
        >>> w = [np.array([[10, -1], [-8, 3]]), np.array([[7], [-1]])]
        >>> b = [np.array([1.5, -8]), np.array([3])]
        >>> tf = ['linear','linear']
        >>> draw_neural_net(w, b, tf)

    :parameters:
        - weights: list of arrays
            List of arrays, each element in list is array of weights in the
            layer, e.g. len(weights) == 2 with a single hidden layer and
            an output layer, and weights[0].shape == (2,3) if the input
            layer is of size two (two input features), and there are 3 hidden
            units in the hidden layer.
        - biases: list of arrays
            Similar to weights, each array in the list defines the bias
            for the given layer, such that len(biases)==2 signifies a
            single hidden layer, and biases[0].shape==(3,) signifies that
            there are three hidden units in that hidden layer, for which
            the array defines the biases of each hidden node.
        - tf: list of strings
            List of strings defining the utilized transfer-function for each
            layer. For use with e.g. neurolab, determine these by:
                tf = [type(e).__name__ for e in transfer_functions],
            when the transfer_functions is the parameter supplied to
            nl.net.newff, e.g.:
                [nl.trans.TanSig(), nl.trans.PureLin()]
        - (optional) figsize: tuple of int
            Tuple of two int designating the size of the figure,
            default is (12, 12)
        - (optional) fontsizes: tuple of int
            Tuple of two ints giving the font sizes to use for node-names and
            for weight displays, default is (15, 12).

    Gist originally developed by @craffel and improved by @ljhuang2017
    [https://gist.github.com/craffel/2d727968c3aaebd10359]

    Modifications (Nov. 7, 2018):
        * adaption for use with 02450
        * display coefficient sign and magnitude as color and
          linewidth, respectively
        * simplifications to how the method in the gist was called
        * added optinal input of figure and font sizes
        * the usage example how  implements a recreation of the Figure 1 in
          Exercise 8 of in the DTU Course 02450
    """

    # Determine list of layer sizes, including input and output dimensionality
    # E.g. layer_sizes == [2,2,1] has 2 inputs, 2 hidden units in a single
    # hidden layer, and 1 outout.
    layer_sizes = [e.shape[0] for e in weights] + [weights[-1].shape[1]]

    # Internal renaming to fit original example of figure.
    coefs_ = weights
    intercepts_ = biases

    # Setup canvas
    fig = plt.figure(figsize=figsize)
    ax = fig.gca()
    ax.axis("off")

    # the center of the leftmost node(s), rightmost node(s), bottommost node(s),
    # topmost node(s) will be placed here:
    left, right, bottom, top = [0.1, 0.9, 0.1, 0.9]

    n_layers = len(layer_sizes)
    v_spacing = (top - bottom) / float(max(layer_sizes))
    h_spacing = (right - left) / float(len(layer_sizes) - 1)

    # Determine normalization for width of edges between nodes:
    largest_coef = np.max([np.max(np.abs(e)) for e in weights])
    min_line_width = 1
    max_line_width = 5

    # Input-Arrows
    layer_top_0 = v_spacing * (layer_sizes[0] - 1) / 2.0 + (top + bottom) / 2.0
    for m in range(layer_sizes[0]):
        plt.arrow(
            left - 0.18,
            layer_top_0 - m * v_spacing,
            0.12,
            0,
            lw=1,
            head_width=0.01,
            head_length=0.02,
        )

    # Nodes
    for n, layer_size in enumerate(layer_sizes):
        layer_top = v_spacing * (layer_size - 1) / 2.0 + (top + bottom) / 2.0
        for m in range(layer_size):
            circle = plt.Circle(
                (n * h_spacing + left, layer_top - m * v_spacing),
                v_spacing / 8.0,
                color="w",
                ec="k",
                zorder=4,
            )
            if n == 0:
                if attribute_names:
                    node_str = str(attribute_names[m])

                else:
                    node_str = r"$X_{" + str(m + 1) + "}$"
                plt.text(
                    left - 0.125,
                    layer_top - m * v_spacing + v_spacing * 0.1,
                    node_str,
                    fontsize=fontsizes[0],
                )
            elif n == n_layers - 1:
                node_str = r"$y_{" + str(m + 1) + "}$"
                plt.text(
                    n * h_spacing + left + 0.10,
                    layer_top - m * v_spacing,
                    node_str,
                    fontsize=fontsizes[0],
                )
                if m == layer_size - 1:
                    tf_str = "Transfer-function: \n" + tf[n - 1]
                    plt.text(
                        n * h_spacing + left, bottom, tf_str, fontsize=fontsizes[0]
                    )
            else:
                node_str = r"$H_{" + str(m + 1) + "," + str(n) + "}$"
                plt.text(
                    n * h_spacing + left + 0.00,
                    layer_top - m * v_spacing + (v_spacing / 8.0 + 0.01 * v_spacing),
                    node_str,
                    fontsize=fontsizes[0],
                )
                if m == layer_size - 1:
                    tf_str = "Transfer-function: \n" + tf[n - 1]
                    plt.text(
                        n * h_spacing + left, bottom, tf_str, fontsize=fontsizes[0]
                    )
            ax.add_artist(circle)

    # Bias-Nodes
    for n, layer_size in enumerate(layer_sizes):
        if n < n_layers - 1:
            x_bias = (n + 0.5) * h_spacing + left
            y_bias = top + 0.005
            circle = plt.Circle(
                (x_bias, y_bias), v_spacing / 8.0, color="w", ec="k", zorder=4
            )
            plt.text(
                x_bias - (v_spacing / 8.0 + 0.10 * v_spacing + 0.01),
                y_bias,
                r"$1$",
                fontsize=fontsizes[0],
            )
            ax.add_artist(circle)

    # Edges
    # Edges between nodes
    for n, (layer_size_a, layer_size_b) in enumerate(
        zip(layer_sizes[:-1], layer_sizes[1:])
    ):
        layer_top_a = v_spacing * (layer_size_a - 1) / 2.0 + (top + bottom) / 2.0
        layer_top_b = v_spacing * (layer_size_b - 1) / 2.0 + (top + bottom) / 2.0
        for m in range(layer_size_a):
            for o in range(layer_size_b):
                colour = "g" if coefs_[n][m, o] > 0 else "r"
                linewidth = (
                    coefs_[n][m, o] / largest_coef
                ) * max_line_width + min_line_width
                line = plt.Line2D(
                    [n * h_spacing + left, (n + 1) * h_spacing + left],
                    [layer_top_a - m * v_spacing, layer_top_b - o * v_spacing],
                    c=colour,
                    linewidth=linewidth,
                )
                ax.add_artist(line)
                xm = n * h_spacing + left
                xo = (n + 1) * h_spacing + left
                ym = layer_top_a - m * v_spacing
                yo = layer_top_b - o * v_spacing
                rot_mo_rad = np.arctan((yo - ym) / (xo - xm))
                rot_mo_deg = rot_mo_rad * 180.0 / np.pi
                xm1 = xm + (v_spacing / 8.0 + 0.05) * np.cos(rot_mo_rad)
                if n == 0:
                    if yo > ym:
                        ym1 = ym + (v_spacing / 8.0 + 0.12) * np.sin(rot_mo_rad)
                    else:
                        ym1 = ym + (v_spacing / 8.0 + 0.05) * np.sin(rot_mo_rad)
                else:
                    if yo > ym:
                        ym1 = ym + (v_spacing / 8.0 + 0.12) * np.sin(rot_mo_rad)
                    else:
                        ym1 = ym + (v_spacing / 8.0 + 0.04) * np.sin(rot_mo_rad)
                plt.text(
                    xm1,
                    ym1,
                    str(round(coefs_[n][m, o], 4)),
                    rotation=rot_mo_deg,
                    fontsize=fontsizes[1],
                )

    # Edges between bias and nodes
    for n, (layer_size_a, layer_size_b) in enumerate(
        zip(layer_sizes[:-1], layer_sizes[1:])
    ):
        if n < n_layers - 1:
            layer_top_a = v_spacing * (layer_size_a - 1) / 2.0 + (top + bottom) / 2.0
            layer_top_b = v_spacing * (layer_size_b - 1) / 2.0 + (top + bottom) / 2.0
        x_bias = (n + 0.5) * h_spacing + left
        y_bias = top + 0.005
        for o in range(layer_size_b):
            colour = "g" if intercepts_[n][o] > 0 else "r"
            linewidth = (
                intercepts_[n][o] / largest_coef
            ) * max_line_width + min_line_width
            line = plt.Line2D(
                [x_bias, (n + 1) * h_spacing + left],
                [y_bias, layer_top_b - o * v_spacing],
                c=colour,
                linewidth=linewidth,
            )
            ax.add_artist(line)
            xo = (n + 1) * h_spacing + left
            yo = layer_top_b - o * v_spacing
            rot_bo_rad = np.arctan((yo - y_bias) / (xo - x_bias))
            rot_bo_deg = rot_bo_rad * 180.0 / np.pi
            xo2 = xo - (v_spacing / 8.0 + 0.01) * np.cos(rot_bo_rad)
            yo2 = yo - (v_spacing / 8.0 + 0.01) * np.sin(rot_bo_rad)
            xo1 = xo2 - 0.05 * np.cos(rot_bo_rad)
            yo1 = yo2 - 0.05 * np.sin(rot_bo_rad)
            plt.text(
                xo1,
                yo1,
                str(round(intercepts_[n][o], 4)),
                rotation=rot_bo_deg,
                fontsize=fontsizes[1],
            )

    # Output-Arrows
    layer_top_0 = v_spacing * (layer_sizes[-1] - 1) / 2.0 + (top + bottom) / 2.0
    for m in range(layer_sizes[-1]):
        plt.arrow(
            right + 0.015,
            layer_top_0 - m * v_spacing,
            0.16 * h_spacing,
            0,
            lw=1,
            head_width=0.01,
            head_length=0.02,
        )

    plt.show()


def windows_graphviz_call(fname, cur_dir, path_to_graphviz):
    from subprocess import call

    call_str = (
        path_to_graphviz
        + r"\bin\dot"
        + " -Tpng "
        + cur_dir
        + "\\"
        + fname
        + ".gvz "
        + "-o"
        + cur_dir
        + "\\"
        + fname
        + ".png"
        + " -Gdpi=600"
    )
    call(call_str)
