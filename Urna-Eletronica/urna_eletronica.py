import tkinter as tk
from tkinter import messagebox
from datetime import datetime

candidatos = []
votacao_ativa = False

FONTE_TITULO = ("Helvetica", 16, "bold")
FONTE_PADRAO = ("Helvetica", 12)
COR_FUNDO = "#f0f8ff"
COR_BOTAO = "#4682b4"
COR_TEXTO_BOTAO = "white"

janela = tk.Tk()
janela.title("Urna Eletrônica - SENAI 'Morvan Figueiredo'")
janela.configure(bg=COR_FUNDO)

def mostra_menu():
    janela.geometry("400x300") # Define o tamanho da janela principal
    janela.configure(padx=20, pady=20) # Adiciona margem grande

    label_menu = tk.Label(janela, text="Urna Eletrônica", font=FONTE_TITULO, bg=COR_FUNDO)
    label_menu.pack(pady=15) # Espaçamento entre o rótulo e os botões

    botao_cadastro = tk.Button(janela, text="Cadastro de Candidato", font=FONTE_PADRAO, bg=COR_BOTAO, fg=COR_TEXTO_BOTAO, command=cadastra_candidato)
    botao_cadastro.pack(pady=8, ipadx=10, ipady=3) # Espaçamento entre os botões

    botao_votacao = tk.Button(janela, text="Iniciar Votação", font=FONTE_PADRAO, bg=COR_BOTAO, fg=COR_TEXTO_BOTAO, command=iniciar_votacao)
    botao_votacao.pack(pady=8, ipadx=10, ipady=3)

    botao_encerrar = tk.Button(janela, text="Encerrar Votação", font=FONTE_PADRAO, bg=COR_BOTAO, fg=COR_TEXTO_BOTAO, command=encerrar_votacao)
    botao_encerrar.pack(pady=8, ipadx=10, ipady=3)

def cadastra_candidato():
    janela_cadastro = tk.Toplevel(janela)
    janela_cadastro.title("Cadastro de Candidato")
    janela_cadastro.geometry("400x300")
    janela_cadastro.configure(bg=COR_FUNDO)

    tk.Label(janela_cadastro, text="Número do Candidato:", font=FONTE_PADRAO, bg=COR_FUNDO).pack(pady=5)
    entrada_numero = tk.Entry(janela_cadastro, font=FONTE_PADRAO)
    entrada_numero.pack(pady=5)

    tk.Label(janela_cadastro, text="Nome do Candidato:", font=FONTE_PADRAO, bg=COR_FUNDO).pack(pady=5)
    entrada_nome = tk.Entry(janela_cadastro, font=FONTE_PADRAO)
    entrada_nome.pack(pady=5)

    tk.Label(janela_cadastro, text="Partido do Candidato:", font=FONTE_PADRAO, bg=COR_FUNDO).pack(pady=5)
    entrada_partido = tk.Entry(janela_cadastro, font=FONTE_PADRAO)
    entrada_partido.pack(pady=5)

    def salvar_candidato():
        numero = entrada_numero.get()
        nome = entrada_nome.get()
        partido = entrada_partido.get()
        candidatos.append({"numero": numero, "nome": nome, "partido": partido, "votos": 0})
        messagebox.showinfo("Sucesso", "Candidato cadastrado com sucesso!")
        janela_cadastro.destroy()

    botao_salvar = tk.Button(janela_cadastro, text="Salvar", font=FONTE_PADRAO, bg=COR_BOTAO, fg=COR_TEXTO_BOTAO, command=salvar_candidato)
    botao_salvar.pack(pady=10, ipadx=10, ipady=3)

def iniciar_votacao():
    global votacao_ativa
    votacao_ativa = True
    registrar_voto()

