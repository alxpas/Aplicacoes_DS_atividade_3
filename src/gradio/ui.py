import gradio as gr
from src.gradio.database import (
    cadastrar_cliente,
    cadastrar_destino,
    cadastrar_venda,
    cadastrar_comentario,
    listar_comentarios
)

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
            
            # Ao clicar, atualiza o status visual E guarda o ID no State
            btn_cliente.click(
                fn=cadastrar_cliente, 
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
            
            btn_destino.click(
                fn=cadastrar_destino, 
                inputs=[nome_dest_input, pais_input, preco_input], 
                outputs=[out_destino_msg, state_destino_id]
            ).then(
                fn=lambda x: x, inputs=state_destino_id, outputs=out_destino_id
            )

        with gr.Tab("3. Registrar Venda (Supabase)"):
            gr.Markdown("*O Cliente e o Destino serão associados automaticamente baseados nos cadastros anteriores.*")
            data_viagem_input = gr.Textbox(label="Data da Viagem (AAAA-MM-DD)")
            btn_venda = gr.Button("Registrar Venda")
            out_venda = gr.Textbox(label="Status", interactive=False)
            
            def processar_venda(cid, did, data):
                if cid is None:
                    return "ERRO: Você precisa cadastrar o Cliente na Aba 1 primeiro.", False
                if did is None:
                    return "ERRO: Você precisa cadastrar o Destino na Aba 2 primeiro.", False
                if not data:
                    return "ERRO: Informe a data da viagem.", False
                return cadastrar_venda(cid, did, data)

            btn_venda.click(
                fn=processar_venda, 
                inputs=[state_cliente_id, state_destino_id, data_viagem_input], 
                outputs=[out_venda, state_venda_concluida]
            )

        with gr.Tab("4. Inserir Comentário (MongoDB)"):
            com_data = gr.Textbox(label="Data do Comentário (AAAA-MM-DD)")
            com_texto = gr.Textbox(label="Comentário", lines=4)
            btn_comentario = gr.Button("Salvar Comentário")
            out_comentario = gr.Textbox(label="Status", interactive=False)
            
            def processar_comentario(cid, did, texto, data, venda_ok):
                # TRAVA DE SEGURANÇA AQUI
                if not venda_ok:
                    return "🛑 TRAVA: É obrigatório terminar de registrar os dados da Venda (Aba 3) antes de deixar um comentário!"
                
                if not texto or not data:
                    return "Preencha a data e o texto do comentário."
                    
                return cadastrar_comentario(cid, did, texto, data)

            btn_comentario.click(
                fn=processar_comentario, 
                # Usa os mesmos IDs que vieram da Aba 1 e Aba 2, mais o status da venda da Aba 3
                inputs=[state_cliente_id, state_destino_id, com_texto, com_data, state_venda_concluida], 
                outputs=out_comentario
            )

        with gr.Tab("5. Ver Comentários (MongoDB)"):
            btn_listar = gr.Button("Atualizar Lista de Comentários")
            out_lista = gr.Textbox(label="Comentários Cadastrados", lines=15, interactive=False)
            
            btn_listar.click(fn=listar_comentarios, inputs=[], outputs=out_lista)

    return app