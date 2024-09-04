import discord, typing
import os, re
import asyncio
from zomboid_rcon import ZomboidRCON
from discord.ext import commands,tasks
from discord.ext.commands import has_permissions
from modules.whbot_custom_checks import Ccheks
from discord import app_commands
from dotenv import load_dotenv
from modules.whbot_locks import wh_locks

load_dotenv()

#CANAL_ADMINISTRADOR = os.getenv("CANAL_ADMINISTRADOR")

#SITE = os.getenv("SITE")
#EPIDEMIAZSERVIDOR = os.getenv("EPIDEMIAZSERVIDOR")
#EPIDEMIAZNOME = os.getenv("EPIDEMIAZNOME")
#EPIDEMIAZRODAPE = os.getenv("EPIDEMIAZRODAPE")
#FUND = os.getenv("FUND")

class _whbot_rcon_autocomplete():

    async def player_auto_complete(self,
                                   itr      : discord.Interaction,
                                   current  : str) -> app_commands.Choice:
        
        zrcon : ZomboidRCON = self.zrcon
        
        str_resposta = zrcon.players().response
        str_regex = r"-(.*)"
        str_jogagores = re.findall(str_regex, str_resposta)
        
        return [app_commands.Choice(name=player, value=player) for player in str_jogagores if current.lower() in player.lower()][:25]
    
    async def perk_auto_complete(self,
                                 itr : discord.Interaction,
                                 current: str) -> app_commands.Choice:
        l_str_perks =["Combat",
                      "Axe",
                      "Blunt",
                      "SmallBlunt",
                      "LongBlade",
                      "SmallBlade",
                      "Spear",
                      "Maintenance",
                      "Firearm",
                      "Aiming",
                      "Reloading",
                      "Crafting",
                      "Woodwork",
                      "Cooking",
                      "Farming",
                      "Doctor",
                      "Electricity",
                      "MetalWelding",
                      "Mechanics",
                      "Tailoring",
                      "Survivalist",
                      "Fishing",
                      "Trapping",
                      "PlantScavenging",
                      "Fitness",
                      "Strength",
                      "Agility",
                      "Sprinting",
                      "Lightfoot",
                      "Nimble",
                      "Sneak",
                      "Engineering",
                      "Machinery",
                      "Miscellaneous",
                      "Scavenging",
                      "Cultivation",
                      "Libations",
                      "Brewing",
                      "Smithing",
                      "Lifestyle",
                      "Dancing",
                      "Meditation",
                      "Music",
                      "Woodcutting",
                      "TraitsPurchaseSystem",
                      "Traits",
                      "Traits2",
                      "Traits3"]
    
        return [app_commands.Choice(name=perk, value=perk) for perk in l_str_perks if current.lower() in perk.lower()][:25]
    
    async def experience_auto_complete(self,
                                       itr  : discord.Interaction,
                                       current : str
                                      ) -> app_commands.Choice:
        l_str_exp = [10, 100, 1000, 20, 200, 2000, 50, 500, 5000]

        return [ app_commands.Choice(name=experience, value=experience) for experience in l_str_exp][:25]
    
    async def access_auto_complete(self,
                                   itr      : discord.Interaction,
                                   current  : str
                                  ) -> app_commands.Choice:
        
        l_str_acesso = ["admin", "moderator", "overseer", "gm", "observer"]

        return [app_commands.Choice(name=access, value=access) for access in l_str_acesso][:25]

class _whbot_rcon_cards():

    @staticmethod
    def rcon_card_a(str_mensagem : str,
                    str_titulo : str,
                    str_site : str,
                    str_doe : str,
                    str_servidor : str,
                    str_rodape : str,
                    str_autor : str) -> discord.Embed:

        emsg = discord.Embed(colour=discord.Colour.red(), 
                             description=str_mensagem,
                             title=str_titulo)
        
        emsg.add_field(name="Site", value=str_site, inline=True)
        emsg.add_field(name="Doações", value=str_doe, inline=True)
        emsg.add_field(name="Servidor", value=str_servidor, inline=False)
        emsg.set_author(name=str_autor)
        emsg.set_footer(text=str_rodape)

        return emsg
