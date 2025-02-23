from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/summarize', methods=['POST'])
def summarize():
    try:
        data = request.get_json()
        document = data.get('document', '')
        
        if not document:
            return jsonify({'error': 'No document provided'}), 400

        # Placeholder for AI summarization logic
        summary = f"Summarized Content: {document[:200]}..."  # Mock summary

        return jsonify({'summary': summary})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

