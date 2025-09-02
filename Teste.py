import subprocess
from rich.console import Console
from rich.panel import Panel

console = Console()

def executar_comando(comando):
    try:
        resultado = subprocess.run(comando, shell=True, check=True, text=True, capture_output=True)
        if resultado.stdout:
            console.print(resultado.stdout)
    except subprocess.CalledProcessError:
        mensagem = "> Doctor Coringa infor VOCÊ 🫵 COLOCOU UM COMANDO INVÁLIDO"
        painel = Panel(mensagem, style="bold red", title="Erro")
        console.print(painel)

def main():
    console.print("[bold green]Mini Terminal Personalizado no Termux[/bold green]")
    while True:
        comando = console.input("[bold blue]Digite um comando[/bold blue] (ou 'sair' para fechar): ")
        if comando.lower() == "sair":
            console.print("[bold yellow]Encerrando o terminal personalizado...[/bold yellow]")
            break
        executar_comando(comando)

if __name__ == "__main__":
    main()
