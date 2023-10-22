TOKEN = "MTE1OTUwODAyODE2NTQ3NjQ1Mw.GD1qcu.rMd7XoWhoiIleteUETXAmWi6jLQ7i-XrbWtU_Q"
from typing import Optional
import discord
from discord.ext import commands
import asyncio 
from typing import Literal, Optional
from discord.ext import commands
import discord
from time import sleep
import asyncio
import asqlite
import random
from rich.console import Console

cmd = Console()

intents = discord.Intents.all()

#--------------------------------------------------------------On_Ready----------------------------------------------------------------------------------------------

class PersistentViewBot(commands.Bot):
    def __init__(self):

        super().__init__(command_prefix="!", intents=intents)
  
  
    async def on_ready(self):
        cmd.print(f"Success: Logged in as:\n-----------------\n {bot.user}\n-----------------", style="bold blue")

    async def setup_hook(self):
      bot.add_view(Verification())
      async with asqlite.connect('channels.db') as conn:
        await conn.execute('CREATE TABLE IF NOT EXISTS channels (GuildID int PRIMARY KEY, ChannelID int, Test int)')
      async with asqlite.connect('announce.db') as conn1:
        await conn1.execute('CREATE TABLE IF NOT EXISTS announce (GuildID int PRIMARY KEY, ChannelID int)')

bot = PersistentViewBot()
tree = bot.tree
bot.remove_command("help")
      
#-------------------------------------------------------------Membercount----------------------------------------------------------------------------------------------- 

@bot.command(aliases=["membercount"])
async def members(ctx):
    await ctx.send(f"This Server Has {ctx.guild.member_count} Members")
             
#------------------------------------------------------------Ban_Command------------------------------------------------------------------------------------------------
                  
@tree.command(description="bans the specified user from the server")
async def ban(interaction: discord.Interaction, user: discord.Member, reason:str="No reason provided"):
    if user == interaction.user:
        embed=discord.Embed(color=0x007bff, title="You cannot Kick youself", description="Sadly you cannot Kick youself")
    elif user.guild_permissions.administrator:
        embed=discord.Embed(color=0x007bff, title="You cannot Kick an admin", description="This user is an admin you cannot Kick them")
    else:
        embed=discord.Embed(color=0xff0000, title=f"Banned {user}\n\n", description=f"{user.mention} has been Banned")
        embed.add_field(name="--------------------", value="", inline=False)
        embed.add_field(name="Banned By", value=f"{interaction.user.mention}", inline=True)
        embed.add_field(name="Reason", value=f"{reason}", inline=True)
        await bot.get_channel(1154180778427682818).send(embed=embed)
        await user.ban(reason=reason)
        await interaction.response.send_message(embed=embed, ephemeral=True)
          
#---------------------------------------------------------------Unban_Command---------------------------------------------------------------------------------------------
   

@tree.command(description="Unbans the specified user, via UserId, from the server")
async def unban(inter: discord.Interaction, id: int = None):
     if id is None:
        embed=discord.Embed(color=0x00ff40, title="No Member Specified", description="Please Specify an ID To Unban")
        await inter.response.send_message(embed=embed)
     else:
        user = await bot.fetch_user(id)
        await inter.guild.unban(user)
        embed=discord.Embed(color=0x00ff40, title=f"Unbanned {user}", description=f"{user.mention} has been Unbanned")
        embed.add_field(name="--------------------", value="", inline=False)
        embed.add_field(name="Unbanned By", value=f"{inter.user.mention}")
        await bot.get_channel(1154180778427682818).send(embed=embed)
        
#----------------------------------------------------------------Kick_Command--------------------------------------------------------------------------------------------

@tree.command(description="Kicks the specified user from the server")
async def kick(interaction: discord.Interaction, user: discord.Member, reason:str="No reason provided"):
    if user == interaction.user:
        embed=discord.Embed(color=0x007bff, title="You cannot Kick youself", description="Sadly you cannot Kick youself")
    elif user.guild_permissions.administrator:
        embed=discord.Embed(color=0x007bff, title="You cannot Kick an admin", description="This user is an admin you cannot Kick them")
    else:
        await user.kick(reason=reason)
        embed=discord.Embed(color=0x007bff, title=f"Kicked {user}", description=f"{user.mention} has been Kicked")
        embed.add_field(name="--------------------", value="", inline=False)
        embed.add_field(name="Kicked By", value=f"{interaction.user.mention}", inline=True)
        embed.add_field(name="Reason", value=f"{reason}", inline=True)
        await bot.get_channel(1154180778427682818).send(embed=embed)
    await interaction.response.send_message(embed=embed, ephemeral=True)
        
