import discord, os, requests
from discord.ext import commands
from discord.ext import *
import time
from datetime import datetime
from time import strftime
from time import gmtime
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", description="TEST",intents=intents)
@bot.event
async def on_ready():
    print("Bot active")
@bot.command(pass_context=True)
async def huongdan(ctx):
    await ctx.send(f"**- Hướng dẫn sử dụng BOT. [!]\n\n- !on **   *Onduty trước khi làm việc.*\n\n**- !off **   *Offduty sau khi làm việc xong.*\n\n**- !me **   *Kiểm tra trong tháng này bản thân đã onduty được bao lâu.*\n\n**- !check_time #   ** *Kiểm tra người khác xem tháng này đã onduty được bao lâu.*\n*- Ví dụ: !check_time #LSPD | 01 | Khun Pham*\n\n\n*- Lưu ý lệnh !check chỉ cấp quản lý mới được sử dụng !!!*")
@bot.command(pass_context=True)
async def on(ctx):
    names = f"{ctx.message.author.display_name}"
    resp = requests.get("https://anhduy.dev/LSPD/checksiquan.php?name="+str(names)).text
    if resp == '0':
        await ctx.send(f"**{names}" + " chưa có tên trong danh sách đồn, liên hệ Quản Lý Ban Ngành để thêm vào !!!**")
    else:
        check_duty = requests.get("https://anhduy.dev/LSPD/check_duty.php?name="+str(names)).text
        if check_duty == "on":
            await ctx.send(f"**{names}" + " bạn đã onduty rồi !!!**")
        else:
            ts = time.time()
            ts = str(ts).split(".")[0]
            now = datetime.now()
            giohientai = now.strftime("%H:%M")
            requests.get(f"https://anhduy.dev/LSPD/index.php?com=on&name="+str(names)+"&ts="+str(ts)).text
            await ctx.send(f"**{names}**" + " đã làm việc vào " + str(giohientai))
@bot.command(pass_context=True)
async def off(ctx):
    names = f"{ctx.message.author.display_name}"
    resp = requests.get("https://anhduy.dev/LSPD/checksiquan.php?name="+str(names)).text
    if resp == '0':
        await ctx.send(f"**{names}" + " chưa có tên trong danh sách đồn, liên hệ Quản Lý Ban Ngành để thêm vào !!!**")
    else:
        check_duty = requests.get("https://anhduy.dev/LSPD/check_duty.php?name="+str(names)).text
        if check_duty == "off":
            await ctx.send(f"**{names}" + " bạn đã offduty rồi !!!**")
        else:
            ids = ctx.author.id
            ts = time.time()
            ts = str(ts).split(".")[0]
            now = datetime.now()
            giohientai = now.strftime("%H:%M")
            off = requests.get(f"https://anhduy.dev/LSPD/index.php?com=off&name="+names+"&ts="+str(ts)).text
            time_on = str(off).split("|")[0]
            time_off = str(off).split("|")[1]
            timelamviec = int(time_off) - int(time_on)
            requests.get("https://anhduy.dev/LSPD/addtime.php?name="+str(names)+"&sec="+str(timelamviec))
            timeonduty = strftime("%Hh%Mp%Ss", gmtime(timelamviec))
            await ctx.send(f"**{names}**" + " đã dừng làm việc vào " + str(giohientai))
            await ctx.send(f"<@{ids}>" + " bạn đã onduty được " + str(timeonduty))
@bot.command(pass_context=True)
async def watch(ctx):
    ds = requests.get("https://anhduy.dev/LSPD/index.php?com=watch").text
    danhsachon = ds.split("<br>")
    ds = ds.replace("<br>", "\n")
    count = len(danhsachon) - 1
    await ctx.send(f"Hiện tại có **"+str(count)+"** sĩ quan đang onduty. \n**"+str(ds)+"**")
@bot.command(pass_context=True)
async def me(ctx):
    ids = ctx.author.id
    names = f"{ctx.message.author.display_name}"
    resp = requests.get("https://anhduy.dev/LSPD/checksiquan.php?name="+str(names)).text
    if resp == '0':
        await ctx.send(f"**{names}" + " chưa có tên trong danh sách đồn, liên hệ Quản Lý Ban Ngành để thêm vào !!!**")
    else:
        me = requests.get("https://anhduy.dev/LSPD/tongtime.php?name="+str(names)).text
        me = timeonduty = strftime("%Hh%Mp%Ss", gmtime(int(me)))
        await ctx.send(f"- Xin chào: **{names}**\n\n- Tổng thời gian onduty tháng này của bạn là: **"+str(me)+"**\n\n*- Lưu ý: Mỗi tháng thời gian onduty của sĩ quan sẽ reset về không.*")
