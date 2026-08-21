from pydantic_settings import BaseSettings, SettingsConfigDict

# Classe para carregar variáveis do .env
## A ideia é não expor segredos no código (como a senha do banco de dados na hora de fazer a conexão)
class Settings(BaseSettings):
    SUPABASE_URL: str
    
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')
    # Poderia adicionar "extra='ignore'" se tivesse variáveis de ambiente que eu não quero carregar por algum motivo
    ## Vou tentar deixar no .env só o que é realmente útil