class _whbot_rcon_comandos_moderador():

    
    def __init__ (self, SITE_PRINCIPAL : str = None, SITE_DOACAO : str = None, TITULO : str = None, SERVIDOR : str = None, RODAPE : str = None):
        
        self.SITE_PRINCIPAL : str = SITE_PRINCIPAL
        self.SITE_DOACAO    : str = SITE_DOACAO
        self.TITULO         : str = TITULO
        self.SERVIDOR       : str = SERVIDOR
        self.RODAPE         : str = RODAPE

    async def players(
                      self,
                      payload : commands.Context | discord.Interaction,
                      zrcon : ZomboidRCON
                     ) -> None:
        
        str_resposta = zrcon.players().response
        
        embed = _whbot_rcon_cards.rcon_card_a(str_mensagem=str_resposta,
                                              str_titulo= self.TITULO,
                                              str_autor="Comando Administrativo",
                                              str_servidor=self.SERVIDOR,
                                              str_site=self.SITE_PRINCIPAL,
                                              str_doe=self.SITE_DOACAO,
                                              str_rodape=self.RODAPE)

        if isinstance(payload, commands.Context):
            ctx : commands.Context = payload
            await ctx.send(embed=embed)

        if isinstance(payload, discord.Interaction):
            itr : discord.Interaction = payload
            await itr.response.send_message(embed=embed)
    
    async def addalltowhitelist(
                                self,
                                payload : commands.Context | discord.Interaction,
                                zrcon : ZomboidRCON
                               ) -> None:
        
        str_resposta = zrcon.addalltowhitelist().response

        embed = _whbot_rcon_cards.rcon_card_a(str_mensagem=str_resposta,
                                              str_titulo= self.TITULO,
                                              str_autor="Comando Administrativo",
                                              str_servidor=self.SERVIDOR,
                                              str_site=self.SITE_PRINCIPAL,
                                              str_doe=self.SITE_DOACAO,
                                              str_rodape=self.RODAPE)

        if isinstance(payload, commands.Context):
            ctx : commands.context = payload
            await ctx.send(embed=embed)
        
        if isinstance(payload, discord.Interaction):
            itr : discord.Interaction = payload
            await itr.response.send_message(embed=embed)

    async def adduser(
                      self, 
                      payload       : commands.Context | discord.Interaction,
                      zrcon         : ZomboidRCON,
                      *,
                      str_usuario   : str,
                      str_senha     : str
                     ) -> None:

        str_resposta = zrcon.adduser(str_usuario, str_senha).response

        embed = _whbot_rcon_cards.rcon_card_a(str_mensagem=str_resposta,
                                              str_titulo= self.TITULO,
                                              str_autor="Comando Administrativo",
                                              str_servidor=self.SERVIDOR,
                                              str_site=self.SITE_PRINCIPAL,
                                              str_doe=self.SITE_DOACAO,
                                              str_rodape=self.RODAPE)

        if isinstance(payload, commands.Context):
            ctx : commands.Context = payload
            await ctx.send(embed=embed)

        if isinstance(payload, discord.Interaction):
            itr : discord.Interaction = payload
            await itr.response.send_message(embed=embed)

    async def addusertowhitelist(
                                 self,
                                 payload        : commands.Context | discord.Interaction,
                                 zrcon          : ZomboidRCON,
                                 *,
                                 str_usuario    : str
                                ) -> None:
        """
        Adiciona um simples usuário a whitelist.
        """

        str_resposta = zrcon.addusertowhitelist(str_usuario).response
        
        embed = _whbot_rcon_cards.rcon_card_a(str_mensagem=str_resposta,
                                              str_titulo= self.TITULO,
                                              str_autor="Comando Administrativo",
                                              str_servidor=self.SERVIDOR,
                                              str_site=self.SITE_PRINCIPAL,
                                              str_doe=self.SITE_DOACAO,
                                              str_rodape=self.RODAPE)

        if isinstance(payload, commands.Context):
            ctx : commands.Context = payload
            await ctx.send(embed=embed)
        
        if isinstance(payload, discord.Interaction):
            itr : discord.Interaction = payload
            await itr.response.send_message(embed=embed)

    async def removeuserfromwhitelist(
                                      self,  
                                      payload       : commands.Context | discord.Interaction,
                                      zrcon         : ZomboidRCON,
                                      *,
                                      str_usuario   : str
                                     ) -> None:
        """
        Remove um simples usuário a whitelist.
        """
        
        str_resposta = zrcon.removeuserfromwhitelist(str_usuario).response

        embed = _whbot_rcon_cards.rcon_card_a(str_mensagem=str_resposta,
                                              str_titulo= self.TITULO,
                                              str_autor="Comando Administrativo",
                                              str_servidor=self.SERVIDOR,
                                              str_site=self.SITE_PRINCIPAL,
                                              str_doe=self.SITE_DOACAO,
                                              str_rodape=self.RODAPE)

        if isinstance(payload, commands.Context):
            ctx : commands.Context = payload
            await ctx.send(embed=embed)
        
        if isinstance(payload, discord.Interaction):
            itr : discord.Interaction = payload
            await itr.response.send_message(embed=embed)
    
    async def removeuserfromwhitelist(
                                      self,
                                      payload       : commands.Context | discord.Interaction,
                                      zrcon         : ZomboidRCON,
                                      *,                                     
                                      str_usuario   : str
                                     ) -> None:
        """
        Remove um simples usuário a whitelist.
        """
        
        str_resposta = zrcon.removeuserfromwhitelist(str_usuario).response

        embed = _whbot_rcon_cards.rcon_card_a(str_mensagem=str_resposta,
                                              str_titulo= self.TITULO,
                                              str_autor="Comando Administrativo",
                                              str_servidor=self.SERVIDOR,
                                              str_site=self.SITE_PRINCIPAL,
                                              str_doe=self.SITE_DOACAO,
                                              str_rodape=self.RODAPE)

        if isinstance(payload, commands.Context):
            ctx : commands.Context = payload
            await ctx.send(embed=embed)
        
        if isinstance(payload, discord.Interaction):
            itr : discord.Interaction = payload
            itr.response.send_message(embed=embed)


    async def banid(
                    self,
                    payload     : commands.Context | discord.Interaction,
                    zrcon       : ZomboidRCON,
                    *,
                    str_id      : str
                   ) -> None:
        """
        Bane o usuario pelo steam ID.
        """
        
        str_resposta = zrcon.banid(str_id).response

        embed = _whbot_rcon_cards.rcon_card_a(str_mensagem=str_resposta,
                                              str_titulo= self.TITULO,
                                              str_autor="Comando Administrativo",
                                              str_servidor=self.SERVIDOR,
                                              str_site=self.SITE_PRINCIPAL,
                                              str_doe=self.SITE_DOACAO,
                                              str_rodape=self.RODAPE)

        if isinstance(payload, commands.Context):
            ctx : commands.Context = payload
            await ctx.send(embed=embed)

        if isinstance(payload, discord.Interaction):
            itr : discord.Interaction = payload
            await itr.response.send_message(embed=embed)

    async def unbanid(
                      self,
                      payload       : commands.Context | discord.Interaction,
                      zrcon         : ZomboidRCON,
                      *,
                      str_id        : str
                     ) -> None:
        """
        Remove o banimento do usuario pelo steam ID.
        """
    
        str_resposta = zrcon.unbanid(str_id).response

        embed = _whbot_rcon_cards.rcon_card_a(str_mensagem=str_resposta,
                                              str_titulo= self.TITULO,
                                              str_autor="Comando Administrativo",
                                              str_servidor=self.SERVIDOR,
                                              str_site=self.SITE_PRINCIPAL,
                                              str_doe=self.SITE_DOACAO,
                                              str_rodape=self.RODAPE)

        if isinstance(payload, commands.Context):
            ctx : commands.Context = payload
            await ctx.send(embed=embed)

        if isinstance(payload, discord.Interaction):
            itr : discord.Interaction = payload
            await itr.response.send_message(embed=embed)


    async def banuser(
                      self,
                      payload       : commands.Context | discord.Interaction,
                      zrcon         : ZomboidRCON,
                      *,
                      str_usuario   : str
                     ) -> None:
        """
        Bane o usuario pelo nome.
        """
        
        str_resposta = zrcon.banuser(str_usuario).response

        embed = _whbot_rcon_cards.rcon_card_a(str_mensagem=str_resposta,
                                              str_titulo= self.TITULO,
                                              str_autor="Comando Administrativo",
                                              str_servidor=self.SERVIDOR,
                                              str_site=self.SITE_PRINCIPAL,
                                              str_doe=self.SITE_DOACAO,
                                              str_rodape=self.RODAPE)

        if isinstance(payload, commands.Context):
            ctx : commands.Context = payload
            await ctx.send(embed=embed)

        if isinstance(payload, discord.Interaction):
            itr : discord.Interaction = payload
            await itr.response.send_message(embed=embed)

    async def unbanuser(
                        self,
                        payload         : commands.Context | discord.Interaction,
                        zrcon           : ZomboidRCON,
                        *,
                        str_usuario     : str
                       ) -> None:
        """
        Remove o banimento do usuario pelo nome.
        Método administrativo. 
        """
        
        str_resposta = zrcon.unbanuser(str_usuario).response

        embed = _whbot_rcon_cards.rcon_card_a(str_mensagem=str_resposta,
                                              str_titulo= self.TITULO,
                                              str_autor="Comando Administrativo",
                                              str_servidor=self.SERVIDOR,
                                              str_site=self.SITE_PRINCIPAL,
                                              str_doe=self.SITE_DOACAO,
                                              str_rodape=self.RODAPE)

        if isinstance(payload, commands.Context):
            ctx : commands.Context = payload
            await ctx.send(embed=embed)

        if isinstance(payload, discord.Interaction):
            itr : discord.Interaction = payload
            await itr.response.send_message(embed=embed) 
    
    async def grantadmin(
                         self,
                         payload        : commands.Context | discord.Interaction,
                         zrcon          : ZomboidRCON,
                         *,
                         str_usuario    : str
                        ) -> None:
        """
        Concede permissoes de admin a um usuario.
        """
        
        str_resposta = zrcon.grantadmin(str_usuario).response

        embed = _whbot_rcon_cards.rcon_card_a(str_mensagem=str_resposta,
                                              str_titulo= self.TITULO,
                                              str_autor="Comando Administrativo",
                                              str_servidor=self.SERVIDOR,
                                              str_site=self.SITE_PRINCIPAL,
                                              str_doe=self.SITE_DOACAO,
                                              str_rodape=self.RODAPE)

        if isinstance(payload, commands.Context):
            ctx : commands.Context = payload
            await ctx.send(embed=embed)

        if isinstance(payload, discord.Interaction):
            itr : discord.Interaction = payload
            itr.response.send_message(embed=embed)

    async def removeadmin(
                          self,  
                          payload       : commands.Context | discord.Interaction,
                          zrcon         : ZomboidRCON,
                          *,
                          str_usuario   : str
                         ) -> None:
        """
        Remove permissoes de admin de um usuario.
        """
        
        str_resposta = zrcon.removeadmin(str_usuario).response

        embed = _whbot_rcon_cards.rcon_card_a(str_mensagem=str_resposta,
                                              str_titulo= self.TITULO,
                                              str_autor="Comando Administrativo",
                                              str_servidor=self.SERVIDOR,
                                              str_site=self.SITE_PRINCIPAL,
                                              str_doe=self.SITE_DOACAO,
                                              str_rodape=self.RODAPE)

        if isinstance(payload, commands.Context):
            ctx : commands.Context = payload
            await ctx.send(embed=embed)

        if isinstance(payload, discord.Interaction):
            itr : discord.Interaction = payload
            await itr.response.send_message(embed=embed)

    async def kickuser(
                       self,
                       payload      : commands.Context,
                       zrcon        : ZomboidRCON,
                       *,
                       str_usuario  : str
                      ) -> None:
        """
        Chuta um usuário do servidor.
        """

        str_resposta = zrcon.kickuser(str_usuario).response

        embed = _whbot_rcon_cards.rcon_card_a(str_mensagem=str_resposta,
                                              str_titulo= self.TITULO,
                                              str_autor="Comando Administrativo",
                                              str_servidor=self.SERVIDOR,
                                              str_site=self.SITE_PRINCIPAL,
                                              str_doe=self.SITE_DOACAO,
                                              str_rodape=self.RODAPE)

        if isinstance(payload, commands.Context):
            ctx : commands.Context = payload
            await ctx.send(embed=embed)

        if isinstance(payload, discord.Interaction):
            itr : discord.Interaction = payload
            await itr.response.send_message(embed=embed)

    async def servermsg(
                        self,
                        payload         : commands.Context | discord.Interaction,
                        zrcon           : ZomboidRCON,
                        *,
                        str_mensagem    : str
                    ) -> None: 
        """
        Envia uma mensagem a todos os jogadores.
        """

        str_resposta = zrcon.servermsg(str_mensagem).response

        embed = _whbot_rcon_cards.rcon_card_a(str_mensagem=str_resposta,
                                              str_titulo= self.TITULO,
                                              str_autor="Comando Administrativo",
                                              str_servidor=self.SERVIDOR,
                                              str_site=self.SITE_PRINCIPAL,
                                              str_doe=self.SITE_DOACAO,
                                              str_rodape=self.RODAPE)

        if isinstance(payload, commands.Context):
            ctx : commands.Context = payload
            await ctx.send(embed=embed)
        
        if isinstance(payload, discord.Interaction):
            itr : discord.Interaction = payload
            await itr.response.send_message(embed=embed)

    async def setaccesslevel(self,
                             payload        : commands.Context | discord.Interaction,
                             zrcon          : ZomboidRCON,
                             *,
                             str_usuario    : str,
                             str_acesso     : str
                            ) -> None: 
        """
        Define o nível de acesso dos jogadores.
        """
        
        str_resposta = zrcon.setaccesslevel(str_usuario, str_acesso).response

        embed = _whbot_rcon_cards.rcon_card_a(str_mensagem=str_resposta,
                                              str_titulo= self.TITULO,
                                              str_autor="Comando Administrativo",
                                              str_servidor=self.SERVIDOR,
                                              str_site=self.SITE_PRINCIPAL,
                                              str_doe=self.SITE_DOACAO,
                                              str_rodape=self.RODAPE)

        if isinstance(payload, commands.Context):
            ctx : commands.Context = payload
            await ctx.send(embed=embed)

        if isinstance(payload, discord.Interaction):
            itr : discord.Interaction = payload
            await itr.response.send_message(embed=embed)

    async def thunder (
                       self, 
                       payload      : commands.Context | discord.Interaction,
                       zrcon        : ZomboidRCON,
                       *,
                       str_usuario  : str
                      ):

        str_resposta = zrcon.command("thunder", str_usuario).response

        embed = _whbot_rcon_cards.rcon_card_a(str_mensagem=str_resposta,
                                              str_titulo= self.TITULO,
                                              str_autor="Comando Administrativo",
                                              str_servidor=self.SERVIDOR,
                                              str_site=self.SITE_PRINCIPAL,
                                              str_doe=self.SITE_DOACAO,
                                              str_rodape=self.RODAPE)
        
        if isinstance(payload, commands.Context):
            ctx : commands.Context = payload
            await ctx.send(embed=embed)
        
        if isinstance(payload, discord.Interaction):
            itr : discord.Interaction = payload
            await itr.response.send_message(embed=embed)

