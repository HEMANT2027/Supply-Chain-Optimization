# AgriRoute PS

AgriRoute PS is a web-based application that optimizes the transportation of agricultural produce from farms to distribution centers via hubs. It implements two algorithms for route optimization: a greedy approach and a novel route selection strategy.

---

## Features

* **Dynamic Route Optimization**: Determines the most cost-effective and time-efficient routes.
* **Greedy Algorithm**: Chooses the nearest available hub and center within constraints.
* **Novel Algorithm**: Considers multiple routes before selecting the most optimal one.
* **Visualization**: Displays the optimized routes and comparative cost/time analysis using Matplotlib.
* **Flask-Based Web Interface**: Allows users to input farm, hub, and center details.

---

## Technologies Used

* **Flask** - Web framework for the application.
* **Pandas & NumPy** - Data handling and processing.
* **Matplotlib** - Visualization of optimized routes.
* **HTML/CSS** - Frontend for user interaction.

---

## Installation and Setup

### Prerequisites

Ensure you have Python installed (Python 3.x recommended). Install the required dependencies using pip:

```bash
pip install flask pandas numpy matplotlib
