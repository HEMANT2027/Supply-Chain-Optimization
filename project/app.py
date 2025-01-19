from flask import Flask, render_template, request
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import io
import base64

app = Flask(__name__)

# Create the "static/images" folder if it doesn't exist
os.makedirs("static/images", exist_ok=True)

# Function to generate data
def generate_plots(NUM_FARMS, NUM_HUBS, NUM_CENTERS):
    
    # [Previous data generation code remains the same]\
    farms = pd.DataFrame({
    "id": range(1, NUM_FARMS + 1),
    "location_x": np.random.uniform(100, 2000, NUM_FARMS),
    "location_y": np.random.uniform(100, 2000, NUM_FARMS),
    "produce_quantity": np.random.randint(500, 1000, NUM_FARMS),
    "perishability_window": np.random.randint(10, 100, NUM_FARMS)
    })

    # Generate Hubs Data
    hubs = pd.DataFrame({
    "id": range(1, NUM_HUBS + 1),
    "location_x": np.random.uniform(10, 2000, NUM_HUBS),
    "location_y": np.random.uniform(10, 2000, NUM_HUBS),
    "capacity": np.random.randint(1000, 2000, NUM_HUBS),
    "fixed_cost": np.random.randint(500, 1500, NUM_HUBS),
    "current_load": np.zeros(NUM_HUBS)  # Track current load at each hub
    })

    # Generate Centers Data
    centers = pd.DataFrame({
    "id": range(1, NUM_CENTERS + 1),
    "location_x": np.random.uniform(700, 2000, NUM_CENTERS),
    "location_y": np.random.uniform(700, 2000, NUM_CENTERS),
    "demand": np.random.randint(400, 1500, NUM_CENTERS),
    "deadline": np.random.randint(3, 100, NUM_CENTERS),
    "received_quantity": np.zeros(NUM_CENTERS)  # Track received quantity at each center
    })
    
    farms.to_csv('./static/farms.csv', index=False)
    hubs.to_csv('./static/hubs.csv', index=False)
    centers.to_csv('./static/centers.csv', index=False)

    # Print CSV file paths
    print("Datasets saved as CSV files:")
    print("- Farms dataset: farms.csv")
    print("- Hubs dataset: hubs.csv")
    print("- Centers dataset: centers.csv")

    def calculate_distance(loc1, loc2):
        return np.sqrt((loc1[0] - loc2[0])**2 + (loc1[1] - loc2[1])**2)

    class HubCapacityTracker:
        def __init__(self, hubs):
            self.hub_loads = {hub['id']: 0 for _, hub in hubs.iterrows()}
            self.hub_capacities = {hub['id']: hub['capacity'] for _, hub in hubs.iterrows()}
        
        def can_add_to_hub(self, hub_id, quantity):
            return self.hub_loads[hub_id] + quantity <= self.hub_capacities[hub_id]
        
        def add_to_hub(self, hub_id, quantity):
            if self.can_add_to_hub(hub_id, quantity):
                self.hub_loads[hub_id] += quantity
                return True
            return False

    # [Include your find_optimal_routes and novel_routes functions here]
    # Greedy Algorithm
    def find_optimal_routes(farms, hubs, centers):
        optimal_routes = []
        hub_tracker = HubCapacityTracker(hubs)
        center_received = {center['id']: 0 for _, center in centers.iterrows()}
        
        # Sort farms by perishability window (process more urgent shipments first)
        farms_sorted = farms.sort_values('perishability_window')
        
        for _, farm in farms_sorted.iterrows():
            best_route = None
            min_cost = float('inf')
            farm_quantity = farm['produce_quantity']
            
            # Try all possible hub combinations
            for _, hub in hubs.iterrows():
                if not hub_tracker.can_add_to_hub(hub['id'], farm_quantity):
                    continue
                    
                for _, center in centers.iterrows():
                    farm_hub_dist = calculate_distance(
                        [farm['location_x'], farm['location_y']],
                        [hub['location_x'], hub['location_y']]
                    )
                    hub_center_dist = calculate_distance(
                        [hub['location_x'], hub['location_y']],
                        [center['location_x'], center['location_y']]
                    )
                    farm_hub_time = farm_hub_dist / 30
                    hub_center_time = hub_center_dist / 30
                    total_time = farm_hub_time + hub_center_time
                    
                    if (total_time <= farm['perishability_window'] and 
                        total_time <= center['deadline']):
                        
                        farm_hub_cost = farm_hub_dist * 5
                        hub_center_cost = hub_center_dist * 8
                        total_cost = farm_hub_cost + hub_center_cost + hub['fixed_cost']
                        
                        if total_cost < min_cost:
                            min_cost = total_cost
                            best_route = {
                                'farm_id': int(farm['id']),
                                'hub_id': int(hub['id']),
                                'center_id': int(center['id']),
                                'farm_coords': (farm['location_x'], farm['location_y']),
                                'hub_coords': (hub['location_x'], hub['location_y']),
                                'center_coords': (center['location_x'], center['location_y']),
                                'total_cost': float(total_cost),
                                'total_time': float(total_time),
                                'quantity': int(farm_quantity)
                            }
            
            if best_route:
                hub_tracker.add_to_hub(best_route['hub_id'], best_route['quantity'])
                center_received[best_route['center_id']] += best_route['quantity']
                optimal_routes.append(best_route)
        
        return optimal_routes

    # Novel Algorithm
    def novel_routes(farms, hubs, centers):
        all_routes = []
        hub_tracker = HubCapacityTracker(hubs)
        center_received = {center['id']: 0 for _, center in centers.iterrows()}
        
        for _, farm in farms.iterrows():
            for _, hub in hubs.iterrows():
                for _, center in centers.iterrows():
                    farm_hub_dist = calculate_distance(
                        [farm['location_x'], farm['location_y']],
                        [hub['location_x'], hub['location_y']]
                    )
                    hub_center_dist = calculate_distance(
                        [hub['location_x'], hub['location_y']],
                        [center['location_x'], center['location_y']]
                    )
                    total_time = (farm_hub_dist + hub_center_dist) / 30
                    
                    if (total_time <= farm['perishability_window'] and 
                        total_time <= center['deadline']):
                        
                        total_cost = (farm_hub_dist * 5 + hub_center_dist * 8 + hub['fixed_cost'])
                        all_routes.append({
                            'farm_id': int(farm['id']),
                            'hub_id': int(hub['id']),
                            'center_id': int(center['id']),
                            'farm_coords': (farm['location_x'], farm['location_y']),
                            'hub_coords': (hub['location_x'], hub['location_y']),
                            'center_coords': (center['location_x'], center['location_y']),
                            'total_cost': float(total_cost),
                            'total_time': float(total_time),
                            'quantity': int(farm['produce_quantity'])
                        })
        
        all_routes.sort(key=lambda x: x['total_cost'])
        selected_routes = []
        
        for route in all_routes:
            if (hub_tracker.can_add_to_hub(route['hub_id'], route['quantity']) and
                center_received[route['center_id']] + route['quantity'] <= centers.loc[route['center_id'] - 1, 'demand']):
                
                hub_tracker.add_to_hub(route['hub_id'], route['quantity'])
                center_received[route['center_id']] += route['quantity']
                selected_routes.append(route)
        
        return selected_routes

    def get_plot_as_base64(figure):
        img = io.BytesIO()
        figure.savefig(img, format='png', bbox_inches='tight')
        img.seek(0)
        return base64.b64encode(img.getvalue()).decode()

    # Calculate routes using both algorithms
    greedy_routes = find_optimal_routes(farms, hubs, centers)
    novel_routes_result = novel_routes(farms, hubs, centers)  # Renamed to avoid naming conflict

    # Calculate costs and times
    greedy_total_cost = sum(route['total_cost'] for route in greedy_routes)
    novel_total_cost = sum(route['total_cost'] for route in novel_routes_result)
    
    greedy_avg_time = np.mean([route['total_time'] for route in greedy_routes])
    novel_avg_time = np.mean([route['total_time'] for route in novel_routes_result])

    plots = []

    # Generate and save the first plot (Greedy Algorithm Routes)
    plt.figure(figsize=(10, 10))
    plt.scatter(farms['location_x'], farms['location_y'], c='blue', label='Farms', alpha=0.6, s=100)
    plt.scatter(hubs['location_x'], hubs['location_y'], c='green', label='Hubs', alpha=0.6, s=150)
    plt.scatter(centers['location_x'], centers['location_y'], c='red', label='Centers', alpha=0.6, s=200)
    
    # Plot Greedy Routes
    for route in greedy_routes:
        # Farm to Hub
        plt.plot(
            [route['farm_coords'][0], route['hub_coords'][0]], 
            [route['farm_coords'][1], route['hub_coords'][1]], 'b-', alpha=0.3
        )
        # Hub to Center
        plt.plot(
            [route['hub_coords'][0], route['center_coords'][0]], 
            [route['hub_coords'][1], route['center_coords'][1]], 'r-', alpha=0.3
        )
    
    plt.title(f'Greedy Algorithm Routes\nTotal Cost: ₹{greedy_total_cost:,.2f}')
    plt.legend()
    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    plt.grid(alpha=0.3)
    plots.append(get_plot_as_base64(plt.gcf()))
    plt.close()

    # Generate and save the second plot (Novel Algorithm Routes)
    plt.figure(figsize=(10, 10))
    plt.scatter(farms['location_x'], farms['location_y'], c='blue', label='Farms', alpha=0.6, s=100)
    plt.scatter(hubs['location_x'], hubs['location_y'], c='green', label='Hubs', alpha=0.6, s=150)
    plt.scatter(centers['location_x'], centers['location_y'], c='red', label='Centers', alpha=0.6, s=200)
    
    # Plot Novel Routes
    for route in novel_routes_result:
        # Farm to Hub
        plt.plot(
            [route['farm_coords'][0], route['hub_coords'][0]], 
            [route['farm_coords'][1], route['hub_coords'][1]], 'b-', alpha=0.3
        )
        # Hub to Center
        plt.plot(
            [route['hub_coords'][0], route['center_coords'][0]], 
            [route['hub_coords'][1], route['center_coords'][1]], 'r-', alpha=0.3
        )
    
    plt.title(f'Novel Algorithm Routes\nTotal Cost: ₹{novel_total_cost:,.2f}')
    plt.legend()
    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    plt.grid(alpha=0.3)
    plots.append(get_plot_as_base64(plt.gcf()))
    plt.close()

    # Generate and save the comparison plots
    plt.figure(figsize=(10, 5))
    
    # Cost comparison
    plt.subplot(1, 2, 1)
    plt.bar(['Greedy', 'Novel'], [greedy_total_cost, novel_total_cost], color=['blue', 'green'])
    plt.title('Total Cost Comparison')
    plt.ylabel('Total Cost (₹)')
    
    # Time comparison
    plt.subplot(1, 2, 2)
    plt.bar(['Greedy', 'Novel'], [greedy_avg_time, novel_avg_time], color=['blue', 'green'])
    plt.title('Average Delivery Time Comparison')
    plt.ylabel('Average Time (hours)')
    plt.tight_layout()
    
    plots.append(get_plot_as_base64(plt.gcf()))
    plt.close()

    return plots

# Flask Routes
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
        # Get form input
            num_farms = int(request.form["num_farms"])
            num_hubs = int(request.form["num_hubs"])
            num_centers = int(request.form["num_centers"])

        # Generate data and create plots
            plots = generate_plots(num_farms, num_hubs, num_centers)

        # Redirect to the results page
            return render_template("results.html",plots=plots)
        except ValueError:
            return render_template('index.html', error="Please enter valid numbers")
    
    return render_template("index.html")

@app.route("/results")
def results():
    return render_template("results.html")

if __name__ == "__main__":
    app.run(debug=True)
