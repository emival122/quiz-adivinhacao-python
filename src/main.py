import customtkinter as ctk
import winsound
import os
import random

# ================= APARÊNCIA =================
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# ================= PERGUNTAS =================
perguntas = [
    ("Quem desenvolveu GTA?", ["Rockstar",
     "Bandai", "Capcom", "Ubisoft"], "A"),
    ("Maior planeta?", ["Terra", "Marte", "Júpiter", "Saturno"], "C"),
    ("Símbolo do Oxigênio?", ["Ouro", "Oxigênio", "Osmio", "Orto"], "B"),
    ("Quem pintou Mona Lisa?", ["Van Gogh",
     "Picasso", "Da Vinci", "Michelangelo"], "C"),
    ("Capital da França?", ["Berlim", "Madrid", "Paris", "Roma"], "C"),
    ("Maior oceano?", ["Atlântico", "Índico", "Ártico", "Pacífico"], "D"),
    ("Primeira Copa do Brasil?", ["1958", "1962", "1970", "1994"], "A"),
    ("Fórmula da água?", ["CO2", "H2O", "O2", "NaCl"], "B"),
    ("Animal mais rápido?", ["Leão", "Guepardo", "Antílope", "Tigre"], "B"),
    ("Língua mais falada?", ["Inglês", "Mandarim", "Espanhol", "Hindi"], "B"),
    ("Quem foi o primeiro imperador de Roma?", [
     "Júlio César", "Augusto", "Nero", "Calígula"], "B"),
    ("País com mais ilhas?", ["Indonésia",
     "Filipinas", "Suécia", "Japão"], "C"),
    ("Ano da queda de Constantinopla?", ["1204", "1302", "1453", "1492"], "C"),
    ("Quem formulou as leis do movimento?", [
     "Einstein", "Galileu", "Newton", "Tesla"], "C"),
    ("Processo das plantas produzir alimento?", [
     "Respiração", "Fermentação", "Fotossíntese", "Quimiossíntese"], "C"),
    ("Planeta Vermelho?", ["Vênus", "Marte", "Júpiter", "Mercúrio"], "B"),
    ("Quantos continentes existem?", ["5", "6", "7", "8"], "C"),
    ("Maior animal do mundo?", ["Elefante",
     "Tubarão-branco", "Baleia-azul", "Orca"], "C"),
    ("Quem escreveu Dom Quixote?", [
     "Machado de Assis", "Cervantes", "Camões", "Saramago"], "B"),
    ("Menor país do mundo?", [
     "Mônaco", "Malta", "Vaticano", "San Marino"], "C"),
    ("Símbolo químico do ferro?", ["Fe", "Ir", "F", "Fr"], "A"),
    ("Quem descobriu o Brasil?", [
     "Pedro Álvares Cabral", "Cristóvão Colombo", "Vasco da Gama", "Américo Vespúcio"], "A"),
    ("Maior deserto do mundo?", [
     "Saara", "Antártida", "Gobi", "Kalahari"], "B"),
    ("Moeda do Japão?", ["Won", "Yuan", "Iene", "Dólar"], "C"),
    ("Quantos lados tem um hexágono?", ["5", "6", "7", "8"], "B"),
    ("Criador da teoria da relatividade?", [
     "Newton", "Galileu", "Einstein", "Tesla"], "C"),
    ("Órgão que bombeia o sangue?", [
     "Pulmão", "Cérebro", "Coração", "Fígado"], "C"),
    ("Gás essencial para respirar?", [
     "Nitrogênio", "Oxigênio", "Hidrogênio", "CO2"], "B"),
    ("Maior país em território?", ["China", "Canadá", "EUA", "Rússia"], "D"),
    ("Quantos minutos tem uma hora?", ["50", "60", "70", "100"], "B"),
]

# ================= VARIÁVEIS =================
indice = 0
pontos = 0
TEMPO_MAX = 30
tempo_restante = TEMPO_MAX
timer_id = None
perguntas_selecionadas = []
quantidade_perguntas = 10
nome_jogador = "Jogador"
modo_sem_tempo = False
dificuldade_atual = "Fácil"

# ================= JANELA =================
app = ctk.CTk()
app.geometry("950x850")
app.title("QuizMaster")

# ================= FUNÇÕES DE TIMER =================


def iniciar_timer():
    if modo_sem_tempo:
        return
    global tempo_restante
    tempo_restante = TEMPO_MAX
    barra_tempo.set(1)
    atualizar_timer()


