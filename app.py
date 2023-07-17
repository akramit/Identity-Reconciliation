from flask import Flask
import dao

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/identify")
def identify():
      return dao.get_all()
      #return "<p> Under Identify<br> </p>"


if __name__ == '__main__':
	app.run(debug=True)