#-------------------------------------------------------------------Verification_System-----------------------------------------------------------------------------------------

class Verification(discord.ui.View):
  def __init__(self):
    super().__init__(timeout = None)
  @discord.ui.button(label="Verify",custom_id = "Verify",style = discord.ButtonStyle.success)
  async def verify(self, interaction, button):
    role = 1145745362116677786
    user = interaction.user
    if role not in [y.id for y in user.roles]:
      await user.add_roles(user.guild.get_role(role))
      
#-------------------------------------------------------------------Verify_Command-----------------------------------------------------------------------------------------

@tree.command(description="sends the verify embed into the verification channel")
async def verify(interaction: discord.Interaction):
  if interaction.user.id == 1154086980959875213:
      embed = discord.Embed(color=0x8c00ff, title = "Verification", description = "Do You Not Have Permission To View Any Channels?.")
      embed.add_field(name="Verify", value="Click The Verify Button To Gain Access To The Server")
      await bot.get_channel(1145745679038287893).send(embed = embed, view = Verification())
      await interaction.response.send_message("Sent the verification message", ephemeral=True)

  
#-------------------------------------------------------------------Purge_Command-------------------------------------------------------------------------------------------
  

@tree.command(description="Purges/Deletes the specified amount of messages from a channel")
async def purge(inter: discord.Interaction, amt:str):
  await inter.response.defer(ephemeral=True)
  await inter.channel.purge(limit = int(amt) + 1)
  embed = discord.Embed(color=0x8c00ff, title = "Purged", description = "Messages Have Been Purged")
  embed.add_field(name="Amount", value=f"{amt}")
  await inter.followup.send(embed=embed, ephemeral=True)
  
#-------------------------------------------------------------------Avatar_Command-----------------------------------------------------------------------------------------

@tree.command(description="Shows the specified users profile picture/avatar")
async def avatar(inter: discord.Interaction , member: discord.Member = None):
  if member == None:
    member = inter.user
  embed = discord.Embed(title = member).set_image(url = member.avatar.url)
  await inter.response.send_message(embed = embed, ephemeral=True)
  
#-----------------------------------------------------------------SkyCrypt_Command-------------------------------------------------------------------------------------------
  
@tree.command(description="Shows the hypixel skyblock stats of the specified player")
async def skycrypt(inter: discord.Interaction, player:str=None):
  if player is None:
    embed = discord.Embed(color=0xffea00, title=f"No Player Provided", description=f"{inter.user.mention} You Did Not Provide A Username To Search For")
    embed.add_field(name="----------------------------------------------------------", value="Please Enter A Username To LookUp On SkyCrypt")
    await inter.response.send_message(embed=embed, ephemeral=True)
  else:
    embed = discord.Embed(color=0xffea00, title=f"SkyCrypt of {player}", description=f"{inter.user.mention} Click On The Link Below To Check Out {player}'s Stats on Hypixel Skyblock")
    embed.add_field(name="Player", value=f"{player}")
    await inter.response.send_message(embed=embed, ephemeral=True)
    await inter.followup.send(f"https://sky.shiiyu.moe/{player}", ephemeral=True)
    
#-------------------------------------------------------------------UserInfo_Command-----------------------------------------------------------------------------------------

@tree.command(description="Gets info about the user")
async def userinfo(inter: discord.Interaction):
    embed=discord.Embed(color=0xfb00ff, title="USER INFO", description=f"Here is the info we retrieved about {int}", colour=inter.user.colour)
    embed.set_image(url=inter.user.avatar.url)
    embed.add_field(name="NAME", value=inter.user.name, inline=True)
    embed.add_field(name="NICKNAME", value=inter.user.nick, inline=True)
    embed.add_field(name="ID", value=inter.user.id, inline=False)
    embed.add_field(name="STATUS", value=inter.user.status, inline=True)
    embed.add_field(name="TOP ROLE", value=inter.user.top_role.name, inline=True)
    await inter.response.send_message(embed=embed, ephemeral=True)
    