def atualizar_timer():
    if modo_sem_tempo:
        return
    global tempo_restante, timer_id
    timer_label.configure(text=f"⏱️ Tempo: {tempo_restante}s")
    barra_tempo.set(tempo_restante / TEMPO_MAX)
    if tempo_restante > 0:
        tempo_restante -= 1
        timer_id = app.after(1000, atualizar_timer)
    else:
        tempo_esgotado()


def cancelar_timer():
    global timer_id
    if timer_id:
        app.after_cancel(timer_id)
        timer_id = None


def tempo_esgotado():
    winsound.Beep(500, 400)
    animacao_erro()
    feedback_label.configure(text="⏰ Tempo esgotado!", text_color="orange")
    app.after(1300, proxima_pergunta)

# ================= ANIMAÇÕES =================


def animacao_acerto():
    frame_pergunta.configure(fg_color="#2ca02c")  # verde
    barra_tempo.configure(progress_color="#2ca02c")
    pulsar_feedback("✅ Acertou!", "green")


def animacao_erro():
    frame_pergunta.configure(fg_color="#d62728")  # vermelho
    barra_tempo.configure(progress_color="#d62728")
    pulsar_feedback(feedback_label.cget("text"), "red")


def pulsar_feedback(texto, cor):
    feedback_label.configure(text=texto, text_color=cor,
                             font=("Arial", 22, "bold"))

    def reduzir():
        feedback_label.configure(font=("Arial", 20, "bold"))
    app.after(300, reduzir)

# ================= PROGRESSO =================


def atualizar_progresso():
    progresso_label.configure(text=f"{indice+1}/{quantidade_perguntas}")

# ================= QUIZ =================


def carregar_pergunta():
    cancelar_timer()
    frame_pergunta.configure(fg_color=COR_PADRAO)
    pergunta_label.configure(text=perguntas_selecionadas[indice][0])
    feedback_label.configure(text="")
    letras = ["A", "B", "C", "D"]
    for i, botao in enumerate(botoes):
        botao.configure(
            text=f"{letras[i]}) {perguntas_selecionadas[indice][1][i]}",
            state="normal",
            fg_color="#1f7a7a",
            hover_color="#3fa3a3"
        )
    atualizar_progresso()
    iniciar_timer()


def responder(opcao):
    global pontos
    cancelar_timer()
    correta = perguntas_selecionadas[indice][2]
    for botao in botoes:
        botao.configure(state="disabled")
    if opcao == correta:
        pontos += 1
        winsound.Beep(900, 200)
        animacao_acerto()
    else:
        winsound.Beep(400, 300)
        animacao_erro()
        feedback_label.configure(
            text=f"❌ Errou! Correta: {correta}", text_color="red")
    app.after(1300, proxima_pergunta)


def proxima_pergunta():
    global indice
    indice += 1
    if indice < quantidade_perguntas:
        carregar_pergunta()
    else:
        finalizar_quiz()

# ================= RANKING =================


def salvar_ranking():
    pasta = "ranking"
    if not os.path.exists(pasta):
        os.makedirs(pasta)
    arquivo = os.path.join(pasta, f"{dificuldade_atual}.txt")

    ranking = []
    if os.path.exists(arquivo):
        with open(arquivo, "r", encoding="utf-8") as f:
            for linha in f:
                if "," in linha:
                    nome, score = linha.strip().split(",")
                    ranking.append((nome, int(score)))

    ranking.append((nome_jogador, pontos))
    ranking.sort(key=lambda x: x[1], reverse=True)
    ranking = ranking[:3]  # mantém só top 3

    with open(arquivo, "w", encoding="utf-8") as f:
        for nome, score in ranking:
            f.write(f"{nome},{score}\n")


def texto_ranking():
    medalhas = ["🥇", "🥈", "🥉"]
    ranking = []
    arquivo = os.path.join("ranking", f"{dificuldade_atual}.txt")
    if os.path.exists(arquivo):
        with open(arquivo, "r", encoding="utf-8") as f:
            for linha in f:
                if "," in linha:
                    nome, score = linha.strip().split(",")
                    ranking.append((nome, int(score)))

    texto = ""
    for i, (nome, score) in enumerate(ranking):
        texto += f"{medalhas[i]} {nome} — {score} pts\n"
    return texto or "Sem ranking ainda"

# ================= FINAL =================


def jogar_novamente():
    frame_ranking.pack_forget()
    frame_menu.pack(pady=30)


def finalizar_quiz():
    cancelar_timer()
    salvar_ranking()
    frame_botoes.pack_forget()
    barra_tempo.pack_forget()
    timer_label.pack_forget()
    pergunta_label.configure(
        text=f"🏁 Fim!\n{nome_jogador}: {pontos}/{quantidade_perguntas}")
    ranking_label.configure(text=texto_ranking())
    frame_ranking.pack(pady=20)

