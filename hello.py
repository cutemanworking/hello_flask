from flask import Flask, render_template
from flask import request
from flask_bootstrap import Bootstrap
app = Flask(__name__)
bootstrap = Bootstrap(app)
@app.route('/')
def index():
#    user_agent = request.headers.get('User-Agent')
#    return '<p>Your browser is {}</p>'.format(user_agent)    
#    return '<h1>HelloWorld!</h1>'
   return render_template('index.html')
@app.route('/user/<name>')
def user(name):
#   return '<h1>Hello, {}!</h1>'.format(name)
   return render_template('user.html', name=name)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(505)
def internal_server_error(e):
    return render_template('500.html'), 500  

if __name__ == '__main__':
    app.run(debug=True)
    