#-------------------------------------------------------------------Mute_Command----------------------------------------------------------------------------------------- 

@tree.command(description="Mutes the specified user.")
async def mute(inter: discord.Interaction, user: discord.Member, *, reason:str=None):
  guild = inter.guild
  mutedRole = discord.utils.get(guild.roles, name="Muted")

  if not mutedRole:
        mutedRole = await guild.create_role(name="Muted")

        for channel in guild.channels:
          await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=True)
          embed=discord.Embed(color=0xff007b, title=f"Muted {user.mention}", description=f"{user.name} Has Been Muted")
  embed.add_field(name="Reason",value=f"{reason}", inline=False)  
  embed.add_field(name="Muted By",value=f"{inter.user.mention}")    
  await user.add_roles(mutedRole, reason=reason)
  await bot.get_channel(1154180778427682818).send(embed=embed)
  await inter.response.send_message(embed=embed, ephemeral=True)
    
#-------------------------------------------------------------------Unmute_Command----------------------------------------------------------------------------------------- 

@tree.command(description="Unmutes the specified user.")
async def unmute(inter: discord.Interaction, user: discord.Member):
    mutedRole = discord.utils.get(inter.guild.roles, name="Muted")
    await user.remove_roles(mutedRole)
    embed=discord.Embed(color=0xff007b, title=f"Unmuted {user.mention}", description=f"{user.name} Has Been Unmuted By")
    embed.add_field(name="Unmuted By",value=f"{inter.user.mention}") 
    await bot.get_channel(1154180778427682818).send(embed=embed)
    await inter.response.send_message(embed=embed, ephemeral=True)
    
#-------------------------------------------------------------------Help_Command-----------------------------------------------------------------------------------------

@bot.command()
async def help(ctx):
   
        embed=discord.Embed(title="HELP")
        embed.add_field(name="[Utilitiy]", value="", inline=False)
        embed.add_field(name="", value="**Skycrypt**: Shows a users minecraft hypixel skyblock stats on Skycrypt", inline=False)
        embed.add_field(name="", value="**Avatar**: Displays a users Avatar/Profile Picture", inline=False)
        embed.add_field(name="", value="**userinfo**: Retreives info about the given user", inline=False)
        embed.add_field(name="", value="**membercount**: Shows how many members the server currently has", inline=False)
        embed.add_field(name="", value="**report**: Lets You Report A Player Due To Bad Behaviour", inline=False)
        embed.add_field(name="---------------------------------------------------------------------", value="", inline=False)
        embed.add_field(name="[Moderation]", value="", inline=False)
        embed.add_field(name="", value="**Ban/Unban**: Bans/Unbans the specified user from the server", inline=False)
        embed.add_field(name="", value="**Kick**: Kicks the specified user from the server", inline=False)
        embed.add_field(name="", value="**Mute/Unmute**: Mutes/Unmutes the specified user in the server", inline=False)
        embed.add_field(name="", value="**Addrole/RemoveRole**: Adds/Removes A Role From A Specified User", inline=False)
        embed.add_field(name="", value="**announnce**: Lets You Send An Announncement into the Announncements Channel", inline=False)
        embed.add_field(name="---------------------------------------------------------------------", value="", inline=False)

        await ctx.message.delete()
        await ctx.send(embed=embed, ephemeral=True)
        
#-------------------------------------------------------------------addrole_command-----------------------------------------------------------------------------------------

@tree.command(description="Gives the specified user the specified rank")
async def addrole(inter: discord.Interaction, user: discord.Member, role:discord.Role):
  embed=discord.Embed(color=0x00ffc4 ,title="Role Added", description=f"{user} Has Been Given The {role} Role")
  embed.add_field(name="Given Role", value=f"{role}", inline=True)
  embed.add_field(name="Recieved Role From", value=f"{inter.user}", inline=True)
  await user.add_roles(role)
  await bot.get_channel(1154180778427682818).send(embed=embed)
  await inter.response.send_message(embed=embed, ephemeral=True)

#-------------------------------------------------------------------removerole_command-----------------------------------------------------------------------------------------

