import networkx as nx
import numpy as np


def get_normalized_images(file_names):
    """Load images as numpy arrays from text files and normalize them."""

    images = {}
    image_shape = None

    for file_name in file_names:
        with open(file_name, "r") as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]
            array = np.array([[int(i) for i in line] for line in lines])
            if image_shape is None:
                image_shape = array.shape
            elif image_shape != array.shape:
                raise ValueError(
                    f"""Shape of {file_name} is different
                     from the shape of previously loaded files."""
                )
            images[file_name] = array

    lcm = np.lcm.reduce([np.sum(image) for image in images.values()])
    normalized_images = {
        name: image * (lcm / np.sum(image)) for name, image in images.items()
    }
    return normalized_images


def comp_dist(image1, image2):
    """Returns the Earth Mover's Distance between two images."""

    def point_dist(p1, p2):
        lengthX = image1.shape[1]
        return (
            p2[1] - p1[1]
        ) % lengthX  # Wrap around in a single (clockwise) direction

    if np.array_equal(image1, image2):
        return 0.0

    non_zero_points1 = np.argwhere(image1)
    non_zero_points2 = np.argwhere(image2)
    nodes1 = {(1, *p): {"demand": float(-image1[tuple(p)])} for p in non_zero_points1}
    nodes2 = {(2, *p): {"demand": float(image2[tuple(p)])} for p in non_zero_points2}
    edges = [
        ((1, *p1), (2, *p2), {"weight": point_dist(p1, p2)})
        for p1 in non_zero_points1
        for p2 in non_zero_points2
    ]

    G = nx.DiGraph()
    G.add_nodes_from(nodes1.items())
    G.add_nodes_from(nodes2.items())
    G.add_edges_from(edges)

    emd_distance = nx.min_cost_flow_cost(G)
    return float(emd_distance)


# This function should sort the files as described in the instructions.
# P1.txt should be the first one.
def sort_files():
    files = [
        "P1.txt",
        "P2.txt",
        "P3.txt",
        "P4.txt",
        "P5.txt",
        "P6.txt",
        "P7.txt",
        "P8.txt",
        "P9.txt",
        "P10.txt",
        "P11.txt",
        "P12.txt",
        "P13.txt",
        "P14.txt",
        "P15.txt",
    ]
    start_file = "P1.txt"
    images = get_normalized_images(files)
    sorted_files = sorted(files, key=lambda x: comp_dist(images[start_file], images[x]))
    return sorted_files


if __name__ == "__main__":
    print(sort_files())
