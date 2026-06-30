"""
Generate and plot a hexagonal (close) packing of circles of radius R,
arranged as an N x N grid of rows/columns.
"""

import argparse

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle


def get_hex_color(col, row):
    # Floor division handles the row/2 offset matching the geometric shift
    color_index = (col + (row // 2)) % 2
    # return "Color A" if color_index == 0 else "Color B"
    return "red" if color_index == 0 else "blue"

def hexagonal_packing(N, R):
    """
    Generate centers for an N x N hexagonal packing of circles of radius R.

    In hexagonal packing, each row is offset by R (half the circle diameter)
    from the previous one, and rows are spaced by R*sqrt(3) (the height of
    an equilateral triangle with side 2R) so that circles in adjacent rows
    are tangent to each other.

    Returns
    -------
    centers : (N*N, 2) ndarray of (x, y) circle centers
    colors  : list of N*N color strings, alternating red/blue in a
              checkerboard pattern based on (row + col) parity
    """
    dx = 2 * R                 # horizontal spacing within a row
    dy = np.sqrt(3) * R        # vertical spacing between rows

    centers = []
    colors = []
    for row in range(N):
        y = row * dy
        x_offset = R if row % 2 == 1 else 0.0  # offset odd rows by R
        for col in range(N):
            x = col * dx + x_offset
            centers.append((x, y))
            colors.append("red" if (row + col) % 2 == 0 else "blue")   # vertical checkerboard
            # colors.append(get_hex_color(col, row))   # diagonal checkerboard

    return np.array(centers), colors


def plot_packing(centers, colors, R, ax=None):
    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 8))

    for (x, y), color in zip(centers, colors):
        circle = Circle((x, y), R, facecolor=color,
                         edgecolor="black", linewidth=0.8, alpha=0.85)
        ax.add_patch(circle)

    ax.set_aspect("equal")
    margin = R
    ax.set_xlim(centers[:, 0].min() - R - margin, centers[:, 0].max() + R + margin)
    ax.set_ylim(centers[:, 1].min() - R - margin, centers[:, 1].max() + R + margin)
    ax.set_title(f"Hexagonal Packing ({len(centers)} circles, R={R})")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    return ax


def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate and plot an N x N hexagonal packing of circles of radius R."
    )
    parser.add_argument("-N", type=int, default=8,
                         help="number of circles per row/column (default: 8)")
    parser.add_argument("-R", type=float, default=1.0,
                         help="circle radius (default: 1.0)")
    parser.add_argument("-p", "--png", type=str, default="hexagonal_packing.png",
                         help="output image filename (default: hexagonal_packing.png)")
    parser.add_argument("-o", "--csv", type=str, default="csort.csv",
                         help="ICs .csv filename (default: csort.csv)")
    parser.add_argument("--no-show", action="store_true",
                         help="do not display the plot window, just save it")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    centers, colors = hexagonal_packing(args.N, args.R)
    # x,y,z,type,volume,cycle entry,custom:GFP,custom:sample
    # fname = "csort.csv"
    print(f"len(centers)={len(centers)}")
    print(f"colors={colors}")
    xmin = centers[:, 0].min()
    xmax = centers[:, 0].max()
    ymin = centers[:, 1].min()
    ymax = centers[:, 1].max()
    xdel = xmax-xmin
    ydel = ymax-ymin
    if xdel > ydel:
        offset = xdel / 2.0
    else:
        offset = ydel / 2.0
    print(f"xmin={xmin}, xmax={xmax},   ymin={ymin}, ymax={ymax} --> offset={offset}")
    with open(args.csv, "w", encoding="utf-8") as file:
        file.write("x,y,z,type,volume,cycle entry,custom:GFP,custom:sample\n")
        for idx in range(len(centers)):
            if colors[idx] == 'red':
                file.write(f"{centers[idx,0] - offset},{centers[idx,1] - offset},0.0,A\n")
            else:
                file.write(f"{centers[idx,0] - offset},{centers[idx,1] - offset},0.0,B\n")
    print(f" --> {args.csv}")

    ax = plot_packing(centers, colors, args.R)
    plt.tight_layout()
    # plt.savefig(args.output, dpi=150)
    # print(f"Saved plot with {len(centers)} circles to {args.output}")

    if not args.no_show:
        plt.show()
