import discord, asyncio
import os, glob, re, time
import paramiko
from discord.ext import commands
from zomboid_rcon import ZomboidRCON
#from watchdog.observers import Observer, polling
from watchdog.events import FileSystemEvent, FileSystemEventHandler
from modules.whbot_locks import wh_locks
from discord import app_commands

class systemd_zomboid ():

    def __init__ (self, 
                    str_host : str,
                    str_usuario : str,
                    str_senha : str,
                    str_servico : str):
        
        self.str_host = str_host
        self.str_senha = str_senha
        self.str_servico = str_servico
        self.str_usuario = str_usuario

    @property
    def host(self):
        return self.str_host

    @host.setter
    def host(self, value):
        self.str_host = value

    @property
    def senha(self):
        return self.str_senha

    @senha.setter
    def senha(self, value):
        self.str_senha = value

    @property
    def servico(self):
        return self.str_servico

    @servico.setter
    def servico(self, value):
        self.str_servico = value
    
    @property
    def usuario(self):
        return self.str_usuario

    @usuario.setter
    def usuario(self, value):
        self.str_usuario = value

class _whbot_log_cards():

    @staticmethod
    def debug_log_mod_card(str_mensagem : str,
                           str_titulo : str,
                           str_rodape : str,
                           str_autor : str) -> discord.Embed:

        emsg = discord.Embed(colour=discord.Colour.yellow(), 
                             description=str_mensagem,
                             title=str_titulo)
        
        #emsg.add_field(name="Site", value=str_site, inline=True)
        #emsg.add_field(name="Doações", value=str_doe, inline=True)
        #emsg.add_field(name="Servidor", value=str_servidor, inline=False)
        emsg.set_author(name=str_autor)
        emsg.set_footer(text=str_rodape)

        return emsg

class _whbot_pz_debug_log_func():
    
    @staticmethod
    def reiniciar_servico_zomboid(str_host : str, int_porta : int, str_usuario : str, str_senha : str, str_servico : str) -> bool:
        
        ssh_client = paramiko.SSHClient()

        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            ssh_client.connect (hostname=str_host, port=int_porta, username=str_usuario, password=str_senha)

            try:
                # Usuário necessita estar no SUDOERS sem password para funcionar
                stdin, stdout, stderr = ssh_client.exec_command(f"sudo systemctl restart {str_servico}")
                #str_output = stdout.read().decode()
                #str_error = stderr.read().decode()
            except Exception as ex:
                return False

        finally:
            ssh_client.close()
        
        return True
