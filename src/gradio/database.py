import os
from dotenv import load_dotenv
from supabase import create_client, Client
from pymongo import MongoClient

load_dotenv()

# --- Configuração Supabase ---
url_supabase = os.environ.get("URL_SUPABASE")
key_supabase = os.environ.get("ANON_KEY")
supabase: Client = create_client(url_supabase, key_supabase)

# --- Configuração MongoDB Atlas ---
mongo_uri = os.environ.get("MONGODB_URI")
mongo_client = MongoClient(mongo_uri)
db_mongo = mongo_client["agencia_viagens"]
comentarios_collection = db_mongo["comentarios"]

# ==========================================
# FUNÇÕES SUPABASE (POSTGRESQL)
# ==========================================
def cadastrar_cliente(nome, email):
    try:
        resultado = supabase.table("clientes").insert({"nome": nome, "email": email}).execute()
        # Captura o ID do cliente recém-inserido
        cliente_id = resultado.data[0]['id']
        return f"Sucesso: Cliente cadastrado!", cliente_id
    except Exception as e:
        return f"Erro ao cadastrar cliente: {str(e)}", None

def cadastrar_destino(nome, pais, preco):
    try:
        resultado = supabase.table("destinos").insert({
            "nome": nome, 
            "pais": pais, 
            "preco": float(preco)
        }).execute()
        # Captura o ID do destino recém-inserido
        destino_id = resultado.data[0]['id']
        return f"Sucesso: Destino cadastrado!", destino_id
    except Exception as e:
        return f"Erro ao cadastrar destino: {str(e)}", None

def cadastrar_venda(cliente_id, destino_id, data_viagem):
    try:
        resultado = supabase.table("vendas").insert({
            "cliente_id": int(cliente_id),
            "destino_id": int(destino_id),
            "data_viagem": data_viagem
        }).execute()
        return "Sucesso: Venda registrada!", True
    except Exception as e:
        return f"Erro ao registrar venda: {str(e)}", False

# ==========================================
# FUNÇÕES MONGODB ATLAS (NOSQL)
# ==========================================
def cadastrar_comentario(cliente_id, destino_id, texto, data):
    try:
        documento = {
            "cliente_id": int(cliente_id),
            "destino_id": int(destino_id),
            "texto": texto,
            "data": data
        }
        comentarios_collection.insert_one(documento)
        return "Sucesso: Comentário registrado no MongoDB!"
    except Exception as e:
        return f"Erro ao salvar comentário: {str(e)}"

def listar_comentarios():
    try:
        comentarios = list(comentarios_collection.find({}, {"_id": 0}))
        
        if not comentarios:
            return "Nenhum comentário encontrado."
        
        texto_formatado = ""
        for c in comentarios:
            texto_formatado += (
                f"Data: {c.get('data')} | Cliente ID: {c.get('cliente_id')} | Destino ID: {c.get('destino_id')}\n"
                f"Comentário: {c.get('texto')}\n"
                f"{'-'*50}\n"
            )
        return texto_formatado
    except Exception as e:
        return f"Erro ao buscar comentários: {str(e)}"