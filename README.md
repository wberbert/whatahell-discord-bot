Aqui está o README atualizado com as novas informações:

---

# Whatahell Discord Bot

O **Whatahell Discord Bot** é um bot para Project Zomboid desenvolvido em Python. Ele automatiza tarefas no jogo, incluindo comandos RCON, verificação de atualizações de mods e reinício automático do servidor após as atualizações. Este bot foi criado para ajudar administradores de servidores a gerenciar e manter seu servidor de Project Zomboid de forma eficiente, com integração ao Discord.

**Nota:** A aplicação está atualmente em versão beta. Algumas funcionalidades podem não funcionar corretamente ou estar sujeitas a mudanças. Agradecemos a sua compreensão e feedback para melhorar o bot.

## Funcionalidades

- **Comandos RCON**: O bot suporta todos os comandos RCON do Project Zomboid, permitindo controle total sobre o servidor. Exemplos de comandos suportados:
  - Gerenciamento de jogadores (kick, ban, whitelist, etc.)
  - Controle do servidor (iniciar, parar, reiniciar, etc.)
  - Envio de mensagens de anúncio para todos os jogadores
  - E muitos outros comandos RCON disponíveis.

- **Verificação de Atualização de Mods**: O bot verifica automaticamente se há atualizações para os mods instalados no servidor.

- **Reinício Automático**: Após detectar e instalar atualizações de mods, o bot reinicia automaticamente o servidor para aplicar as mudanças.

- **Notificações no Discord**: O bot envia notificações sobre o status do servidor, atualizações de mods e outros eventos importantes diretamente para um canal do Discord.

## Requisitos

- Python 3.7 ou superior
- Bibliotecas Python:
  - `pyautogui`
  - `opencv-python`
  - `numpy`
  - `pynput`
  - `paramiko` (para conexão SSH)
  - `rcon` (para suporte a comandos RCON)
  - `python-dotenv` (para carregar variáveis de ambiente do arquivo `.env`)
  - `discord.py` (para integração com o Discord)

Instale as dependências usando o comando:

```bash
pip install -r requirements.txt
```

## Como Usar

1. Clone este repositório:

   ```bash
   git clone https://github.com/seu_usuario/whatahell-discord-bot.git
   cd whatahell-discord-bot
   ```

2. Certifique-se de que o servidor do Project Zomboid está configurado corretamente e que o RCON está habilitado.

3. Configure o arquivo `.env` com as credenciais do servidor, integração com o Discord e preferências do bot. Aqui está um exemplo de arquivo `.env`:

   ```env
   CANAL_ADMINISTRADOR="administrador"
   CANAL_ANUNCIOS="anuncios"
   CANAL_MODS="mods-update"
   CANAL_GERAL="bate-papo"  # Canal para mensagens gerais

   CARGO_ID_NOVO_MEMBRO=0  # ID do cargo inicial para novos membros

   RCON_HOST="host.com"
   RCON_PORT=27063
   RCON_PASS="password"

   SSH_HOST="host.com"
   SSH_SENHA="123456"
   SSH_USUARIO="user"
   SYSTEM_SERVICO="systemd-service"

   CAMINHO_LOG="<caminho dos logs do zomboid>"

   TOKEN="<Token do Discord>"

   BOTNOME="<nome do bot>"
   SITE="<url do jogo>"
   FUND="<url de doação>"

   EPIDEMIAZSERVIDOR="<url do servidor Zomboid>"
   EPIDEMIAZNOME="<nome do servidor>"
   EPIDEMIAZRODAPE="<mensagem de rodapé>"
   ```

4. **Configuração de Reinício do Servidor**: Para que o reinício automático do servidor funcione corretamente, é necessário configurar o jogo para rodar como um serviço do `systemd` usando o parâmetro `SYSTEM_SERVICO`. Além disso, é preciso garantir que o usuário especificado no parâmetro `SSH_USUARIO` tenha permissões adequadas para gerenciar e reiniciar o serviço do servidor. Certifique-se de que o `systemd` está configurado corretamente para o serviço do Project Zomboid.

5. Execute o bot:

   ```bash
   python whatahell_bot.py
   ```

6. O bot executará comandos RCON conforme necessário, verificará atualizações de mods, reiniciará o servidor automaticamente e enviará notificações para o Discord. Para interromper o bot, use `Ctrl + C` no terminal.

## Configuração

As configurações do bot devem ser definidas no arquivo `.env`, como:

- **Canais do Discord**: Defina os nomes apropriados dos canais para diferentes tipos de mensagens (`CANAL_ADMINISTRADOR`, `CANAL_ANUNCIOS`, `CANAL_MODS`, `CANAL_GERAL`).
- **Credenciais RCON**: Defina o IP, porta e senha do RCON.
- **Credenciais SSH**: Defina o host, usuário e senha SSH para gerenciamento do servidor.
- **Nome do Serviço**: Especifique o nome do serviço do sistema para gerenciar o servidor (`SYSTEM_SERVICO`).
- **Caminho dos Logs**: Defina o caminho onde os logs do servidor são armazenados.
- **Token do Discord**: Defina o token do bot para integração com o Discord.


- **Informações do Servidor**: Defina o nome do bot, URL do jogo, URL de doação, URL do servidor Zomboid, nome do servidor e mensagem de rodapé.

## Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para abrir um *pull request* ou relatar problemas na seção de *issues*.

## Licença

Este projeto está licenciado sob a Licença Pública Geral GNU (GPL). Consulte o arquivo `LICENSE` para mais detalhes.

---

Se precisar de mais alguma alteração ou de ajuda adicional, é só avisar!