class whbot_pz_debug_log(commands.Cog):

    def __init__(self, 
                 bot : commands.Bot, 
                 zrcon : ZomboidRCON, 
                 str_canal_notificacoes : str,
                 zsystem : systemd_zomboid
                ):
        
        self.str_canal_notificacoes = discord.utils.get(bot.get_all_channels(), name=str_canal_notificacoes)
        self.bot = bot
        self.zrcon = zrcon
        self.zsystem = zsystem

        embcard : discord.Embed = _whbot_log_cards.debug_log_mod_card (str_mensagem="Monitorando continuamente atualização de MODS...",
                                                                       str_titulo="[WH_PZ_BOT]",
                                                                       str_rodape="Project Zomboid",
                                                                       str_autor="CheckModsUpdate"
                                                                      )
                        
        bot.loop.create_task(self.str_canal_notificacoes.send(embed=embcard))
    
    async def atualizar_mod(self):
        
        async with wh_locks.lck_atulizar_mods:

            embcard : discord.Embed = discord.Embed(colour=discord.Colour.dark_red(), 
                                                    description="***[WH_PZ_BOT]*** Processo de atualização de mods inicalizado.")
            await self.str_canal_notificacoes.send(embed=embcard)
            
            embcard : discord.Embed = discord.Embed(colour=discord.Colour.dark_red(), 
                                                    description="***[WH_PZ_BOT]*** Servidor será reiniciado em 5 minutos.")
            await self.str_canal_notificacoes.send(embed=embcard)

            embcard : discord.Embed = discord.Embed(colour=discord.Colour.dark_red(), 
                                                    description="***[WH_PZ_BOT]*** Notificando jogadores ...")
            await self.str_canal_notificacoes.send(embed=embcard)
            self.zrcon.servermsg("ATUALIZACAO DE MODS 5 MIN")
            await asyncio.sleep(120)

            embcard : discord.Embed = discord.Embed(colour=discord.Colour.dark_red(), 
                                                    description="***[WH_PZ_BOT]*** Servidor será reiniciado em 3 minutos.")
                    
            await self.str_canal_notificacoes.send(embed=embcard)
            self.zrcon.servermsg("ATUALIZACAO DE MODS 3 MIN")
            await asyncio.sleep(120)

            embcard : discord.Embed = discord.Embed(colour=discord.Colour.dark_red(), 
                                                    description="***[WH_PZ_BOT]*** Servidor será reiniciado em 1 minuto.")
            
            await self.str_canal_notificacoes.send(embed=embcard)
            self.zrcon.servermsg("ATUALIZACAO DE MODS 1 MIN")
            await asyncio.sleep(50)

            embcard : discord.Embed = discord.Embed(colour=discord.Colour.dark_red(), 
                                                    description="***[WH_PZ_BOT]*** Servidor será reiniciado em 10 segundos.")
                    
            self.str_canal_notificacoes.send(embed=embcard)
            self.zrcon.servermsg("ATUALIZACAO DE MODS 10 SEG")
            await asyncio.sleep(10)
            
            embcard : discord.Embed = discord.Embed(colour=discord.Colour.dark_red(), 
                                                    description="***[WH_PZ_BOT]*** Chutando jogadores ...")
                        
            await self.str_canal_notificacoes.send(embed=embcard)

            # Lista os jogadores online.
            str_resposta = self.zrcon.players().response
            str_regex = r"-(.*)"
            str_jogagores : list[str] = re.findall(str_regex, str_resposta)
            
            for str_jogador in str_jogagores:
                self.zrcon.kickuser(str_jogador)

            await asyncio.sleep(10)

            embcard : discord.Embed = discord.Embed(colour=discord.Colour.dark_red(), 
                                                    description="***[WH_PZ_BOT]*** Salvando o estado do servidor ...") 
            await self.str_canal_notificacoes.send(embed=embcard)
            
            self.zrcon.save()
            await asyncio.sleep(10)

            embcard : discord.Embed = discord.Embed(colour=discord.Colour.dark_red(), 
                                                    description="***[WH_PZ_BOT]*** Fechando a sessão ...") 
            await self.str_canal_notificacoes.send(embed=embcard)

            self.zrcon.quit()
            await asyncio.sleep(10)

            bln_resp =  _whbot_pz_debug_log_func.reiniciar_servico_zomboid(self.zsystem.host, 22, self.zsystem.usuario, self.zsystem.senha, self.zsystem.servico)
            
            await asyncio.sleep(10)

            if bln_resp :

                embcard : discord.Embed = discord.Embed(colour=discord.Colour.green(), 
                                                        description="***[WH_PZ_BOT]*** Servidor reiniciado com sucesso  ...") 
                                
                await self.str_canal_notificacoes.send(embed=embcard)

            else:

                embcard : discord.Embed = discord.Embed(colour=discord.Colour.red(), 
                                                        description="***[WH_PZ_BOT]*** Falha ao reiniciar o servidor ...") 
                
                await self.str_canal_notificacoes.send(embed=embcard)
            
            await asyncio.sleep(10)

            embcard : discord.Embed = discord.Embed(colour=discord.Colour.green(), 
                                        description="***[WH_PZ_BOT]*** Módulos atualizados ...")
            
            await self.str_canal_notificacoes.send(embed=embcard)            
                
    async def eventos_de_atualizacao_de_mod(self, str_entrada_log : str) -> None:
        """Procura na linha do log atual um evento que indica uma atualização de MOD"""
        
        #str_regexp = r"\[(.{1,2}-.{1,2}-.{1,2}\s.{1,2}:.{1,2}:.{1,2}\..{1,3})\]\s(\w*)\s*:\s(\w*)\s*,\s(\d*)>\s(\d*,\d*,\d*)>\s(CheckModsNeedUpdate):\s(.*))"
        str_regexp = r"\[(.{1,2}-.{1,2}-.{1,2}\s.{1,2}:.{1,2}:.{1,2}\..{1,3})\]\s(\w*)\s*:\s(\w*)\s*,\s(\d*)>(.*)>\s(CheckModsNeedUpdate):\s(.*)"

        str_padrao = re.search(pattern=str_regexp, string=str_entrada_log)
       # print ("log read : Padrao %s, entrada log: %s" % (str_padrao, str_entrada_log))
        if str_padrao is not None:
            #if str_padrao.group(7) == "Checking....":

            #    embcard : discord.Embed = discord.Embed(colour=discord.Colour.dark_red(), 
            #                                description="***[WH_PZ_BOT]*** Verificando por atualização de MOD ...")
            #    embcard : discord.Embed = _whbot_log_cards.debug_log_mod_card (str_mensagem="Verificando por atualização de MOD ...",
            #                                                                   str_titulo="[WH_PZ_BOT] ",
            #                                                                   str_rodape="Epidemia Z",
            #                                                                   str_autor="CheckModsUpdate"
            #                                                                  )
                                
            #    await self.str_canal_notificacoes.send(embed=embcard)

            #if str_padrao.group(7) == "Mods updated.":

            #    embcard : discord.Embed = discord.Embed(colour=discord.Colour.dark_red(), 
            #                                description="***[WH_PZ_BOT]*** Todos os MODS atualizados ...")
                
            #    embcard : discord.Embed = _whbot_log_cards.debug_log_mod_card (str_mensagem="Todos os MODS atualizados.",
            #                                                                   str_titulo="[WH_PZ_BOT]",
            #                                                                   str_rodape="Epidemia Z",
            #                                                                   str_autor="CheckModsUpdate"
            #                                                                  )
                
            #    await self.str_canal_notificacoes.send(embed=embcard)

            if str_padrao.group(7) == "Mods need update.":
                
                embcard : discord.Embed = _whbot_log_cards.debug_log_mod_card (str_mensagem="Modulos desatualizados.",
                                                                               str_titulo="[WH_PZ_BOT]",
                                                                               str_rodape="Project Zomboid",
                                                                               str_autor="CheckModsUpdate"
                                                                              )

                await self.str_canal_notificacoes.send(embed=embcard)

                # Chama rotina de atualização de MOD
                #asyncio.run(self.AtualizarMod())
                await self.atualizar_mod()

