from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('homepage.html')

@app.route('/detection', methods=['GET', 'POST'])
def detection():
    if request.method == 'POST':
        # Here you would have your detection logic
        # For demonstration, let's assume detection is caught
        detection_caught = True

        if detection_caught:
            # Send signal to client side to show notification
            return jsonify({'message': 'Detection caught!'})
    return render_template('detection.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(debug=True)
