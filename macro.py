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