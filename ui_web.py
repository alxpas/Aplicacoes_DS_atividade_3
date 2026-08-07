from src.gradio.ui import criar_interface

if __name__ == "__main__":
    # Inicializa a interface criada no módulo src.gradio.ui
    app = criar_interface()
    
    # Executa o servidor local do Gradio
    app.launch()