@tree.command(description="Removes the specified rank from the specified user")
async def removerole(inter: discord.Interaction, user: discord.Member, role:discord.Role):
  embed=discord.Embed(color=0x00ffc4 ,title="Role Removed", description=f"{role} Has Been Removed From {user}")
  embed.add_field(name="Removed Role", value=f"{role}", inline=True)
  embed.add_field(name="Role Removed By", value=f"{inter.user}", inline=True)
  await user.remove_roles(role)
  await bot.get_channel(1154180778427682818).send(embed=embed)
  await inter.response.send_message(embed=embed, ephemeral=True)
  
 #-------------------------------------------------------------------announcne_command-----------------------------------------------------------------------------------------
  
@tree.command(description="announces a message to your set announcements channel")
async def announce(inter: discord.Interaction, announncement: str):
      embed=discord.Embed(color=0xaca6e3, title="announncement")
      embed.add_field(name=" ",value=f"{announncement}")

      async with asqlite.connect('announce.db') as f:
       channelf = await f.fetchone("SELECT * FROM announce WHERE GuildID = ?", (inter.guild.id))

      if channelf is not None:
        channel = bot.get_channel(channelf[1])
        await channel.send(embed=embed)
        await inter.response.send_message(embed=embed, ephemeral=True)

 #-------------------------------------------------------------------set_announce_channel_command-----------------------------------------------------------------------------------------
 
@tree.command(description="Creates the announcements channel")
async def set_announce_channel(inter: discord.Interaction, channel: discord.TextChannel):
  if inter.user.id == 1154086980959875213:
    guild = inter.guild
    async with asqlite.connect('announce.db') as f:
     await f.execute("INSERT OR REPLACE INTO announce VALUES (?, ?)", guild.id, channel.id)
     await f.commit()
     await inter.response.send_message(f"{channel} has been set to your announcements channel", ephemeral=True)
 
#-------------------------------------------------------------------set_report_channel_command-----------------------------------------------------------------------------------------
 
@tree.command(description="Creates the reports channel")
async def set_report_channel(inter: discord.Interaction, channel: discord.TextChannel):
  if inter.user.id == 1154086980959875213:
    guild = inter.guild
    async with asqlite.connect('channels.db') as f:
     await f.execute("INSERT OR REPLACE INTO channels VALUES (?, ?)", guild.id, channel.id)
     await f.commit()
     await inter.response.send_message(f"{channel} has been set to your reports channel", ephemeral=True)

 #-------------------------------------------------------------------report_command-----------------------------------------------------------------------------------------

@tree.command(description="Reports the specified user for the entered reason")
async def report(inter: discord.Interaction, user: discord.Member, reason:str=None):
      embed=discord.Embed(color=0x007bff, title="Report", description="")
      embed.add_field(name="Reported By", value=f"{inter.user.mention}", inline=True)
      embed.add_field(name="Reportee", value=f"{user.mention}", inline=True)
      embed.add_field(name="Reason", value=f"{reason}", inline=False)

      async with asqlite.connect('channels.db') as f:
       channelf = await f.fetchone("SELECT * FROM channels WHERE GuildID = ?", (inter.guild.id))

      if channelf is not None:
        channel = bot.get_channel(channelf[1])
        await channel.send(embed=embed)
        await inter.response.send_message(f"{user} has been successfully reported for {reason}", ephemeral=True)

#-------------------------------------------------------------------sync_command-----------------------------------------------------------------------------------------

@bot.command()
@commands.guild_only()
@commands.is_owner()
async def sync(ctx: commands.Context, guilds: commands.Greedy[discord.Object], spec: Optional[Literal["~", "*", "^"]] = None) -> None:
    if not guilds:
        if spec == "~":
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
        elif spec == "*":
            ctx.bot.tree.copy_global_to(guild=ctx.guild)
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
        elif spec == "^":
            ctx.bot.tree.clear_commands(guild=ctx.guild)
            await ctx.bot.tree.sync(guild=ctx.guild)
            synced = []
        else:
            synced = await ctx.bot.tree.sync()

        await ctx.send(
            f"Synced {len(synced)} commands {'globally' if spec is None else 'to the current guild.'}"
        )
        return

    ret = 0
    for guild in guilds:
        try:
            await ctx.bot.tree.sync(guild=guild)
        except discord.HTTPException:
            pass
        else:
            ret += 1

    await ctx.send(f"Synced the tree to {ret}/{len(guilds)}.")


bot.run(TOKEN)

