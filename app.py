from flask import Flask, render_template, request, jsonify, session
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Needed for session management

@app.route('/')
def index():
    # Start a new game
    session['number'] = random.randint(1, 10)
    session['attempts_left'] = 7
    return render_template('index.html')

@app.route('/guess', methods=['POST'])
def guess():
    if 'number' not in session or 'attempts_left' not in session:
        return jsonify({'status': 'error', 'message': 'Game not started'}), 400

    data = request.get_json()
    try:
        guess = int(data['guess'])
    except (ValueError, TypeError):
        return jsonify({'status': 'error', 'message': 'Invalid input'}), 400

    if guess < 1 or guess > 10:
        return jsonify({'status': 'error', 'message': 'Enter number between 1 and 10'}), 400

    session['attempts_left'] -= 1
    number = session['number']

    if guess == number:
        return jsonify({'status': 'win', 'message': '🎉 Correct! You guessed the number!'})
    elif session['attempts_left'] == 0:
        return jsonify({'status': 'lose', 'message': f'❌ Game over! The number was {number}.'})
    elif guess < number:
        return jsonify({'status': 'continue', 'message': '🔻 Too low!'})
    else:
        return jsonify({'status': 'continue', 'message': '🔺 Too high!'})

if __name__ == '__main__':
    app.run(debug=True)
