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
    previous_transaction = Transaction.query.filter_by(user_id=user.id, project_id=project.id).order_by(
        Transaction.id.desc()).first()

    if previous_transaction:
        make_transaction(user, -1 * previous_transaction.amount, 'PC', f'Отмена инвестиции в проект {project.name}',
                         project_id=project.id)

    make_transaction(user, -1 * amount, 'PC', f'Инвестиция в проект {project.name}', project_id=project.id)


@transaction
def add_comment(project, user, comment):
    if comment:
        comment = Comment(project_id=project.id, user_id=user.id, text=comment)
        db.session.add(comment)

        return comment
    else:
        raise InsufficientData


@transaction
def make_project(name, description, link, users):
    if not name or not description or not link:
        raise InsufficientData

    project = Project(name=name, description=description, link=link)
    db.session.add(project)
    project.users = users
    return project


@transaction
def update_project(project, name, description, link, users):
    project.description = description
    project.name = name
    project.link = link
    project.users = users


def has_investmensts_from(project, user):
    return Transaction.query.filter_by(user_id=user.id, project_id=project.id).first() is not None
