from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Equipo(db.Model):
    __tablename__ = 'equipos'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)  # Contraseña del equipo
    avatar = db.Column(db.String(255), nullable=True)  # Ruta del avatar (o URL)
    
    def __init__(self, nombre, password, avatar=None):
        self.nombre = nombre
        self.password = password
        self.avatar = avatar
    
    def __repr__(self):
        return f'<Equipo {self.nombre}>'

    @classmethod
    def crear_equipo(cls, nombre, password, avatar=None):
        nuevo_equipo = cls(nombre=nombre, password=password, avatar=avatar)
        db.session.add(nuevo_equipo)
        db.session.commit()
        return nuevo_equipo
    
    @classmethod
    def obtener_todos(cls):
        return cls.query.all()
    
    @classmethod
    def obtener_por_id(cls, equipo_id):
        return cls.query.get(equipo_id)
    
    @classmethod
    def eliminar_equipo(cls, equipo_id):
        equipo = cls.query.get(equipo_id)
        if equipo:
            db.session.delete(equipo)
            db.session.commit()
            return True
        return False
