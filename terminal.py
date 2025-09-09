import os
import sys
import subprocess

# --- Instalação de dependências ---
def instalar_pacote(pacote):
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", pacote])
    except subprocess.CalledProcessError:
        print(f"Erro ao instalar o pacote: {pacote}. Tente instalar manualmente com 'pip install {pacote}'")
        sys.exit(1)

pacotes_necessarios = ["rich", "pyfiglet"]
for pacote in pacotes_necessarios:
    try:
        __import__(pacote)
    except ImportError:
        print(f"Pacote '{pacote}' não encontrado. Instalando...")
        instalar_pacote(pacote)

# Importações após a verificação
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt, IntPrompt
from rich.align import Align
import pyfiglet
from time import sleep

console = Console()

# --- Configurações globais ---
FONT_OPTIONS = {
    1: 'slant', 2: 'starwars', 3: 'banner', 4: 'big',
    5: 'standard', 6: 'puffy', 7: '3d'
}
PANEL_COLORS = ['red', 'green', 'blue', 'yellow', 'purple', 'cyan', 'white']

# --- Funções do painel ---
def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def show_creator_message():
    clear_screen()
    texto = ("Criado por Doctor Coringa Lunático\n"
             "O mestre das linhas de código obscuras\n"
             "Aperte Enter para continuar...")
    console.print(Panel(texto, title="[bold green]Mensagem do Criador[/bold green]", style="green"))
    input()

def get_name():
    console.print(Panel("Digite seu nome para o banner:", style="bold blue"))
    return Prompt.ask("")

def select_font():
    console.print(Panel("\nEscolha a fonte do banner:\n" +
        "\n".join(f"[cyan]{k}[/cyan]) {v.capitalize()}" for k,v in FONT_OPTIONS.items()), style="green"))
    escolha = IntPrompt.ask("Escolha uma opção", choices=[str(k) for k in FONT_OPTIONS.keys()], show_choices=False)
    return FONT_OPTIONS[escolha]

def select_banner_color():
    console.print(Panel("\nEscolha a cor do banner:\n" +
        "\n".join(f"[{color}]{i}) {color.capitalize()}[/]" for i, color in enumerate(PANEL_COLORS, 1)), style="green"))
    escolha = IntPrompt.ask("Escolha uma opção", choices=[str(i) for i in range(1, len(PANEL_COLORS)+1)], show_choices=False)
    return PANEL_COLORS[int(escolha) - 1]

def ask_password():
    resp = Prompt.ask("Deseja criar uma senha para proteger o Termux? (s/n)", choices=["s", "n"], default="n", show_choices=False)
    if resp.lower() == "s":
        while True:
            senha = Prompt.ask("Digite a senha", password=True)
            confirma = Prompt.ask("Confirme a senha", password=True)
            if senha == confirma:
                return senha
            console.print("[red]Senhas não conferem! Tente novamente.[/]")
    return ""

def get_prompt_name(default_name):
    console.print(Panel("Digite o texto do prompt (linha de comando):", style="bold magenta"))
    texto_prompt = Prompt.ask(f"Texto do prompt (padrão: [bold]{default_name}[/])", default=default_name)
    return texto_prompt

def create_banner(name, font, color):
    try:
        f = pyfiglet.Figlet(font=font)
        ascii_art = f.renderText(name)
        banner = Panel(
            Text(ascii_art, style=color, justify="center"),
            title=f"[{color}]Banner[/]",
            subtitle=f"Fonte: [bold]{font}[/], Cor: [bold]{color}[/]",
            style=color
        )
    except pyfiglet.FontNotFound:
        banner = Panel(Text(f"Banner para {name} (fonte não encontrada)", style="red"))
    return banner

# --- Menu Principal ---
def main_menu():
    current_name = "Convidado"
    current_font = FONT_OPTIONS[1]
    current_prompt_name = current_name
    current_password = ""
    current_color = "green"

    show_creator_message()

    while True:
        clear_screen()
        console.print(Panel(
            "[bold cyan]Painel de Personalização do Termux[/bold cyan]",
            subtitle="Escolha uma opção para personalizar seu terminal",
            style="green"
        ))

        console.print(f"\n  [1]) Alterar Nome (Atual: [bold green]{current_name}[/bold green])")
        console.print(f"  [2]) Alterar Fonte do Banner (Atual: [bold green]{current_font}[/bold green])")
        console.print(f"  [3]) Alterar Cor do Banner (Atual: [bold {current_color}]{current_color}[/bold {current_color}])")
        console.print(f"  [4]) Configurar Senha (Atual: [bold red]{'Não configurada' if not current_password else 'Configurada'}[/bold red])")
        console.print(f"  [5]) Alterar Texto do Prompt (Atual: [bold magenta]{current_prompt_name}[/bold magenta])")
        console.print("  [6]) Visualizar Painel")
        console.print("  [7]) Sair sem Salvar\n")

        choice = IntPrompt.ask("Escolha uma opção", choices=[str(i) for i in range(1, 8)], show_choices=False)

        if choice == 1:
            current_name = get_name()
        elif choice == 2:
            current_font = select_font()
        elif choice == 3:
            current_color = select_banner_color()
        elif choice == 4:
            current_password = ask_password()
        elif choice == 5:
            current_prompt_name = get_prompt_name(current_name)
        elif choice == 6:
            clear_screen()
            banner = create_banner(current_name, current_font, current_color)
            console.print(Align.center(banner))
            Prompt.ask("\nPressione Enter para voltar ao menu")
        elif choice == 7:
            console.print("[yellow]Saindo sem salvar as alterações.[/yellow]\n")
            sleep(2)
            break

if __name__ == "__main__":
    main_menu()
