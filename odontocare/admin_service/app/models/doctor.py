from app.extensions import db


class Doctor(db.Model):

    __tablename__ = "doctores"

    id_doctor = db.Column(
        db.Integer,
        primary_key=True
    )

    id_usuario = db.Column(
        db.Integer,
        db.ForeignKey("usuarios.id_usuario"),
        nullable=True
    )

    nombre = db.Column(
        db.String(100),
        nullable=False
    )

    especialidad = db.Column(
        db.String(100),
        nullable=False
    )

    def to_dict(self):
        return {
            "id_doctor": self.id_doctor,
            "id_usuario": self.id_usuario,
            "nombre": self.nombre,
            "especialidad": self.especialidad
        }