import discord
from discord.commands.core import slash_command
from discord.ext import commands
from verify import DebugServer, BOT_NAME_TAG_VER

class RoleButton(discord.ui.Button):
    def __init__(self, role: discord.Role):
        super().__init__(
            label=role.name,
            style=discord.enums.ButtonStyle.primary,
            custom_id=str(role.id),
        )

    async def callback(self, interaction: discord.Interaction):
        user = interaction.user
        role = interaction.guild.get_role(int(self.custom_id))

        if role is None:
            return

        if role not in user.roles:
            await user.add_roles(role)
            await interaction.response.send_message(f"π {role.mention} μ­ν μ μ§κΈ λ°μΌμ¨μ΄μ!", ephemeral=True)
        else:
            await user.remove_roles(role)
            await interaction.response.send_message(
                f"β {role.mention} μ­ν μ΄ μ κ±° λμμ΄μ!", ephemeral=True
            )


class ButtonRoleCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @slash_command(guild_ids=DebugServer, description="μ­ν  μ§κΈ μ€μ ")
    async def post(self, ctx: commands.Context,roleid,message):

        view = discord.ui.View(timeout=None)
        role_ids = [int(roleid)]
        for role_id in role_ids:
            role = ctx.guild.get_role(role_id)
            view.add_item(RoleButton(role))

        await ctx.respond(message, view=view)

def setup(bot):
    bot.add_cog(ButtonRoleCog(bot))
