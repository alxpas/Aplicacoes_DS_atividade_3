import tkinter as tk
from tkinter import ttk, messagebox
import src.desktop.database as db

class AgenciaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Gerenciamento Agência de Viagens")
        self.root.geometry("800x600")

        # Criando o Notebook (Abas)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # Criando as abas
        self.aba_clientes = ttk.Frame(self.notebook)
        self.aba_destinos = ttk.Frame(self.notebook)
        self.aba_vendas = ttk.Frame(self.notebook)

        self.notebook.add(self.aba_clientes, text="Clientes")
        self.notebook.add(self.aba_destinos, text="Destinos")
        self.notebook.add(self.aba_vendas, text="Vendas")

        # Inicializando cada aba
        self.setup_aba_clientes()
        self.setup_aba_destinos()
        self.setup_aba_vendas()

    # ==================== ABA CLIENTES ====================
    def setup_aba_clientes(self):
        # Formulário
        frame_form = tk.LabelFrame(self.aba_clientes, text="Formulário de Cliente", padx=10, pady=10)
        frame_form.pack(fill="x", padx=10, pady=5)

        tk.Label(frame_form, text="ID:").grid(row=0, column=0, sticky="w")
        self.cli_id_var = tk.StringVar()
        tk.Entry(frame_form, textvariable=self.cli_id_var, state="readonly", width=5).grid(row=0, column=1, sticky="w", pady=2)

        tk.Label(frame_form, text="Nome:").grid(row=1, column=0, sticky="w")
        self.cli_nome_var = tk.StringVar()
        tk.Entry(frame_form, textvariable=self.cli_nome_var, width=40).grid(row=1, column=1, sticky="w", pady=2)

        tk.Label(frame_form, text="E-mail:").grid(row=2, column=0, sticky="w")
        self.cli_email_var = tk.StringVar()
        tk.Entry(frame_form, textvariable=self.cli_email_var, width=40).grid(row=2, column=1, sticky="w", pady=2)

        # Botões
        frame_botoes = tk.Frame(self.aba_clientes)
        frame_botoes.pack(fill="x", padx=10, pady=5)
        tk.Button(frame_botoes, text="Cadastrar", command=self.cadastrar_cliente, width=15).pack(side="left", padx=5)
        tk.Button(frame_botoes, text="Atualizar", command=self.atualizar_cliente, width=15).pack(side="left", padx=5)
        tk.Button(frame_botoes, text="Excluir", command=self.excluir_cliente, width=15).pack(side="left", padx=5)
        tk.Button(frame_botoes, text="Limpar Campos", command=self.limpar_clientes, width=15).pack(side="left", padx=5)
        tk.Button(frame_botoes, text="Atualizar Lista", command=self.carregar_clientes, width=15).pack(side="right", padx=5)

        # Treeview
        colunas = ("ID", "Nome", "E-mail")
        self.tree_clientes = ttk.Treeview(self.aba_clientes, columns=colunas, show="headings")
        for col in colunas:
            self.tree_clientes.heading(col, text=col)
        self.tree_clientes.pack(fill="both", expand=True, padx=10, pady=10)
        self.tree_clientes.bind("<ButtonRelease-1>", self.selecionar_cliente)
        
        self.carregar_clientes()

    def limpar_clientes(self):
        self.cli_id_var.set("")
        self.cli_nome_var.set("")
        self.cli_email_var.set("")

    def carregar_clientes(self):
        for item in self.tree_clientes.get_children():
            self.tree_clientes.delete(item)
        try:
            for row in db.listar_clientes():
                self.tree_clientes.insert("", "end", values=(row['id'], row['nome'], row['email']))
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar clientes: {e}")

    def selecionar_cliente(self, event):
        item = self.tree_clientes.selection()
        if item:
            valores = self.tree_clientes.item(item, "values")
            self.cli_id_var.set(valores[0])
            self.cli_nome_var.set(valores[1])
            self.cli_email_var.set(valores[2])

    def cadastrar_cliente(self):
        nome = self.cli_nome_var.get()
        email = self.cli_email_var.get()
        if nome and email:
            try:
                db.criar_cliente(nome, email)
                messagebox.showinfo("Sucesso", "Cliente cadastrado!")
                self.limpar_clientes()
                self.carregar_clientes()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro: {e}")
        else:
            messagebox.showwarning("Aviso", "Preencha nome e e-mail.")

    def atualizar_cliente(self):
        cid = self.cli_id_var.get()
        nome = self.cli_nome_var.get()
        email = self.cli_email_var.get()
        if cid and nome and email:
            try:
                db.atualizar_cliente(cid, nome, email)
                messagebox.showinfo("Sucesso", "Cliente atualizado!")
                self.limpar_clientes()
                self.carregar_clientes()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro: {e}")
        else:
            messagebox.showwarning("Aviso", "Selecione um cliente para atualizar.")

    def excluir_cliente(self):
        cid = self.cli_id_var.get()
        if cid:
            if messagebox.askyesno("Confirmar", "Tem certeza que deseja excluir este cliente?"):
                try:
                    db.excluir_cliente(cid)
                    messagebox.showinfo("Sucesso", "Cliente excluído!")
                    self.limpar_clientes()
                    self.carregar_clientes()
                except Exception as e:
                    messagebox.showerror("Erro", f"Erro: {e}")
        else:
            messagebox.showwarning("Aviso", "Selecione um cliente para excluir.")

    # ==================== ABA DESTINOS ====================
    def setup_aba_destinos(self):
        frame_form = tk.LabelFrame(self.aba_destinos, text="Formulário de Destino", padx=10, pady=10)
        frame_form.pack(fill="x", padx=10, pady=5)

        tk.Label(frame_form, text="ID:").grid(row=0, column=0, sticky="w")
        self.dest_id_var = tk.StringVar()
        tk.Entry(frame_form, textvariable=self.dest_id_var, state="readonly", width=5).grid(row=0, column=1, sticky="w")

        tk.Label(frame_form, text="Nome:").grid(row=1, column=0, sticky="w")
        self.dest_nome_var = tk.StringVar()
        tk.Entry(frame_form, textvariable=self.dest_nome_var, width=30).grid(row=1, column=1, sticky="w")

        tk.Label(frame_form, text="País:").grid(row=2, column=0, sticky="w")
        self.dest_pais_var = tk.StringVar()
        tk.Entry(frame_form, textvariable=self.dest_pais_var, width=30).grid(row=2, column=1, sticky="w")

        tk.Label(frame_form, text="Preço:").grid(row=3, column=0, sticky="w")
        self.dest_preco_var = tk.StringVar()
        tk.Entry(frame_form, textvariable=self.dest_preco_var, width=15).grid(row=3, column=1, sticky="w")

        frame_botoes = tk.Frame(self.aba_destinos)
        frame_botoes.pack(fill="x", padx=10, pady=5)
        tk.Button(frame_botoes, text="Cadastrar", command=self.cadastrar_destino, width=15).pack(side="left", padx=5)
        tk.Button(frame_botoes, text="Atualizar", command=self.atualizar_destino, width=15).pack(side="left", padx=5)
        tk.Button(frame_botoes, text="Excluir", command=self.excluir_destino, width=15).pack(side="left", padx=5)
        tk.Button(frame_botoes, text="Limpar", command=self.limpar_destinos, width=10).pack(side="left", padx=5)
        tk.Button(frame_botoes, text="Atualizar Lista", command=self.carregar_destinos, width=15).pack(side="right", padx=5)

        colunas = ("ID", "Nome", "País", "Preço")
        self.tree_destinos = ttk.Treeview(self.aba_destinos, columns=colunas, show="headings")
        for col in colunas:
            self.tree_destinos.heading(col, text=col)
        self.tree_destinos.pack(fill="both", expand=True, padx=10, pady=10)
        self.tree_destinos.bind("<ButtonRelease-1>", self.selecionar_destino)
        
        self.carregar_destinos()

    def limpar_destinos(self):
        self.dest_id_var.set("")
        self.dest_nome_var.set("")
        self.dest_pais_var.set("")
        self.dest_preco_var.set("")

    def carregar_destinos(self):
        for item in self.tree_destinos.get_children():
            self.tree_destinos.delete(item)
        try:
            for row in db.listar_destinos():
                self.tree_destinos.insert("", "end", values=(row['id'], row['nome'], row['pais'], row['preco']))
        except Exception as e:
            messagebox.showerror("Erro", f"Erro: {e}")

    def selecionar_destino(self, event):
        item = self.tree_destinos.selection()
        if item:
            valores = self.tree_destinos.item(item, "values")
            self.dest_id_var.set(valores[0])
            self.dest_nome_var.set(valores[1])
            self.dest_pais_var.set(valores[2])
            self.dest_preco_var.set(valores[3])

    def cadastrar_destino(self):
        n, pa, pr = self.dest_nome_var.get(), self.dest_pais_var.get(), self.dest_preco_var.get()
        if n and pa and pr:
            try:
                db.criar_destino(n, pa, pr)
                messagebox.showinfo("Sucesso", "Destino cadastrado!")
                self.limpar_destinos()
                self.carregar_destinos()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro: {e}")
        else:
            messagebox.showwarning("Aviso", "Preencha todos os campos.")

    def atualizar_destino(self):
        did, n, pa, pr = self.dest_id_var.get(), self.dest_nome_var.get(), self.dest_pais_var.get(), self.dest_preco_var.get()
        if did:
            try:
                db.atualizar_destino(did, n, pa, pr)
                messagebox.showinfo("Sucesso", "Destino atualizado!")
                self.limpar_destinos()
                self.carregar_destinos()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro: {e}")

    def excluir_destino(self):
        did = self.dest_id_var.get()
        if did and messagebox.askyesno("Confirmar", "Excluir destino?"):
            try:
                db.excluir_destino(did)
                self.limpar_destinos()
                self.carregar_destinos()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro: {e}")

    # ==================== ABA VENDAS ====================
    def setup_aba_vendas(self):
        frame_form = tk.LabelFrame(self.aba_vendas, text="Formulário de Venda", padx=10, pady=10)
        frame_form.pack(fill="x", padx=10, pady=5)

        tk.Label(frame_form, text="ID Venda:").grid(row=0, column=0, sticky="w")
        self.venda_id_var = tk.StringVar()
        tk.Entry(frame_form, textvariable=self.venda_id_var, state="readonly", width=5).grid(row=0, column=1, sticky="w")

        tk.Label(frame_form, text="ID Cliente:").grid(row=1, column=0, sticky="w")
        self.venda_cli_var = tk.StringVar()
        tk.Entry(frame_form, textvariable=self.venda_cli_var, width=10).grid(row=1, column=1, sticky="w")

        tk.Label(frame_form, text="ID Destino:").grid(row=2, column=0, sticky="w")
        self.venda_dest_var = tk.StringVar()
        tk.Entry(frame_form, textvariable=self.venda_dest_var, width=10).grid(row=2, column=1, sticky="w")

        tk.Label(frame_form, text="Data (YYYY-MM-DD):").grid(row=3, column=0, sticky="w")
        self.venda_data_var = tk.StringVar()
        tk.Entry(frame_form, textvariable=self.venda_data_var, width=15).grid(row=3, column=1, sticky="w")

        frame_botoes = tk.Frame(self.aba_vendas)
        frame_botoes.pack(fill="x", padx=10, pady=5)
        tk.Button(frame_botoes, text="Cadastrar", command=self.cadastrar_venda, width=15).pack(side="left", padx=5)
        tk.Button(frame_botoes, text="Atualizar", command=self.atualizar_venda, width=15).pack(side="left", padx=5)
        tk.Button(frame_botoes, text="Excluir", command=self.excluir_venda, width=15).pack(side="left", padx=5)
        tk.Button(frame_botoes, text="Limpar", command=self.limpar_vendas, width=10).pack(side="left", padx=5)
        tk.Button(frame_botoes, text="Atualizar Lista", command=self.carregar_vendas, width=15).pack(side="right", padx=5)

        colunas = ("ID", "ID Cliente", "ID Destino", "Data Viagem")
        self.tree_vendas = ttk.Treeview(self.aba_vendas, columns=colunas, show="headings")
        for col in colunas:
            self.tree_vendas.heading(col, text=col)
        self.tree_vendas.pack(fill="both", expand=True, padx=10, pady=10)
        self.tree_vendas.bind("<ButtonRelease-1>", self.selecionar_venda)
        
        self.carregar_vendas()

    def limpar_vendas(self):
        self.venda_id_var.set("")
        self.venda_cli_var.set("")
        self.venda_dest_var.set("")
        self.venda_data_var.set("")

    def carregar_vendas(self):
        for item in self.tree_vendas.get_children():
            self.tree_vendas.delete(item)
        try:
            for row in db.listar_vendas():
                self.tree_vendas.insert("", "end", values=(row['id'], row['cliente_id'], row['destino_id'], row['data_viagem']))
        except Exception as e:
            messagebox.showerror("Erro", f"Erro: {e}")

    def selecionar_venda(self, event):
        item = self.tree_vendas.selection()
        if item:
            valores = self.tree_vendas.item(item, "values")
            self.venda_id_var.set(valores[0])
            self.venda_cli_var.set(valores[1])
            self.venda_dest_var.set(valores[2])
            self.venda_data_var.set(valores[3])

    def cadastrar_venda(self):
        c, d, dt = self.venda_cli_var.get(), self.venda_dest_var.get(), self.venda_data_var.get()
        if c and d and dt:
            try:
                db.criar_venda(c, d, dt)
                messagebox.showinfo("Sucesso", "Venda cadastrada!")
                self.limpar_vendas()
                self.carregar_vendas()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro: {e}")

    def atualizar_venda(self):
        vid, c, d, dt = self.venda_id_var.get(), self.venda_cli_var.get(), self.venda_dest_var.get(), self.venda_data_var.get()
        if vid:
            try:
                db.atualizar_venda(vid, c, d, dt)
                messagebox.showinfo("Sucesso", "Venda atualizada!")
                self.limpar_vendas()
                self.carregar_vendas()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro: {e}")

    def excluir_venda(self):
        vid = self.venda_id_var.get()
        if vid and messagebox.askyesno("Confirmar", "Excluir venda?"):
            try:
                db.excluir_venda(vid)
                self.limpar_vendas()
                self.carregar_vendas()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro: {e}")