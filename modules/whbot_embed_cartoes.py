import discord, typing

class whbot_embed_cartoes():

    @staticmethod
    def whbot_membro_entrou(
                            clr_cor         : discord.Colour,
                            str_descricao   : str,
                            str_titulo      : str
                            ) -> discord.Embed:

        ecartao = discord.Embed(colour=clr_cor, 
                                description=str_descricao,
                                title=str_titulo)
        
        #emsg.add_field(name="Site", value=str_site, inline=True)
        #emsg.add_field(name="Doações", value=str_doe, inline=True)
        #emsg.add_field(name="Servidor", value=str_servidor, inline=False)
        #emsg.set_author(name=str_autor)
        #emsg.set_footer(text=str_rodape)        
        return ecartao

