import discord
import os, datetime
from discord.ext import commands
from discord.ext.commands import has_permissions
from zomboid_rcon import ZomboidRCON
from dotenv import load_dotenv

load_dotenv()

CANAL_ANUNCIOS = os.getenv("CANAL_ANUNCIOS", "anuncios")

SITE = os.getenv("SITE")
EPIDEMIAZSERVIDOR = os.getenv("EPIDEMIAZSERVIDOR")
EPIDEMIAZNOME = os.getenv("EPIDEMIAZNOME")
EPIDEMIAZRODAPE = os.getenv("EPIDEMIAZRODAPE")

class whbot_avisos_comandos (commands.Cog, name="Avisos"):

    def __init__(self, bot : commands.Bot, zrcon : ZomboidRCON):

        self.bot : commands.Bot = bot
        self.zrcon : ZomboidRCON = zrcon

    @commands.command() 
    @has_permissions(administrator=True)
    async def manutencao (self, 
                          ctx : commands.Context, 
                          str_canal : str = commands.parameter(default=CANAL_ANUNCIOS, displayed_name="canal", description="Canal onde a mensagem sera enviada.")
                         ) -> None:
        
        channel = discord.utils.get(self.bot.get_all_channels(), name=str_canal)

        str_menssagem = ("Anúncio de Manutenção do Servidor \n\n"
                        "Prezados jogadores, \n\n"
                        "Informamos que o servidor do Project Zomboid passará por uma manutenção programada para melhorar a estabilidade e desempenho do sistema. \n A manutenção ocorrerá na próxima [data], a partir das [hora] e deverá durar aproximadamente [duração estimada].\n\n" 
                        "Durante este período, o servidor estará temporariamente offline. Pedimos desculpas por qualquer inconveniente que isso possa causar e agradecemos pela sua compreensão e paciência.\n\n" 
                        "Estamos trabalhando arduamente para garantir uma experiência de jogo ainda melhor para todos. Qualquer atualização sobre o progresso da manutenção será comunicada em nossos canais oficiais.\n\n"
                        "Agradecemos pelo seu apoio contínuo!\n" 
                        "Atenciosamente,\n"
                        "[Nome da Equipe/Administração do Servidor]\n"
                        )
        
        embed = discord.Embed(colour=discord.Colour.blue(), 
                              description=str_menssagem,
                              title=EPIDEMIAZNOME)
        
        embed.add_field(name="Site", value=SITE, inline=True)
        embed.add_field(name="Servidor", value=EPIDEMIAZSERVIDOR, inline=True)
        embed.set_author(name="Comando administrativo")
        embed.set_footer(text=EPIDEMIAZRODAPE)
        
        await channel.send (embed=embed)

        return