class _whbot_rcon_comandos_geral():
    
    def __init__ (self, SITE_PRINCIPAL : str = None, SITE_DOACAO : str = None, TITULO : str = None, SERVIDOR : str = None, RODAPE : str = None):
        
        self.SITE_PRINCIPAL : str = SITE_PRINCIPAL
        self.SITE_DOACAO    : str = SITE_DOACAO
        self.TITULO         : str = TITULO
        self.SERVIDOR       : str = SERVIDOR
        self.RODAPE         : str = RODAPE

    async def additem(
                      self,
                      payload   : commands.Context | discord.Interaction,
                      zrcon     : ZomboidRCON,
                      *,
                      str_user  : str,
                      str_item  : str
                     ) -> None:
        """
        Adiciona um item para o jogador.
        """

        str_resposta = zrcon.additem(str_user, str_item).response

        embed = _whbot_rcon_cards.rcon_card_a(str_mensagem=str_resposta,
                                              str_titulo= self.TITULO,
                                              str_autor="Comando Administrativo",
                                              str_servidor=self.SERVIDOR,
                                              str_site=self.SITE_PRINCIPAL,
                                              str_doe=self.SITE_DOACAO,
                                              str_rodape=self.RODAPE)
        
        if isinstance(payload, commands.Context):
            ctx : commands.Context = payload
            await ctx.send(embed=embed)
        
        if isinstance(payload, discord.Interaction):
            itr : discord.Interaction = payload
            await itr.response.send_message(embed=embed)

    async def addvehicle (
                          self,  
                          payload       : commands.Context | discord.Interaction,
                          zrcon         : ZomboidRCON,
                          *,
                          str_usuario   : str
                         ) -> None:
        """
        Materializa um veículo perto do usuário.
        """
        
        str_resposta = zrcon.addvehicle(str_usuario).response

        embed = _whbot_rcon_cards.rcon_card_a(str_mensagem=str_resposta,
                                              str_titulo= self.TITULO,
                                              str_autor="Comando Administrativo",
                                              str_servidor=self.SERVIDOR,
                                              str_site=self.SITE_PRINCIPAL,
                                              str_doe=self.SITE_DOACAO,
                                              str_rodape=self.RODAPE)
        
        if isinstance(payload, commands.Context):
            ctx : commands.Context = payload
            await ctx.send(embed=embed)
        
        if isinstance(payload, discord.Interaction):
            itr : discord.Interaction = payload
            await itr.response.send_message(embed=embed)

    async def addxp(
                    self,
                    payload     : commands.Context | discord.Interaction,
                    zrcon       : ZomboidRCON,
                    *,
                    str_user    : str,
                    str_perk    : str,
                    int_xp      : int,
                )-> None:
        """
        Dá experiência a um usuário.
        """
        
        str_resposta = zrcon.addxp(str_user, str_perk, int_xp).response

        embed = _whbot_rcon_cards.rcon_card_a(str_mensagem=str_resposta,
                                              str_titulo= self.TITULO,
                                              str_autor="Comando Administrativo",
                                              str_servidor=self.SERVIDOR,
                                              str_site=self.SITE_PRINCIPAL,
                                              str_doe=self.SITE_DOACAO,
                                              str_rodape=self.RODAPE)
        
        if isinstance(payload, commands.Context):
            ctx : commands.Context = payload
            await ctx.send(embed=embed)
        
        if isinstance(payload, discord.Interaction):
            itr : discord.Interaction = payload
            await itr.response.send_message(embed=embed)

    async def alarm(
                    self,
                    payload     : commands.Context | discord.Interaction, 
                    zrcon       : ZomboidRCON
                   ) -> None:
        """
        Soa um alarme no local onde o administrador está. Necessário estar dentro de uma sala.
        """

        str_resposta = zrcon.alarm().response

        embed = _whbot_rcon_cards.rcon_card_a(str_mensagem=str_resposta,
                                              str_titulo= self.TITULO,
                                              str_autor="Comando Administrativo",
                                              str_servidor=self.SERVIDOR,
                                              str_site=self.SITE_PRINCIPAL,
                                              str_doe=self.SITE_DOACAO,
                                              str_rodape=self.RODAPE)
        
        if isinstance(payload, commands.Context):
            ctx : commands.Context = payload
            await ctx.send(embed=embed)
        
        if isinstance(payload, discord.Interaction):
            itr : discord.Interaction = payload
            await itr.response.send_message(embed=embed)

    async def chopper(
                      self,
                      payload   : commands.Context | discord.Interaction,
                      zrcon     : ZomboidRCON
                     ) -> None:
        """
        Coloca um helicóptero em um usuário aleatório
        """

        str_resposta = zrcon.chopper().response

        embed = _whbot_rcon_cards.rcon_card_a(str_mensagem=str_resposta,
                                              str_titulo= self.TITULO,
                                              str_autor="Comando Administrativo",
                                              str_servidor=self.SERVIDOR,
                                              str_site=self.SITE_PRINCIPAL,
                                              str_doe=self.SITE_DOACAO,
                                              str_rodape=self.RODAPE)
        
        if isinstance(payload, commands.Context):
            ctx : commands.Context = payload
            await ctx.send(embed=embed)
        
        if isinstance(payload, discord.Interaction):
            itr : discord.Interaction = payload
            await itr.response.send_message(embed=embed)
    
    async def createhorde(
                          self,
                          payload       : commands.Context | discord.Interaction, 
                          zrcon         : ZomboidRCON,
                          int_hordas    : str
                         )-> None:
        """
        Cria uma horda próximo do jogador.
        """

        str_resposta = zrcon.createhorde(int_hordas).response

        embed = _whbot_rcon_cards.rcon_card_a(str_mensagem=str_resposta,
                                              str_titulo= self.TITULO,
                                              str_autor="Comando Administrativo",
                                              str_servidor=self.SERVIDOR,
                                              str_site=self.SITE_PRINCIPAL,
                                              str_doe=self.SITE_DOACAO,
                                              str_rodape=self.RODAPE)
        
        if isinstance(payload, commands.Context):
            ctx : commands.Context = payload
            await ctx.send(embed=embed)
        
        if isinstance(payload, discord.Interaction):
            itr : discord.Interaction = payload
            await itr.response.send_message(embed=embed)

    async def godmode(
                      self,  
                      payload       : commands.Context | discord.Interaction,
                      zrcon         : ZomboidRCON,
                      *,
                      str_usuario   : str
                     )-> None:
        """
        Faz um jogador invencível.
        """
        
        str_resposta = zrcon.godmode(str_usuario).response

        embed = _whbot_rcon_cards.rcon_card_a(str_mensagem=str_resposta,
                                              str_titulo= self.TITULO,
                                              str_autor="Comando Administrativo",
                                              str_servidor=self.SERVIDOR,
                                              str_site=self.SITE_PRINCIPAL,
                                              str_doe=self.SITE_DOACAO,
                                              str_rodape=self.RODAPE)
        
        if isinstance(payload, commands.Context):
            ctx : commands.Context = payload
            await ctx.send(embed=embed)
        
        if isinstance(payload, discord.Interaction):
            itr : discord.Interaction = payload
            await itr.response.send_message(embed=embed)

    async def invisible(
                        self,
                        payload     : commands.Context | discord.Interaction,
                        zrcon       : ZomboidRCON,
                        *,
                        str_usuario : str
                       )-> None:
        """
        Faz um jogador invisível aos zumbis.
        """
        
        str_resposta = zrcon.invisible(str_usuario).response

        embed = _whbot_rcon_cards.rcon_card_a(str_mensagem=str_resposta,
                                              str_titulo= self.TITULO,
                                              str_autor="Comando Administrativo",
                                              str_servidor=self.SERVIDOR,
                                              str_site=self.SITE_PRINCIPAL,
                                              str_doe=self.SITE_DOACAO,
                                              str_rodape=self.RODAPE)
        
        if isinstance(payload, commands.Context):
            ctx : commands.Context = payload
            await ctx.send(embed=embed)
        
        if isinstance(payload, discord.Interaction):
            itr : discord.Interaction = payload
            await itr.response.send_message(embed=embed)

    async def noclip(
                     self,
                     payload        : commands.Context | discord.Interaction,
                     zrcon          : ZomboidRCON,
                     str_usuario    : str
                    )-> None:
        """
        Permite o usuário atravessar objetos sólidos.
        """
        
        str_resposta = zrcon.noclip(str_usuario).response

        embed = _whbot_rcon_cards.rcon_card_a(str_mensagem=str_resposta,
                                              str_titulo= self.TITULO,
                                              str_autor="Comando Administrativo",
                                              str_servidor=self.SERVIDOR,
                                              str_site=self.SITE_PRINCIPAL,
                                              str_doe=self.SITE_DOACAO,
                                              str_rodape=self.RODAPE)
        
        if isinstance(payload, commands.Context):
            ctx : commands.Context = payload
            await ctx.send(embed=embed)
        
        if isinstance(payload, discord.Interaction):
            itr : discord.Interaction = payload
            await itr.response.send_message(embed=embed)

    async def reloadoptions(
                            self,
                            payload     : commands.Context | discord.Interaction,
                            zrcon       : ZomboidRCON
                           )-> None:
        """
        Recarrega opções do servidor
        """

        str_resposta = zrcon.reloadoptions().response

        embed = _whbot_rcon_cards.rcon_card_a(str_mensagem=str_resposta,
                                              str_titulo= self.TITULO,
                                              str_autor="Comando Administrativo",
                                              str_servidor=self.SERVIDOR,
                                              str_site=self.SITE_PRINCIPAL,
                                              str_doe=self.SITE_DOACAO,
                                              str_rodape=self.RODAPE)
        
        if isinstance(payload, commands.Context):
            ctx : commands.Context = payload
            await ctx.send(embed=embed)
        
        if isinstance(payload, discord.Interaction):
            itr : discord.Interaction = payload
            await itr.response.send_message(embed=embed)
    
    async def save(
                   self,
                   payload  : commands.Context | discord.Interaction,
                   zrcon    : ZomboidRCON
                  ) -> None:
        """
        Salva o mundo atual.
        """

        str_resposta = zrcon.save().response

        embed = _whbot_rcon_cards.rcon_card_a(str_mensagem=str_resposta,
                                              str_titulo= self.TITULO,
                                              str_autor="Comando Administrativo",
                                              str_servidor=self.SERVIDOR,
                                              str_site=self.SITE_PRINCIPAL,
                                              str_doe=self.SITE_DOACAO,
                                              str_rodape=self.RODAPE)
        
        if isinstance(payload, commands.Context):
            ctx : commands.Context = payload
            await ctx.send(embed=embed)
        
        if isinstance(payload, discord.Interaction):
            itr : discord.Interaction = payload
            await itr.response.send_message(embed=embed)
    
    async def sendpulse(
                        self,
                        payload     : commands.Context | discord.Interaction,
                        zrcon       : ZomboidRCON
                       ) -> None:

        """
        Alterna envio de performance do servidor para o cliente.
        """
        
        str_resposta = zrcon.sendpulse().response

        embed = _whbot_rcon_cards.rcon_card_a(str_mensagem=str_resposta,
                                              str_titulo= self.TITULO,
                                              str_autor="Comando Administrativo",
                                              str_servidor=self.SERVIDOR,
                                              str_site=self.SITE_PRINCIPAL,
                                              str_doe=self.SITE_DOACAO,
                                              str_rodape=self.RODAPE)
        
        if isinstance(payload, commands.Context):
            ctx : commands.Context = payload
            await ctx.send(embed=embed)
        
        if isinstance(payload, discord.Interaction):
            itr : discord.Interaction = payload
            await itr.response.send_message(embed=embed)
    
    async def showoptions(
                          self,
                          payload   : commands.Context | discord.Interaction,
                          zrcon     : ZomboidRCON
                         ) -> None:
        """
        Mostra as opções configuradas no servidor. (ainda não funcionando)
        """
        
        str_resposta = zrcon.showoptions().response

        embed = _whbot_rcon_cards.rcon_card_a(str_mensagem=str_resposta,
                                              str_titulo= self.TITULO,
                                              str_autor="Comando Administrativo",
                                              str_servidor=self.SERVIDOR,
                                              str_site=self.SITE_PRINCIPAL,
                                              str_doe=self.SITE_DOACAO,
                                              str_rodape=self.RODAPE)
        
        if isinstance(payload, commands.Context):
            ctx : commands.Context = payload
            await ctx.send(embed=embed)
        
        if isinstance(payload, discord.Interaction):
            itr : discord.Interaction = payload
            await itr.response.send_message(embed=embed)
    
    async def startrain(
                        self,
                        payload     : commands.Context | discord.Interaction,
                        zrcon       : ZomboidRCON
                       ) -> None:
        """
        Inicia uma chuva no servidor.
        """
        
        str_resposta = zrcon.startrain().response

        embed = _whbot_rcon_cards.rcon_card_a(str_mensagem=str_resposta,
                                              str_titulo= self.TITULO,
                                              str_autor="Comando Administrativo",
                                              str_servidor=self.SERVIDOR,
                                              str_site=self.SITE_PRINCIPAL,
                                              str_doe=self.SITE_DOACAO,
                                              str_rodape=self.RODAPE)
        
        if isinstance(payload, commands.Context):
            ctx : commands.Context = payload
            await ctx.send(embed=embed)
        
        if isinstance(payload, discord.Interaction):
            itr : discord.Interaction = payload
            await itr.response.send_message(embed=embed)

    async def stoprain(
                       self, 
                       payload      : commands.Context | discord.Interaction,
                       zrcon        : ZomboidRCON
                      ) -> None:
        """
        Para uma chuva no servidor.
        """

        str_resposta = zrcon.stoprain().response

        embed = _whbot_rcon_cards.rcon_card_a(str_mensagem=str_resposta,
                                              str_titulo= self.TITULO,
                                              str_autor="Comando Administrativo",
                                              str_servidor=self.SERVIDOR,
                                              str_site=self.SITE_PRINCIPAL,
                                              str_doe=self.SITE_DOACAO,
                                              str_rodape=self.RODAPE)
        
        if isinstance(payload, commands.Context):
            ctx : commands.Context = payload
            await ctx.send(embed=embed)
        
        if isinstance(payload, discord.Interaction):
            itr : discord.Interaction = payload
            await itr.response.send_message(embed=embed)
    
    async def teleport(
                       self,
                       payload          : commands.Context | discord.Interaction,
                       zrcon            : ZomboidRCON,
                       *,
                       str_usuario_d    : str,
                       str_usuario_p    : str
                      )-> None:
        """
        Telaporta o usuário para perto de outro usuário.
        """

        str_resposta = zrcon.teleport(str_usuario_d, str_usuario_p).response

        embed = _whbot_rcon_cards.rcon_card_a(str_mensagem=str_resposta,
                                              str_titulo= self.TITULO,
                                              str_autor="Comando Administrativo",
                                              str_servidor=self.SERVIDOR,
                                              str_site=self.SITE_PRINCIPAL,
                                              str_doe=self.SITE_DOACAO,
                                              str_rodape=self.RODAPE)
        
        if isinstance(payload, commands.Context):
            ctx : commands.Context = payload
            await ctx.send(embed=embed)
        
        if isinstance(payload, discord.Interaction):
            itr : discord.Interaction = payload
            await itr.response.send_message(embed=embed)

    async def teleportto(
                         self,
                         payload    : commands.Context | discord.Interaction,
                         zrcon      : ZomboidRCON,
                         *,
                         int_x      : str,
                         int_y      : str, 
                         int_z      : str,
                        )-> None:
        """
        Transporta o usuário para uma determinada coordenada.
        """

        str_resposta = zrcon.teleportto(int_x, int_y, int_z).response

        embed = _whbot_rcon_cards.rcon_card_a(str_mensagem=str_resposta,
                                              str_titulo= self.TITULO,
                                              str_autor="Comando Administrativo",
                                              str_servidor=self.SERVIDOR,
                                              str_site=self.SITE_PRINCIPAL,
                                              str_doe=self.SITE_DOACAO,
                                              str_rodape=self.RODAPE)
        
        if isinstance(payload, commands.Context):
            ctx : commands.Context = payload
            await ctx.send(embed=embed)
        
        if isinstance(payload, discord.Interaction):
            itr : discord.Interaction = payload
            await itr.response.send_message(embed=embed)

    async def checkupdate (
                           self, 
                           payload  : commands.Context | discord.Interaction,
                           zrcon    : ZomboidRCON  
                          ) -> None:

        str_resposta = zrcon.checkModsNeedUpdate().response

        embed = _whbot_rcon_cards.rcon_card_a(str_mensagem=str_resposta,
                                              str_titulo= self.TITULO,
                                              str_autor="Comando Administrativo",
                                              str_servidor=self.SERVIDOR,
                                              str_site=self.SITE_PRINCIPAL,
                                              str_doe=self.SITE_DOACAO,
                                              str_rodape=self.RODAPE)
        
        if isinstance(payload, commands.Context):
            ctx : commands.Context = payload
            await ctx.send(embed=embed)
        
        if isinstance(payload, discord.Interaction):
            itr : discord.Interaction = payload
            await itr.response.send_message(embed=embed)

        return

