from flask import Flask, request, render_template, jsonify, redirect, url_for

app = Flask(__name__)

# Initial number of customers
current_customers = 0

@app.route('/', methods=['GET'])
def index():
    # Serve HTML template with current number of customers
    return render_template('index.html', current_customers=current_customers)

@app.route('/api/endpoint', methods=['GET', 'POST'])
def handle_api_request():
    global current_customers

    if request.method == 'GET':
        # Return current number of customers in JSON format
        return jsonify({'current_customers': current_customers})
    elif request.method == 'POST':
        # Update current number of customers from POST request
        new_customers = request.form.get('new_customers')
        if new_customers:
            current_customers = int(new_customers)
            # Redirect back to the original page after update
            return redirect(url_for('index'))
        else:
            return 'No new number of customers provided'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
