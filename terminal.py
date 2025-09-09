import os
import sys
import subprocess
import json
import pyfiglet
from time import sleep
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt, IntPrompt
from rich.align import Align

console = Console()

CONFIG_FILE = os.path.expanduser("~/.painel_config.json")
BASHRC_FILE = os.path.expanduser("~/.bashrc")

FONT_OPTIONS = {
    1: 'slant', 2: 'starwars', 3: 'banner', 4: 'big',
    5: 'standard', 6: 'puffy', 7: '3d'
}
PANEL_COLORS = ['red', 'green', 'blue', 'yellow', 'purple', 'cyan', 'white']

# --- Salvar / Carregar ---
def salvar_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f)

def carregar_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {
        "name": "Convidado",
        "font": FONT_OPTIONS[1],
        "prompt": "Convidado",
        "password": "",
        "color": "green"
    }

# --- Tela inicial ---
def mostrar_banner(config):
    try:
        f = pyfiglet.Figlet(font=config["font"])
        ascii_art = f.renderText(config["name"])
        banner = Panel(
            Text(ascii_art, style=config["color"], justify="center"),
            style=config["color"]
        )
    except pyfiglet.FontNotFound:
        banner = Panel(Text(f"Banner para {config['name']} (fonte não encontrada)", style="red"))
    console.print(Align.center(banner))

def pedir_senha(config):
    if config.get("password"):
        for _ in range(3):
            senha = Prompt.ask("Digite a senha para acessar", password=True)
            if senha == config["password"]:
                return True
            console.print("[red]Senha incorreta![/red]")
        console.print("[bold red]Acesso negado![/bold red]")
        sys.exit(1)
    return True

# --- Configuração automática para abrir no Termux ---
def configurar_autostart():
    linha_exec = f'python {os.path.abspath(__file__)} --auto\n'
    if os.path.exists(BASHRC_FILE):
        with open(BASHRC_FILE, "r") as f:
            conteudo = f.readlines()
        if linha_exec not in conteudo:
            with open(BASHRC_FILE, "a") as f:
                f.write(f"\n# Painel personalizado\n{linha_exec}")
    else:
        with open(BASHRC_FILE, "w") as f:
            f.write(f"# Painel personalizado\n{linha_exec}")

# --- Menu Principal ---
def main_menu():
    config = carregar_config()

    while True:
        console.print(Panel(
            "[bold cyan]Painel de Personalização do Termux[/bold cyan]",
            subtitle="Escolha uma opção",
            style="green"
        ))

        console.print(f"\n  [1]) Alterar Nome (Atual: [bold green]{config['name']}[/bold green])")
        console.print(f"  [2]) Alterar Fonte do Banner (Atual: [bold green]{config['font']}[/bold green])")
        console.print(f"  [3]) Alterar Cor do Banner (Atual: [bold {config['color']}]{config['color']}[/bold {config['color']}])")
        console.print(f"  [4]) Configurar Senha (Atual: [bold red]{'Não configurada' if not config['password'] else 'Configurada'}[/bold red])")
        console.print(f"  [5]) Alterar Texto do Prompt (Atual: [bold magenta]{config['prompt']}[/bold magenta])")
        console.print("  [6]) Visualizar Painel")
        console.print("  [7]) Sair e Salvar\n")

        choice = IntPrompt.ask("Escolha uma opção", choices=[str(i) for i in range(1, 8)], show_choices=False)

        if choice == 1:
            config["name"] = Prompt.ask("Digite o nome")
        elif choice == 2:
            console.print("\n".join(f"{k}) {v}" for k, v in FONT_OPTIONS.items()))
            esc = IntPrompt.ask("Escolha a fonte", choices=[str(k) for k in FONT_OPTIONS.keys()])
            config["font"] = FONT_OPTIONS[esc]
        elif choice == 3:
            console.print("\n".join(f"{i}) {c}" for i, c in enumerate(PANEL_COLORS, 1)))
            esc = IntPrompt.ask("Escolha a cor", choices=[str(i) for i in range(1, len(PANEL_COLORS)+1)])
            config["color"] = PANEL_COLORS[int(esc)-1]
        elif choice == 4:
            resp = Prompt.ask("Deseja criar senha? (s/n)", choices=["s","n"], default="n")
            if resp == "s":
                senha = Prompt.ask("Digite a senha", password=True)
                confirma = Prompt.ask("Confirme a senha", password=True)
                if senha == confirma:
                    config["password"] = senha
                else:
                    console.print("[red]Senhas não conferem![/red]")
        elif choice == 5:
            config["prompt"] = Prompt.ask("Digite o texto do prompt", default=config["name"])
        elif choice == 6:
            mostrar_banner(config)
            Prompt.ask("\nPressione Enter para voltar")
        elif choice == 7:
            salvar_config(config)
            configurar_autostart()
            console.print("[yellow]Configurações salvas! Ao abrir o Termux já vai mostrar o banner.[/yellow]")
            sleep(2)
            break

# --- Modo auto (quando abrir o Termux) ---
def auto_start():
    config = carregar_config()
    pedir_senha(config)
    mostrar_banner(config)

if __name__ == "__main__":
    if "--auto" in sys.argv:
        auto_start()
    else:
        main_menu()
