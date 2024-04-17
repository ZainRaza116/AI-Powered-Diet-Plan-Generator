from flask import Flask, request, jsonify
import openai

app = Flask(__name__)

@app.route('/meal_suggestion', methods=['POST'])
def meal_suggestion():
    openai.api_key = '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'

    age = request.json.get('age')
    height = request.json.get('height')
    increase = request.json.get('increase')
    amount = request.json.get('amount')
    unit = request.json.get('unit')
    vegetarian = request.json.get('vegetarian')
    specific_allergies = request.json.get('specific_allergies')
    prompt = f'Hello chat GPT my age is {age} height is {height}cm and I want to {"increase" if increase else "decrease"} my weight by {amount} {unit}, please suggest me  {"vegetarian" if vegetarian else "non-vegetarian"} meal and we are allergic to {specific_allergies} and specify Breakfast, Lunch and Dinner'

    try:
        response = openai.Completion.create(
            engine="gpt-3.5-turbo-instruct",
            prompt=prompt,
            max_tokens=1000
        )
        data = response.choices[0].text.strip()

        breakfast_options = extract_options(data, "Breakfast")
        lunch_options = extract_options(data, "Lunch")
        dinner_options = extract_options(data, "Dinner")
        snacks_options = extract_options(data, "Snacks")

        response_data = {
            "Breakfast": breakfast_options,
            "Lunch": lunch_options,
            "Dinner": dinner_options,
            "Snacks": snacks_options
        }

        return jsonify(response_data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def extract_options(data, meal_title):
    options = []
    start_index = data.find(meal_title) + len(meal_title)
    end_index = data.find("\n\n", start_index) if data.find("\n\n", start_index) != -1 else len(data)
    meal_text = data[start_index:end_index].strip()
    options = meal_text.split("\n- ")[1:]  # Split meal options and remove the first element which is the title itself
    return options


if __name__ == '__main__':
    app.run(debug=True)