class whbot_rcon_tarefas_recorrentes(commands.Cog, name="Automatizacao"):

    def __init__(self,
                 bot : commands.Bot, 
                 zrcon : ZomboidRCON,
                 str_site_principal : str = None,
                 str_site_doacao    : str = None,
                 str_titulo         : str = None,
                 str_servidor       : str = None,
                 str_rodape         : str = None                 
                ):

        self.bot : commands.Bot = bot
        self.zrcon : ZomboidRCON = zrcon
        self.bln_mod_check = True

        self.str_site_principal = str_site_principal
        self.str_site_doacao = str_site_doacao
        self.str_titulo = str_titulo
        self.str_titulo = str_titulo
        self.str_servidor = str_servidor
        self.str_rodape = str_rodape

        self.checkmodupdate.start()

    @tasks.loop(minutes=5, count=None)
    async def checkmodupdate(self) -> None:
        if self.bln_mod_check:
            async with wh_locks.lck_atulizar_mods:
                await self.bot.wait_until_ready()
                self.zrcon.checkModsNeedUpdate()

    @app_commands.command(name="checarporatualizacoes", description="Habilita ou desabilita a checagem de atualização de MODS")
    @app_commands.rename(bln_mod_check="ativo")
    @app_commands.describe(bln_mod_check="Checagem de atualizações ativa?.")
    async def checarporatualizacoes(self,
                                    itx : discord.Interaction,
                                    *,
                                    bln_mod_check : bool
                                    ) -> None:
        
        if bln_mod_check:
            str_resposta = "Verificação de atualização de mods habilitada."
        else: 
            str_resposta = "Verificação de atualização de mods desabilitada."

        embed = _whbot_rcon_cards.rcon_card_a(str_mensagem=str_resposta,
                                              str_titulo=self.str_titulo,
                                              str_autor="Comando Administrativo",
                                              str_servidor=self.str_servidor,
                                              str_site=self.str_site_principal,
                                              str_doe=self.str_site_doacao,
                                              str_rodape=self.str_rodape)
                
        self.bln_mod_check = bln_mod_check

        await itx.response.send_message(embed=embed)

