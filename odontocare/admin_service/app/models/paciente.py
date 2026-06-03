from app.extensions import db


class Paciente(db.Model):

    __tablename__ = "pacientes"

    id_paciente = db.Column(
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

    telefono = db.Column(
        db.String(30),
        nullable=False
    )

    estado = db.Column(
        db.String(20),
        nullable=False,
        default="ACTIVO"
    )

    def to_dict(self):
        return {
            "id_paciente": self.id_paciente,
            "id_usuario": self.id_usuario,
            "nombre": self.nombre,
            "telefono": self.telefono,
            "estado": self.estado
        }