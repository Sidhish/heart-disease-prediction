from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.form
        # Mock prediction logic
        risk_level = "Low" if int(data['age']) < 50 else "High"
        return jsonify({
            'status': 'success',
            'prediction': f"Risk Level: {risk_level}",
            'details': dict(data)
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)