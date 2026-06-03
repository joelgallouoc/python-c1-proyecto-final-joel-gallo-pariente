from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from app.extensions import db


class Usuario(db.Model):

    __tablename__ = "usuarios"

    id_usuario = db.Column(
        db.Integer,
        primary_key=True
    )

    username = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    password_hash = db.Column(
        db.String(255),
        nullable=False
    )

    rol = db.Column(
        db.String(20),
        nullable=False
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(
            self.password_hash,
            password
        )

    def to_dict(self):
        return {
            "id_usuario": self.id_usuario,
            "username": self.username,
            "rol": self.rol
        }