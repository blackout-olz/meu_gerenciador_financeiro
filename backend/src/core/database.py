from src.core.config import Settings
from sqlmodel import Session, create_engine

# Carrega as variáveis de ambientes a partir do .env
settings = Settings()

# Engine do SQLModel: gerencia o pool de conexões nativas com o Supabase
# Pode adicionar `echo=True` para visualizar as queries SQL brutas no terminal durante o dev
engine = create_engine(settings.SUPABASE_URL)

def get_session():
    """
    Gera uma sessão temporária do banco de dados para uso nas rotas da API.

    Injetado nas rotas via 'Depends(get_session)'. O bloco 'with' combinado
    com o 'yield' garante que a conexão abra no início da requisição HTTP
    e seja finalizada com segurança após o retorno da resposta.
    """
    with Session(engine) as session:
        yield session