class whbot_pz_log(FileSystemEventHandler):
    """Responsável por monitorar os logs do zomboid"""

    def __init__(self, bot : commands.Bot, str_caminho_debug_log : str):
        self.str_caminho_debug_log : str = str_caminho_debug_log
        self.bot = bot
        
        self.inicilizar_logs()

    def on_modified(self, event : FileSystemEvent) -> None:
        
        for str_debug_log, iow_arquivo in self.json_debug_log.items():
            
            if event.src_path in str_debug_log:
                iow_arquivo.seek(0, os.SEEK_CUR)
                str_novas_linhas = iow_arquivo.readlines()
                
                for str_nova_linha in str_novas_linhas:
                    # Procura no log eventos de atualização de MOD
                    pz_debug = self.bot.get_cog("whbot_pz_debug_log") # Obtem o COG já instanciado.
                    self.bot.loop.create_task(pz_debug.eventos_de_atualizacao_de_mod(str_entrada_log=str_nova_linha))
                    #self.EventosAtualizacaoMOD(str_entrada_log=str_nova_linha)

    
    def on_created(self, event: FileSystemEvent) -> None:
        self.inicilizar_logs()
    
    def inicilizar_logs(self):
        """Incializa os logs que serão monitorados"""

        str_debug_logs : list[str] = glob.glob(os.path.join(self.str_caminho_debug_log,"*DebugLog-server.txt"))
        
        self.json_debug_log = {str_debug_log: open(str_debug_log, "r") for str_debug_log in str_debug_logs}
        
        for file in self.json_debug_log.values():
            file.seek(0, os.SEEK_END)

