from flask import Flask
from flask import request
from flask import render_template
from SearchInDB import keywords_to_base


app = Flask(__name__)


@app.route('/')
def indexpage():
    html = open('index.html', 'r').read()
    return html


@app.route('/search/')
def show_search():
    results = keywords_to_base(request.args.get('Keywords'))

    return render_template('search.html', pages=results)

if __name__ == '__main__':
    app.run(debug=True)
