from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import networkx as nx
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import google.generativeai as genai
import os
import json  # Added missing import
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, static_folder='static')
CORS(app)

# Configure Gemini AI
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
model = genai.GenerativeModel('models/gemini-1.5-pro-latest')


# Global variables
processes = {}

def detect_deadlock():
    if not processes:
        return False
    
    graph = nx.DiGraph()
    for process, details in processes.items():
        graph.add_edge(process, details["requests"])
        graph.add_edge(details["holds"], process)
    
    try:
        return len(list(nx.simple_cycles(graph))) > 0
    except nx.NetworkXNoCycle:
        return False

def generate_rag_image():
    G = nx.DiGraph()
    for process, details in processes.items():
        G.add_node(process, color='#6366f1')  # Indigo
        G.add_node(details["holds"], color='#10b981')  # Emerald
        G.add_node(details["requests"], color='#10b981')  # Emerald
        G.add_edge(details["holds"], process)
        G.add_edge(process, details["requests"])
    
    plt.figure(figsize=(4,3), facecolor='#1e293b')  # Smaller figsize for medium graph
    pos = nx.spring_layout(G, seed=42)
    colors = [G.nodes[node]['color'] for node in G.nodes]
    nx.draw(
        G, pos, with_labels=True, node_color=colors,
        node_size=1600,  # Reduced from 2500
        font_size=10,    # Reduced from 12
        font_weight='bold', arrows=True, 
        arrowstyle='->', arrowsize=15,
        edge_color='white', font_color='white'
    )
    
    ax = plt.gca()
    ax.set_facecolor('#1e293b')
    plt.title("Resource Allocation Graph", fontsize=12, pad=15, color='white')
    
    img = BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight', dpi=100, facecolor=ax.get_facecolor())
    img.seek(0)
    plt.close()
    return base64.b64encode(img.read()).decode('utf-8')


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/processes', methods=['GET', 'POST', 'DELETE'])
def handle_processes():
    if request.method == 'POST':
        data = request.get_json()
        process_name = data.get('process_name')
        holds = data.get('holds_resource')
        requests = data.get('requests_resource')
        
        if not all([process_name, holds, requests]):
            return jsonify({"error": "All fields are required"}), 400
            
        processes[process_name] = {"holds": holds, "requests": requests}
        return jsonify({"success": True, "process": process_name})
    
    elif request.method == 'DELETE':
        processes.clear()
        return jsonify({"success": True})
    
    return jsonify({"processes": processes})

@app.route('/api/detect', methods=['GET'])
def detect():
    has_deadlock = detect_deadlock()
    return jsonify({"deadlock": has_deadlock})

@app.route('/api/visualize', methods=['GET'])
def visualize():
    if not processes:
        return jsonify({"error": "No processes to visualize"}), 400
    return jsonify({"image": generate_rag_image()})

@app.route('/api/resolve', methods=['POST'])
def resolve():
    if not processes:
        return jsonify({"message": "No processes to resolve"})
    
    if detect_deadlock():
        process_to_terminate = min(processes.keys(), key=lambda x: len(processes[x]["holds"]))
        del processes[process_to_terminate]
        return jsonify({
            "resolved": True,
            "terminated": process_to_terminate,
            "processes": processes
        })
    return jsonify({"resolved": False, "message": "No deadlock detected"})

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        
        if not user_message:
            return jsonify({"error": "Message is required"}), 400
        
        # Enhanced prompt for better deadlock analysis
        prompt = f"""You are an expert in operating system deadlocks analyzing this system state:
        {json.dumps(processes, indent=2)}

        User Question: {user_message}

        Provide a comprehensive response with:
        1. Deadlock analysis (present or not)
        2. Explanation of the current situation
        3. Step-by-step resolution if deadlock exists
        4. Prevention techniques
        5. Best practices for resource allocation

        Format your response with clear headings and keep it under 300 words.
        """
        
        response = model.generate_content(prompt)
        return jsonify({"response": response.text})
    
    except Exception as e:
        return jsonify({
            "error": str(e),
            "fallback": "Basic deadlock resolution: Terminate the process holding the fewest resources."
        }), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
