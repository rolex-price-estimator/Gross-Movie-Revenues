from flask import Flask, request, render_template

# declare a flap initialized to a Flask instance
app = Flask(__name__)

# define an endpoint to return the main html form
@app.route('/', methods=['GET'])
def index():
  # render_template looks for files within a 'templates' directory
  # accepts key-word arguments to render in html document
  return render_template("index.html")


# endpoint to make model predictions
@app.route('/predict', methods=['POST'])
def predict():
  return


if __name__ == '__main__':
  # run() method of Flask class runs the application
  # on the local development server.
  app.run()