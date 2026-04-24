import discord
from discord.ext import commands
import os
from datetime import datetime
import asyncio
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Bot configuration
intents = discord.Intents.default()
intents.members = True  # Required for member join events
intents.message_content = True

bot = commands.Bot(command_prefix='w!', intents=intents)

# Welcome channel ID - Replace with your channel ID
WELCOME_CHANNEL_ID = 1431752582673727644  # CHANGE THIS

# Welcome message configuration
WELCOME_CONFIG = {
    "server_name": "WARRIOR TEAM OFFICIAL", # Server Name
    "footer_text": "Thanks For Joining Our Community!", # Embed Footer Text
    "thumbnail_url": "https://cdn.discordapp.com/avatars/{user_id}/{user_avatar}.png",  # Will be formatted
    "banner_color": 0xff0001,  # Hex Color
}

@bot.event
async def on_ready():
    print(f'✅ {bot.user} is now online!')
    print(f'📊 Connected to {len(bot.guilds)} servers')
    
    # Set bot status
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name=f"new members join | {len(bot.guilds)} servers"
        ),
        status=discord.Status.online
    )
    
    # Print startup banner
    print("""
    ╔══════════════════════════════════════╗
    ║     Welcome Bot is Ready!                   ║
    ║     Made By Subhan.                         ║
    ╚══════════════════════════════════════╝
    """)

@bot.event
async def on_member_join(member):
    """Handle new member join event with premium welcome message"""
    
    # Get welcome channel
    welcome_channel = member.guild.get_channel(WELCOME_CHANNEL_ID)
    
    if welcome_channel is None:
        print(f"⚠️ Welcome channel not found! Check channel ID: {WELCOME_CHANNEL_ID}")
        return
    
    # Create premium welcome embed
    embed = discord.Embed(
        title=f"Welcome to {member.guild.name}",
        description=f"""
        **{member.mention}** has joined the server!
        
        **> Member Count:** `{member.guild.member_count}`
        **> Account Created:** <t:{int(member.created_at.timestamp())}:R>
        
        **About Server:**
        • Server News: <#1431752582673727646>
        • Introduce Yourself in: <#1431752583147688081>
        • Grab Warrior Products: <#ROLES_CHANNEL_ID>
        
        *Enjoy Your Stay!*
        """,
        color=0xff0001  # Hex Red
    )
    
    # Set user avatar
    if member.avatar:
        avatar_url = member.avatar.url
        embed.set_thumbnail(url=avatar_url)
    
    # Set server icon
    if member.guild.icon:
        embed.set_image(url=member.guild.icon.url)
    
    # Footer with timestamp
    embed.set_footer(
        text=f"ID: {member.id} • {WELCOME_CONFIG['footer_text']}",
        icon_url=member.guild.icon.url if member.guild.icon else None
    )
    embed.timestamp = datetime.utcnow()
    
    # Add fields with premium design
    embed.add_field(
        name="**User Info**",
        value=f"**Username:** {member.name}\n**Discriminator:** #{member.discriminator}\n**Joined Discord:** <t:{int(member.created_at.timestamp())}:D>",
        inline=True
    )
    
    embed.add_field(
        name="**Server Status**",
        value=f"**Members:** {member.guild.member_count}\n**Roles:** {len(member.guild.roles)}\n**Channels:** {len(member.guild.channels)}",
        inline=True
    )
    
    # Bot role or specific role mention (optional)
    # admin_role = member.guild.get_role(ADMIN_ROLE_ID)
    # role_mention = admin_role.mention if admin_role else ""
    
    try:
        # Send welcome message with member mention
        await welcome_channel.send(
            content=f"{member.mention} New Member Joined! | Everyone welcome them!",
            embed=embed
        )
        
        # Optional: Send a DM to the new member
        try:
            dm_embed = discord.Embed(
                title=f"Welcome to {member.guild.name}!",
                description=f"""
                Thanks for joining **{member.guild.name}**!
                
                We're excited to have you here! Make sure to:
                • Read the rules
                • Introduce yourself
                • Check out our channels
                
                Enjoy your stay!
                """,
                color=0x00FF00
            )
            dm_embed.set_thumbnail(url=member.guild.icon.url if member.guild.icon else None)
            await member.send(embed=dm_embed)
        except discord.Forbidden:
            print(f"❌ Cannot send DM to {member.name} (DMs closed)")
        except Exception as e:
            print(f"❌ Error sending DM: {e}")
            
    except discord.Forbidden:
        print(f"❌ Missing permissions to send message in welcome channel!")
    except Exception as e:
        print(f"❌ Error sending welcome message: {e}")

