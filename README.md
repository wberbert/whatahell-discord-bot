# Whatahell Discord Bot

O **Whatahell Discord Bot** é um bot para Project Zomboid desenvolvido em Python. Ele automatiza tarefas no jogo, incluindo comandos RCON, verificação de atualização de mods e reinício automático do servidor após a atualização. Este bot foi criado para ajudar administradores de servidores a gerenciar e manter seu servidor de Project Zomboid de forma eficiente, com integração ao Discord.

## Funcionalidades

- **Comandos RCON**: O bot suporta todos os comandos RCON do Project Zomboid, permitindo controle total sobre o servidor. Exemplos de comandos suportados:
  - Gerenciamento de jogadores (kick, ban, whitelist, etc.)
  - Controle do servidor (iniciar, parar, reiniciar, etc.)
  - Envio de mensagens de anúncio para todos os jogadores
  - E muitos outros comandos disponíveis no RCON.

- **Verificação de atualização de mods**: O bot verifica automaticamente se há atualizações para os mods instalados no servidor.

- **Reinício automático**: Após a detecção e instalação de atualizações de mods, o bot reinicia automaticamente o servidor para aplicar as mudanças.

- **Notificações no Discord**: O bot envia notificações sobre o status do servidor, atualizações de mods e outros eventos importantes diretamente em um canal do Discord.

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

3. Configure o arquivo `.env` com as credenciais do servidor, integração com o Discord, e as preferências do bot. Um exemplo de arquivo `.env` pode ser encontrado abaixo:

   ```env
   RCON_HOST=seu_ip_do_servidor
   RCON_PORT=sua_porta_rcon
   RCON_PASSWORD=sua_senha_rcon
   DISCORD_TOKEN=seu_token_discord
   DISCORD_CHANNEL_ID=id_do_canal_discord
   CHECK_MOD_INTERVAL=3600  # Intervalo em segundos para verificar atualizações de mods
   ```

4. Execute o bot:

   ```bash
   python whatahell_bot.py
   ```

5. O bot executará comandos RCON conforme necessário, verificará atualizações de mods, reiniciará o servidor automaticamente e enviará notificações para o Discord. Para interromper o bot, use `Ctrl + C` no terminal.

## Configuração

As configurações do bot devem ser definidas no arquivo `.env`, como:

- **Credenciais do RCON**: Defina o IP, porta, e senha do RCON.
- **Token do Discord**: Defina o token do bot para integração com o Discord.
- **Canal do Discord**: Especifique o ID do canal onde o bot enviará notificações.
- **Intervalo de verificação de mods**: Ajuste o tempo em que o bot verifica por atualizações de mods.
- **Comportamento de reinício**: Configure como o bot deve reiniciar o servidor após atualizações.

## Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para abrir um *pull request* ou relatar problemas na seção de *issues*.

## Licença

Este projeto está licenciado sob a licença MIT. Consulte o arquivo `LICENSE` para mais detalhes.
