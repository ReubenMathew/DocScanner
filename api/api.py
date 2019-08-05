from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def hello():
	return render_template('hello.html')

@app.route('/image')
def get_image():
	return "<img src='/static/test.jpg'/>"

if __name__ == "__main__":
    app.run('localhost',5000,debug=True)
