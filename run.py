from app import app
from app import views

if __name__ == '__main__':
    app.run(
        debug=app.config.get('DEBUG', False),
        host=app.config.get('HOST', 'localhost'),
        port=app.config.get('PORT', 5000)
    )
