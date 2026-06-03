from app.extensions import db


class Cita(db.Model):

    __tablename__ = "citas"
    __table_args__ = (
    db.UniqueConstraint(
        "id_doctor",
        "fecha",
        name="uq_doctor_fecha"
    ),
)

    id_cita = db.Column(
        db.Integer,
        primary_key=True
    )

    fecha = db.Column(
        db.DateTime,
        nullable=False
    )

    motivo = db.Column(
        db.String(255),
        nullable=False
    )

    estado = db.Column(
        db.String(50),
        nullable=False,
        default="PROGRAMADA"
    )

    id_paciente = db.Column(
        db.Integer,
        nullable=False
    )

    id_doctor = db.Column(
        db.Integer,
        nullable=False
    )

    id_centro = db.Column(
        db.Integer,
        nullable=False
    )

    id_usuario_registra = db.Column(
        db.Integer,
        nullable=False
    )

    def to_dict(self):

        return {
            "id_cita": self.id_cita,
            "fecha": self.fecha.isoformat(),
            "motivo": self.motivo,
            "estado": self.estado,
            "id_paciente": self.id_paciente,
            "id_doctor": self.id_doctor,
            "id_centro": self.id_centro,
            "id_usuario_registra": self.id_usuario_registra
        }