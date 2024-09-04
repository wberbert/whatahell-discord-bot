import discord
from discord.ext import commands

from modules.whbot_embed_cartoes import whbot_embed_cartoes

class whbot_eventos_jogador (commands.Cog):

    def __init__(self, bot : commands.Bot, str_id_role : str, str_canal : str):

        self.bot : commands.Bot = bot
        self.str_id_role : str = str_id_role
        self.str_canal = str_canal
        
    #@commands.Cog.listener()
    async def on_message(self,
                         message : discord.Message):

        if message.author == self.bot.user:
            return
        
        #w = discord.WidgetMember ()
        #w.name =  "teste"

        channel = discord.utils.get(self.bot.get_all_channels(), name="anuncios")
        #await channel.send(embed=w)
        await channel.send ("Enviaram uma mesangem")
        pass
    
    @commands.Cog.listener()
    async def on_member_join(self,
                             member : discord.Member
                            ) -> None:
    
        embed : discord.Embed = whbot_embed_cartoes.whbot_membro_entrou(clr_cor=discord.Colour.gold(),
                                                                        str_titulo="Novo membro no canal",
                                                                        str_descricao=f"***Deêm as boas vindas ao novo membro do canal {member.name}.***")
        try:
            member.send (f"Meus parabens, você agora faz parte do grupo.")
        except:
            pass
        
        if member.guild.get_role(self.str_id_role):
            await member.add_roles(member.guild.get_role(self.str_id_role))
            
            channel = discord.utils.get(member.guild.channels, name=self.str_canal)
            channel.send(embed=embed)
