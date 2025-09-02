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

pacotes_necessarios = ["rich", "pyfiglet", "psutil"]
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
import psutil
from time import sleep

console = Console()

# --- Configurações globais ---
FONT_OPTIONS = {
    1: 'slant', 2: 'starwars', 3: 'banner', 4: 'big',
    5: 'standard', 6: 'puffy', 7: '3d'
}
PANEL_COLORS = ['red', 'green', 'blue', 'yellow', 'purple', 'cyan', 'white']
PSUTIL_COLORS = {
    'cpu': 'green',
    'memory': 'cyan',
    'disk': 'magenta'
}
HOME_DIR = os.path.expanduser("~")

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
    while True:
        try:
            escolha = IntPrompt.ask("Escolha uma opção", choices=[str(k) for k in FONT_OPTIONS.keys()], show_choices=False)
            return FONT_OPTIONS[escolha]
        except (KeyError, ValueError):
            console.print("[red]Opção inválida! Tente novamente.[/]")

def select_color(item):
    console.print(Panel(f"\nEscolha a cor para o {item}:\n" +
        "\n".join(f"[{color}]{i}) {color.capitalize()}[/]" for i, color in enumerate(PANEL_COLORS, 1)), style="green"))
    while True:
        try:
            escolha = IntPrompt.ask("Escolha uma opção", choices=[str(i) for i in range(1, len(PANEL_COLORS)+1)], show_choices=False)
            return PANEL_COLORS[int(escolha) - 1]
        except (ValueError, IndexError):
            console.print("[red]Opção inválida! Tente novamente.[/]")

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

def create_banner_and_panel(name, font, panel_colors):
    # Gerar banner
    try:
        f = pyfiglet.Figlet(font=font)
        ascii_art = f.renderText(name)
        banner = Panel(
            Text(ascii_art, justify="center"),
            title=f"[{panel_colors['cpu']}]Banner[/]",
            subtitle=f"Fonte: [bold]{font}[/]",
            style=panel_colors['cpu']
        )
    except pyfiglet.FontNotFound:
        console.print(f"[red]Erro: Fonte '{font}' não encontrada. Tente outra.[/red]")
        banner = Panel(Text(f"Banner para {name} (fonte não encontrada)"), style='red')

    # Obter dados reais do sistema
    cpu_percent = psutil.cpu_percent(interval=1)
    mem_percent = psutil.virtual_memory().percent
    disk_percent = psutil.disk_usage('/').percent

    content = Text()
    content.append(f"CPU: {cpu_percent}% de uso\n", style=panel_colors['cpu'])
    content.append(f"Memória: {mem_percent}% usada\n", style=panel_colors['memory'])
    content.append(f"Espaço em disco: {disk_percent}% ocupado\n", style=panel_colors['disk'])

    system_info_panel = Panel(
        content,
        title=Text("Informações do Sistema", style="bold magenta", justify="center"),
        border_style="bright_blue"
    )

    return banner, system_info_panel

def save_bashrc(name, font, prompt_name, senha, panel_colors):
    # Conteúdo do .bashrc
    bashrc_content = f"""
clear
# Arquivo .bashrc gerado pelo painel de personalização do Termux
# Criado por Doctor Coringa Lunático

# Mensagem de introdução (digitando)
typed_text() {{
  texto="$1"
  delay=${{2:-0.03}}
  for ((i=0; i<${{#texto}}; i++)); do
    echo -n "${{texto:i:1}}"
    sleep $delay
  done
  echo ""
}}
if [ ! -f "$HOME/.termux_msg_flag" ]; then
  typed_text "Aqui começa sua jornada hacker."
  touch "$HOME/.termux_msg_flag"
  sleep 1
  clear
fi

# Banner
figlet -f "{font}" "{name}"

# Senha de proteção
if [ ! -z "{senha}" ]; then
  for i in {{1..3}}; do
    read -s -p "Digite a senha para continuar: " input_senha
    echo
    if [ "$input_senha" = "{senha}" ]; then
      break
    else
      echo "Senha incorreta. Tente novamente."
    fi
    if [ $i -eq 3 ]; then
      echo "Falha na autenticação, saindo..."
      exit 1
    fi
  done
fi

# Informações do sistema
clear
figlet -f "{font}" "{name}"
echo ""
echo "\\[\\033[1;32m\\]--- Informações do Sistema ---\\[\\033[0m\\]"
echo "\\[\\033[1;31m\\]CPU:\\[\\033[0m\\] $(termux-info | grep 'CPU' | sed 's/  CPU architecture: //g')"
echo "\\[\\033[1;32m\\]Memória:\\[\\033[0m\\] $(free -m | grep Mem | awk '{{print $2}}') MB"
echo "\\[\\033[1;33m\\]Armazenamento:\\[\\033[0m\\] $(df -h /data | grep /dev/root | awk '{{print $4}}') livre"
echo ""

# Prompt estilizado
export PS1="\\[\\033[1;32m\\]{prompt_name} \\[\\033[0m\\]\\$ "
"""

    bashrc_path = os.path.join(HOME_DIR, ".bashrc")
    try:
        with open(bashrc_path, "w") as file:
            file.write(bashrc_content)
        return True
    except IOError:
        console.print("[bold red]Erro: Não foi possível escrever no arquivo .bashrc. Verifique as permissões.[/bold red]")
        return False

# --- Menu Principal ---
def main_menu():
    current_name = "Convidado"
    current_font = FONT_OPTIONS[1]
    current_prompt_name = current_name
    current_password = ""
    current_colors = PSUTIL_COLORS.copy()

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
        console.print(f"  [3]) Alterar Cores do Painel (Atual: CPU=[{current_colors['cpu']}], MEM=[{current_colors['memory']}], DISK=[{current_colors['disk']}])")
        console.print(f"  [4]) Configurar Senha (Atual: [bold red]{'Não configurada' if not current_password else 'Configurada'}[/bold red])")
        console.print(f"  [5]) Alterar Texto do Prompt (Atual: [bold magenta]{current_prompt_name}[/bold magenta])")
        console.print("  [6]) Visualizar Painel")
        console.print("  [7]) Salvar e Sair")
        console.print("  [8]) Sair sem Salvar\n")

        choice = IntPrompt.ask("Escolha uma opção", choices=[str(i) for i in range(1, 9)], show_choices=False)

        if choice == 1:
            current_name = get_name()
        elif choice == 2:
            current_font = select_font()
        elif choice == 3:
            current_colors['cpu'] = select_color("CPU")
            current_colors['memory'] = select_color("Memória")
            current_colors['disk'] = select_color("Disco")
        elif choice == 4:
            current_password = ask_password()
        elif choice == 5:
            current_prompt_name = get_prompt_name(current_name)
        elif choice == 6:
            clear_screen()
            banner, system_info_panel = create_banner_and_panel(current_name, current_font, current_colors)
            console.print(Align.center(banner))
            console.print(Align.center(system_info_panel))
            Prompt.ask("\nPressione Enter para voltar ao menu")
        elif choice == 7:
            clear_screen()
            if save_bashrc(current_name, current_font, current_prompt_name, current_password, current_colors):
                console.print("[green]Configuração salva! Reinicie o Termux para aplicar.[/green]\n")
                sleep(2)
            break
        elif choice == 8:
            console.print("[yellow]Saindo sem salvar as alterações.[/yellow]\n")
            sleep(2)
            break

if __name__ == "__main__":
    main_menu()
    
