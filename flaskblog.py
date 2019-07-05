from flask import Flask, render_template
app = Flask(__name__)

Title = "Nice Title"

posts = [
	{
		'author': "Jhon",
		'title': "title1",
		'content': "Nice post",
		'date_posted': "April 20,2019"
	},
	{
		'author': 'Jhon the 2',
		'title': 'title2',
		'content': "Nice post2",
		'date_posted': "April 22,2019"
	}

]

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html',posts=posts, title=Title )


@app.route("/about")
def about():
    return render_template('about.html', title=Title )


if __name__ == '__main__':
    app.run(debug=True)