from riotwatcher import LolWatcher,TftWatcher, ApiError
import discord
import nest_asyncio
import crap
import macro
import datetime  
import requests
from math import log, floor
from bs4 import BeautifulSoup

# Je sais plus ce que ça fait mais c'est utile
nest_asyncio.apply()
client = discord.Client()
Mmr_Check = crap.MmrCheck()


#api riot key

api_key = 'ENTER YOUR RIOT API KEY HERE' # ENTER YOUR RIOT API KEY HERE
watcher = LolWatcher(api_key)
tft_watcher = TftWatcher(api_key)
my_region = 'euw1'

months = ['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre']


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game('Lee sin a essayer de me dive j ai flash pour'))
    print('We have logged in as {0.user}'.format(client))

#--------------------- Partie pour les messages -------------------------------  
@client.event
async def on_message(message): 
    if message.author == client.user:
        return

    # answer to $help -> syntax $help
    if (message.content.startswith('$help') and (message.author.name != "Layther")):
        await message.channel.send(":sunflower: 𝗩𝗼𝗶𝗰𝗶 𝘁𝗼𝘂𝘁𝗲𝘀 𝗹𝗲𝘀 𝗰𝗼𝗺𝗺𝗮𝗻𝗱𝗲𝘀 𝗱𝗶𝘀𝗽𝗼𝗻𝗶𝗯𝗹𝗲𝘀 𝗮𝘃𝗲𝗰 𝗰𝗲 𝗯𝗼𝘁  :sunflower:\n╔════════════════════════════════════════════════╗ \n    『-』__$mmr__ : ca marche pas pr linstant tg 'Te permet de voir ton MMR'\n    『-』__$info <pseudo>__ : Te permet de voir les informations de ton profil\n    『-』__$clash__ : Te permet de voir la date du prochain clash\n    『-』__$pingclash__ : Te permet de recruter des gens pour clash\n    『-』__$time <pseudo>__ : Indique le temps de jeu depuis la S11 (prend du temps)\n╚════════════════════════════════════════════════╝")

    if (message.content.startswith('👋')  and (message.author.name != "Layther")):
        await message.channel.send("👋 {}".format(message.author.display_name))

    if ('$info' in message.content and (message.author.name != "Layther")):
        # get the current version of the game
        versions_raw = watcher.data_dragon.versions_for_region(my_region)
        versionId = versions_raw.get("v")

        # extract the nickname as : 
        # pseudo_url --> the nickname with %20 for space (used for url)
        # pseudo --> the nick name as original without the trigger command (here $info)
        pseudo_url, pseudo = Mmr_Check.key_words_search_words(message.content)

        
        # try catch error about wrong summoner name
        try:
            me = watcher.summoner.by_name(my_region, pseudo)
            exists_name = True
        except ApiError as err:
            await message.channel.send("Cet invocateur n'existe pas")
            exists_name = False

        if (exists_name):
            # get basic informations (name, icon, level)
            me = watcher.summoner.by_name(my_region, pseudo)
            print(me)
        
            last_game = (me['revisionDate']/1000)

            # get even more informations
            ranked_stats = watcher.league.by_summoner(my_region,me['id'])
            rank_name = pseudo
            print(ranked_stats)

            # get the most played champ
            champions_mastery = watcher.champion_mastery.by_summoner(my_region,me['id'])


            #get the index for the soloQ in the ranked_stats list
            soloq_index = next((index for (index, d) in enumerate(ranked_stats) if d["queueType"] == "RANKED_SOLO_5x5"), None)
            #if player is not ranked in soloQ they are unranked otherwise their rank is being diplayed
            if (soloq_index is None):
                rank_soloq = "Unranked"
                league_points_soloq = 0
                wins_soloq = 0
                loses_soloq = 0
                total_game_soloq = wins_soloq + loses_soloq 
                winrate_soloq = 0
            else:
                rank_soloq = ranked_stats[soloq_index]["tier"] + " " + ranked_stats[soloq_index]["rank"]
                league_points_soloq = ranked_stats[soloq_index]["leaguePoints"]
                rank_name = ranked_stats[soloq_index]["summonerName"]
                wins_soloq = ranked_stats[soloq_index]["wins"]
                loses_soloq = ranked_stats[soloq_index]["losses"]
                total_game_soloq = wins_soloq + loses_soloq 
                winrate_soloq = (wins_soloq*100 // (loses_soloq+wins_soloq))
             
            #if player is not ranked in flexQ they are unranked otherwise their rank is being diplayed
            flexq_index = next((index for (index, d) in enumerate(ranked_stats) if d["queueType"] == "RANKED_FLEX_SR"), None)
            if (flexq_index is None):
                rank_flexq = "Unranked"
                league_points_flexq = 0
                wins_flexq = 0
                loses_flexq = 0
                total_game_flexq = wins_flexq + loses_flexq 
                winrate_flexq = 0
            else:
                rank_flexq = ranked_stats[flexq_index]["tier"] + " " + ranked_stats[flexq_index]["rank"]
                league_points_flexq = ranked_stats[flexq_index]["leaguePoints"]
                rank_name = ranked_stats[flexq_index]["summonerName"]
                wins_flexq = ranked_stats[flexq_index]["wins"]
                loses_flexq = ranked_stats[flexq_index]["losses"]
                total_game_flexq = wins_flexq + loses_flexq 
                winrate_flexq = (wins_flexq * 100 // (loses_flexq + wins_flexq))


            # creation of the embed
            embed = discord.Embed(title=me["name"], url="https://euw.op.gg/summoner/userName={}".format(pseudo_url), description="Voici les informations concernants l'invocateur **{}**".format(me["name"]), color=discord.Color.blue())
            embed.set_author(name="Kevin Disocord bot", url="https://twitter.com/Kevin_Kevzer", icon_url="https://i.ibb.co/82m2VGf/unknow333n.png")
            # field about the informations
            embed.add_field(name="Informations",value="Pseudo : **{}**\nNiveau : {}\nLast game : {}\nRang IZ : *soon*".format(me["name"], me.get("summonerLevel"), datetime.datetime.fromtimestamp(last_game).strftime('%d/%m/%Y %H:%M:%S')),inline=False)
          
            embed.add_field(name="Ranked Solo",value="Rank : **{0}**\n LP : **{1}**\nGames : **{5}**\nWins - Loses : **{2}** - **{3}**\n Winrate : **{4}%**".format(rank_soloq, league_points_soloq, wins_soloq, loses_soloq, winrate_soloq,total_game_soloq),inline=True)
            embed.add_field(name="Ranked Flex",value="Rank : **{0}**\n LP : **{1}**\nGames : **{5}**\nWins - Loses : **{2}** - **{3}**\n Winrate : **{4}%**".format(rank_flexq, league_points_flexq, wins_flexq, loses_flexq, winrate_flexq,total_game_flexq),inline=True)

            if (len(champions_mastery) >= 5):
                embed.add_field(name="Top 5 Champions",value="1. {0} ({1})\n2. {2} ({3})\n3. {4} ({5})\n4. {6} ({7})\n5. {8} ({9})".format(macro.get_champions_name(champions_mastery[0]["championId"]), macro.human_format(champions_mastery[0]["championPoints"]),macro.get_champions_name(champions_mastery[1]["championId"]), macro.human_format(champions_mastery[1]["championPoints"]),macro.get_champions_name(champions_mastery[2]["championId"]), macro.human_format(champions_mastery[2]["championPoints"]),macro.get_champions_name(champions_mastery[3]["championId"]), macro.human_format(champions_mastery[3]["championPoints"]),macro.get_champions_name(champions_mastery[4]["championId"]), macro.human_format(champions_mastery[4]["championPoints"])),inline=False)
            if (len(champions_mastery) == 4):
                embed.add_field(name="Top 4 Champions",value="1. {0} ({1})\n2. {2} ({3})\n3. {4} ({5})\n4. {6} ({7})".format(macro.get_champions_name(champions_mastery[0]["championId"]), macro.human_format(champions_mastery[0]["championPoints"]),macro.get_champions_name(champions_mastery[1]["championId"]), macro.human_format(champions_mastery[1]["championPoints"]),macro.get_champions_name(champions_mastery[2]["championId"]), macro.human_format(champions_mastery[2]["championPoints"]),macro.get_champions_name(champions_mastery[3]["championId"]), macro.human_format(champions_mastery[3]["championPoints"])),inline=False)
            if (len(champions_mastery) == 3):
                embed.add_field(name="Top 3 Champions",value="1. {0} ({1})\n2. {2} ({3})\n3. {4} ({5})".format(macro.get_champions_name(champions_mastery[0]["championId"]), macro.human_format(champions_mastery[0]["championPoints"]),macro.get_champions_name(champions_mastery[1]["championId"]), macro.human_format(champions_mastery[1]["championPoints"]),macro.get_champions_name(champions_mastery[2]["championId"]), macro.human_format(champions_mastery[2]["championPoints"])),inline=False)
            if (len(champions_mastery) == 2):
                embed.add_field(name="Top 2 Champions",value="1. {0} ({1})\n2. {2} ({3})".format(macro.get_champions_name(champions_mastery[0]["championId"]), macro.human_format(champions_mastery[0]["championPoints"]),macro.get_champions_name(champions_mastery[1]["championId"]), macro.human_format(champions_mastery[1]["championPoints"])),inline=False)
            if (len(champions_mastery) == 1):
                embed.add_field(name="Top 1 Champions",value="1. {0} ({1})".format(macro.get_champions_name(champions_mastery[0]["championId"]), macro.human_format(champions_mastery[0]["championPoints"])),inline=False)
            if (len(champions_mastery) == 0):
                embed.add_field(name="Top 5 Champions",value="Cet invocateur n'as jamais joué de champion",inline=False)
            
            embed.set_footer(text="Version patch : {}".format(versionId))

            # put the icon as a thumbnail in the embed window
            iconId = me.get("profileIconId")
            icon_url = "https://ddragon.leagueoflegends.com/cdn/{}/img/profileicon/{}.png".format(versionId,iconId)
            embed.set_thumbnail(url=icon_url)

            #send embed
            await message.channel.send(embed=embed)


    if "$mmr" in message.content:
        pseudo_url, pseudo = Mmr_Check.key_words_search_words(message.content)
        mmr_request = Mmr_Check.search_mmr(pseudo_url)
        result_mmr, result_rank, summary = Mmr_Check.trans_mmr(mmr_request)
        A = macro.tradu(summary,result_rank)
        await message.channel.send("{0} a un mmr de {2}, soit {1}".format(pseudo,A,result_mmr))


    # Get the informations about the upcomming clash
    if ('$clash' in message.content  and (message.author.name != "Layther")):

        clash_info = watcher.clash.tournaments(my_region)
        #datetime_time = datetime.datetime.fromtimestamp(clash_info[1]["schedule"][0]["startTime"])
        clash_start = (clash_info[0]["schedule"][0]["startTime"]/1000)
        date_time_clash_start_day1 = datetime.datetime.fromtimestamp(clash_start)

        await message.channel.send("La date du prochain clash est le **{0} {1}** à **{2}h**".format(date_time_clash_start_day1.day,months[date_time_clash_start_day1.month-1],date_time_clash_start_day1.hour))


    # display a message box to allow people to react if they want to play the clash
    if ('$pingclash' in message.content  and (message.author.name != "Layther")):

        message_before = message.content.split()
        clash_day = (int((message_before[1]))-1)

        if (clash_day == 1):
            clash_number = 0
        else:
            clash_number = 1

        # delete the previous message
        await message.delete()

        # get information about the previous clash
        clash_info = watcher.clash.tournaments(my_region)
        clash_start = (clash_info[clash_number]["schedule"][0]["startTime"]/1000)

        date_time_clash_start_day1 = datetime.datetime.fromtimestamp(clash_start)

        # embed creation
        if (clash_day == 0):
            embed_clash = discord.Embed(title="Clash Samedi", description="**{0}** aimerait faire le clash de **Samedi**\nLa date du prochain clash (samedi) est le **{1} {2} à {3}h**\nSi vous souhaitez participer au clash mettez la réaction ☑️".format(message.author.display_name,date_time_clash_start_day1.day,months[date_time_clash_start_day1.month-1],date_time_clash_start_day1.hour),color=discord.Color.blue())
        elif (clash_day == 1):
            embed_clash = discord.Embed(title="Clash Dimanche", description="**{0}** aimerait faire le clash de **Dimanche** !\nLe date du prochain clash (dimanche) est le **{1} {2} à {3}h**\nSi vous souhaitez participer au clash mettez la réaction ☑️".format(message.author.display_name,date_time_clash_start_day1.day,months[date_time_clash_start_day1.month-1],date_time_clash_start_day1.hour),color=discord.Color.blue())
        else:
            embed_clash = discord.Embed(title="Grosse merde", description="**{0}** est un énorme abruti car on lui demande de faire $pingclash 1 ou $pingclash 2 et ce gros shlag met autre chose c'est fou quand même de se dire que tes parents ont voulu te garder".format(message.author),color=discord.Color.blue())
        embed_clash.set_author(name=message.author.display_name, icon_url=message.author.avatar_url)
        embed_clash.set_thumbnail(url="https://images.contentstack.io/v3/assets/blt731acb42bb3d1659/blt127a56b2f8bc7e73/5f8537721f5f6d4173b4ed4d/ClashIcon_Tier1.jpg")
        
        # send message & réaction
        await message.channel.send(Lol_mention)
        react = await message.channel.send(embed=embed_clash)
        await react.add_reaction("☑️")
        

    # get informations about the time spend on League
    if ("$time" in message.content  and (message.author.name != "Layther")):
        pseudo_url, pseudo = Mmr_Check.key_words_search_words(message.content)

        hours_played = search_time(pseudo_url)

        await message.channel.send("Le temps de jeu pour __{}__ est de **{}** heures\n--> https://wol.gg/stats/euw/{}/ <--".format(pseudo,hours_played,pseudo_url))


    if ("$histo" in message.content  and (message.author.name != "Layther")):
        pseudo_url, pseudo = Mmr_Check.key_words_search_words(message.content)

        me = watcher.summoner.by_name(my_region, pseudo)
        match_info = watcher.match.matchlist_by_puuid("europe", me['puuid'])
        print(match_info)

        match_1 = match_info[1]
        match_specs = watcher.match.by_id("europe", match_1)
        print(match_specs)


    # get informations about tft
    """
    if '$tft' in message.content:

        # get the current version of the game
        versions_raw = watcher.data_dragon.versions_for_region(my_region)
        versionId = versions_raw.get("v")

        # extract the nickname as : 
        # pseudo_url --> the nickname with %20 for space (used for url)
        # pseudo --> the nick name as original without the trigger command (here $info)
        pseudo_url, pseudo = Mmr_Check.key_words_search_words(message.content)

        tft = tft_watcher.summoner.by_name(my_region, pseudo)

        tft_ranked = tft_watcher.league.by_summoner(my_region,tft['id'])
        print(tft_ranked)
    """

def tradu(summ,unrank):
        L = summ.split()
        G = []
        for i in range(len(L)):
            if L[i] == 'Slightly':
                G.append('un peu')
            if L[i] == 'Significally':
                G.append('très')
            if L[i] == 'Approximately':
                G.append('à peu près')
        N = unrank.split()
        B = []
        for i in range(len(N)):
            if N[i] == 'below':
                B.append('en dessous de')
            if N[i] == 'above':
                B.append('au dessus de')
        B.append(N[-2])
        B.append(N[-1])
        A = ' '.join(G+B)
        A = str(A)
        A.capitalize()
        return A

def get_champions_name(_id):
    """
    Get the name depending on the champion ID
    """
    all_champion_id = {
        1: 'Annie',
        2: 'Olaf',
        3: 'Galio',
        4: 'Twisted Fate',
        5: 'Xin Zhao',
        6: 'Urgot',
        7: 'LeBlanc',
        8: 'Vladimir',
        9: 'Fiddlesticks',
        10: 'Kayle',
        11: 'Master Yi',
        12: 'Alistar',
        13: 'Ryze',
        14: 'Sion',
        15: 'Sivir',
        16: 'Soraka',
        17: 'Teemo',
        18: 'Tristana',
        19: 'Warwick',
        20: 'Nunu & Willump',
        21: 'Miss Fortune',
        22: 'Ashe',
        23: 'Tryndamere',
        24: 'Jax',
        25: 'Morgana',
        26: 'Zilean',
        27: 'Singed',
        28: 'Evelynn',
        29: 'Twitch',
        30: 'Karthus',
        31: "Cho'Gath",
        32: 'Amumu',
        33: 'Rammus',
        34: 'Anivia',
        35: 'Shaco',
        36: 'Dr.Mundo',
        37: 'Sona',
        38: 'Kassadin',
        39: 'Irelia',
        40: 'Janna',
        41: 'Gangplank',
        42: 'Corki',
        43: 'Karma',
        44: 'Taric',
        45: 'Veigar',
        48: 'Trundle',
        50: 'Swain',
        51: 'Caitlyn',
        53: 'Blitzcrank',
        54: 'Malphite',
        55: 'Katarina',
        56: 'Nocturne',
        57: 'Maokai',
        58: 'Renekton',
        59: 'JarvanIV',
        60: 'Elise',
        61: 'Orianna',
        62: 'Wukong',
        63: 'Brand',
        64: 'LeeSin',
        67: 'Vayne',
        68: 'Rumble',
        69: 'Cassiopeia',
        72: 'Skarner',
        74: 'Heimerdinger',
        75: 'Nasus',
        76: 'Nidalee',
        77: 'Udyr',
        78: 'Poppy',
        79: 'Gragas',
        80: 'Pantheon',
        81: 'Ezreal',
        82: 'Mordekaiser',
        83: 'Yorick',
        84: 'Akali',
        85: 'Kennen',
        86: 'Garen',
        89: 'Leona',
        90: 'Malzahar',
        91: 'Talon',
        92: 'Riven',
        96: "Kog'Maw",
        98: 'Shen',
        99: 'Lux',
        101: 'Xerath',
        102: 'Shyvana',
        103: 'Ahri',
        104: 'Graves',
        105: 'Fizz',
        106: 'Volibear',
        107: 'Rengar',
        110: 'Varus',
        111: 'Nautilus',
        112: 'Viktor',
        113: 'Sejuani',
        114: 'Fiora',
        115: 'Ziggs',
        117: 'Lulu',
        119: 'Draven',
        120: 'Hecarim',
        121: "Kha'Zix",
        122: 'Darius',
        126: 'Jayce',
        127: 'Lissandra',
        131: 'Diana',
        133: 'Quinn',
        134: 'Syndra',
        136: 'AurelionSol',
        141: 'Kayn',
        142: 'Zoe',
        143: 'Zyra',
        145: "Kai'sa",
        147: "Seraphine",
        150: 'Gnar',
        154: 'Zac',
        157: 'Yasuo',
        161: "Vel'Koz",
        163: 'Taliyah',
        166: "Akshan",
        164: 'Camille',
        201: 'Braum',
        202: 'Jhin',
        203: 'Kindred',
        222: 'Jinx',
        223: 'TahmKench',
        234: 'Viego',
        235: 'Senna',
        236: 'Lucian',
        238: 'Zed',
        240: 'Kled',
        245: 'Ekko',
        246: 'Qiyana',
        254: 'Vi',
        266: 'Aatrox',
        267: 'Nami',
        268: 'Azir',
        350: 'Yuumi',
        360: 'Samira',
        412: 'Thresh',
        420: 'Illaoi',
        421: "Rek'Sai",
        427: 'Ivern',
        429: 'Kalista',
        432: 'Bard',
        497: 'Rakan',
        498: 'Xayah',
        516: 'Ornn',
        517: 'Sylas',
        526: 'Rell',
        518: 'Neeko',
        523: 'Aphelios',
        555: 'Pyke',
        875: "Sett",
        711: "Vex",
        777: "Yone",
        887: "Gwen",
        876: "Lillia",
        }
    return all_champion_id.get(_id)

def search_time(words):
    username = 'https://wol.gg/stats/euw/'+words+"/"
    response = requests.get(username)
    content = response.content
    soup = BeautifulSoup(content, 'html.parser')
    sousp = soup.find("div", {"id": "time-hours"})
    soups = str(sousp)
    index_rank = soups.find('<p>')
    index_rank_end = soups.find('<br/>')
    res_soup = soups[index_rank+3:index_rank_end]
    return res_soup 


def human_format(num, precision=2, suffixes=['', 'K', 'M', 'G', 'T', 'P']):
    m = sum([abs(num/1000.0**x) >= 1 for x in range(1, len(suffixes))])
    return f'{num/1000.0**m:.{precision}f}{suffixes[m]}'


client.run('ENTER YOUR DISCORD KEY HERE') # ENTER YOUR DISCORD KEY HERE