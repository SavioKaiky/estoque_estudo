from app import create_app
from database import db
import models.insumo
import models.produto
import models.lote_insumo
import models.ficha_tecnica
import models.movimentacao_insumo
import models.movimentacao_produto
 
app = create_app()
 
with app.app_context():
    db.create_all()
    print("Banco criado com sucesso!")
 