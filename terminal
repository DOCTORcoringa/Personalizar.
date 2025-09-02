import subprocess
import sys

# Função para instalar pacotes automaticamente
def instalar_pacote(pacote):
    subprocess.check_call([sys.executable, "-m", "pip", "install", pacote])

# Verifica e instala dependências
pacotes_necessarios = ["rich", "pyfiglet"]
for pacote in pacotes_necessarios:
    try:
        __import__(pacote)
    except ImportError:
        print(f"Pacote '{pacote}' não encontrado. Instalando...")
        instalar_pacote(pacote)

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.prompt import Prompt
from rich.align import Align
from time import sleep
import pyfiglet
import random
import os

console = Console()

cores_disponiveis = ["red", "green", "yellow", "blue", "magenta", "cyan", "white"]
fontes_disponiveis = ["3-d", "3x5", "5lineoblique", "acrobatic", "alligator", "slant", "starwars"]

def efeito_digitando(texto, delay=0.05):
    for char in texto:
        print(char, end="", flush=True)
        sleep(delay)
    print()

def gerar_banner(nome, estilo, cor):
    ascii_art = pyfiglet.figlet_format(nome, font=estilo)
    texto_colorido = Text(ascii_art, style=cor)
    return texto_colorido

def painel_escolha(opcoes, titulo):
    table = Table(title=titulo, box=None)
    table.add_column("Opção", justify="center")
    for i, opcao in enumerate(opcoes, 1):
        cor = random.choice(cores_disponiveis)
        table.add_row(f"[{cor}]{i}[/] - {opcao}")
    console.print(table)
    escolha = Prompt.ask(f"Digite o número da sua escolha para {titulo}")
    try:
        idx = int(escolha) - 1
        if 0 <= idx < len(opcoes):
            return opcoes[idx]
        else:
            return None
    except:
        return None

def painel_monitoramento(cor_cpu, cor_mem, cor_disco):
    content = Text()
    content.append("CPU: 45% de uso\n", style=cor_cpu)
    content.append("Memória: 60% usada\n", style=cor_mem)
    content.append("Espaço em disco: 70% ocupado\n", style=cor_disco)
    panel = Panel(content, title=Text("Painel Estilizado", style="bold magenta", justify="center"), border_style="bright_blue")
    return panel

def painel_interativo():
    console.clear()
    efeito_digitando("Bem-vindo ao seu painel personalizado!", 0.07)

    nome = Prompt.ask("Digite o seu nome para o banner ASCII")

    estilo = painel_escolha(fontes_disponiveis, "estilo da fonte para o nome")
    while estilo is None:
        console.print("Escolha inválida, tente novamente.", style="bold red")
        estilo = painel_escolha(fontes_disponiveis, "estilo da fonte para o nome")

    cor_nome = painel_escolha(cores_disponiveis, "cor do nome")
    while cor_nome is None:
        console.print("Escolha inválida, tente novamente.", style="bold red")
        cor_nome = painel_escolha(cores_disponiveis, "cor do nome")

    cor_cpu = painel_escolha(cores_disponiveis, "cor CPU")
    cor_mem = painel_escolha(cores_disponiveis, "cor Memória")
    cor_disco = painel_escolha(cores_disponiveis, "cor Disco")

    banner = gerar_banner(nome, estilo, cor_nome)
    painel = painel_monitoramento(cor_cpu, cor_mem, cor_disco)

    console.clear()
    console.print(Align.center(banner))
    console.print(Align.center(painel))

    opcao_salvar = Prompt.ask("Deseja salvar essa configuração e sair? (s/n)")
    if opcao_salvar.lower() == "s":
        with open("config.txt", "w") as f:
            f.write(f"{nome}\n{estilo}\n{cor_nome}\n{cor_cpu}\n{cor_mem}\n{cor_disco}\n")
        console.print("Configuração salva! Feche e abra o Termux para ver o painel automaticamente.", style="bold green")
    else:
        console.print("Configuração não salva.", style="bold yellow")

def carregar_e_mostrar_painel():
    if not os.path.isfile("config.txt"):
        console.print("Nenhuma configuração salva encontrada. Rode o painel interativo para criar uma.", style="bold red")
        return
    with open("config.txt", "r") as f:
        nome = f.readline().strip()
        estilo = f.readline().strip()
        cor_nome = f.readline().strip()
        cor_cpu = f.readline().strip()
        cor_mem = f.readline().strip()
        cor_disco = f.readline().strip()
    banner = gerar_banner(nome, estilo, cor_nome)
    painel = painel_monitoramento(cor_cpu, cor_mem, cor_disco)
    console.clear()
    console.print(Align.center(banner))
    console.print(Align.center(painel))

def main():
    if os.path.isfile("config.txt") and Prompt.ask("Deseja carregar painel salvo? (s/n)").lower() == "s":
        carregar_e_mostrar_painel()
    else:
        painel_interativo()

if __name__ == "__main__":
    main()
