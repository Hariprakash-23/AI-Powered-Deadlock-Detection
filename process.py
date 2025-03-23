import tkinter as tk
from tkinter import messagebox, simpledialog
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Global dictionary to store processes and their resource allocations
processes = {}
