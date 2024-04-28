from .alchemy import db

project_user = db.Table('project_user',
                           db.Column('project_id', db.Integer, db.ForeignKey('project.id', ondelete="CASCADE")),
                           db.Column('user_id', db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"))
                           )