# ================= MENU =================


def escolher_modo(qtd, dif):
    global quantidade_perguntas, dificuldade_atual, nome_jogador
    # garante que não ultrapasse o total
    quantidade_perguntas = min(qtd, len(perguntas))
    dificuldade_atual = dif
    nome_jogador = entrada_nome.get() or "Jogador"
    frame_menu.pack_forget()
    frame_modo.pack(pady=30)


def iniciar_com_tempo(sem_tempo):
    global modo_sem_tempo, perguntas_selecionadas, indice, pontos
    modo_sem_tempo = sem_tempo
    indice = 0
    pontos = 0
    perguntas_selecionadas = random.sample(perguntas, quantidade_perguntas)
    frame_modo.pack_forget()
    frame_botoes.pack(expand=True)
    if not modo_sem_tempo:
        barra_tempo.pack(pady=10)
        timer_label.pack()
    carregar_pergunta()


# ================= UI =================
titulo = ctk.CTkLabel(app, text="QuizMaster", font=("Arial", 36, "bold"))
titulo.pack(pady=20)

# Menu
frame_menu = ctk.CTkFrame(app, corner_radius=20)
frame_menu.pack(pady=30, padx=50, fill="x")
ctk.CTkLabel(frame_menu, text="👤 Nome do jogador",
             font=("Arial", 20)).pack(pady=10)
entrada_nome = ctk.CTkEntry(frame_menu, width=400, font=(
    "Arial", 18), placeholder_text="Digite seu nome...")
entrada_nome.pack(pady=15)
ctk.CTkLabel(frame_menu, text="🎯 Quantidade de perguntas",
             font=("Arial", 18)).pack(pady=10)
ctk.CTkButton(frame_menu, text="10 (Fácil)", height=60, font=(
    "Arial", 18), command=lambda: escolher_modo(10, "Fácil")).pack(pady=5)
ctk.CTkButton(frame_menu, text="20 (Médio)", height=60, font=(
    "Arial", 18), command=lambda: escolher_modo(20, "Médio")).pack(pady=5)
ctk.CTkButton(frame_menu, text="30 (Difícil)", height=60, font=(
    "Arial", 18), command=lambda: escolher_modo(30, "Difícil")).pack(pady=5)

# Modo
frame_modo = ctk.CTkFrame(app, corner_radius=20)
ctk.CTkLabel(frame_modo, text="⏱️ Escolha o modo",
             font=("Arial", 20)).pack(pady=20)
ctk.CTkButton(frame_modo, text="Com tempo", width=300, height=60, font=(
    "Arial", 18), command=lambda: iniciar_com_tempo(False)).pack(pady=10)
ctk.CTkButton(frame_modo, text="Sem tempo", width=300, height=60, font=(
    "Arial", 18), command=lambda: iniciar_com_tempo(True)).pack(pady=10)

# Timer e progresso
timer_label = ctk.CTkLabel(app, text="", font=("Arial", 18))
barra_tempo = ctk.CTkProgressBar(app, width=560)
progresso_label = ctk.CTkLabel(app, text="", font=("Arial", 18))
progresso_label.place(x=820, y=60)  # canto superior direito

# Pergunta
frame_pergunta = ctk.CTkFrame(app, corner_radius=15)
frame_pergunta.pack(padx=30, pady=20, fill="x")
COR_PADRAO = frame_pergunta.cget("fg_color")
pergunta_label = ctk.CTkLabel(frame_pergunta, text="", wraplength=700, font=(
    "Arial", 24, "bold"), justify="center")
pergunta_label.pack(pady=30)
feedback_label = ctk.CTkLabel(app, text="", font=("Arial", 20))
feedback_label.pack(pady=10)

# Botões
frame_botoes = ctk.CTkFrame(app, fg_color="transparent")
botoes = []
for letra in ["A", "B", "C", "D"]:
    botao = ctk.CTkButton(frame_botoes, width=600, height=60, font=(
        "Arial", 18), command=lambda l=letra: responder(l))
    botao.pack(pady=10)
    botoes.append(botao)

# Ranking
frame_ranking = ctk.CTkFrame(app, corner_radius=20)
ranking_label = ctk.CTkLabel(frame_ranking, font=("Arial", 18))
ranking_label.pack(pady=10)
ctk.CTkButton(frame_ranking, text="🔁 Jogar novamente", width=300,
              height=60, font=("Arial", 18), command=jogar_novamente).pack(pady=15)

app.mainloop()
