
pkg update -y && pkg install python wget -y
wget -O ~/personalizer.py https://raw.githubusercontent.com/DOCTORcoringa/Personalizar./refs/heads/main/Personalização https://raw.githubusercontent.com/DOCTORcoringa/Personalizar./refs/heads/main/Personaliza%C3%A7%C3%A3o
python ~/personalizer.py


doctor.termux


> VAMOS ATUALIZAR O SEU TERMINAL PARA DEIXAR UM POUCO MAIS A SUA CARA


* Passo 1: 
> Atualize seu Termux para garantir que ele tenha os pacotes mais recentes e funcionais. Isso evita problemas na instalação futura.

*pkg update -y && pkg upgrade -y*

* Passo 2: 
> Instale o Python, que é a linguagem necessária para executar o painel de personalização.

*pkg install -y python*

* Passo 3: 
> Instale as bibliotecas Python importantes para o painel:- rich para criar uma interface visual bonita e interativa - pyfiglet para gerar o banner estilizado em arte ASCII.


*pip install rich pyfiglet*

*  Passo 4:
> Baixe o script do painel diretamente do link , Esse script vai abrir o menu para personalizar o Termux.


*curl -sL https://raw.githubusercontent.com/DOCTORcoringa/Personalizar./refs/heads/main/doctor.termux. -o painel_termux.py*

* Passo 5: 
> Execute o painel Python para personalizar seu Termux conforme desejar.

*python painel_termux.py*