class whbot_rcon_comandos_moderador(commands.Cog, name="Moderadores"): 

    def __init__(self,
                 bot                : commands.Bot, 
                 zrcon              : ZomboidRCON,
                 str_site_principal : str = None,
                 str_site_doacao    : str = None,
                 str_titulo         : str = None,
                 str_servidor       : str = None,
                 str_rodape         : str = None):

        self.bot        : commands.Bot = bot
        self.zrcon      : ZomboidRCON = zrcon
        self.moderador  : _whbot_rcon_comandos_moderador = _whbot_rcon_comandos_moderador(SITE_PRINCIPAL = str_site_principal, 
                                                                                          SITE_DOACAO = str_site_doacao, 
                                                                                          TITULO = str_titulo, 
                                                                                          SERVIDOR = str_servidor, 
                                                                                          RODAPE = str_rodape)

    @commands.command(name="players")
    @has_permissions(administrator=True)
    #@Ccheks.e_canal_administrativo(str_canal=CANAL_ADMINISTRADOR)
    async def players(self, 
                      ctx : commands.Context
                     ) -> None:
        """
        Mostra os jogadores conectados.
        Método administrativo.
        
        Sintaxe:
            !players            
        """

        await self.moderador.players(
                                     payload = ctx,
                                     zrcon = self.zrcon
                                    )
    
    @commands.command()
    @has_permissions(administrator=True)
    #@Ccheks.e_canal_administrativo(str_canal=CANAL_ADMINISTRADOR)
    async def addalltowhitelist(self, 
                                ctx : commands.Context
                               ) -> None:
        """
        Adiciona todos os usuários conectado a whitelist.
        Método administrativo. 

        Sintaxe:
            !addalltowhitelist
        """

        await self.moderador.addalltowhitelist(
                                               payload = ctx,
                                               zrcon = self.zrcon
                                              )

    @commands.command()
    @has_permissions(administrator=True)
    #@Ccheks.e_canal_administrativo(str_canal=CANAL_ADMINISTRADOR)
    async def adduser(self, 
                      ctx           : commands.Context,
                      str_usuario   : str = commands.parameter(default=None, displayed_name="usuario", description=": str -> Nome do usuario"),
                      str_senha     : str = commands.parameter(default=None, displayed_name="senha", description=": str -> Senha do usuario")
                     ) -> None:
        """
        Adiciona um novo usuário na whitelist.
        Método administrativo. 

        Sintaxe:
            !adduser usuario senha
        """

        await self.moderador.adduser(
                                     payload = ctx,
                                     zrcon = self.zrcon,
                                     str_usuario = str_usuario,
                                     str_senha = str_senha  
                                    )

    @commands.command()
    @has_permissions(administrator=True)
    #@Ccheks.e_canal_administrativo(str_canal=CANAL_ADMINISTRADOR)
    async def addusertowhitelist(
                                 self, 
                                 ctx        : commands.Context,
                                 str_usuario: str = commands.parameter(default=None, displayed_name="usuario", description=": str -> Nome do usuario")
                                ) -> None:
        """
        Adiciona um simples usuário a whitelist.
        Método administrativo. 

        Argumentos:
            usuario : str -> Nome do usuário

        Sintaxe:
            !addusertowhitelist usuario
        """
        
        await self.moderador.addusertowhitelist(
                                                payload = ctx,
                                                zrcon = self.zrcon,
                                                str_usuario = str_usuario
                                               )


    @commands.command()
    @has_permissions(administrator=True)
    #@Ccheks.e_canal_administrativo(str_canal=CANAL_ADMINISTRADOR)
    async def removeuserfromwhitelist(
                                      self, 
                                      ctx           : commands.Context,
                                      str_usuario   : str = commands.parameter(default=None, displayed_name="usuario", description=": str -> Nome do usuario")
                                     ) -> None:
        """
        Remove um simples usuário a whitelist.
        Método administrativo. 

        Argumentos:
            usuario : str -> Nome do usuário

        Sintaxe:
            !removeuserfromwhitelist usuario
        """

        await self.moderador.removeuserfromwhitelist(
                                                     payload = ctx,
                                                     zrcon = self.zrcon,
                                                     str_usuario = str_usuario
                                                    )


    @commands.command()
    @has_permissions(administrator=True)
    #@Ccheks.e_canal_administrativo(str_canal=CANAL_ADMINISTRADOR)
    async def banid(
                    self,
                    ctx     : commands.Context,
                    str_id  : str = commands.parameter(default=None, displayed_name="steamid", description=": str -> Identificador da steam")
                   ) -> None:
        """
        Bane o usuario pelo steam ID.
        Método administrativo. 

        Argumentos:
            steamid : int - > Identificador da Steam

        Sintaxe:
            !banid steamid
        """
        
        await self.moderador.banid(
                                   payload = ctx,
                                   zrcon = self.zrcon,
                                   str_id = str_id
                                  )

    @commands.command()
    @has_permissions(administrator=True)
    #@Ccheks.e_canal_administrativo(str_canal=CANAL_ADMINISTRADOR)
    async def unbanid(
                      self,
                      ctx       : commands.Context,
                      str_id    : str = commands.parameter(default=None, displayed_name="steamid", description=": str -> Identificador da steam")
                     ) -> None:
        """
        Remove o banimento do usuario pelo steam ID.
        Método administrativo. 

        Sintaxe:
            !unbanid steamid
        """
    
        await self.moderador.unbanid(
                                     payload = ctx,
                                     zrcon = self.zrcon,
                                     str_id = str_id
                                    )

    @commands.command()
    @has_permissions(administrator=True)
    #@Ccheks.e_canal_administrativo(str_canal=CANAL_ADMINISTRADOR)
    async def banuser(
                      self,
                      ctx           : commands.Context,
                      str_usuario   : str = commands.parameter(default=None, displayed_name="usuario", description=": str -> Nome do usuario")
                     ) -> None:
        """
        Bane o usuario pelo nome.
        Método administrativo. 

        Sintaxe:
            !banuser usuario
        """
        
        await self.moderador.banuser(
                                     payload = ctx,
                                     zrcon = self.zrcon,
                                     str_usuario = str_usuario
                                    )
    @commands.command()
    @has_permissions(administrator=True)
    #@Ccheks.e_canal_administrativo(str_canal=CANAL_ADMINISTRADOR)
    async def unbanuser(
                        self,
                        ctx         : commands.Context,
                        str_usuario : str = commands.parameter(default=None, displayed_name="usuario", description=": str -> Nome do usuario")
                       ) -> None:
        """
        Remove o banimento do usuario pelo nome.
        Método administrativo. 

        Sintaxe:
            !unbanuser usuario
        """
        
        await self.moderador.unbanuser(
                                       payload=ctx,
                                       zrcon=self.zrcon,
                                       str_usuario=str_usuario
                                      )

    @commands.command()
    @has_permissions(administrator=True)
    #@Ccheks.e_canal_administrativo(str_canal=CANAL_ADMINISTRADOR)
    async def grantadmin(
                         self,
                         ctx : commands.Context,
                         str_usuario : str = commands.parameter(default=None, displayed_name="usuario", description=": str -> Nome do usuario")
                        ) -> None:
        """
        Concede permissoes de admin a um usuario.
        Método administrativo. 

        Sintaxe:
            !grantadmin usuario
        """

        await self.moderador.grantadmin(
                                        payload = ctx,
                                        zrcon = self.zrcon,
                                        str_usuario = str_usuario
                                       )

    @commands.command()
    @has_permissions(administrator=True)
    #@Ccheks.e_canal_administrativo(str_canal=CANAL_ADMINISTRADOR)
    async def removeadmin(
                          self,
                          ctx           : commands.Context,
                          str_usuario   : str = commands.parameter(default=None, displayed_name="usuario", description=": str -> Nome do usuario")
                         ) -> None:
        """
        Remove permissoes de admin de um usuario.
        Método administrativo. 

        Sintaxe:
            !removeadmin usuario
        """
        
        await self.moderador.removeadmin(
                                         payload = ctx,
                                         zrcon = self.zrcon,
                                         str_usuario = str_usuario
                                        )

    @commands.command()
    @has_permissions(administrator=True)
    #@Ccheks.e_canal_administrativo(str_canal=CANAL_ADMINISTRADOR)
    async def kickuser(
                       self,
                       ctx          : commands.Context,
                       str_usuario  : str = commands.parameter(default=None, displayed_name="usuario", description=": str -> Nome do usuario")
                      ) -> None:
        """
        Chuta um usuário do servidor.
        Método administrativo. 

        Sintaxe:
            !kickuser usuario
        """
        
        await self.moderador.kickuser(
                                      payload = ctx,
                                      zrcon = self.zrcon,
                                      str_usuario = str_usuario
                                     )

    @commands.command()
    @has_permissions(administrator=True)
    #@Ccheks.e_canal_administrativo(str_canal=CANAL_ADMINISTRADOR)
    async def servermsg(self,
                        ctx             : commands.Context,
                        str_mensagem    : str = commands.parameter(default=None, displayed_name="mensagem", description=": str -> Mensagem a ser enviada."),
                    ) -> None: 
        """
        Envia uma mensagem a todos os jogadores.
        Método administrativo. 

        Sintaxe:
            !servermsg mensagem
        """

        await self.moderador.servermsg(
                                       payload = ctx,
                                       zrcon = self.zrcon,
                                       str_mensagem = str_mensagem
                                      )

    @commands.command()
    @has_permissions(administrator=True)
    #@Ccheks.e_canal_administrativo(str_canal=CANAL_ADMINISTRADOR)
    async def setaccesslevel(
                             self,
                             ctx        : commands.Context,
                             str_usuario: str = commands.parameter(default=None, displayed_name="usuario", description=": str -> Nome do usuario"),
                             str_acesso : str = commands.parameter(default=None, displayed_name="acesso", description=": str -> Nível de acesso [admin | moderator | overseer | gm  | observer].")
                            ) -> None: 
        """
        Define o nível de acesso dos jogadores.
        Método administrativo. 

        Sintaxe:
            !setaccesslevel usuario acesso
        """

        await self.moderador.setaccesslevel(
                                            payload = ctx,
                                            zrcon = self.zrcon,
                                            str_usuario = str_usuario,
                                            str_acesso = str_acesso
                                           )

    @commands.command()
    @has_permissions(administrator=True)
    #@Ccheks.e_canal_administrativo(str_canal=CANAL_ADMINISTRADOR)
    async def thunder (
                       self,
                       ctx          : commands.Context,
                       str_usuario  : str = commands.parameter(default=None, displayed_name="usuario", description=": str -> Nome do usuario")
                      ):

        await self.moderador.thunder(
                                     payload = ctx,
                                     zrcon = self.zrcon,
                                     str_usuario = str_usuario
                                    )

