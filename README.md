#AgriRoute PS

AgriRoute PS is a web-based application that optimizes the transportation of agricultural produce from farms to distribution centers via hubs. It implements two algorithms for route optimization: a greedy approach and a novel route selection strategy.

Features

Dynamic Route Optimization: Determines the most cost-effective and time-efficient routes.

Greedy Algorithm: Chooses the nearest available hub and center within constraints.

Novel Algorithm: Considers multiple routes before selecting the most optimal one.

Visualization: Displays the optimized routes and comparative cost/time analysis using Matplotlib.

Flask-Based Web Interface: Allows users to input farm, hub, and center details.

Technologies Used

Flask - Web framework for the application.

Pandas & NumPy - Data handling and processing.

Matplotlib - Visualization of optimized routes.

HTML/CSS - Frontend for user interaction.

Installation and Setup

Prerequisites

Ensure you have Python installed (Python 3.x recommended). Install required dependencies using:

pip install flask pandas numpy matplotlib

Running the Application

Navigate to the project directory.

Run the Flask application:

python app.py

Open a browser and go to http://127.0.0.1:5000/ to access the web interface.

Usage

Enter the number of farms, hubs, and distribution centers.

Submit the form to generate optimized routes.

View the plotted routes and comparative cost/time analysis.

Project Structure

/AgriRoute-PS
│── app.py              # Main Flask application
│── templates/          # HTML templates
│   ├── index.html      # User input form
│   ├── result.html     # Displays results & visualizations
│── static/             # CSS & JavaScript files
│── README.md           # Project documentation

License

This project is licensed under the MIT License.

Contributors

[HEMANT PATHAK]

Feel free to modify and extend the project as needed!
