from blogapp import app
from flask_script import Manager

app = app
manage = Manager(app)

if __name__ == '__main__':
    manage.run()