class whbot_pz_servico_slash_command(commands.Cog):
    
    def __init__(self, 
                 zrcon : ZomboidRCON,
                 zsystem : systemd_zomboid,
                ):
        self.zrcon = zrcon
        self.zsystem = zsystem

    @app_commands.command(name="zreiniciar", description="Reinicia o servidor zomboid")
    #@app_commands.checks.has_permissions(administrator=True)
    async def reiniciar (self,
                         itx : discord.Interaction):
        
        await itx.response.defer()

        embcard : discord.Embed = discord.Embed(colour=discord.Colour.green(), 
                                                description="***[WH_PZ_BOT]*** Reinício manual do servidor.")
        
        await itx.followup.send(embed=embcard)

        embcard : discord.Embed = discord.Embed(colour=discord.Colour.green(), 
                                                description="***[WH_PZ_BOT]*** Servidor será reiniciado em 2 minutos.")
        
        await itx.followup.send(embed=embcard)
        self.zrcon.servermsg("ATUALIZACAO DE MODS 2 MIN")
        await asyncio.sleep(50)

        embcard : discord.Embed = discord.Embed(colour=discord.Colour.green(), 
                                                description="***[WH_PZ_BOT]*** Servidor será reiniciado em 1 minuto.")
        
        await itx.followup.send(embed=embcard)
        self.zrcon.servermsg("ATENCAO - REINICIANDO EM 1 MIN...")
        await asyncio.sleep(50)

        embcard : discord.Embed = discord.Embed(colour=discord.Colour.green(), 
                                                description="***[WH_PZ_BOT]*** Reiniciando em 10...9...8...7...6...5...")
        
        await itx.followup.send(embed=embcard)
        self.zrcon.servermsg("REINICIANDO EM 10 SEG...")
        await asyncio.sleep(10)

        embcard = _whbot_log_cards.debug_log_mod_card(str_mensagem="Reiniciando servidor Zomboid ...",
                                                      str_titulo="[WH_PZ_BOT]",
                                                      str_rodape="Project Zomboid",
                                                      str_autor="Reiniciar Servidor"
                                                     )
        await itx.followup.send(embed=embcard) 

        try:
            self.zrcon.save()
        except:
            embcard = _whbot_log_cards.debug_log_mod_card(str_mensagem="Falha ao reiniciar servidor, não foi possível salvar o estado do servidor.",
                                                          str_titulo="[WH_PZ_BOT]",
                                                          str_rodape="Project Zomboid",
                                                          str_autor="Reiniciar Servidor"
                                                         )
            await itx.followup.send(embed=embcard)
            return
        
        bln_resp =  _whbot_pz_debug_log_func.reiniciar_servico_zomboid(self.zsystem.host, 22, self.zsystem.usuario, self.zsystem.senha, self.zsystem.servico)
       
        await asyncio.sleep(10)

        if bln_resp:
            embcard = _whbot_log_cards.debug_log_mod_card(str_mensagem="Servidor reiniciado com sucesso",
                                                          str_titulo="[WH_PZ_BOT]",
                                                          str_rodape="Project Zomboid",
                                                          str_autor="Reiniciar Servidor"
                                                         )

        else:
            
            embcard = _whbot_log_cards.debug_log_mod_card(str_mensagem="Falha ao reiniciar o servidor",
                                                          str_titulo="[WH_PZ_BOT]",
                                                          str_rodape="Project Zomboid",
                                                          str_autor="Reiniciar Servidor"
                                                         )
        
        await itx.followup.send(embed=embcard)