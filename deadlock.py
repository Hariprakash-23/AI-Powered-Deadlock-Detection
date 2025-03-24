from main import processes

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
