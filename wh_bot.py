import discord, discord.context_managers, discord.ext
import os,re
from discord.ext import commands
from zomboid_rcon import ZomboidRCON
from modules.whbot_comandos_rcon import whbot_rcon_comandos_geral, whbot_rcon_comandos_moderador, whbot_rcon_slash_comandos_moderador, whbot_rcon_slash_comandos_geral, whbot_rcon_tarefas_recorrentes
from modules.whbot_comandos_geral import whbot_geral_comandos
from modules.whbot_comandos_bot import whbot_bot_comandos, whbot_bot_slash_comandos
from modules.whbot_eventos_jogador import whbot_eventos_jogador
from modules.whbot_comandos_avisos import whbot_avisos_comandos
from modules.whbot_log_monitor import whbot_pz_log, whbot_pz_debug_log, whbot_pz_servico_slash_command, systemd_zomboid

from watchdog.observers import Observer, polling
from watchdog.events import FileSystemEvent, FileSystemEventHandler

from dotenv import load_dotenv

load_dotenv()

CANAL_ADMINISTRADOR = os.getenv("CANAL_ADMINISTRADOR", "administrador")
CANAL_ANUNCIOS = os.getenv("CANAL_ANUNCIOS", "anuncios")
CANAL_MODS = os.getenv("CANAL_MODS", "mods-update")
CANAL_GERAL = os.getenv("CANAL_GERAL", "geral")

CARGO_ID_NOVO_MEMBRO = os.getenv("CARGO_ID_NOVO_MEMBRO")

RCON_HOST = os.getenv("RCON_HOST", "localhost")
RCON_PORT = os.getenv("RCON_PORT", "27015")
RCON_PASS = os.getenv("RCON_PASS")

# Informações para utilização do systemd para reinializar o serviço zomboid.
SSH_HOST = os.getenv("SSH_HOST", "localhost")
SSH_SENHA = os.getenv("SSH_SENHA")
SSH_USUARIO = os.getenv("SSH_USUARIO")
SYSTEM_SERVICO = os.getenv("SYSTEM_SERVICO")

BOTNOME = os.getenv("BOTNOME")
SITE = os.getenv("SITE")
FUND = os.getenv("FUND")

EPIDEMIAZSERVIDOR = os.getenv("EPIDEMIAZSERVIDOR")
EPIDEMIAZNOME = os.getenv("EPIDEMIAZNOME")
EPIDEMIAZRODAPE = os.getenv("EPIDEMIAZRODAPE")

CAMINHO_LOG = os.getenv("CAMINHO_LOG")

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.messages=True

#client = discord.Client(intents=intents)
# Conecta-se ao servidor de jogo
rcon_client = ZomboidRCON(ip=RCON_HOST, port=int(RCON_PORT), password=RCON_PASS)

# Cria o bot
bot = commands.Bot(command_prefix="!", intents=intents)

# Configuração de LOG
#bot.log = logging.getLogger("WHbot")
#coloredlogs.install(level="DEBUG", logger=bot.log)

