import pandas as pd
from flask import Flask, request, jsonify
import random

data = pd.read_csv('user_data.csv')

app = Flask(__name__)

destinations = [
    {"destination": "Hawaii", "vibe": "Adventure", "average_cost_per_day": 180, "activities": ['hiking', 'beach']},
    {"destination": "Santorini", "vibe": "Relaxation", "average_cost_per_day": 200, "activities": ['spa', 'beach', 'fine dining']},
    {"destination": "Iceland", "vibe": "Adventure", "average_cost_per_day": 150, "activities": ['hiking', 'wildlife']},
    {"destination": "Tokyo", "vibe": "Socializing", "average_cost_per_day": 140, "activities": ['nightlife', 'shopping', 'city tours']},
    {"destination": "Paris", "vibe": "Luxury", "average_cost_per_day": 220, "activities": ['fine dining', 'shopping']},
    {"destination": "Thailand", "vibe": "Budget", "average_cost_per_day": 70, "activities": ['street food', 'beach', 'temples']}
]

def recommend_itinerary(user_id):
    # Get user profile
    user = data[data['user_id'] == user_id].iloc[0]

    user_vibe = user['vibe']
    user_expenses = user['expenses']
    previous_destinations = eval(user['previous_destinations'])
    favorite_activities = eval(user['favorite_activities'])

    suitable_destinations = [
        d for d in destinations
        if d['vibe'] == user_vibe and d['average_cost_per_day'] <= user_expenses and d['destination'] not in previous_destinations
    ]
    final_recommendations = [
        d for d in suitable_destinations
        if any(activity in d['activities'] for activity in favorite_activities)
    ]
    
    if not final_recommendations:
        final_recommendations = random.sample(destinations, 1)

    return final_recommendations

@app.route('/itinerary', methods=['GET'])
def get_itinerary():
    user_id = int(request.args.get('user_id'))
    if user_id not in data['user_id'].values:
        return jsonify({"error": "User ID not found"}), 404

    itinerary = recommend_itinerary(user_id)
    
    return jsonify(itinerary)

if __name__ == '__main__':
    app.run(debug=True)
