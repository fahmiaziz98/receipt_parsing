from flask import Flask, render_template, request
from vision import get_predictions

app = Flask(__name__)
run_with_ngrok(app)

@app.route('/', methods=['GET', 'POST'])
def index(): 
    if request.method == 'GET':
        return render_template('index.html', predictions=None)
    elif request.method == 'POST' and request.files:
        file_image = request.files['gambar']
        if file_image:
            predictions = get_predictions(file_image)
            return render_template("index.html", predictions=predictions)
    return render_template('index.html', predictions=None)


if __name__ == "__main__":
    app.run(debug=True)
