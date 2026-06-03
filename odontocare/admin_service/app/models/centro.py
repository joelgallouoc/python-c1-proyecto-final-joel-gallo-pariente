from app.extensions import db


class Centro(db.Model):

    __tablename__ = "centros"

    id_centro = db.Column(
        db.Integer,
        primary_key=True
    )

    nombre = db.Column(
        db.String(100),
        nullable=False
    )

    direccion = db.Column(
        db.String(255),
        nullable=False
    )

    def to_dict(self):
        return {
            "id_centro": self.id_centro,
            "nombre": self.nombre,
            "direccion": self.direccion
        }