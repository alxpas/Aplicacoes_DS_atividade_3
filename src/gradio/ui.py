import gradio as gr
import re
from datetime import datetime
from src.gradio.database import (
    cadastrar_cliente,
    cadastrar_destino,
    cadastrar_venda,
    cadastrar_comentario,
    listar_comentarios
)

# ==========================================
# FUNÇÕES DE VALIDAÇÃO
# ==========================================
def validar_email(email):
    """Verifica se o e-mail possui um formato válido (ex: nome@dominio.com)"""
    padrao = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(padrao, email) is not None

def validar_data(data_str):
    """Verifica se a data está exatamente no formato DD/MM/AAAA"""
    try:
        datetime.strptime(data_str, "%d/%m/%Y")
        return True
    except ValueError:
        return False

# ==========================================
# INTERFACE GRADIO
# ==========================================
def criar_interface():
    with gr.Blocks(title="Agência de Viagens - Web") as app:
        gr.Markdown("# Sistema da Agência de Viagens (Gradio)")
        gr.Markdown("### Siga o fluxo sequencial pelas abas abaixo.")
        
        # Variáveis de estado invisíveis para conectar as abas
        state_cliente_id = gr.State(None)
        state_destino_id = gr.State(None)
        state_venda_concluida = gr.State(False)

        with gr.Tab("1. Cliente (Supabase)"):
            nome_input = gr.Textbox(label="Nome do Cliente")
            email_input = gr.Textbox(label="E-mail")
            btn_cliente = gr.Button("Salvar Cliente")
            
            with gr.Row():
                out_cliente_msg = gr.Textbox(label="Status", interactive=False)
                out_cliente_id = gr.Number(label="ID Gerado (Interno)", interactive=False)
            
            def processar_cliente(nome, email):
                if not nome or not email:
                    return "ERRO: Preencha todos os campos.", None
                if not validar_email(email):
                    return "ERRO: Formato de e-mail inválido. Utilize nome@dominio.com", None
                return cadastrar_cliente(nome, email)

            btn_cliente.click(
                fn=processar_cliente, 
                inputs=[nome_input, email_input], 
                outputs=[out_cliente_msg, state_cliente_id]
            ).then(
                fn=lambda x: x, inputs=state_cliente_id, outputs=out_cliente_id
            )

        with gr.Tab("2. Destino (Supabase)"):
            nome_dest_input = gr.Textbox(label="Nome do Destino")
            pais_input = gr.Textbox(label="País")
            preco_input = gr.Number(label="Preço")
            btn_destino = gr.Button("Salvar Destino")
            
            with gr.Row():
                out_destino_msg = gr.Textbox(label="Status", interactive=False)
                out_destino_id = gr.Number(label="ID Gerado (Interno)", interactive=False)
            
            def processar_destino(nome, pais, preco):
                if not nome or not pais or preco is None:
                    return "ERRO: Preencha todos os campos.", None
                return cadastrar_destino(nome, pais, preco)

            btn_destino.click(
                fn=processar_destino, 
                inputs=[nome_dest_input, pais_input, preco_input], 
                outputs=[out_destino_msg, state_destino_id]
            ).then(
                fn=lambda x: x, inputs=state_destino_id, outputs=out_destino_id
            )

        with gr.Tab("3. Registrar Venda (Supabase)"):
            gr.Markdown("*O Cliente e o Destino serão associados automaticamente baseados nos cadastros anteriores.*")
            data_viagem_input = gr.Textbox(label="Data da Viagem (DD/MM/AAAA)")
            btn_venda = gr.Button("Registrar Venda")
            out_venda = gr.Textbox(label="Status", interactive=False)
            
            def processar_venda(cid, did, data):
                if cid is None:
                    return "ERRO: Você precisa cadastrar o Cliente na Aba 1 primeiro.", False
                if did is None:
                    return "ERRO: Você precisa cadastrar o Destino na Aba 2 primeiro.", False
                if not data:
                    return "ERRO: Informe a data da viagem.", False
                
                # Validação do formato DD/MM/AAAA
                if not validar_data(data):
                    return "ERRO: A data deve estar no formato DD/MM/AAAA (ex: 31/12/2024).", False
                
                # Conversão para o formato padrão do banco de dados (AAAA-MM-DD)
                data_banco = datetime.strptime(data, "%d/%m/%Y").strftime("%Y-%m-%d")
                
                return cadastrar_venda(cid, did, data_banco)

            btn_venda.click(
                fn=processar_venda, 
                inputs=[state_cliente_id, state_destino_id, data_viagem_input], 
                outputs=[out_venda, state_venda_concluida]
            )

        with gr.Tab("4. Inserir Comentário (MongoDB)"):
            com_data = gr.Textbox(label="Data do Comentário (DD/MM/AAAA)")
            com_texto = gr.Textbox(label="Comentário", lines=4)
            btn_comentario = gr.Button("Salvar Comentário")
            out_comentario = gr.Textbox(label="Status", interactive=False)
            
            def processar_comentario_wrapper(cid, did, texto, data, venda_ok):
                # TRAVA DE SEGURANÇA AQUI
                if not venda_ok:
                    return "🛑 TRAVA: É obrigatório terminar de registrar os dados da Venda (Aba 3) antes de deixar um comentário!"
                
                if not texto or not data:
                    return "ERRO: Preencha a data e o texto do comentário."
                
                # Validação do formato DD/MM/AAAA
                if not validar_data(data):
                    return "ERRO: A data do comentário deve estar no formato DD/MM/AAAA."
                
                # Conversão para o formato padrão do banco de dados (AAAA-MM-DD)
                data_banco = datetime.strptime(data, "%d/%m/%Y").strftime("%Y-%m-%d")
                    
                return cadastrar_comentario(cid, did, texto, data_banco)

            btn_comentario.click(
                fn=processar_comentario_wrapper, 
                inputs=[state_cliente_id, state_destino_id, com_texto, com_data, state_venda_concluida], 
                outputs=out_comentario
            )

        with gr.Tab("5. Ver Comentários (MongoDB)"):
            btn_listar = gr.Button("Atualizar Lista de Comentários")
            out_lista = gr.Textbox(label="Comentários Cadastrados", lines=15, interactive=False)
            
            btn_listar.click(fn=listar_comentarios, inputs=[], outputs=out_lista)

    return app