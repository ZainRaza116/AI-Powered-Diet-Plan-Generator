from flask import Flask, request, jsonify
import openai
from openai import OpenAI
from g4f.client import Client

app = Flask(__name__)

@app.route('/meal_suggestion', methods=['POST'])
def meal_suggestion():
    client = Client()
    age = request.json.get('age')
    height = request.json.get('height')
    increase = request.json.get('increase')
    amount = request.json.get('amount')
    unit = request.json.get('unit')
    vegetarian = request.json.get('vegetarian')
    specific_allergies = request.json.get('specific_allergies')
    prompt = f'Hello chat GPT my age is {age}, height is {height}cm and I want to {"increase" if increase else "decrease"} my weight by {amount} {unit}. Please suggest me {"vegetarian" if vegetarian else "non-vegetarian"} meals and I am allergic to {specific_allergies}. Specify options for Breakfast, Lunch, and Dinner.'

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo", 
            messages=[
                {"role": "system", "content": "You are a helpful assistant that provides meal suggestions."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000
        )
        data = response.choices[0].message.content.strip()

        response_data = parse_meal_suggestions(data)

        return jsonify(response_data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def parse_meal_suggestions(data):
    meal_titles = ["Breakfast", "Lunch", "Dinner"]
    parsed_data = {title: [] for title in meal_titles}

    for title in meal_titles:
        start_index = data.find(title)
        if start_index != -1:
            start_index += len(title)
            end_index = min([data.find(next_title, start_index) for next_title in meal_titles if data.find(next_title, start_index) != -1] + [len(data)])
            meal_text = data[start_index:end_index].strip()
            options = [option.strip() for option in meal_text.split('\n') if option.startswith('- ')]
            parsed_data[title] = [option[2:].strip() for option in options]

    return parsed_data


if __name__ == '__main__':
    app.run(debug=True)
