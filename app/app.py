from flask import Flask, request, jsonify, render_template
import data
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/get-answer', methods=['POST'])
def get_answer():
    request_body = request.get_json()
    query = request_body.get('query')
    answer, references = data.get_answer(query)
    # Process the query and generate an answer and references
    # This is a placeholder - you'll need to replace this with your actual search processing logic

    return jsonify(answer=answer, references=references)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