@bot.command(pass_context=True)
async def check_time(ctx):
    names = f"{ctx.message.author.display_name}"
    f = open("permissions.txt", "r+")
    f = f.read()
    if names in f:
        ids = ctx.author.id
        message = ctx.message.content
        messname = str(message).split("#")[1]
        names = f"{ctx.message.author.display_name}"
        me = requests.get("https://anhduy.dev/LSPD/tongtime.php?name="+str(messname)).text
        if me == "0":
            await ctx.send(f"- Xin chào: **{names}**\n\n- Tổng thời gian onduty tháng này của **"+str(messname)+"** là: **00h00p00s**\n\n*- Lưu ý: Mỗi tháng thời gian onduty của sĩ quan sẽ reset về không.*")
        else:
            me = strftime("%Hh%Mp%Ss", gmtime(int(me)))
            await ctx.send(f"- Xin chào: **{names}**\n\n- Tổng thời gian onduty tháng này của **"+str(messname)+"** là: **"+str(me)+"**\n\n*- Lưu ý: Mỗi tháng thời gian onduty của sĩ quan sẽ reset về không.*")
    else:
        await ctx.send(f"***Bạn không đủ quyền hạn để sử dụng lệnh này !!!***")
@bot.command(pass_context=True)
async def reset(ctx):
    names = f"{ctx.message.author.display_name}"
    f = open("pers.txt", "r+")
    f = f.read()
    if names in f:
        requests.get("https://anhduy.dev/LSPD/reset.php")
        await ctx.send(f"***Xóa lịch sử onduty thành công !!!***")
    else:
        await ctx.send(f"***Bạn không đủ quyền hạn để sử dụng lệnh này !!!***")
@bot.command(pass_context=True)
async def add(ctx):
    names = f"{ctx.message.author.display_name}"
    message = ctx.message.content
    namesiquan = str(message).split("#")[1]
    f = open("pers.txt", "r+")
    f = f.read()
    if names in f:
        requests.get("https://anhduy.dev/LSPD/themsiquan.php?name="+str(namesiquan))
        await ctx.send(f"***Thêm thành công sĩ quan **{namesiquan}** vào danh sách đồn !!!***")
    else:
        await ctx.send(f"***Bạn không đủ quyền hạn để sử dụng lệnh này !!!***")
@bot.command(pass_context=True)
async def remove(ctx):
    names = f"{ctx.message.author.display_name}"
    message = ctx.message.content
    namesiquan = str(message).split("#")[1]
    f = open("pers.txt", "r+")
    f = f.read()
    if names in f:
        requests.get("https://anhduy.dev/LSPD/xoasiquan.php?name="+str(namesiquan))
        await ctx.send(f"***Xóa thành công sĩ quan **{namesiquan}** khỏi danh sách đồn !!!***")
    else:
        await ctx.send(f"***Bạn không đủ quyền hạn để sử dụng lệnh này !!!***")
@bot.command(pass_context=True)
async def check_list(ctx):
    names = f"{ctx.message.author.display_name}"
    message = ctx.message.content
    namesiquan = str(message).split("#")[1]
    f = open("pers.txt", "r+")
    f = f.read()
    if names in f:
        resp = requests.get("https://anhduy.dev/LSPD/checksiquan.php?name="+str(namesiquan)).text
        if resp == '1':
            await ctx.send(f"***Sĩ quan **{namesiquan}** đã có tên trong danh sách đồn.***")
        else:
            await ctx.send(f"***Sĩ quan **{namesiquan}** chưa có tên trong danh sách đồn.***")
    else:
        await ctx.send(f"***Bạn không đủ quyền hạn để sử dụng lệnh này !!!***")
@bot.command(pass_context=True)
async def check_off(ctx):
    names = f"{ctx.message.author.display_name}"
    f = open("pers.txt", "r+")
    f = f.read()
    if names in f:
        resp = requests.get("https://anhduy.dev/LSPD/offline.php").text
        resp = resp.replace("<br>", "\n")
        await ctx.send(f"*- Danh sách các sĩ quan 3 ngày gần đây không onduty.*\n\n**{resp}**")
    else:
        await ctx.send(f"***Bạn không đủ quyền hạn để sử dụng lệnh này !!!***")
bot.run("MTExNTQ4MDkzMDM0MjE0MjA0Mg.GIvS8H.minSd4HlMaU939zclF4wNGz2NVkP9wyMW64RRo")