class whbot_rcon_comandos_geral(commands.Cog, name="Administradores"): #ajustar aqui

    def __init__(self, 
                 bot                : commands.Bot, 
                 zrcon              : ZomboidRCON,
                 str_site_principal : str = None,
                 str_site_doacao    : str = None,
                 str_titulo         : str = None,
                 str_servidor       : str = None,
                 str_rodape         : str = None):

        self.bot    : commands.Bot = bot
        self.zrcon  : ZomboidRCON = zrcon
        self.geral  : _whbot_rcon_comandos_geral = _whbot_rcon_comandos_geral(SITE_PRINCIPAL = str_site_principal, 
                                                                              SITE_DOACAO = str_site_doacao, 
                                                                              TITULO = str_titulo, 
                                                                              SERVIDOR = str_servidor, 
                                                                              RODAPE = str_rodape)

    @commands.command()
    @has_permissions(administrator=True)
    #@Ccheks.e_canal_administrativo(str_canal=CANAL_ADMINISTRADOR)    
    async def additem(
                      self,
                      ctx       : commands.Context, 
                      str_user  : str=commands.parameter(default=None, displayed_name="usuario", description=": str -> Nome do usuário"), 
                      str_item  : str =commands.parameter(default=None, displayed_name="item", description=": str -> Item a ser adicionado")
                     ) -> None:
        """
        Adiciona um item para o jogador.
        Método administrativo.
        Items can be found on the PZ wiki: https://pzwiki.net/wiki/Items

        Sintaxe:
            !additem usuario item
        """

        await self.geral.additem(
                                 payload = ctx,
                                 zrcon = self.zrcon,
                                 str_user = str_user,
                                 str_item = str_item
                                )

    @commands.command()
    @has_permissions(administrator=True)
    #@Ccheks.e_canal_administrativo(str_canal=CANAL_ADMINISTRADOR)
    async def addvehicle (
                          self,
                          ctx           : commands.Context, 
                          str_usuario   : str = commands.parameter(default=None, displayed_name="usuario", description=": str -> Nome do usuário")
                         ) -> None:
        """
        Materializa um veículo perto do usuário.
        Método Administrativo.

        Sintaxe:
            !addvehicle usuario
        """

        await self.geral.addvehicle(
                                    payload = ctx,
                                    zrcon = self.zrcon,
                                    str_usuario = str_usuario
                                   )
    
    @commands.command()
    @has_permissions(administrator=True)
    #@Ccheks.e_canal_administrativo(str_canal=CANAL_ADMINISTRADOR)
    async def addxp(
                    self,
                    ctx         : commands.Context, 
                    str_user    : str = commands.parameter(default=None, displayed_name="usuario", description=": str -> Nome do usuário"), 
                    str_perk    : str = commands.parameter(default=None, displayed_name="perk", description=": str -> Perk do usuário"), 
                    int_xp      : int = commands.parameter(default=None, displayed_name="xp", description=": str -> XP do usuário") 
                )-> None:
        """
        Dá experiência a um usuário.
        Método Administrativo.

        Returns:
            None
        
        Syntax:
            !addxp usuario perk experiencia
        """
        
        await self.geral.addxp(
                               payload = ctx,
                               zrcon = self.zrcon,
                               str_user = str_user,
                               str_perk = str_perk,
                               int_xp = int_xp
                              )

    @commands.command()
    @has_permissions(administrator=True)
    #@Ccheks.e_canal_administrativo(str_canal=CANAL_ADMINISTRADOR)
    async def alarm(
                    self, 
                    ctx : commands.Context
                   ) -> None:
        """
        Soa um alarme no local onde o administrador está. Necessário estar dentro de uma sala.
        Método administrativo. 
                    
        Sintaxe:
            !alarm
        """

        await self.geral.alarm(
                               payload = ctx,
                               zrcon = self.zrcon
                              )

    @commands.command()
    @has_permissions(administrator=True)
    #@Ccheks.e_canal_administrativo(str_canal=CANAL_ADMINISTRADOR)
    async def chopper(self,
                      ctx : commands.Context
                     ) -> None:
        """
        Coloca um helicóptero em um usuário aleatório
        Método administrativo. 

        Sintaxe:
            !chopper    
        """

        await self.geral.chopper(
                                 payload = ctx,
                                 zrcon = self.zrcon
                                )

    @commands.command()
    @has_permissions(administrator=True)
    #@Ccheks.e_canal_administrativo(str_canal=CANAL_ADMINISTRADOR)
    async def createhorde(
                          self, 
                          ctx           : commands.Context, 
                          int_hordas    : str = commands.parameter(default=None, displayed_name="horda", description=": str -> Quantidade") 
                         )-> None:
        """
        Cria uma horda próximo do jogador.
        Método Administrativo.
        
        Sintaxe:
            !createhorde horda
        """

        await self.geral.createhorde(
                                     payload = ctx,
                                     zrcon = self.zrcon,
                                     int_hordas = int_hordas
                                    )
        
    @commands.command()
    @has_permissions(administrator=True)
    #@Ccheks.e_canal_administrativo(str_canal=CANAL_ADMINISTRADOR)    
    async def godmode(
                      self,
                      ctx           : commands.Context, 
                      str_usuario   : str = commands.parameter(default=None, displayed_name="usuario", description=": str -> Nome do usuário."), 
                     )-> None:
        """
        Faz um jogador invencível.
        Método Administrativo.

        Sintaxe:
            !godmode usuario
        """
        
        await self.geral.godmode(
                                 payload = ctx,
                                 zrcon = self.zrcon,
                                 str_usuario = str_usuario
                                )

    @commands.command()
    @has_permissions(administrator=True)
    #@Ccheks.e_canal_administrativo(str_canal=CANAL_ADMINISTRADOR)    
    async def invisible(
                        self,
                        ctx         : commands.Context, 
                        str_usuario : str = commands.parameter(default=None, displayed_name="usuario", description=": str -> Nome do usuário."), 
                       )-> None:
        """
        Faz um jogador invisível aos zumbis.
        Método Administrativo.
        
        Sintaxe:
            !invisible usuario
        """
        
        await self.geral.invisible(
                                   payload = ctx,
                                   zrcon = self.zrcon,
                                   str_usuario = str_usuario
                                  )
        
    @commands.command()
    @has_permissions(administrator=True)
    #@Ccheks.e_canal_administrativo(str_canal=CANAL_ADMINISTRADOR)
    async def noclip(
                     self,
                     ctx            : commands.Context, 
                     str_usuario    : str = commands.parameter(default=None, displayed_name="usuario", description=": str -> Nome do usuário."), 
                    )-> None:
        """
        Permite o usuário atravessar objetos sólidos.
        Método Administrativo.
        
        Sintaxe:
            !noclip usuario
        """
        
        await self.geral.noclip(
                                payload = ctx,
                                zrcon = self.zrcon,
                                str_usuario = str_usuario
                               )

    @commands.command()
    @has_permissions(administrator=True)
    #@Ccheks.e_canal_administrativo(str_canal=CANAL_ADMINISTRADOR)
    async def reloadoptions(
                            self,
                            ctx     : commands.Context
                           )-> None:
        """
        Recarrega opções do servidor
        Método Administrativo.
        
        Syntax:
            !reloadoptions
        """

        await self.geral.reloadoptions(
                                       payload = ctx,
                                       zrcon = self.zrcon
                                      )

    @commands.command()
    @has_permissions(administrator=True)
    #@Ccheks.e_canal_administrativo(str_canal=CANAL_ADMINISTRADOR)
    async def save(
                   self,
                   ctx : commands.Context
                  ) -> None:
        """
        Salva o mundo atual.
        Método administrativo. 
                    
        Sintaxe:
            !save    
        """

        await self.geral.save(
                              payload = ctx,
                              zrcon=self.zrcon
                             )

    @commands.command()
    @has_permissions(administrator=True)
    #@Ccheks.e_canal_administrativo(str_canal=CANAL_ADMINISTRADOR)
    async def sendpulse(
                        self,
                        ctx : commands.Context
                       ) -> None:

        """
        Alterna envio de performance do servidor para o cliente.
        Método administrativo. 

        Sintaxe:
            !sendpulse    
        """

        await self.geral.sendpulse(
                                   payload = ctx,
                                   zrcon = self.zrcon
                                  )

    @commands.command()
    @has_permissions(administrator=True)
    #@Ccheks.e_canal_administrativo(str_canal=CANAL_ADMINISTRADOR)
    async def showoptions(
                          self,
                          ctx : commands.Context
                         ) -> None:
        """
        Mostra as opções configuradas no servidor. (ainda não funcionando)
        Método administrativo. 

        Sintaxe:
            !showoptions    
        """
        
        await self.geral.showoptions(
                                     payload = ctx,
                                     zrcon = self.zrcon
                                    )

    @commands.command()
    @has_permissions(administrator=True)
    #@Ccheks.e_canal_administrativo(str_canal=CANAL_ADMINISTRADOR)
    async def startrain(
                        self,
                        ctx : commands.Context
                       ) -> None:
        """
        Inicia uma chuva no servidor.
        Método administrativo. 

        Sintaxe:
            !startrain    
        """
        
        await self.geral.startrain(
                                   payload = ctx,
                                   zrcon = self.zrcon
                                  )
        
    @commands.command()
    @has_permissions(administrator=True)
    #@Ccheks.e_canal_administrativo(str_canal=CANAL_ADMINISTRADOR)
    async def stoprain(
                       self,
                       ctx : commands.Context
                      ) -> None:
        """
        Para uma chuva no servidor.
        Método administrativo. 

        Sintaxe:
            !stoprain    
        """
        
        await self.geral.stoprain(
                                  payload = ctx,
                                  zrcon = self.zrcon
                                 )

    @commands.command()
    @has_permissions(administrator=True)
    #@Ccheks.e_canal_administrativo(str_canal=CANAL_ADMINISTRADOR)
    async def teleport(
                       self,
                       ctx              : commands.Context, 
                       str_usuario_d    : str = commands.parameter(default=None, displayed_name="de_usuario", description=":str -> Nome do usuário."), 
                       str_usuario_p    : str = commands.parameter(default=None, displayed_name="para_usuario", description=": str -> Nome do usuário.")
                      )-> None:
        """
        Telaporta o usuário para perto de outro usuário.
        Método Administrativo.
        
        Syntax:
            !teleport de_usuario para_usuario
        """
        
        await self.geral.teleport(
                                  payload = ctx,
                                  zrcon = self.zrcon,
                                  str_usuario_d = str_usuario_d,
                                  str_usuario_p = str_usuario_p
                                 )


    @commands.command()
    @has_permissions(administrator=True)
    #@Ccheks.e_canal_administrativo(str_canal=CANAL_ADMINISTRADOR)
    async def teleportto(
                         self,
                         ctx    : commands.Context, 
                         int_x  : str = commands.parameter(default=None, displayed_name="x", description=": int -> Coordenada X."), 
                         int_y  : str = commands.parameter(default=None, displayed_name="x", description=": int -> Coordenada Y."), 
                         int_z  : str = commands.parameter(default=None, displayed_name="x", description=": int -> Coordenada Z.")
                        )-> None:
        """
        Transporta o usuário para uma determinada coordenada.
        Método Administrativo.

        Syntax:
            !teleportto x y z
        """

        await self.geral.teleportto (
                                     payload = ctx,
                                     zrcon = self.zrcon,
                                     int_x = int_x,
                                     int_y = int_y,
                                     int_z = int_z
                                    )

    @commands.command()
    @has_permissions(administrator=True)
    #@Ccheks.e_canal_administrativo(str_canal=CANAL_ADMINISTRADOR)
    async def checkupdate (
                           self,
                           ctx : commands.Context
                          ):


        await self.geral.checkupdate(
                                     payload = ctx,
                                     zrcon = self.zrcon
                                    )

