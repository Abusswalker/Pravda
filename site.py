from app import create_app, db
from app.models import User, Articles

app = create_app()


# flask shell
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Article': Articles}
