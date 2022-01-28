from app.extensions import db
from app.models import BaseModel
from datetime import date

class Produto(BaseModel):

    __tablename__ = "produto"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(30))
    sabor = db.Column(db.String(30))
    cod = db.Column(db.String, unique=True)
    preco = db.Column(db.Float)
    fabricacao = db.Column(db.String(10), default=date.today().strftime("%d-%m-%Y"))
    pedido = db.Column(db.Boolean, default = False)

    cart_id = db.Column(db.Integer, db.ForeignKey("cart.id"))

    def json(self):
        return {
            "id": self.id,
            "code": self.cod,
            "nome": self.nome,
            "sabor": self.sabor,
            "preco": self.preco,
            "fabricacao": self.fabricacao,
            "pedido": self.pedido,
            "cart_id": self.cart_id
        }

