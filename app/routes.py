from app import flaskapp

@flaskapp.route('/')
@flaskapp.route('/index')
def index():
    return "Hello, World!"

@flaskapp.route('/<name>')
def hello_name(name):
    return "\nWelcome, {}.\n\n".format(name)