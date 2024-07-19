from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Configuração do banco de dados
engine = create_engine('sqlite:///exemplo_sqlalchemy.db')
Base = declarative_base()

# Definição do modelo
class Usuario(Base):
    __tablename__ = 'usuarios'
    id = Column(Integer, primary_key=True)
    nome = Column(String)

# Criação das tabelas
Base.metadata.create_all(engine)

# Criação de uma sessão
Session = sessionmaker(bind=engine)
session = Session()

# Inserção de dados
novo_usuario = Usuario(nome='Ana')
session.add(novo_usuario)
session.commit()

# Consulta de dados
usuarios = session.query(Usuario).all()
for usuario in usuarios:
    print(usuario.nome)

# Fechamento da sessão
session.close()
