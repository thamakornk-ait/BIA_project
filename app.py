from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('homepage.html')

@app.route('/detection', methods=['GET', 'POST'])
def detection():
    if request.method == 'POST':
        pass
    return render_template('detection.html')

@app.route('/dashboard')
def dashboard():

    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(debug=True)
