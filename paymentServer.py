from flask import Flask, request, render_template, jsonify, redirect

app = Flask(__name__)

# Assume status is defined somewhere in your application
status = True  # Just for demonstration

@app.route('/', methods=['GET'])
def index():
    # Serve HTML template with status
    return render_template('VinchenzoPayment.html', status=status)

@app.route('/api/endpoint', methods=['GET', 'POST'])
def handle_api_request():
    global status

    if request.method == 'GET':
        # Return current status
        return jsonify({'status': status})
    elif request.method == 'POST':
        # Update status with the value from the form
        status = request.form['status'] == 'True'
        return redirect('/')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
