import tkinter as tk
from gui import add_process, check_deadlock
from rag import draw_rag

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
