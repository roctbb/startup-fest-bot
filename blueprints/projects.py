from flask import Blueprint, render_template, request, redirect
from objects.basic_auth import *
from methods import *

projects_blueprint = Blueprint('projects', __name__)


@auth.login_required
@projects_blueprint.route('/', methods=['GET'])
def projects():
    return render_template("projects/list.html", projects=get_all_projects())


@auth.login_required
@projects_blueprint.route('/add', methods=['POST', 'GET'])
@transaction
def add_project():
    name = request.form.get('name', '')
    description = request.form.get('description', '')
    link = request.form.get('link', '')
    members = request.form.getlist('members')
    error = ''

    if request.method == 'POST':
        try:
            project_users = [find_user_by_id(user_id) for user_id in members]
            make_project(name, description, link, members, project_users)

            return redirect("/projects")
        except NotFound:
            error = 'Пользователь не найден!'
        except:
            error = 'Заполните все поля!'

    return render_template('projects/add.html', error=error, users=get_all_users(), name=name, description=description,
                           link=link, members=members)


@auth.login_required
@projects_blueprint.route('/edit/<int:project_id>', methods=['POST', 'GET'])
@transaction
def edit_project(project_id):
    project = find_project_by_id(project_id)
    error = ''

    if request.method == 'POST':
        try:
            description = request.form.get('description', '')
            name = request.form.get('name', '')
            members = request.form.getlist('members')
            link = request.form.get('link', '')

            project_users = [find_user_by_id(user_id) for user_id in members]
            update_project(project, name, description, link, project_users)

            return redirect("/projects")
        except NotFound:
            error = 'Пользователь не найден!'
        except:
            error = 'Заполните все поля!'
    else:
        description = project.description
        name = project.name
        link = project.link
        members = [user.id for user in project.users]

    return render_template("projects/edit.html", project=project, name=name, description=description, link=link,
                           users=get_all_users(), members=members, error=error)
