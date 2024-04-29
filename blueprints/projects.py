from flask import Blueprint, render_template, request, redirect
from objects.basic_auth import *
from methods import *
projects_blueprint = Blueprint('projects', __name__)


@auth.login_required
@projects_blueprint.route('/', methods=['GET'])
def projects():
    return render_template("projects/projects.html", projects=get_all_projects(), users=get_all_users())


@auth.login_required
@projects_blueprint.route('/add_project', methods=['POST', 'GET'])
@transaction
def add_project():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        link = request.form.get('link')
        members = request.form.getlist('members')
        project = make_project(name, description, link, members)
        for member in members:
            user = find_user_by_name(member)
            if not user:
                return render_template('projects/error.html', error='Пользователь не найден.')
            user.projects.append(project)
        return redirect("/projects")

    return render_template('projects/add_project.html', users=get_all_users())


@auth.login_required
@projects_blueprint.route('/edit_description/<int:id>', methods=['POST', 'GET'])
@transaction
def edit_description(id):
    project = Project.query.filter_by(id=id).first_or_404()
    if request.method == 'POST':
        description = request.form.get('edit_description')
        members = request.form.getlist('edit_members')
        change_description(description, project)
        for member in members:
            member2 = find_user_by_name(member)
            if project not in member2.projects:
                member2.projects.append(project)
            for user in get_all_users():
                if project in user.projects:
                    for pr in user.projects:
                        if pr.id == project.id:
                            if member2.name != user.name and user.name not in members:
                                user.projects.remove(project)

        return redirect("/projects")

    return render_template("projects/edit_description.html", des=project.description, id=id, users=get_all_users())


