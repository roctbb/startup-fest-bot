from flask import Blueprint, render_template, request, redirect
from objects.basic_auth import *
from models import *
from methods import *
projects_blueprint = Blueprint('projects', __name__)


@auth.login_required
@projects_blueprint.route('/', methods=['GET'])
def projects():
    list_of_projects = Project.query.all()
    if not list_of_projects:
        return "Erorr"

    return render_template("projects/projects.html", projects=list_of_projects, users=get_all_users())


@auth.login_required
@projects_blueprint.route('/add_project', methods=['POST', 'GET'])
def add_project():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        link = request.form.get('link')
        members = request.form.getlist('members')
        try:
            db.session.add(Project(name=name, description=description, link=link))
            db.session.commit()
        except:
            print("er2")
        project = Project.query.filter_by(name=name).first()
        for member in members:
            user = User.query.filter_by(name=member).first()
            user.projects.append(project)
            db.session.commit()
            print(user.projects)
        return redirect("/projects")

    return render_template('projects/add_project.html', users=get_all_users())


@auth.login_required
@projects_blueprint.route('/edit_description/<int:id>', methods=['POST', 'GET'])
def edit_description(id):
    project = Project.query.filter_by(id=id).first()
    if request.method == 'POST':
        if not project:
            return "Error"
        else:
            description = request.form.get('edit_description')
            members = request.form.getlist('edit_members')
            try:
                project.description = description
                for user in get_all_users():
                    for member in members:
                        for projectt in user.projects:
                            if projectt.id == project.id:
                                if member != user.name:
                                    user.projects.remove(project)
                            else:
                                if member == user.name:
                                    user.projects.append(project)
                db.session.commit()
                return redirect("/projects")
            except:
                print("er3")

    return render_template("projects/edit_description.html", des=project.description, id=id, users=get_all_users())


