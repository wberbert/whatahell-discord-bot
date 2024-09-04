import discord, re, os
from zomboid_rcon import ZomboidRCON
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

SITE = os.getenv("SITE")
EPIDEMIAZSERVIDOR = os.getenv("EPIDEMIAZSERVIDOR")
EPIDEMIAZNOME = os.getenv("EPIDEMIAZNOME")
EPIDEMIAZRODAPE = os.getenv("EPIDEMIAZRODAPE")
FUND = os.getenv("FUND")
class _whbot_geral_cards():

    @staticmethod
    def card_default(str_mensagem : str,
                     str_titulo : str,
                     str_site : str,
                     str_doe : str,
                     str_servidor : str,
                     str_rodape : str,
                     str_autor : str) -> discord.Embed:

        emsg = discord.Embed(colour=discord.Colour.blue(), 
                             description=str_mensagem,
                             title=str_titulo)
        
        emsg.add_field(name="Site", value=str_site, inline=True)
        emsg.add_field(name="Doações", value=str_doe, inline=True)
        emsg.add_field(name="Servidor", value=str_servidor, inline=False)
        emsg.set_author(name=str_autor)
        emsg.set_footer(text=str_rodape)

        return emsg
    
#Comandos publicos de uso geral
class whbot_geral_comandos (commands.Cog, name="Comandos do Usuário"):

    def __init__(self, bot : commands.Bot, zrcon : ZomboidRCON):

        self.bot : commands.Bot = bot
        self.zrcon : ZomboidRCON = zrcon

    @commands.command()
    async def ping (self, 
                    ctx : commands.Context):
        """
        Informa se o bot está ativo.

        Sintaxe:
            !ping
        """

        embed = _whbot_geral_cards.card_default(str_mensagem="PONG",
                                                str_titulo=EPIDEMIAZNOME,
                                                str_site=SITE,
                                                str_servidor=EPIDEMIAZSERVIDOR,
                                                str_doe=FUND,
                                                str_rodape=EPIDEMIAZRODAPE,
                                                str_autor="Comando Público")

        await ctx.send(embed=embed)

    @commands.command()
    async def jogadores(self, 
                        ctx : commands.Context) -> None:
        """
        Informa os jogadores online no momento.

        Sintaxe:
            !jogadores
        """

        str_resposta : str = self.zrcon.players().response
        str_regex : str = r"\d{1,2}\b"
        int_jogadores = re.search(str_regex, str_resposta).group()
        int_max_jogadores = 32
        str_jogadores = "\n".join(str_resposta.split("\n")[1:])

        embed = _whbot_geral_cards.card_default(str_mensagem=f"Jogadores Online : {int_jogadores}/{int_max_jogadores}\n {str_jogadores}",
                                                str_titulo=EPIDEMIAZNOME,
                                                str_site=SITE,
                                                str_servidor=EPIDEMIAZSERVIDOR,
                                                str_doe=FUND,
                                                str_rodape=EPIDEMIAZRODAPE,
                                                str_autor="Comando Público")
        await ctx.send(embed=embed)

        return    
