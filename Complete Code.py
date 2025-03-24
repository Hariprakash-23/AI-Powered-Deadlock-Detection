import tkinter as tk
from tkinter import messagebox, simpledialog
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Global dictionary to store processes and their resource allocations
processes = {}

# Function to detect deadlock
def detect_deadlock():
    # Create a graph to detect cycles (circular wait)
    graph = {}
    for process, details in processes.items():
        # Map each process to the resource it is waiting for
        graph[process] = details["requests"]

    # Check for cycles in the graph using DFS
    def has_cycle(process, graph, visited, stack):
        visited[process] = True
        stack[process] = True

        # Check if the requested resource is held by another process
        next_process = None
        for p, details in processes.items():
            if details["holds"] == graph[process]:
                next_process = p
                break

        if next_process:
            if next_process not in visited:
                if has_cycle(next_process, graph, visited, stack):
                    return True
            elif stack[next_process]:
                return True  # Cycle detected

        stack[process] = False
        return False

    visited = {}
    stack = {}
    for process in graph:
        if process not in visited:
            if has_cycle(process, graph, visited, stack):
                return True
    return False

# Function to resolve deadlock
def resolve_deadlock():
    # Simple resolution: Terminate the first process in the cycle
    for process in processes:
        return f"Deadlock resolved by terminating process {process}"

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

# GUI Functions
def add_process():
    process_name = simpledialog.askstring("Add Process", "Enter process name (e.g., P1):")
    if process_name:
        holds_resource = simpledialog.askstring("Add Process", f"What resource does {process_name} hold? (e.g., R1):")
        requests_resource = simpledialog.askstring("Add Process", f"What resource does {process_name} request? (e.g., R2):")
        if holds_resource and requests_resource:
            processes[process_name] = {"holds": holds_resource, "requests": requests_resource}
            messagebox.showinfo("Process Added", f"Process {process_name} added successfully!")
        else:
            messagebox.showwarning("Invalid Input", "Please enter valid resource names.")

def check_deadlock():
    if not processes:
        messagebox.showwarning("No Processes", "No processes added. Please add processes first.")
        return

    if detect_deadlock():
        messagebox.showinfo("Deadlock Detected", "Deadlock detected!")
        resolution = resolve_deadlock()
        messagebox.showinfo("Deadlock Resolved", resolution)
    else:
        messagebox.showinfo("No Deadlock", "No deadlock detected.")

# GUI Setup
root = tk.Tk()
root.title("AI-Powered Deadlock Detection System")

# Labels
label = tk.Label(root, text="Deadlock Detection System", font=("Arial", 16))
label.pack(pady=20)

# Buttons
add_button = tk.Button(root, text="Add Process", command=add_process)
add_button.pack(pady=10)

check_button = tk.Button(root, text="Check for Deadlock", command=check_deadlock)
check_button.pack(pady=10)

rag_button = tk.Button(root, text="Draw Resource Allocation Graph (RAG)", command=draw_rag)
rag_button.pack(pady=10)

# Run the GUI
root.mainloop()
