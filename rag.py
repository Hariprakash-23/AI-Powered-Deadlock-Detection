import networkx as nx
import matplotlib.pyplot as plt
from main import processes

# Function to draw the Resource Allocation Graph (RAG)
def draw_rag():
    G = nx.DiGraph()  # Directed graph for RAG

    # Add nodes and edges to the graph
    for process, details in processes.items():
        # Add process node
        G.add_node(process, color='lightblue')
        # Add resource node
        resource_held = details["holds"]
        G.add_node(resource_held, color='lightgreen')
        # Add edge from resource to process (resource held by process)
        G.add_edge(resource_held, process)

        # Add edge from process to requested resource
        resource_requested = details["requests"]
        G.add_node(resource_requested, color='lightgreen')
        G.add_edge(process, resource_requested)

    # Draw the graph
    pos = nx.spring_layout(G)  # Layout for the graph
    colors = [G.nodes[node]['color'] for node in G.nodes]
    nx.draw(G, pos, with_labels=True, node_color=colors, node_size=2000, font_size=10, font_weight='bold', arrows=True)
    plt.title("Resource Allocation Graph (RAG)")
    plt.show()