@bot.event
async def on_member_remove(member):
    """Handle member leave event"""
    welcome_channel = member.guild.get_channel(WELCOME_CHANNEL_ID)
    
    if welcome_channel:
        leave_embed = discord.Embed(
            title="Member Left",
            description=f"**{member.name}** has left the server.",
            color=0xFF0000
        )
        leave_embed.add_field(
            name="Updated Member Count",
            value=f"`{member.guild.member_count}` members remaining",
            inline=False
        )
        leave_embed.timestamp = datetime.utcnow()
        
        if member.avatar:
            leave_embed.set_thumbnail(url=member.avatar.url)
            
        try:
            await welcome_channel.send(embed=leave_embed)
        except discord.Forbidden:
            print(f"❌ Missing permissions to send message!")

@bot.command(name="welcome_test")
@commands.has_permissions(administrator=True)
async def welcome_test(ctx):
    """Test the welcome message (Admin only)"""
    welcome_channel = ctx.guild.get_channel(WELCOME_CHANNEL_ID)
    
    if welcome_channel is None:
        await ctx.send("❌ Welcome channel not found! Check the channel ID.")
        return
    
    # Create test embed
    embed = discord.Embed(
        title=f"🧪 Welcome Test",
        description=f"""
        **{ctx.author.mention}** This is a test welcome message!
        
        **📊 Member Count:** `{ctx.guild.member_count}`
        **📅 Account Created:** <t:{int(ctx.author.created_at.timestamp())}:R>
        """,
        color=0x9B59B6
    )
    
    if ctx.author.avatar:
        embed.set_thumbnail(url=ctx.author.avatar.url)
    
    if ctx.guild.icon:
        embed.set_image(url=ctx.guild.icon.url)
    
    embed.set_footer(text="Test Message • Bot Working! ✅")
    embed.timestamp = datetime.utcnow()
    
    embed.add_field(name="✅ Status", value="Welcome system is working!", inline=False)
    
    await ctx.send(embed=embed)
    await ctx.send("✅ Welcome test completed!")

@bot.command(name="set_welcome_channel")
@commands.has_permissions(administrator=True)
async def set_welcome_channel(ctx, channel: discord.TextChannel = None):
    """Set the welcome channel"""
    if channel is None:
        await ctx.send("❌ Please mention a channel! Usage: `!set_welcome_channel #channel`")
        return
    
    global WELCOME_CHANNEL_ID
    WELCOME_CHANNEL_ID = channel.id
    
    await ctx.send(f"✅ Welcome channel set to {channel.mention}!")
    
    # Optional: Save to a file or database for persistence
    # You can implement file saving here

@bot.command(name="info")
async def info(ctx):
    """Display bot information"""
    embed = discord.Embed(
        title="Welcome Bot Info",
        description="Made By Subhan",
        color=0x9B59B6,
        timestamp=datetime.utcnow()
    )
    
    embed.add_field(name="📊 Servers", value=f"`{len(bot.guilds)}`", inline=True)
    embed.add_field(name="👥 Total Users", value=f"`{sum(g.member_count for g in bot.guilds)}`", inline=True)
    embed.add_field(name="🏓 Latency", value=f"`{round(bot.latency * 1000)}ms`", inline=True)
    
    embed.add_field(
        name="🔧 Commands",
        value="`!welcome_test` - Test welcome message\n`!set_welcome_channel #channel` - Set channel\n`!bot_info` - Show this info",
        inline=False
    )
    
    embed.set_footer(text="Made with ❤️ | Hosted on Railway")
    
    await ctx.send(embed=embed)

# Error Handling
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ You don't have permission to use this command!")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("❌ Missing required arguments!")
    else:
        print(f"Error: {error}")

# Run the bot
if __name__ == "__main__":
    token = os.getenv('DISCORD_BOT_TOKEN')
    if not token:
        print("❌ No token found! Please set DISCORD_BOT_TOKEN in .env file")
        exit(1)
    
    bot.run(token)
