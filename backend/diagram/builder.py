import io
import matplotlib.pyplot as plt
import networkx as nx

DEVICE_COLOR_MAP = {
    "Router": "#e6194B",
    "Switch": "#3cb44b",
    "Server": "#4363d8",
    "Firewall": "#f58231",
    "PC": "#911eb4",
    "Laptop": "#46f0f0",
    "Printer": "#f032e6",
    "IP Phone": "#bcf60c",
    "Camera": "#fabebe",
    "Unknown": "#a9a9a9"
}


def get_color(device_type):
    return DEVICE_COLOR_MAP.get(device_type, "#808080")


def generate_diagram_image(devices_df, connections_df):
    G = nx.DiGraph()

    # Add devices as nodes
    for _, row in devices_df.iterrows():
        G.add_node(row["id"],
                   label=row["name"],
                   layer=row["layer"],
                   color=get_color(row["type"]))

    # Add connections as edges
    for _, row in connections_df.iterrows():
        G.add_edge(row["source"], row["target"])

    pos = nx.spring_layout(G, seed=42)  # for consistent layout
    node_colors = [G.nodes[n]["color"] for n in G.nodes]
    labels = {n: G.nodes[n]["label"] for n in G.nodes}

    plt.figure(figsize=(14, 8))
    nx.draw_networkx_edges(G, pos, edge_color='gray')
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=1500)
    nx.draw_networkx_labels(G, pos, labels=labels,
                            font_size=10, font_weight="bold")

    plt.title("Network Architecture Diagram")
    plt.axis("off")

    img_io = io.BytesIO()
    plt.savefig(img_io, format="png", bbox_inches="tight")
    img_io.seek(0)
    plt.close()
    return img_io
