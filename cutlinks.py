from app import application, db
from app.models import Users, Clicks, Links, TreeLinks


@application.shell_context_processor
def make_shell_context():
    return {'db': db, 'Users': Users, 'Clicks': Clicks,
            'Links': Links, 'TreeLinks': TreeLinks}
