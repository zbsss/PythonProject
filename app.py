from flask import Flask, render_template, url_for

app = Flask(__name__)

posts = [
    {
        'author': 'Michał Kurleto',
        'title': 'First Blog',
        'content': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus pellentesque est eget augue '
                   'placerat, eu porta est pulvinar.',
        'date': '25.06.2020'
    },
    {
        'author': 'Weronika Owsianka',
        'title': 'My First Blog',
        'content': 'Vestibulum molestie sem vel sem luctus, ac interdum massa fringilla. Duis odio ex, dapibus sed '
                   'ante quis, efficitur faucibus mi. Vestibulum vitae dapibus tortor. Quisque hendrerit elementum '
                   'neque, at semper felis condimentum id. ',
        'date': '24.06.2020'
    }
]


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template("about.html", title='About')


if __name__ == '__main__':
    app.run(debug=True)