class whbot_rcon_slash_comandos_moderador(commands.Cog):

    def __init__(self, 
                 bot                : commands.Bot, 
                 zrcon              : ZomboidRCON,
                 str_site_principal : str = None,
                 str_site_doacao    : str = None,
                 str_titulo         : str = None,
                 str_servidor       : str = None,
                 str_rodape         : str = None):

        self.bot : commands.Bot = bot
        self.zrcon : ZomboidRCON = zrcon
        self.moderador = _whbot_rcon_comandos_moderador(SITE_PRINCIPAL=str_site_principal, 
                                                        SITE_DOACAO=str_site_doacao, 
                                                        TITULO=str_titulo, 
                                                        SERVIDOR=str_servidor, 
                                                        RODAPE=str_rodape)

    @app_commands.command(name="zplayers", description="Mostra os jogadores conectados.")
    @app_commands.checks.has_permissions(administrator=True)
    async def players(
                      self,
                      itr   : discord.Interaction
                     ) -> None:
        """
        Mostra os jogadores conectados.
        Método administrativo.
        """

        await self.moderador.players(
                                     payload=itr,
                                     zrcon=self.zrcon
                                    )
    
    @app_commands.command(name="zaddalltowhitelist", description="Adiciona todos os usuários conectado a whitelist.")
    @app_commands.checks.has_permissions(administrator=True)
    async def addalltowhitelist(
                                self, 
                                itr : discord.Interaction
                               ) -> None:
        """
        Adiciona todos os usuários conectado a whitelist.
        Método administrativo. 
        """

        await self.moderador.addalltowhitelist(
                                               payload = itr,
                                               zrcon = self.zrcon
                                              )

    @app_commands.command(name="zadduser", description="Adiciona um novo usuário na whitelist.")
    @app_commands.rename(str_usuario="jogador", str_senha="senha")
    @app_commands.describe(str_usuario="Nome do jogador.", str_senha="Senha do jogador.")
    @app_commands.autocomplete(str_usuario=_whbot_rcon_autocomplete.player_auto_complete)
    @app_commands.checks.has_permissions(administrator=True)
    async def adduser(
                      self, 
                      itr           : discord.Interaction,
                      *,
                      str_usuario   : str,
                      str_senha     : str
                     ) -> None:
        """
        Adiciona um novo usuário na whitelist.
        Método administrativo. 
        """

        await self.moderador.adduser(
                                     payload = itr,
                                     zrcon = self.zrcon,
                                     str_usuario = str_usuario,
                                     str_senha = str_senha
                                    )

    @app_commands.command(name="zaddusertowhitelist", description="Adiciona um simples usuário a whitelist.")
    @app_commands.rename(str_usuario="jogador")
    @app_commands.describe(str_usuario="Nome do jogador.")
    @app_commands.autocomplete(str_usuario=_whbot_rcon_autocomplete.player_auto_complete)
    @app_commands.checks.has_permissions(administrator=True)
    async def addusertowhitelist(
                                 self, 
                                 itr            : discord.Interaction,
                                 *,
                                 str_usuario    : str
                                ) -> None:
        """
        Adiciona um simples usuário a whitelist.
        Método administrativo. 
        """
        
        await self.moderador.addusertowhitelist(
                                                payload = itr,
                                                zrcon = self.zrcon,
                                                str_usuario = str_usuario
                                               )

    @app_commands.command(name="zremoveuserfromwhitelist", description="Remove um simples usuário a whitelist.")
    @app_commands.rename(str_usuario="jogador")
    @app_commands.describe(str_usuario="Nome do jogador.")
    @app_commands.autocomplete(str_usuario=_whbot_rcon_autocomplete.player_auto_complete)
    @app_commands.checks.has_permissions(administrator=True)
    async def removeuserfromwhitelist(
                                      self, 
                                      itr           : discord.Interaction,
                                      *,
                                      str_usuario   : str
                                     ) -> None:
        """
        Remove um simples usuário a whitelist.
        Método administrativo. 
        """

        await self.moderador.removeuserfromwhitelist(
                                                     payload = itr,
                                                     zrcon = self.zrcon,
                                                     str_usuario = str_usuario
                                                    )

    @app_commands.command(name="zbanid", description="Bane o usuario pelo steam ID.")
    @app_commands.rename(str_id="steamid")
    @app_commands.describe(str_id="Identificador da STEAM.")
    @app_commands.checks.has_permissions(administrator=True)
    async def banid(
                    self,
                    itr     : discord.Interaction,
                    *,
                    str_id  : str
                   ) -> None:
        """
        Bane o usuario pelo steam ID.
        Método administrativo. 
        """
        
        await self.moderador.banid(
                                   payload = itr,
                                   zrcon = self.zrcon,
                                   str_id = str_id
                                  )

    @app_commands.command(name="zunbanid", description="Remove o banimento do usuario pelo steam ID.")
    @app_commands.rename(str_id="steamid")
    @app_commands.describe(str_id="Identificador da STEAM.")
    @app_commands.checks.has_permissions(administrator=True)
    async def unbanid(
                      self,
                      itr       : discord.Interaction,
                      *,
                      str_id    : str
                     ) -> None:
        """
        Remove o banimento do usuario pelo steam ID.
        Método administrativo.
        """
    
        await self.moderador.unbanid(
                                     payload = itr,
                                     zrcon = self.zrcon,
                                     str_id = str_id
                                    )

    @app_commands.command(name="zbanuser", description="Bane o usuario pelo nome.")
    @app_commands.rename(str_usuario="jogador")
    @app_commands.describe(str_usuario="Nome do jogador.")
    @app_commands.autocomplete(str_usuario=_whbot_rcon_autocomplete.player_auto_complete)
    @app_commands.checks.has_permissions(administrator=True)
    async def banuser(
                      self,
                      itr           : discord.Interaction,
                      *,
                      str_usuario   : str
                     ) -> None:
        """
        Bane o usuario pelo nome.
        Método administrativo. 
        """
        
        await self.moderador.banuser(
                                     payload = itr,
                                     zrcon = self.zrcon,
                                     str_usuario = str_usuario
                                    )

    @app_commands.command(name="zgrantadmin", description="Concede permissoes de admin a um usuario.")
    @app_commands.rename(str_usuario="jogador")
    @app_commands.describe(str_usuario="Nome do jogador.")
    @app_commands.autocomplete(str_usuario=_whbot_rcon_autocomplete.player_auto_complete)
    @app_commands.checks.has_permissions(administrator=True)
    async def grantadmin(
                         self,
                         itr        : discord.Interaction,
                         *,
                         str_usuario: str
                        ) -> None:
        """
        Concede permissoes de admin a um usuario.
        Método administrativo. 
        """

        await self.moderador.grantadmin(
                                        payload = itr,
                                        zrcon = self.zrcon,
                                        str_usuario = str_usuario
                                       )

    @app_commands.command(name="zremoveadmin", description="Remove permissoes de admin de um usuario.")
    @app_commands.rename(str_usuario="jogador")
    @app_commands.describe(str_usuario="Nome do jogador.")
    @app_commands.autocomplete(str_usuario=_whbot_rcon_autocomplete.player_auto_complete)
    @app_commands.checks.has_permissions(administrator=True)
    async def removeadmin(
                          self,
                          itr           : discord.Interaction,
                          *,
                          str_usuario   : str
                         ) -> None:
        """
        Remove permissoes de admin de um usuario.
        Método administrativo. 
        """
        
        await self.moderador.removeadmin(
                                         payload = itr,
                                         zrcon = self.zrcon,
                                         str_usuario = str_usuario
                                        )
        
    @app_commands.command(name="zkickuser", description="Chuta um usuário do servidor.")
    @app_commands.rename(str_usuario="jogador")
    @app_commands.describe(str_usuario="Nome do jogador.")
    @app_commands.autocomplete(str_usuario=_whbot_rcon_autocomplete.player_auto_complete)
    @app_commands.checks.has_permissions(administrator=True)
    async def kickuser(
                       self,
                       itr          : discord.Interaction,
                       *,
                       str_usuario  : str
                      ) -> None:
        """
        Chuta um usuário do servidor.
        Método administrativo. 
        """

        await self.moderador.kickuser(
                                      payload = itr,
                                      zrcon = self.zrcon,
                                      str_usuario = str_usuario
                                     )

    @app_commands.command(name="zservermsg", description="Envia uma mensagem a todos os jogadores.")
    @app_commands.rename(str_mensagem="mensagem")
    @app_commands.describe(str_mensagem="Mensagem a ser enviado ao servidor.")
    @app_commands.checks.has_permissions(administrator=True)
    async def servermsg(
                        self,
                        itr             : discord.Interaction,
                        *,
                        str_mensagem    : str
                    ) -> None: 
        """
        Envia uma mensagem a todos os jogadores.
        Método administrativo. 
        """

        await self.moderador.servermsg(
                                       payload = itr,
                                       zrcon = self.zrcon,
                                       str_mensagem = str_mensagem
                                      )

    @app_commands.command(name="zsetaccesslevel", description="Define o nível de acesso dos jogadores.")
    @app_commands.rename(str_usuario="jogador", str_acesso="acesso")
    @app_commands.describe(str_usuario="Nome do jogador", str_acesso="Nível de acesso [admin | moderator | overseer | gm  | observer].")
    @app_commands.autocomplete(str_acesso=_whbot_rcon_autocomplete.access_auto_complete)
    @app_commands.autocomplete(str_usuario=_whbot_rcon_autocomplete.player_auto_complete)
    @app_commands.checks.has_permissions(administrator=True)
    async def setaccesslevel(
                             self,
                             itr            : discord.Interaction,
                             *,
                             str_usuario    : str,
                             str_acesso     : str
                            ) -> None: 
        """
        Define o nível de acesso dos jogadores. Nível de acesso [admin | moderator | overseer | gm  | observer].
        Método administrativo. 
        """

        await self.moderador.setaccesslevel(
                                            payload = itr,
                                            zrcon = self.zrcon,
                                            str_usuario = str_usuario,
                                            str_acesso = str_acesso
                                           )

    @app_commands.command(name="zthunder", description="Trovão próximo do jogador.")
    @app_commands.rename(str_usuario="jogador")
    @app_commands.describe(str_usuario="Nome do jogador.")
    @app_commands.autocomplete(str_usuario=_whbot_rcon_autocomplete.player_auto_complete)
    @app_commands.checks.has_permissions(administrator=True)
    async def thunder(
                      self,
                      itr          : discord.Interaction,
                      *,
                      str_usuario  : str 
                     ):
        """
        Trovão próximo do jogador.
        Método administrativo. 
        """
        await self.moderador.thunder(
                                     payload = itr,
                                     zrcon = self.zrcon,
                                     str_usuario = str_usuario
                                    )

    @app_commands.command(name="zunbanuser", description="Remove o banimento do usuario pelo nome.")
    @app_commands.rename(str_usuario="jogador")
    @app_commands.describe(str_usuario="Nome do jogador")
    @app_commands.autocomplete(str_usuario=_whbot_rcon_autocomplete.player_auto_complete)
    @app_commands.checks.has_permissions(administrator=True)
    async def unbanuser(
                        self,
                        itr         : discord.Interaction,
                        *,
                        str_usuario : str
                       ) -> None:
        """
        Remove o banimento do usuario pelo nome.
        Método administrativo. 
        """
        
        await self.moderador.unbanuser(
                                       payload = itr,
                                       zrcon = self.zrcon,
                                       str_usuario = str_usuario
                                      )