def registrar_voto():
    if not votacao_ativa:
        messagebox.showwarning("Votação Inativa", "A Votação ainda não foi iniciada!")
        return
    
    janela_votacao = tk.Toplevel(janela)
    janela_votacao.title("Votação")
    janela_votacao.geometry("400x300")
    janela_votacao.configure(bg=COR_FUNDO)

    tk.Label(janela_votacao, text="Digite seu Título de Eleitor:", font=FONTE_PADRAO, bg=COR_FUNDO).pack(pady=5)
    entrada_matricula = tk.Entry(janela_votacao, font=FONTE_PADRAO)
    entrada_matricula.pack(pady=5)

    tk.Label(janela_votacao, text="Digite o Número do Candidato:", font=FONTE_PADRAO, bg=COR_FUNDO).pack(pady=5)
    entrada_voto = tk.Entry(janela_votacao, font=FONTE_PADRAO)
    entrada_voto.pack(pady=5)
        
    def confirmar_voto():
        matricula = entrada_matricula.get()
        voto = entrada_voto.get()
            
        if not matricula:
            messagebox.showwarning("Erro", "Digite o seu Título de Eleitor.")
            return

        candidato_escolhido = next((c for c in candidatos if c["numero"] == voto), None)
            
        if candidato_escolhido:
            confirmar = messagebox.askyesno(
                "Confirmação", 
                f"Confirmar Voto para {candidato_escolhido['nome']} ({candidato_escolhido['partido']})?"
            )

            if confirmar:
                candidato_escolhido["votos"] += 1
                messagebox.showinfo("Sucesso", "Voto Registrado com Sucesso!")
                janela_votacao.destroy()
                registrar_voto()

        else:
            confirmar = messagebox.askyesno("Confirmação", "Candidato Inexistente. Confirmar Voto Nulo?")
            if confirmar:
                messagebox.showinfo("Sucesso", "Voto Nulo Registrado!")
                janela_votacao.destroy()
                registrar_voto()

    botao_votar = tk.Button(janela_votacao, text="Votar", font=FONTE_PADRAO, bg=COR_BOTAO, fg=COR_TEXTO_BOTAO, command=confirmar_voto)
    botao_votar.pack(pady=10, ipadx=10, ipady=3)

def imprime_relatorio():
    janela_relatorio = tk.Toplevel(janela)
    janela_relatorio.title("Resultados")
    janela_relatorio.geometry("400x300")
    janela_relatorio.configure(bg=COR_FUNDO)

    total_votos = sum(c["votos"] for c in candidatos)
    if total_votos > 0:
        for candidato in candidatos:
            tk.Label(
                janela_relatorio,
                text=f"{candidato['nome']} ({candidato['partido']}): {candidato['votos']} votos",
                font=FONTE_PADRAO,
                bg=COR_FUNDO
            ).pack(pady=5)
    else:
        tk.Label(janela_relatorio, text="Não houve votos válidos.", font=FONTE_PADRAO, bg=COR_FUNDO).pack(pady=5)

    botao_fechar = tk.Button(janela_relatorio, text="Fechar", font=FONTE_PADRAO, bg=COR_BOTAO, fg=COR_TEXTO_BOTAO, command=janela_relatorio.destroy)
    botao_fechar.pack(pady=10, ipadx=10, ipady=3)

    # EXPORTAÇÃO PARA ARQUIVO .TXT COM DATA E HORA NO NOME
    data_hora = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    nome_arquivo = f"resultado_eleicao_{data_hora}.txt"
    with open(nome_arquivo, "w", encoding="utf-8") as arquivo:
        arquivo.write("RESULTADO DA ELEIÇÃO - URNA ELETRÔNICA SENAI\n\n")
        if total_votos > 0:
            for candidato in candidatos:
                linha = f"{candidato['nome']} ({candidato['partido']}): {candidato['votos']} votos\n"
                arquivo.write(linha)
        else:
            arquivo.write("Não Houve Votos Válidos.\n")

def encerrar_votacao():
    global votacao_ativa
    votacao_ativa = False
    imprime_relatorio()

mostra_menu()
janela.mainloop()