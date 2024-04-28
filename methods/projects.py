from models import Project
from .transactions import *


def get_all_projects():
    return Project.query.all()


def find_project_by_id(project_id):
    return Project.query.filter_by(id=project_id).first_or_404()


def find_project_by_name(project_name):
    return Project.query.filter_by(name=project_name).first_or_404()


@transaction
def make_investment(project, user, amount):
    previous_transaction = Transaction.query.filter_by(user_id=user.id, project_id=project.id).first()

    if not previous_transaction:
        make_transaction(user, -1 * amount, 'PC', f'Инвестиция в проект {project.name}', project_id=project.id)
    else:
        previous_transaction.amount = -1 * amount


@transaction
def add_comment(project, user, comment):
    if comment:
        comment = Comment(project_id=project.id, user_id=user.id, text=comment)
        db.session.add(comment)

        return comment
    else:
        raise InsufficientData


def has_investmensts_from(project, user):
    return Transaction.query.filter_by(user_id=user.id, project_id=project.id) is not None