class whbot_rcon_slash_comandos_geral(commands.Cog):

    def __init__(self, 
                 bot                : commands.Bot, 
                 zrcon              : ZomboidRCON,
                 str_site_principal : str = None,
                 str_site_doacao    : str = None,
                 str_titulo         : str = None,
                 str_servidor       : str = None,
                 str_rodape         : str = None
                ):

        self.bot : commands.Bot = bot
        self.zrcon : ZomboidRCON = zrcon        
        self.geral  : _whbot_rcon_comandos_geral = _whbot_rcon_comandos_geral(SITE_PRINCIPAL=str_site_principal, 
                                                                              SITE_DOACAO=str_site_doacao, 
                                                                              TITULO=str_titulo, 
                                                                              SERVIDOR=str_servidor, 
                                                                              RODAPE=str_rodape
                                                                             )

    @app_commands.command(name="zadditem", description="Adiciona um item para o jogador.")
    @app_commands.rename(str_usuario="jogador", str_item="item")
    @app_commands.describe(str_usuario="Nome do jogador.", str_item="Item a ser adicionado.")
    @app_commands.autocomplete(str_usuario=_whbot_rcon_autocomplete.player_auto_complete)
    @app_commands.checks.has_permissions(administrator=True)
    async def additem(
                      self,
                      itr           : discord.Interaction, 
                      *,
                      str_usuario   : str,
                      str_item      : str
                     ) -> None:
        """
        Adiciona um item para o jogador.
        Método administrativo.
        Items can be found on the PZ wiki: https://pzwiki.net/wiki/Items
        """

        await self.geral.additem(
                                 payload = itr,
                                 zrcon = self.zrcon,
                                 str_user = str_usuario,
                                 str_item = str_item
                                )

    @app_commands.command(name="zaddvehicle", description="Materializa um veículo perto do usuário.")
    @app_commands.rename(str_usuario="jogador")
    @app_commands.describe(str_usuario="Nome do jogador.")
    @app_commands.autocomplete(str_usuario=_whbot_rcon_autocomplete.player_auto_complete)
    @app_commands.checks.has_permissions(administrator=True)
    async def addvehicle (
                          self,
                          itr           : discord.Interaction,
                          *, 
                          str_usuario   : str
                         ) -> None:
        """
        Materializa um veículo perto do usuário.
        Método Administrativo.
        """

        await self.geral.addvehicle(
                                    payload = itr,
                                    zrcon = self.zrcon,
                                    str_usuario = str_usuario
                                   )

    @app_commands.command(name="zaddxp", description="Dá experiência a um usuário.")
    @app_commands.rename(str_usuario="jogador", str_perk="perk", int_xp="experiencia")
    @app_commands.describe(str_usuario="Nome do jogador.", str_perk="Perk.", int_xp="Experiência.")
    @app_commands.autocomplete(str_perk=_whbot_rcon_autocomplete.perk_auto_complete)
    @app_commands.autocomplete(int_xp=_whbot_rcon_autocomplete.experience_auto_complete)
    @app_commands.autocomplete(str_usuario=_whbot_rcon_autocomplete.player_auto_complete)
    @app_commands.checks.has_permissions(administrator=True)
    async def addxp(
                    self,
                    itr         : discord.Interaction,
                    *,
                    str_usuario : str, 
                    str_perk    : str, 
                    int_xp      : int
                )-> None:
        """
        Dá experiência a um usuário.
        Método Administrativo.
        """
        
        await self.geral.addxp(
                               payload = itr,
                               zrcon = self.zrcon,
                               str_user = str_usuario,
                               str_perk = str_perk,
                               int_xp = int_xp
                              )

    @app_commands.command(name="zalarm", description="Soa um alarme no local onde o administrador está. Necessário estar dentro de uma sala.")
    @app_commands.checks.has_permissions(administrator=True)
    async def alarm(
                    self, 
                    itr : discord.Interaction
                   ) -> None:
        """
        Soa um alarme no local onde o administrador está. Necessário estar dentro de uma sala.
        Método administrativo. 
        """

        await self.geral.alarm(
                               payload = itr,
                               zrcon = self.zrcon
                              )

    @app_commands.command(name="zchopper", description="Coloca um helicóptero em um usuário aleatório.")
    @app_commands.checks.has_permissions(administrator=True)
    async def chopper(
                      self,
                      itr   : discord.Interaction
                     ) -> None:
        """
        Coloca um helicóptero em um usuário aleatório
        Método administrativo. 
        """

        await self.geral.chopper(
                                 payload = itr,
                                 zrcon = self.zrcon
                                )

    @app_commands.command(name="zcreatehorde", description="Cria uma horda próximo do jogador.")
    @app_commands.rename(int_hordas="hordas")
    @app_commands.describe(int_hordas="Quantidade de Hordas.")
    @app_commands.checks.has_permissions(administrator=True)
    async def createhorde(
                          self, 
                          ctx           : commands.Context,
                          *,
                          int_hordas    : str
                         )-> None:
        """
        Cria uma horda próximo do jogador.
        Método Administrativo.
        """

        await self.geral.createhorde(
                                     payload = ctx,
                                     zrcon = self.zrcon,
                                     int_hordas = int_hordas
                                    )

    @app_commands.command(name="zgodmode", description="Faz um jogador invencível.")
    @app_commands.rename(str_usuario="jogador")
    @app_commands.describe(str_usuario="Nome do jogador.")
    @app_commands.autocomplete(str_usuario=_whbot_rcon_autocomplete.player_auto_complete)
    @app_commands.checks.has_permissions(administrator=True)    
    async def godmode(
                      self,
                      itr           : discord.Interaction,
                      *,
                      str_usuario   : str
                     )-> None:
        """
        Faz um jogador invencível.
        Método Administrativo.
        """
        
        await self.geral.godmode(
                                 payload = itr,
                                 zrcon = self.zrcon,
                                 str_usuario = str_usuario
                                )

    @app_commands.command(name="zinvisible", description="Faz um jogador invencível.")
    @app_commands.rename(str_usuario="jogador")
    @app_commands.describe(str_usuario="Nome do jogador.")
    @app_commands.autocomplete(str_usuario=_whbot_rcon_autocomplete.player_auto_complete)
    @app_commands.checks.has_permissions(administrator=True)
    async def invisible(
                        self,
                        itr         : discord.Interaction,
                        *,
                        str_usuario : str
                       )-> None:
        """
        Faz um jogador invisível aos zumbis.
        Método Administrativo.
        """
        
        await self.geral.invisible(
                                   payload = itr,
                                   zrcon = self.zrcon,
                                   str_usuario = str_usuario
                                  )

    @app_commands.command(name="znoclip", description="Permite o usuário atravessar objetos sólidos.")
    @app_commands.rename(str_usuario="jogador")
    @app_commands.describe(str_usuario="Nome do jogador.")
    @app_commands.autocomplete(str_usuario=_whbot_rcon_autocomplete.player_auto_complete)
    @app_commands.checks.has_permissions(administrator=True)
    async def noclip(
                     self,
                     itr            : discord.Interaction,
                     *, 
                     str_usuario    : str
                    )-> None:
        """
        Permite o usuário atravessar objetos sólidos.
        Método Administrativo.
        """
        
        await self.geral.noclip(
                                payload = itr,
                                zrcon = self.zrcon,
                                str_usuario = str_usuario
                               )

    @app_commands.command(name="zreloadoptions", description="Recarrega opções do servidor.")
    @app_commands.checks.has_permissions(administrator=True)
    async def reloadoptions(
                            self,
                            itr     : discord.Interaction
                           )-> None:
        """
        Recarrega opções do servidor.
        Método Administrativo.
        """

        await self.geral.reloadoptions(
                                       payload = itr,
                                       zrcon = self.zrcon
                                      )

    @app_commands.command(name="zsave", description="Salva o mundo atual.")
    @app_commands.checks.has_permissions(administrator=True)
    async def save(
                   self,
                   itr      : discord.Interaction
                  )-> None:
        """
        Salva o mundo atual.
        Método administrativo. 
        """

        await self.geral.save(
                              payload = itr,
                              zrcon = self.zrcon
                             )

    @app_commands.command(name="zsendpulse", description="Alterna envio de performance do servidor para o cliente.")
    @app_commands.checks.has_permissions(administrator=True)
    async def sendpulse(
                        self,
                        ctx     : commands.Context
                       )-> None:

        """
        Alterna envio de performance do servidor para o cliente.
        Método administrativo. 
        """

        await self.geral.sendpulse(
                                   payload = ctx,
                                   zrcon = self.zrcon
                                  )

    @app_commands.command(name="zshowoptions", description="Mostra as opções configuradas no servidor.")
    @app_commands.checks.has_permissions(administrator=True)
    async def showoptions(
                          self,
                          itr   : discord.Interaction,
                         )-> None:
        """
        Mostra as opções configuradas no servidor.
        Método administrativo. 
        """
        
        await self.geral.showoptions(
                                     payload = itr,
                                     zrcon = self.zrcon
                                    )

    @app_commands.command(name="zstartrain", description="Inicia uma chuva no servidor.")
    @app_commands.checks.has_permissions(administrator=True)
    async def startrain(
                        self,
                        itr     : discord.Interaction
                       ) -> None:
        """
        Inicia uma chuva no servidor.
        Método administrativo. 
        """
        
        await self.geral.startrain(
                                   payload = itr,
                                   zrcon = self.zrcon
                                  )

    @app_commands.command(name="zstoprain", description="Para uma chuva no servidor.")
    @app_commands.checks.has_permissions(administrator=True)
    async def stoprain(
                       self,
                       itr      : discord.Interaction
                      )-> None:
        """
        Para uma chuva no servidor.
        Método administrativo. 
        """
        
        await self.geral.stoprain(
                                  payload = itr,
                                  zrcon = self.zrcon
                                 )

    @app_commands.command(name="zteleport", description="Telaporta o usuário para perto de outro usuário.")
    @app_commands.rename(str_usuario_d="jogadororigem", str_usuario_p="jogadordestino")
    @app_commands.describe(str_usuario_d="Nome do jogador.", str_usuario_p="Nome do Jogador.")
    @app_commands.autocomplete(str_usuario_d=_whbot_rcon_autocomplete.player_auto_complete)
    @app_commands.autocomplete(str_usuario_p=_whbot_rcon_autocomplete.player_auto_complete)
    @app_commands.checks.has_permissions(administrator=True)
    async def teleport(
                       self,
                       itr              : discord.Interaction,
                       *,
                       str_usuario_d    : str,
                       str_usuario_p    : str
                      )-> None:
        """
        Telaporta o usuário para perto de outro usuário.
        Método Administrativo.
        """
        
        await self.geral.teleport(
                                  payload = itr,
                                  zrcon = self.zrcon,
                                  str_usuario_d = str_usuario_d,
                                  str_usuario_p = str_usuario_p
                                 )

    @app_commands.command(name="zteleportto", description="Transporta o usuário para uma determinada coordenada.")
    @app_commands.rename(int_x="x", int_y="y", int_z="z")
    @app_commands.describe(int_x="Coordenada X.", int_y="Coordenada Y.", int_z ="Coordenada Z.")    
    @app_commands.checks.has_permissions(administrator=True)
    async def teleportto(
                         self,
                         itr        : discord.Interaction, 
                         int_x      : str, 
                         int_y      : str, 
                         int_z      : str
                        )-> None:
        """
        Transporta o usuário para uma determinada coordenada.
        Método Administrativo.
        """

        await self.geral.teleportto (
                                     payload = itr,
                                     zrcon = self.zrcon,
                                     int_x = int_x,
                                     int_y = int_y,
                                     int_z = int_z
                                    )

    @app_commands.command(name="zcheckupdate", description="Checa por mods updates e envia para o log.")
    @app_commands.checks.has_permissions(administrator=True)
    async def checkupdate (
                           self,
                           itr : discord.Interaction
                          )-> None:


        await self.geral.checkupdate(
                                     payload = itr,
                                     zrcon = self.zrcon
                                    )