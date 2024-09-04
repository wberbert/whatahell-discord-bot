import discord
import os
import discord.ext.commands
from zomboid_rcon import ZomboidRCON
from discord.ext import commands,tasks
from discord.ext.commands import has_permissions
from dotenv import load_dotenv
import discord.ext
from modules.whbot_custom_checks import Ccheks
from discord import app_commands


load_dotenv()

CANAL_ADMINISTRADOR = os.getenv("CANAL_ADMINISTRADOR")

SITE = os.getenv("SITE")
EPIDEMIAZSERVIDOR = os.getenv("EPIDEMIAZSERVIDOR")
EPIDEMIAZNOME = os.getenv("EPIDEMIAZNOME")
EPIDEMIAZRODAPE = os.getenv("EPIDEMIAZRODAPE")

class _whbot_bot_comandos():

    async def versao (self,
                      payload : commands.Context | discord.Interaction
                      ) -> None:
        str_notas_versao = ("# wh_pz_bot\n"
                           "### Bot zomboid para administração de servidor e automação!\n"
                           "## Atualizações de Versão\n"
                           "### [v1.1.2] - 20/06/2024\n"
                           "- Correção de bugs.\n"                           
                           "### [v1.1.2] - 19/06/2024\n"
                           "- Melhorias na manutebilidade do código.\n"
                           "- Correção de bugs.\n"
                           "### [v1.1.1] - 18/06/2024\n"
                           "- Melhoria na rotina de autalização de MODS.\n"
                           "- Comandos para controle do serviço zomboid.\n"
                           "### [v1.1.0] - 17/06/2024\n"
                           "- Primeira versão completa do BOT.\n"
                           "- Adicionado funcionalidade para atualização automática de mods.\n"
                           "- Novos comandos disponíveis para o administrador\n")

        embed = discord.Embed(colour=discord.Colour.green(), 
                              description=str_notas_versao,
                              title=EPIDEMIAZNOME)

        embed.add_field(name="Site", value=SITE, inline=True)
        embed.add_field(name="Servidor", value=EPIDEMIAZSERVIDOR, inline=True)
        embed.add_field(name="Autor", value="B3rb3rT", inline=False)
        embed.set_footer(text=EPIDEMIAZRODAPE)
        embed.set_author(name="B3rb3rT")        

        if isinstance(payload, commands.Context):
            ctx : commands.Context = payload
            await ctx.send (embed=embed)
        
        if isinstance(payload, discord.Interaction):
            itr : discord.Interaction = payload
            await itr.response.send_message(embed=embed)

class whbot_bot_comandos(commands.Cog, name="Comandos de BOT"):
    
    _canal : str

    def __init__(self, bot : commands.Bot, zrcon : ZomboidRCON, botnome : str):

        self.bot : commands.Bot = bot
        self.zrcon : ZomboidRCON = zrcon
        self.botnome : str = botnome

        self.atualizar_nome_canal.start()

    @tasks.loop(minutes=30)
    async def atualizar_nome_canal (self) -> None:
        
        await self.bot.user.edit(username=self.botnome)

    
#    @commands.command()
#    @has_permissions(administrator=True)
#    @Ccheks.e_canal_administrativo(CANAL_ADMINISTRADOR)
#    async def nome_do_canal(self,
#                            ctx : commands.Context,
#                            *,
#                            str_nome = commands.parameter(default=None, displayed_default=None, displayed_name="Nome", description="Nome do bot no canal")
#                           ) -> None:
#        """
#            Altera o nome do BOT.
#
#            Sintaxe:
#                !nome_do_canal novonome
#        """
#
#        await ctx.send(f"Oi, {ctx.author.mention}, \n O canal {self.bot.user.name} foi alterado para")
#        await self.bot.user.edit (username=str_nome)
#        await ctx.send(f"{self.bot.user.name}")
#    
#    
    @commands.command()
    async def versao(self,
                     ctx : commands.Context 
                     ) -> None:
        """
            Informa a versão do BOT.
        """

        await _whbot_bot_comandos.versao (self,
                                          ctx)
        

class whbot_bot_slash_comandos(commands.Cog, name="Comandos Slash de BOT"):

    def __init__(self, bot : commands.Bot, zrcon : ZomboidRCON):

        self.bot : commands.Bot = bot
        self.zrcon : ZomboidRCON = zrcon

    @app_commands.command(name="zversao", description="Versão fo BOT")
    async def versao(self,
                     itr : discord.Interaction
                     ) -> None:
        """
            Informa a versão do BOT.
        """

        await _whbot_bot_comandos.versao (self,
                                          itr)
        