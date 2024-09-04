from discord.ext import commands

class Ccheks():

    # Decorador customizado para ser utilizado no BOT.
    # Verifica se o comando está sendo executado em um canal expecífico.
    def e_canal_administrativo(str_canal : str):
        async def decorator (ctx : commands.Context):
            if ctx.channel.name == str_canal:
                return True
            else:
                return False
            decorator.__name__ = function.__name__
        return commands.check(decorator)    