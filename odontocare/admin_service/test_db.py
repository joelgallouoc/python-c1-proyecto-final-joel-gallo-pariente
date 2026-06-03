from app import create_app
from app.extensions import db
from app.models.usuario import Usuario

app = create_app()

with app.app_context():

    usuario = Usuario(
        username="admin",
        rol="ADMIN"
    )

    usuario.set_password("admin123")

    db.session.add(usuario)
    db.session.commit()

    print(usuario.to_dict())