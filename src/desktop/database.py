import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

url_supabase = os.environ.get("URL_SUPABASE")
key_supabase = os.environ.get("ANON_KEY")
supabase: Client = create_client(url_supabase, key_supabase)


# funções CRUD conectadas ao Supabase, reaproveitando as mesmas tabelas (clientes, destinos, vendas) #

# ==================== CLIENTES ====================
def listar_clientes():
    return supabase.table("clientes").select("*").order("id").execute().data

def criar_cliente(nome, email):
    supabase.table("clientes").insert({"nome": nome, "email": email}).execute()

def atualizar_cliente(cliente_id, nome, email):
    supabase.table("clientes").update({"nome": nome, "email": email}).eq("id", cliente_id).execute()

def excluir_cliente(cliente_id):
    supabase.table("clientes").delete().eq("id", cliente_id).execute()

# ==================== DESTINOS ====================
def listar_destinos():
    return supabase.table("destinos").select("*").order("id").execute().data

def criar_destino(nome, pais, preco):
    supabase.table("destinos").insert({"nome": nome, "pais": pais, "preco": float(preco)}).execute()

def atualizar_destino(destino_id, nome, pais, preco):
    supabase.table("destinos").update({"nome": nome, "pais": pais, "preco": float(preco)}).eq("id", destino_id).execute()

def excluir_destino(destino_id):
    supabase.table("destinos").delete().eq("id", destino_id).execute()

# ==================== VENDAS ====================
def listar_vendas():
    return supabase.table("vendas").select("*").order("id").execute().data

def criar_venda(cliente_id, destino_id, data_viagem):
    supabase.table("vendas").insert({
        "cliente_id": int(cliente_id), 
        "destino_id": int(destino_id), 
        "data_viagem": data_viagem
    }).execute()

def atualizar_venda(venda_id, cliente_id, destino_id, data_viagem):
    supabase.table("vendas").update({
        "cliente_id": int(cliente_id), 
        "destino_id": int(destino_id), 
        "data_viagem": data_viagem
    }).eq("id", venda_id).execute()

def excluir_venda(venda_id):
    supabase.table("vendas").delete().eq("id", venda_id).execute()