@bot.event
async def on_ready():
    
    # Classes com os comandos normal precedidos com "!"
    await bot.add_cog(whbot_rcon_comandos_moderador(bot = bot,
                                                    zrcon = rcon_client,
                                                    str_site_principal = SITE,
                                                    str_site_doacao = FUND,
                                                    str_titulo = EPIDEMIAZNOME,
                                                    str_servidor = EPIDEMIAZSERVIDOR,
                                                    str_rodape = EPIDEMIAZRODAPE                                                    
                                                   )
                     )
    # Classes com os comandos normal precedidos com "!"
    await bot.add_cog(whbot_rcon_comandos_geral(bot = bot,
                                                zrcon = rcon_client,
                                                str_site_principal = SITE,
                                                str_site_doacao = FUND,
                                                str_titulo = EPIDEMIAZNOME,
                                                str_servidor = EPIDEMIAZSERVIDOR,
                                                str_rodape = EPIDEMIAZRODAPE                                                 
                                               )
                     )

    # Classes com os eventos aplicados ao canal referente ao membro participante.
    await bot.add_cog(whbot_eventos_jogador(bot=bot,str_id_role=CARGO_ID_NOVO_MEMBRO, str_canal=CANAL_GERAL ))
    
    await bot.add_cog(whbot_bot_comandos(bot=bot, zrcon=rcon_client, botnome=BOTNOME))
    await bot.add_cog(whbot_avisos_comandos(bot=bot, zrcon=rcon_client))
    await bot.add_cog(whbot_geral_comandos(bot=bot, zrcon=rcon_client))

    # Classes com os comandos slash "/"
    await bot.add_cog(whbot_bot_slash_comandos(bot=bot, zrcon=rcon_client))

    await bot.add_cog(whbot_rcon_slash_comandos_geral(bot = bot, 
                                                      zrcon = rcon_client,
                                                      str_site_principal = SITE,
                                                      str_site_doacao = FUND,
                                                      str_titulo = EPIDEMIAZNOME,
                                                      str_servidor = EPIDEMIAZSERVIDOR,
                                                      str_rodape = EPIDEMIAZRODAPE
                                                     )
                     )
    
    await bot.add_cog(whbot_rcon_slash_comandos_moderador(bot = bot, 
                                                          zrcon = rcon_client,
                                                          str_site_principal = SITE,
                                                          str_site_doacao = FUND,
                                                          str_titulo = EPIDEMIAZNOME,
                                                          str_servidor = EPIDEMIAZSERVIDOR,
                                                          str_rodape = EPIDEMIAZRODAPE
                                                         )
                     )
    
    # Classe com comandos executados periodicamente
    await bot.add_cog(whbot_rcon_tarefas_recorrentes(bot = bot, 
                                                     zrcon = rcon_client,
                                                     str_site_principal = SITE,
                                                     str_site_doacao = FUND,
                                                     str_titulo = EPIDEMIAZNOME,
                                                     str_servidor = EPIDEMIAZSERVIDOR,
                                                     str_rodape = EPIDEMIAZRODAPE
                                                    )
                     )

    # Alguns comandos para manipulação do servico zomboid (EXPERIMENTAL)
    await bot.add_cog(whbot_pz_servico_slash_command(zrcon = rcon_client, 
                                                     zsystem=systemd_zomboid(str_host=SSH_HOST, str_senha=SSH_SENHA, str_usuario=SSH_USUARIO, str_servico=SYSTEM_SERVICO)
                                                    )
                     )

    await bot.add_cog(whbot_pz_debug_log(bot = bot, 
                                         zrcon = rcon_client,
                                         str_canal_notificacoes = CANAL_MODS,
                                         zsystem=systemd_zomboid(str_host=SSH_HOST, str_senha=SSH_SENHA, str_usuario=SSH_USUARIO, str_servico=SYSTEM_SERVICO)
                                        )
                     )
    
    eventh = whbot_pz_log(str_caminho_debug_log=CAMINHO_LOG, bot=bot)

    #observer = Observer()
    observer = polling.PollingObserver()
    #observer.schedule(eventh, path=os.path.dirname("/mnt/epidemia/Zomboid/Logs/*DebugLog-server.txt"), recursive=False)
    observer.schedule(eventh, path=CAMINHO_LOG)
    observer.start()

    bot.loop.run_in_executor(None, observer.join)

    await bot.tree.sync()

    print ("\nCONFIGURACOES \n")
    print (f"Canal do administrador : {CANAL_ADMINISTRADOR}")
    print (f"Canal de anuncios      : {CANAL_ANUNCIOS}")
    print (f"Canal de MODS          : {CANAL_MODS}")
    print (f"Host RCON              : {RCON_HOST}")
    print (f"Porta RCON             : {RCON_PORT}")
    print (f"Senha RCON             : {RCON_PASS}")
    print (f"Nome do BOT            : {BOTNOME}")
    print (f"TOKEN                  : {TOKEN}")
    print ()
    print (f"SSH HOST               : {SSH_HOST}")
    print (f"SSH SENHA              : {SSH_SENHA}")
    print (f"SSH USUARIO            : {SSH_USUARIO}")
    print (f"SYSTEMD SERVICO        : {SYSTEM_SERVICO}")

# Outros comandos
@bot.event
async def on_command_error (ctx     : commands.Context, 
                            error   : commands.CommandError
                           ):
    
    await ctx.send (f"Erro ao executar a operação: \n {error}")


# Executa o bot
bot.run(TOKEN)
