from tkinter import messagebox, simpledialog
from main import processes
from deadlock import detect_deadlock, resolve_deadlock
from rag import draw_rag

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
