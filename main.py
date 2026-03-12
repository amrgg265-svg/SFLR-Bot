import discord
from discord.ext import commands
import datetime

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'تم تشغيل السيستم بنجاح: {bot.user.name}')

# 1. أمر الترحيب التلقائي (حدث يرسل رسالة عند دخول عضو جديد)
@bot.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.text_channels, name="welcome") # ابحث عن قناة اسمها welcome
    if channel:
        embed = discord.Embed(title="عضو جديد!", description=f"أهلاً بك {member.mention} في سيرفرنا!", color=discord.Color.green())
        embed.set_thumbnail(url=member.avatar.url)
        await channel.send(embed=embed)

# 2. أمر إعطاء رتبة (Role) لشخص
@bot.command()
@commands.has_permissions(manage_roles=True)
async def addrole(ctx, member: discord.Member, role: discord.Role):
    await member.add_roles(role)
    await ctx.send(f"✅ تم إعطاء رتبة **{role.name}** للعضو **{member.display_name}**")

# 3. أمر سحب رتبة (Role) من شخص
@bot.command()
@commands.has_permissions(manage_roles=True)
async def removerole(ctx, member: discord.Member, role: discord.Role):
    await member.remove_roles(role)
    await ctx.send(f"❌ تم سحب رتبة **{role.name}** من العضو **{member.display_name}**")

# 4. أمر "إسكات" عضو (Mute) - يمنعه من الكتابة
@bot.command()
@commands.has_permissions(manage_messages=True)
async def mute(ctx, member: discord.Member):
    role = discord.utils.get(ctx.guild.roles, name="Muted")
    if not role:
        # إذا لم تكن الرتبة موجودة، يتم إنشاؤها تلقائياً ببرمجية بسيطة
        role = await ctx.guild.create_role(name="Muted")
        for channel in ctx.guild.channels:
            await channel.set_permissions(role, speak=False, send_messages=False)
    
    await member.add_roles(role)
    await ctx.send(f"🔇 تم إسكات {member.mention}.")

# 5. أمر معلومات المستخدم (User Info)
@bot.command()
async def userinfo(ctx, member: discord.Member = None):
    member = member or ctx.author
    embed = discord.Embed(title=f"معلومات {member.name}", color=member.color)
    embed.add_field(name="الاسم الكامل:", value=member.display_name)
    embed.add_field(name="تاريخ الانضمام للدسكورد:", value=member.created_at.strftime("%Y-%m-%d"))
    embed.set_thumbnail(url=member.avatar.url)
    await ctx.send(embed=embed)

# 6. أمر قفل الشات (Lock)
@bot.command()
@commands.has_permissions(manage_channels=True)
async def lock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
    await ctx.send("🔒 تم قفل القناة.")

# 7. أمر فتح الشات (Unlock)
@bot.command()
@commands.has_permissions(manage_channels=True)
async def unlock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
    await ctx.send("🔓 تم فتح القناة.")

bot.run('YOUR_TOKEN_HERE')
