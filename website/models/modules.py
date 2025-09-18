from website.app import db
from datetime import datetime

MolduleList = [
    {"name": "productmanager"}
]

class Modules(db.Model):
    __tablename__ = "modules"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False, unique=True)
    create_at = db.Column(db.DateTime(timezone=True), default=datetime.now())

def addModules():

    for module in MolduleList:
        print(module['name'])
        if not Modules.query.filter_by(name=module['name']).first():
            moduledb = Modules(name=module['name'])
            db.session.add(moduledb)
            db.session.commit()
            print("Admin user created: admin@example.com / admin123")
        else:
            print("Admin already exists.")