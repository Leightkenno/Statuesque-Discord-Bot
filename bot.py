import discord
from discord import app_commands
from discord.ext import commands, tasks
from discord.ui import View, Button, Select
import aiohttp
import aiosqlite
import asyncio
from datetime import datetime, timedelta, timezone
from typing import Optional, List
import os
import random
import re
import json
import uuid
import io

# ==================== CONFIGURATION ====================
BOT_CONFIG = {
    "clan_name": "Statuesque",
    "clan_motto": "Always Aiming Higher",
    "logo_url": "https://images2.imgbox.com/5b/69/CQ2uyKbe_o.png",
    "banner_url": "",
    "primary_color": 0x00A2E8,
    "success_color": 0x2ECC71,
    "error_color": 0xE74C3C,
    "warning_color": 0xF39C12,
    "gold_color": 0xFFD700,
    "website": "",
    "discord_invite": "",
    "activity_check_interval": 3,
    "clan_check_interval": 5,

    "clan_public_channel": 1462568455038304287,   # Joins & Promotions
    "clan_private_channel": 1014968289241354240,  # Demotions & Leaves
}

GUILD_ID = 975438156868505690 

BOT_TOKEN = ""
DATABASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "clan_bot.db")

# API URLs
RUNEMETRICS_URL = "https://apps.runescape.com/runemetrics/profile/profile?user={}&activities=20"
HISCORES_URL = "https://secure.runescape.com/m=hiscore/index_lite.ws?player={}"
CLAN_API_URL = "https://secure.runescape.com/m=clan-hiscores/members_lite.ws?clanName={}"
WIKI_PRICE_URL = "https://api.weirdgloop.org/exchange/history/rs/latest?name={}"
WIKI_SEARCH_URL = "https://runescape.wiki/api.php?action=opensearch&search={}&limit=10&namespace=0&format=json"
ELY_PRICE_URL = "https://api.ely.gg/price/{}"

SKILLS = ["Overall", "Attack", "Defence", "Strength", "Constitution", "Ranged", "Prayer", "Magic", "Cooking", "Woodcutting", "Fletching", "Fishing", "Firemaking", "Crafting", "Smithing", "Mining", "Herblore", "Agility", "Thieving", "Slayer", "Farming", "Runecrafting", "Hunter", "Construction", "Summoning", "Dungeoneering", "Divination", "Invention", "Archaeology", "Necromancy"]

SKILL_ICONS = {"Overall": "https://runescape.wiki/images/Skills_icon.png", "Attack": "https://runescape.wiki/images/Attack_detail.png?346f8", "Defence": "https://runescape.wiki/images/Defence_detail.png?346f8", "Strength": "https://runescape.wiki/images/thumb/Strength_detail.png/100px-Strength_detail.png?0f0af", "Constitution": "https://runescape.wiki/images/Constitution_detail.png?346f8", "Ranged": "https://runescape.wiki/images/thumb/Ranged_detail.png/100px-Ranged_detail.png?0f0af", "Prayer": "https://runescape.wiki/images/thumb/Prayer_detail.png/100px-Prayer_detail.png?0f0af", "Magic": "https://runescape.wiki/images/Magic_detail.png?4c3a6", "Cooking": "https://runescape.wiki/images/Cooking_detail.png?346f8", "Woodcutting": "https://runescape.wiki/images/Woodcutting_detail.png?bf108", "Fletching": "https://runescape.wiki/images/Fletching_detail.png?4c3a6", "Fishing": "https://runescape.wiki/images/Fishing_detail.png?4c3a6", "Firemaking": "https://runescape.wiki/images/Firemaking_detail.png?4c3a6", "Crafting": "https://runescape.wiki/images/Crafting_detail.png?346f8", "Smithing": "https://runescape.wiki/images/Smithing_detail.png?0f0af", "Mining": "https://runescape.wiki/images/Mining_detail.png?4c3a6", "Herblore": "https://runescape.wiki/images/Herblore_detail.png?4c3a6", "Agility": "https://runescape.wiki/images/thumb/Agility_detail.png/100px-Agility_detail.png?346f8g", "Thieving": "https://runescape.wiki/images/Thieving_detail.png?bf108", "Slayer": "https://runescape.wiki/images/thumb/Slayer_detail.png/100px-Slayer_detail.png?0f0af", "Farming": "https://runescape.wiki/images/Farming_detail.png?4c3a6", "Runecrafting": "https://runescape.wiki/images/Runecrafting_detail.png?0f0af", "Hunter": "https://runescape.wiki/images/Hunter_detail.png?4c3a6", "Construction": "https://runescape.wiki/images/thumb/Construction_detail.png/100px-Construction_detail.png?346f8", "Summoning": "https://runescape.wiki/images/Summoning_detail.png?0f0af", "Dungeoneering": "https://runescape.wiki/images/Dungeoneering_detail.png?4c3a6", "Divination": "https://runescape.wiki/images/Divination_detail.png?346f8", "Invention": "https://runescape.wiki/images/Invention_detail.png?4c3a6", "Archaeology": "https://runescape.wiki/images/thumb/Archaeology_detail.png/100px-Archaeology_detail.png?346f8", "Necromancy": "https://runescape.wiki/images/thumb/Necromancy_detail.png/100px-Necromancy_detail.png?0f0af"}

XP_TABLE = [0, 0, 83, 174, 276, 388, 512, 650, 801, 969, 1154, 1358, 1584, 1833, 2107, 2411, 2746, 3115, 3523, 3973, 4470, 5018, 5624, 6291, 7028, 7842, 8740, 9730, 10824, 12031, 13363, 14833, 16456, 18247, 20224, 22406, 24815, 27473, 30408, 33648, 37224, 41171, 45529, 50339, 55649, 61512, 67983, 75127, 83014, 91721, 101333, 111945, 123660, 136594, 150872, 166636, 184040, 203254, 224466, 247886, 273742, 302288, 333804, 368599, 407015, 449428, 496254, 547953, 605032, 668051, 737627, 814445, 899257, 992895, 1096278, 1210421, 1336443, 1475581, 1629200, 1798808, 1986068, 2192818, 2421087, 2673114, 2951373, 3258594, 3597792, 3972294, 4385776, 4842295, 5346332, 5902831, 6517253, 7195629, 7944614, 8771558, 9684577, 10692629, 11805606, 13034431]
ELITE_XP = {120: 104273167, 150: 200000000}
BOSSES = ["Araxxor", "Arch-Glacor", "Croesus", "ED1: Seiryu", "ED2: BSD", "ED3: Ambassador", "Giant Mole", "Gregorovic", "Helwyr", "Kalphite King", "Kerapac", "King Black Dragon", "Legiones", "Magister", "Nex", "Nex: AoD", "Raksha", "Rasial", "Solak", "Telos", "TzKal-Zuk", "Vindicta", "Vorago", "Zamorak", "Zammy GWD", "Bandos GWD", "Sara GWD", "Arma GWD", "ED4: Zamorak", "Sanctum of Rebirth"]

# RS3 Clan Ranks (highest to lowest)
CLAN_RANKS = ["Owner", "Deputy Owner", "Overseer", "Coordinator", "Organiser", "Admin", "General", "Captain", "Lieutenant", "Sergeant", "Corporal", "Recruit", "Guest"]
RANK_HIERARCHY = {rank: len(CLAN_RANKS) - i for i, rank in enumerate(CLAN_RANKS)}

WILDERNESS_FLASH_EVENTS = [{"name": "King Black Dragon Rampage", "icon": "🐉", "type": "boss"}, {"name": "Infernal Star", "icon": "⭐", "type": "skilling"}, {"name": "Evil Bloodwood Tree", "icon": "🌳", "type": "skilling"}, {"name": "Spider Swarm", "icon": "🕷️", "type": "combat"}, {"name": "Forgotten Soldiers", "icon": "⚔️", "type": "combat"}, {"name": "Demon Stragglers", "icon": "😈", "type": "combat"}, {"name": "Butterfly Swarm", "icon": "🦋", "type": "skilling"}, {"name": "Ramokee Incursion", "icon": "👹", "type": "combat"}, {"name": "Wilderness Wyrm", "icon": "🐛", "type": "boss"}, {"name": "Stryke the Wyrm", "icon": "🔥", "type": "boss"}, {"name": "Chaos Elemental", "icon": "🌀", "type": "boss"}, {"name": "Hellhound Pack", "icon": "🐕", "type": "combat"}]
WORLD_EVENTS = {"merchant": {"name": "Travelling Merchant", "icon": "🛒"}, "gorajo": {"name": "Gorajo Resource Dungeon", "icon": "🏔️"}, "seren": {"name": "Voice of Seren", "icon": "🔮"}, "cache": {"name": "Guthixian Cache", "icon": "💚"}, "sinkholes": {"name": "Sinkholes", "icon": "🕳️"}, "warbands": {"name": "Warbands", "icon": "⚔️"}, "spotlight": {"name": "Minigame Spotlight", "icon": "🎮"}}

# Weird Gloop API for live event data
VOS_API_URL = "https://api.weirdgloop.org/runescape/vos"
TMS_API_URL = "https://api.weirdgloop.org/runescape/tms/current?lang=en"

# Voice of Seren clan benefits
VOS_BENEFITS = {
    "Amlodd": {"skills": "Summoning, Divination", "benefit": "20% more Summoning XP, +10% divine location gather", "location": "NE Prifddinas"},
    "Cadarn": {"skills": "Ranged, Magic", "benefit": "+200 Combat XP per elf kill, faster crystal weapon attuning", "location": "SE Prifddinas"},
    "Crwys": {"skills": "Woodcutting, Farming", "benefit": "20% more WC XP, +5% farming yield", "location": "SW Prifddinas"},
    "Hefin": {"skills": "Agility, Prayer", "benefit": "20% more Agility XP, +5 prayer points restored", "location": "N Prifddinas"},
    "Iorwerth": {"skills": "Melee, Slayer", "benefit": "+200 Combat XP per elf kill, 20% slayer XP boost", "location": "W Prifddinas"},
    "Ithell": {"skills": "Crafting, Construction", "benefit": "20% more Crafting XP, clay won't deplete", "location": "NW Prifddinas"},
    "Meilyr": {"skills": "Dungeoneering, Herblore", "benefit": "20% more Dung XP, harmony moss +5 mins", "location": "N Prifddinas"},
    "Trahaearn": {"skills": "Mining, Smithing", "benefit": "20% more Mining XP, corrupted ore bonus, animica spawns", "location": "S Prifddinas"},
}

# Warbands camp locations  
WARBANDS_CAMPS = ["Dark Warriors' Fortress (lvl 14)", "Red Dragon Isle (lvl 35)", "Lava Maze (lvl 42)", "Wilderness Volcano (lvl 20)"]

# Minigame Spotlight rotation (14 day cycle)
SPOTLIGHT_GAMES = ["Pest Control", "Soul Wars", "Fist of Guthix", "Barbarian Assault", "Conquest", "Castle Wars", "Stealing Creation", "Cabbage Facepunch Bonanza", "Heist", "Mobilising Armies", "Spotlight: TBD", "The Great Orb Project", "Flash Powder Factory", "Trouble Brewing"]
VALUABLE_DROPS = [
    # Nex
    "torva", "pernix", "virtus", "zaryte bow", "zaryte crossbow",
    # AoD
    "wand of the praesul", "imperium core", "praesul codex", "chest of praesul",
    # Telos
    "dormant", "orb", "reprisor", "seren godbow", "staff of sliske", "zaros godsword",
    # Solak
    "blightbound", "erethdor's grimoire", "grimoire",
    # ED
    "greater ricochet", "greater chain", "divert", "shadow spike", "laceration boots", "blast diffusion boots",
    # Vorago
    "seismic wand", "seismic singularity", "vitalis",
    # ED3/Raksha
    "eldritch crossbow", "ecb", "greater chain", "divert", "fleeting boots",
    # FSOA/Kerapac
    "fractured", "fsoa", "staff of armadyl", "greater concentrated blast",
    # Croesus
    "cryptbloom",
    # Zammy
    "bow of the last guardian", "vestments", "chaos roar",
    # Arch-Glacor
    "frozen core", "dark nilas", "leng artefact", "dark shard of leng", "glacor remnants",
    # GWD2
    "crest of", "lance", "anima core", "dormant anima",
    # Araxxor
    "araxxi", "leg piece", "fang", "eye", "web", "hilt", "araxyte",
    # Clue/Rare
    "hazelmere", "blurberry", "orlando", "cheese+tom", "third-age", "blood dye", "barrows dye", "shadow dye", "ice dye", "backstab cape",
    # Codex/Scripture
    "shard of", "codex", "scripture", "complete",
    # Rasial (Necromancy)
    "soulbound lantern", "soulbound", "omni guard", "death guard", "undead slayer codex", "first necromancer",
    # Sanctum of Rebirth
    "ode to deceit", "roar of awakening", "shard of genesis", "eye of the dagannoth", "horn of the dagannoth", "amulet of blood fury",
    # Pets
    "pet", "vitalis", "bombi", "barry", "shrimpy", "rex", "mallory", "otto", "baby araxxi", "kevin", "lilwyr", "rawrvek", "greg", "vindiddy",
    # Zamorak
    "infernal", "vestments of havoc", "bow of the last guardian",
    # Misc high value
    "essence of finality", "eof", "enchantment of", "scripture of",
]
TRASH_DROPS = ["triskelion", "clue scroll", "elite clue", "hard clue", "master clue", "dragon helm", "dragon shield", "dragon platelegs", "dragon plateskirt", "dragon chainbody", "dragon med", "dragon sq", "dragon dagger", "dragon longsword", "dragon battleaxe", "dragon mace", "warrior's ring", "berserker ring", "seers' ring", "archers' ring", "rune", "adamant", "mithril", "black", "steel", "iron", "bronze", "ancient effigy", "effigy", "lootbeam", "starved ancient effigy", "clue", "casket", "mimic", "puzzle", "reward casket", "Guthix bow", "saradomin sword", "zamorak spear", "loop half", "tooth half", "shield left half", "shield right half", "dragon spear", "curved bone", "long bone"]

# Item aliases for /price command - maps shorthand to full item name
ITEM_ALIASES = {
    # Weapons
    "fsoa": "Fractured Staff of Armadyl",
    "ecb": "Eldritch crossbow",
    "sgb": "Seren godbow",
    "zgs": "Zaros godsword",
    "sos": "Staff of Sliske",
    "bolg": "Bow of the Last Guardian",
    "lotd": "Luck of the Dwarves",
    "eof": "Essence of Finality amulet",
    "grico": "Greater Ricochet ability codex",
    "gconc": "Greater Concentrated Blast ability codex",
    "gchain": "Greater Chain ability codex",
    "gbarge": "Greater Barge ability codex",
    "gfury": "Greater Fury ability codex",
    "gflurry": "Greater Flurry ability codex",
    "limitless": "Limitless ability codex",
    "divert": "Divert ability codex",
    # Crossbows
    "ascmh": "Ascension crossbow",
    "ascoh": "Off-hand Ascension crossbow",
    "asc": "Ascension crossbow",
    "blights": "Blightbound crossbow",
    "bbc": "Blightbound crossbow",
    # Armour
    "tmw": "Trimmed masterwork platebody",
    "cryptbloom": "Cryptbloom helm",
    "sirenic": "Sirenic hauberk",
    "elite sirenic": "Elite sirenic hauberk",
    "tectonic": "Tectonic robe top",
    "elite tectonic": "Elite tectonic robe top",
    # Nex
    "torva helm": "Torva full helm",
    "torva body": "Torva platebody",
    "torva legs": "Torva platelegs",
    "pernix cowl": "Pernix cowl",
    "pernix body": "Pernix body",
    "pernix chaps": "Pernix chaps",
    "virtus mask": "Virtus mask",
    "virtus body": "Virtus robe top",
    "virtus legs": "Virtus robe legs",
    # Scriptures
    "scripture of jas": "Scripture of Jas",
    "scripture of ful": "Scripture of Ful",
    "scripture of wen": "Scripture of Wen",
    "scripture of bik": "Scripture of Bik",
    "grim": "Erethdor's grimoire",
    "grimoire": "Erethdor's grimoire",
    # Misc
    "praesul wand": "Wand of the Praesul",
    "praesul core": "Imperium core",
    "seismic wand": "Seismic wand",
    "seismic sing": "Seismic singularity",
    "sing": "Seismic singularity",
    "nox scythe": "Noxious scythe",
    "nox staff": "Noxious staff",
    "nox bow": "Noxious longbow",
    "scythe": "Noxious scythe",
    "zbow": "Zaryte bow",
    "zcb": "Zaryte crossbow",
    "leng": "Dark Shard of Leng",
    "dark ice shard": "Dark Shard of Leng",
    "dark ice sliver": "Dark Sliver of Leng",
    "frozen core": "Frozen core of Leng",
    # Dyes
    "ice dye": "Ice dye",
    "shadow dye": "Shadow dye",
    "blood dye": "Blood dye",
    "barrows dye": "Barrows dye",
    "third age dye": "Third Age dye",
    "3a dye": "Third Age dye",
    # Rares
    "phat": "Red partyhat",
    "red phat": "Red partyhat",
    "blue phat": "Blue partyhat",
    "green phat": "Green partyhat",
    "yellow phat": "Yellow partyhat",
    "purple phat": "Purple partyhat",
    "white phat": "White partyhat",
    "black phat": "Black partyhat",
    "santa": "Santa hat",
    "bsh": "Black Santa hat",
    "hween": "Green h'ween mask",
    "green hween": "Green h'ween mask",
    "red hween": "Red h'ween mask",
    "blue hween": "Blue h'ween mask",
    "christmas cracker": "Christmas cracker",
    "cracker": "Christmas cracker",
    # Arch-Glacor
    "nilas": "Dark nilas",
    "leng artefact": "Leng artefact",
    # Raksha
    "fleeting boots": "Fleeting Boots",
    "blast boots": "Blast Diffusion Boots",
    "laceration": "Laceration Boots",
    "shadow spike": "Shadow Spike",
    "grico codex": "Greater Ricochet ability codex",
    "gchain codex": "Greater Chain ability codex",
    "divert codex": "Divert ability codex",
    # Necromancy
    "omni guard": "Omni guard",
    "soulbound lantern": "Soulbound lantern",
    "death guard": "Death guard tier 90",
    "first necro": "First necromancer's robe top",
}

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

def create_embed(title, description=None, color=None, thumbnail=True, footer=True, timestamp=True):
    embed = discord.Embed(title=title, description=description, color=color or BOT_CONFIG["primary_color"])
    if thumbnail and BOT_CONFIG["logo_url"]: embed.set_thumbnail(url=BOT_CONFIG["logo_url"])
    if footer: embed.set_footer(text=BOT_CONFIG['clan_name'], icon_url=BOT_CONFIG["logo_url"] if BOT_CONFIG["logo_url"] else None)
    if timestamp: embed.timestamp = datetime.now(timezone.utc)
    return embed

def create_error_embed(msg): return create_embed("Error", msg, BOT_CONFIG["error_color"], thumbnail=False)
def create_success_embed(title, msg): return create_embed(title, msg, BOT_CONFIG["success_color"])
def format_number(num):
    if num >= 1_000_000_000: return f"{num/1_000_000_000:.2f}B"
    elif num >= 1_000_000: return f"{num/1_000_000:.2f}M"
    elif num >= 1_000: return f"{num/1_000:.1f}K"
    return f"{num:,}"
def get_xp_for_level(level): return XP_TABLE[level] if level <= 99 and level < len(XP_TABLE) else ELITE_XP.get(level, 0)
def get_progress_bar(current, total, length=10):
    if total == 0: return "░" * length
    filled = int(min(current/total, 1.0) * length)
    return "█" * filled + "░" * (length - filled)
def is_valuable_drop(text):
    t = text.lower()
    if not any(k in t for k in ["found", "received", "obtained", "got"]): return False
    if any(x.lower() in t for x in TRASH_DROPS): return False
    if any(x.lower() in t for x in VALUABLE_DROPS): return True
    return "pet" in t or "yay!" in t
def is_major_achievement(text):
    t = text.lower()
    if (" 99" in text or "99 " in text or " 120" in text or "120 " in text) and any(s.lower() in t for s in SKILLS): return True
    return "200m" in t or "maxed" in t or "completionist" in t or "max cape" in t
def get_game_time(): return datetime.now(timezone.utc).strftime("%H:%M")
def get_next_wildy_flash():
    now = datetime.now(timezone.utc)
    idx = now.hour % len(WILDERNESS_FLASH_EVENTS)
    mins = int(((now + timedelta(hours=1)).replace(minute=0, second=0, microsecond=0) - now).total_seconds() // 60)
    return {"current": WILDERNESS_FLASH_EVENTS[idx], "next": WILDERNESS_FLASH_EVENTS[(idx+1) % len(WILDERNESS_FLASH_EVENTS)], "minutes_left": mins}
def is_promotion(old, new): return RANK_HIERARCHY.get(new, 0) > RANK_HIERARCHY.get(old, 0)
def is_demotion(old, new): return RANK_HIERARCHY.get(new, 0) < RANK_HIERARCHY.get(old, 0)

async def init_db():
    async with aiosqlite.connect(DATABASE) as db:
        await db.execute("CREATE TABLE IF NOT EXISTS linked_accounts (id INTEGER PRIMARY KEY, discord_id INTEGER NOT NULL, rsn TEXT NOT NULL, linked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, is_primary BOOLEAN DEFAULT 0, UNIQUE(discord_id, rsn))")
        await db.execute("CREATE TABLE IF NOT EXISTS drop_log (id INTEGER PRIMARY KEY, discord_id INTEGER NOT NULL, rsn TEXT NOT NULL, item_name TEXT NOT NULL, boss_name TEXT, value INTEGER DEFAULT 0, timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")
        await db.execute("CREATE TABLE IF NOT EXISTS boss_kills (id INTEGER PRIMARY KEY, discord_id INTEGER NOT NULL, rsn TEXT NOT NULL, boss_name TEXT NOT NULL, kill_count INTEGER DEFAULT 0, personal_best TEXT, last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP, UNIQUE(discord_id, rsn, boss_name))")
        await db.execute("CREATE TABLE IF NOT EXISTS activity_tracking (rsn TEXT PRIMARY KEY, last_activity_text TEXT, last_activity_date TEXT, last_checked TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")
        await db.execute("CREATE TABLE IF NOT EXISTS guild_settings (guild_id INTEGER PRIMARY KEY, drops_channel INTEGER, achievements_channel INTEGER, events_channel INTEGER, welcome_channel INTEGER, welcome_message TEXT, world_events_channel INTEGER, schedule_channel INTEGER, clan_name TEXT, auto_role_sync BOOLEAN DEFAULT 0)")
        await db.execute("CREATE TABLE IF NOT EXISTS schedule_sessions (session_id TEXT PRIMARY KEY, guild_id INTEGER NOT NULL, started_by INTEGER NOT NULL, title TEXT DEFAULT 'Clan Events', started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, is_active BOOLEAN DEFAULT 1, week_start TEXT)")
        await db.execute("CREATE TABLE IF NOT EXISTS schedule_entries (id INTEGER PRIMARY KEY, session_id TEXT NOT NULL, event_name TEXT NOT NULL, host_rsn TEXT NOT NULL, event_day TEXT NOT NULL, game_time TEXT NOT NULL, category TEXT DEFAULT 'clan_events', world_number INTEGER, tags TEXT, added_by INTEGER NOT NULL, added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")
        await db.execute("CREATE TABLE IF NOT EXISTS clan_members (id INTEGER PRIMARY KEY, guild_id INTEGER NOT NULL, rsn TEXT NOT NULL, clan_rank TEXT NOT NULL, clan_xp INTEGER DEFAULT 0, kills INTEGER DEFAULT 0, first_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP, last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP, UNIQUE(guild_id, rsn))")
        await db.execute("CREATE TABLE IF NOT EXISTS rank_mappings (id INTEGER PRIMARY KEY, guild_id INTEGER NOT NULL, clan_rank TEXT NOT NULL, discord_role_id INTEGER NOT NULL, UNIQUE(guild_id, clan_rank))")
        await db.execute("CREATE TABLE IF NOT EXISTS name_changes (id INTEGER PRIMARY KEY, guild_id INTEGER NOT NULL, old_rsn TEXT NOT NULL, new_rsn TEXT NOT NULL, detected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")
        await db.execute("CREATE TABLE IF NOT EXISTS competitions (id INTEGER PRIMARY KEY AUTOINCREMENT, guild_id INTEGER, skill TEXT, title TEXT, start_time TEXT, end_time TEXT, created_by INTEGER, ended INTEGER DEFAULT 0)")
        await db.execute("CREATE TABLE IF NOT EXISTS competition_participants (id INTEGER PRIMARY KEY AUTOINCREMENT, competition_id INTEGER, rsn TEXT, start_xp INTEGER, current_xp INTEGER, UNIQUE(competition_id, rsn))")
        await db.commit()

async def fetch_runemetrics(rsn):
    async with aiohttp.ClientSession() as s:
        try:
            async with s.get(RUNEMETRICS_URL.format(rsn.replace(" ", "%20")), timeout=15) as r:
                if r.status == 200:
                    d = await r.json()
                    if "error" not in d: return d
        except: pass
    return None

async def fetch_hiscores(rsn):
    async with aiohttp.ClientSession() as s:
        try:
            async with s.get(HISCORES_URL.format(rsn.replace(" ", "%20")), timeout=15) as r:
                if r.status == 200:
                    lines = (await r.text()).strip().split("\n")
                    skills = {}
                    for i, line in enumerate(lines[:len(SKILLS)]):
                        parts = line.split(",")
                        if len(parts) >= 3: skills[SKILLS[i]] = {"rank": int(parts[0]), "level": int(parts[1]), "xp": int(parts[2])}
                    return skills
        except: pass
    return None

async def fetch_clan_members(clan_name):
    async with aiohttp.ClientSession() as s:
        try:
            async with s.get(CLAN_API_URL.format(clan_name.replace(" ", "%20")), timeout=30) as r:
                if r.status == 200:
                    # Use latin-1 encoding to handle special characters like 0xa0
                    raw_bytes = await r.read()
                    text = raw_bytes.decode('latin-1')
                    lines = text.strip().split("\n")
                    members = []
                    for line in lines[1:]:
                        parts = line.split(",")
                        if len(parts) >= 4:
                            # Replace non-breaking space and other special chars
                            rsn = parts[0].replace("\xa0", " ").replace("\u00a0", " ").strip()
                            members.append({"rsn": rsn, "rank": parts[1].strip(), "clan_xp": int(parts[2]) if parts[2].isdigit() else 0, "kills": int(parts[3]) if parts[3].isdigit() else 0})
                    return members
        except Exception as e: print(f"Clan API error: {e}")
    return None

async def fetch_vos():
    """Fetch current Voice of Seren from Weird Gloop API"""
    async with aiohttp.ClientSession() as s:
        try:
            async with s.get(VOS_API_URL, headers={"User-Agent": "RS3 Clan Bot"}, timeout=10) as r:
                if r.status == 200:
                    data = await r.json()
                    return data  # Returns dict with current VoS clans
        except Exception as e: print(f"VoS API error: {e}")
    return None

async def fetch_travelling_merchant():
    """Fetch current Travelling Merchant stock from Weird Gloop API"""
    async with aiohttp.ClientSession() as s:
        try:
            async with s.get(TMS_API_URL, headers={"User-Agent": "RS3 Clan Bot"}, timeout=10) as r:
                if r.status == 200:
                    data = await r.json()
                    return data  # Returns list of current stock items
        except Exception as e: print(f"TMS API error: {e}")
    return None

def get_warbands_times():
    """Get next Warbands times - occurs every 7 hours starting from 00:00 UTC"""
    now = datetime.now(timezone.utc)
    base = now.replace(hour=0, minute=0, second=0, microsecond=0)
    times = []
    for h in [0, 7, 14, 21]:
        t = base.replace(hour=h)
        if t < now:
            t += timedelta(days=1) if h == 0 else timedelta(hours=0)
        if t > now:
            times.append(t)
    # Sort and get next 2
    times.sort()
    next_wb = times[0] if times else base + timedelta(days=1)
    mins_until = int((next_wb - now).total_seconds() / 60)
    return {"next": next_wb.strftime("%H:%M UTC"), "minutes_until": mins_until, "camps": WARBANDS_CAMPS}

def get_cache_times():
    """Guthixian Cache occurs every hour at :00"""
    now = datetime.now(timezone.utc)
    next_cache = now.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
    mins_until = int((next_cache - now).total_seconds() / 60)
    return {"next": next_cache.strftime("%H:%M UTC"), "minutes_until": mins_until, "location": "Guthixian Cache (via Divination colonies)"}

def get_sinkhole_times():
    """Sinkholes occur every 30 minutes at :00 and :30"""
    now = datetime.now(timezone.utc)
    if now.minute < 30:
        next_sh = now.replace(minute=30, second=0, microsecond=0)
    else:
        next_sh = now.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
    mins_until = int((next_sh - now).total_seconds() / 60)
    return {"next": next_sh.strftime("%H:%M UTC"), "minutes_until": mins_until, "location": "Daemonheim (speak to Talsar)"}

def get_spotlight_game():
    """Get current Minigame Spotlight - rotates every 3 days"""
    epoch = datetime(2015, 9, 7, tzinfo=timezone.utc)  # Spotlight start date
    now = datetime.now(timezone.utc)
    days_since = (now - epoch).days
    index = (days_since // 3) % len(SPOTLIGHT_GAMES)
    days_remaining = 3 - (days_since % 3)
    return {"game": SPOTLIGHT_GAMES[index], "days_remaining": days_remaining}

async def fetch_wiki_price(item):
    async with aiohttp.ClientSession() as s:
        try:
            async with s.get(WIKI_PRICE_URL.format(item.replace(" ", "_")), headers={"User-Agent": "RS3 Bot"}, timeout=10) as r:
                if r.status == 200: return await r.json()
        except: pass
    return None

async def fetch_ely_price(item):
    async with aiohttp.ClientSession() as s:
        try:
            async with s.get(ELY_PRICE_URL.format(item.replace(" ", "%20")), headers={"User-Agent": "RS3 Bot"}, timeout=10) as r:
                if r.status == 200: return await r.json()
        except: pass
    return None

async def search_wiki_items(q):
    async with aiohttp.ClientSession() as s:
        try:
            async with s.get(WIKI_SEARCH_URL.format(q.replace(" ", "+")), headers={"User-Agent": "RS3 Bot"}, timeout=10) as r:
                if r.status == 200:
                    d = await r.json()
                    if len(d) >= 2: return d[1][:10]
        except: pass
    return None

async def get_linked_rsn(did):
    async with aiosqlite.connect(DATABASE) as db:
        c = await db.execute("SELECT rsn FROM linked_accounts WHERE discord_id = ? ORDER BY is_primary DESC LIMIT 1", (did,))
        r = await c.fetchone()
        return r[0] if r else None

async def get_discord_id_by_rsn(rsn):
    async with aiosqlite.connect(DATABASE) as db:
        c = await db.execute("SELECT discord_id FROM linked_accounts WHERE LOWER(rsn) = LOWER(?)", (rsn,))
        r = await c.fetchone()
        return r[0] if r else None

async def get_channel(gid, col):
    async with aiosqlite.connect(DATABASE) as db:
        c = await db.execute(f"SELECT {col} FROM guild_settings WHERE guild_id = ?", (gid,))
        r = await c.fetchone()
        return r[0] if r else None

async def get_drops_channel(gid): return await get_channel(gid, "drops_channel")
async def get_achievements_channel(gid): return await get_channel(gid, "achievements_channel")
async def get_world_events_channel(gid): return await get_channel(gid, "world_events_channel")
async def get_clan_name(gid): return await get_channel(gid, "clan_name")

async def is_auto_role_enabled(gid):
    async with aiosqlite.connect(DATABASE) as db:
        c = await db.execute("SELECT auto_role_sync FROM guild_settings WHERE guild_id = ?", (gid,))
        r = await c.fetchone()
        return bool(r[0]) if r else False

async def check_clan_changes(guild_id):
    """Check for clan membership changes and announce them."""
    clan_name = await get_clan_name(guild_id)
    if not clan_name: return
    
    current_members = await fetch_clan_members(clan_name)
    if not current_members: return
    
    async with aiosqlite.connect(DATABASE) as db:
        c = await db.execute("SELECT rsn, clan_rank, clan_xp FROM clan_members WHERE guild_id = ?", (guild_id,))
        stored = {r[0].lower(): {"rsn": r[0], "rank": r[1], "xp": r[2]} for r in await c.fetchall()}
        current_dict = {m["rsn"].lower(): m for m in current_members}
        
        new_members, left_members, promotions, demotions, name_changes = [], [], [], [], []
        
        for rsn_l, m in current_dict.items():
            if rsn_l not in stored:
                # Check for possible name change
                potential_old = None
                for old_rsn, old_data in stored.items():
                    if old_rsn not in current_dict and old_data["rank"] == m["rank"] and abs(old_data["xp"] - m["clan_xp"]) < 100000:
                        potential_old = old_data
                        break
                if potential_old:
                    name_changes.append({"old": potential_old["rsn"], "new": m["rsn"], "rank": m["rank"]})
                else:
                    new_members.append(m)
            else:
                old_rank, new_rank = stored[rsn_l]["rank"], m["rank"]
                if old_rank != new_rank:
                    if is_promotion(old_rank, new_rank):
                        promotions.append({"rsn": m["rsn"], "old": old_rank, "new": new_rank})
                    elif is_demotion(old_rank, new_rank):
                        demotions.append({"rsn": m["rsn"], "old": old_rank, "new": new_rank})
        
        for rsn_l, old in stored.items():
            if rsn_l not in current_dict and not any(nc["old"].lower() == rsn_l for nc in name_changes):
                left_members.append(old)
        
        # Update database
        for m in current_members:
            await db.execute("INSERT INTO clan_members (guild_id, rsn, clan_rank, clan_xp, kills, last_seen) VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP) ON CONFLICT(guild_id, rsn) DO UPDATE SET clan_rank=excluded.clan_rank, clan_xp=excluded.clan_xp, kills=excluded.kills, last_seen=CURRENT_TIMESTAMP", (guild_id, m["rsn"], m["rank"], m["clan_xp"], m["kills"]))
        for m in left_members:
            await db.execute("DELETE FROM clan_members WHERE guild_id = ? AND LOWER(rsn) = LOWER(?)", (guild_id, m["rsn"]))
        for nc in name_changes:
            await db.execute("INSERT INTO name_changes (guild_id, old_rsn, new_rsn) VALUES (?, ?, ?)", (guild_id, nc["old"], nc["new"]))
            await db.execute("UPDATE linked_accounts SET rsn = ? WHERE LOWER(rsn) = LOWER(?)", (nc["new"], nc["old"]))
        await db.commit()
    
    # Get channels - PUBLIC for joins/promos, PRIVATE for demotes/leaves
    public_channel = bot.get_channel(BOT_CONFIG["clan_public_channel"])
    private_channel = bot.get_channel(BOT_CONFIG["clan_private_channel"])
    
    guild = bot.get_guild(guild_id)
    auto_role = await is_auto_role_enabled(guild_id)
    
    # ===== PUBLIC CHANNEL: New joins =====
    if public_channel:
        for m in new_members:
            embed = create_embed("👋 New Clan Member!", f"**{m['rsn']}** has joined the clan!", BOT_CONFIG["success_color"])
            embed.add_field(name="Rank", value=m["rank"], inline=True)
            try: await public_channel.send(embed=embed)
            except: pass
            if auto_role and guild: await sync_member_role(guild, m["rsn"], m["rank"])
        
        # ===== PUBLIC CHANNEL: Promotions =====
        for p in promotions:
            embed = create_embed("⬆️ Promotion!", f"**{p['rsn']}** has been promoted!", BOT_CONFIG["gold_color"])
            embed.add_field(name="From", value=p["old"], inline=True)
            embed.add_field(name="To", value=p["new"], inline=True)
            try: await public_channel.send(embed=embed)
            except: pass
            if auto_role and guild: await sync_member_role(guild, p["rsn"], p["new"])
        
        # ===== PUBLIC CHANNEL: Name changes =====
        for nc in name_changes:
            embed = create_embed("📝 Name Change Detected", f"**{nc['old']}** → **{nc['new']}**", BOT_CONFIG["primary_color"])
            embed.add_field(name="Rank", value=nc["rank"], inline=True)
            try: await public_channel.send(embed=embed)
            except: pass
    
    # ===== PRIVATE CHANNEL: Members who left =====
    if private_channel:
        for m in left_members:
            embed = create_embed("🚪 Member Left", f"**{m['rsn']}** has left the clan.", BOT_CONFIG["error_color"])
            embed.add_field(name="Previous Rank", value=m["rank"], inline=True)
            try: await private_channel.send(embed=embed)
            except: pass
            if auto_role and guild: await remove_clan_roles(guild, m["rsn"])
        
        # ===== PRIVATE CHANNEL: Demotions =====
        for d in demotions:
            embed = create_embed("⬇️ Demotion", f"**{d['rsn']}** has been demoted.", BOT_CONFIG["warning_color"])
            embed.add_field(name="From", value=d["old"], inline=True)
            embed.add_field(name="To", value=d["new"], inline=True)
            try: await private_channel.send(embed=embed)
            except: pass
            if auto_role and guild: await sync_member_role(guild, d["rsn"], d["new"])

async def sync_member_role(guild, rsn, clan_rank):
    did = await get_discord_id_by_rsn(rsn)
    if not did: return
    member = guild.get_member(did)
    if not member: return
    async with aiosqlite.connect(DATABASE) as db:
        c = await db.execute("SELECT clan_rank, discord_role_id FROM rank_mappings WHERE guild_id = ?", (guild.id,))
        mappings = {r[0]: r[1] for r in await c.fetchall()}
    if not mappings: return
    roles_to_remove = [guild.get_role(rid) for rid in mappings.values() if guild.get_role(rid) in member.roles]
    new_role = guild.get_role(mappings.get(clan_rank)) if clan_rank in mappings else None
    try:
        if roles_to_remove: await member.remove_roles(*roles_to_remove, reason="Clan rank sync")
        if new_role: await member.add_roles(new_role, reason="Clan rank sync")
    except: pass

async def remove_clan_roles(guild, rsn):
    did = await get_discord_id_by_rsn(rsn)
    if not did: return
    member = guild.get_member(did)
    if not member: return
    async with aiosqlite.connect(DATABASE) as db:
        c = await db.execute("SELECT discord_role_id FROM rank_mappings WHERE guild_id = ?", (guild.id,))
        role_ids = [r[0] for r in await c.fetchall()]
    roles_to_remove = [guild.get_role(rid) for rid in role_ids if guild.get_role(rid) in member.roles]
    try:
        if roles_to_remove: await member.remove_roles(*roles_to_remove, reason="Left clan")
    except: pass

async def check_player_activities():
    # Get all clan members, not just linked accounts
    async with aiosqlite.connect(DATABASE) as db:
        c = await db.execute("SELECT rsn, guild_id FROM clan_members")
        clan_members = await c.fetchall()
    
    if not clan_members:
        return
    
    for rsn, guild_id in clan_members:
        try:
            data = await fetch_runemetrics(rsn)
            if not data or "activities" not in data: continue
            activities = data.get("activities", [])
            if not activities: continue
            latest = activities[0]
            lt, ld = latest.get("text", ""), latest.get("date", "")
            async with aiosqlite.connect(DATABASE) as db:
                c = await db.execute("SELECT last_activity_text, last_activity_date FROM activity_tracking WHERE rsn = ?", (rsn,))
                r = await c.fetchone()
                if r and r[0] == lt and r[1] == ld: continue
                await db.execute("INSERT INTO activity_tracking (rsn, last_activity_text, last_activity_date, last_checked) VALUES (?, ?, ?, CURRENT_TIMESTAMP) ON CONFLICT(rsn) DO UPDATE SET last_activity_text=excluded.last_activity_text, last_activity_date=excluded.last_activity_date, last_checked=CURRENT_TIMESTAMP", (rsn, lt, ld))
                await db.commit()
            if is_valuable_drop(lt): await announce_drop(rsn, guild_id, lt)
            elif is_major_achievement(lt): await announce_achievement(rsn, guild_id, lt)
        except Exception as e: print(f"Activity error {rsn}: {e}")
        await asyncio.sleep(1)

async def announce_drop(rsn, guild_id, text):
    embed = create_embed("💎 Rare Drop!", f"**{rsn}**\n\n{text}", BOT_CONFIG["gold_color"])
    
    # Try to extract item name and set thumbnail
    m = re.search(r"(?:received|found|obtained|got)\s+(?:a\s+|an\s+)?(.+?)(?:\s+from|\s+on|\s+at|\s*!|\s*\.|$)", text, re.IGNORECASE)
    if m:
        item_name = m.group(1).strip().rstrip('.,!')
        # Handle special characters for wiki URLs
        wiki_name = item_name.replace(' ', '_').replace("'", "%27").replace(",", "%2C")
        # Try detail.png first, common format for items
        embed.set_thumbnail(url=f"https://runescape.wiki/images/{wiki_name}_detail.png")
    
    # Send to the specific guild where this clan member belongs
    guild = bot.get_guild(guild_id)
    if guild:
        cid = await get_drops_channel(guild_id)
        if cid:
            ch = bot.get_channel(cid)
            if ch:
                try: await ch.send(embed=embed)
                except: pass

async def announce_achievement(rsn, guild_id, text):
    t = text.lower()
    title = "🎉 120 Achieved!" if "120" in text else "🎉 99 Achieved!" if "99" in text else "🎉 200M XP!" if "200m" in t else "🎉 MAXED!" if "maxed" in t else "🎉 Achievement!"
    embed = create_embed(title, f"**{rsn}**\n\n{text}", BOT_CONFIG["success_color"])
    for s in SKILLS:
        if s.lower() in t:
            embed.set_thumbnail(url=SKILL_ICONS.get(s, BOT_CONFIG["logo_url"]))
            break
    
    # Send to the specific guild where this clan member belongs
    guild = bot.get_guild(guild_id)
    if guild:
        cid = await get_achievements_channel(guild_id)
        if cid:
            ch = bot.get_channel(cid)
            if ch:
                try: await ch.send(embed=embed)
                except: pass

@bot.event
async def on_ready():
    await init_db()
    print(f"{'='*50}\n  {BOT_CONFIG['clan_name']} Bot Online!\n  {bot.user} | {len(bot.guilds)} servers\n{'='*50}")
    print(f"  Public clan channel: {BOT_CONFIG['clan_public_channel']}")
    print(f"  Private clan channel: {BOT_CONFIG['clan_private_channel']}")
    guild = discord.Object(id=GUILD_ID)
    await bot.tree.sync(guild=guild)
    print("Commands synced to guild")
    update_status.start()
    activity_monitor.start()
    wildy_flash_announcer.start()
    clan_monitor.start()
    competition_sync.start()
    try: synced = await bot.tree.sync(); print(f"Synced {len(synced)} commands")
    except Exception as e: print(f"Sync failed: {e}")

@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    """Global error handler for slash commands"""
    if isinstance(error, app_commands.CommandInvokeError):
        original = error.original
        # Ignore "Unknown interaction" errors - these happen when bot is slow
        if isinstance(original, discord.errors.NotFound) and original.code == 10062:
            print(f"[TIMEOUT] Command '{interaction.command.name}' took too long to respond")
            return
    
    # Log other errors
    print(f"[ERROR] Command '{interaction.command.name}': {error}")
    
    # Try to send error message to user
    try:
        if interaction.response.is_done():
            await interaction.followup.send(embed=create_error_embed("An error occurred. Please try again."), ephemeral=True)
        else:
            await interaction.response.send_message(embed=create_error_embed("An error occurred. Please try again."), ephemeral=True)
    except:
        pass

@tasks.loop(minutes=5)
async def update_status():
    await bot.change_presence(activity=random.choice([discord.Activity(type=discord.ActivityType.watching, name=BOT_CONFIG['clan_name']), discord.Activity(type=discord.ActivityType.playing, name="RuneScape 3"), discord.Activity(type=discord.ActivityType.listening, name="/help"), discord.Activity(type=discord.ActivityType.listening, name="Made by Oogle :)")]))

@tasks.loop(minutes=3)
async def activity_monitor():
    try: await check_player_activities()
    except Exception as e: print(f"Activity monitor error: {e}")

@activity_monitor.before_loop
async def before_am(): await bot.wait_until_ready()

@tasks.loop(minutes=5)
async def clan_monitor():
    for g in bot.guilds:
        try: await check_clan_changes(g.id)
        except Exception as e: print(f"Clan monitor error {g.name}: {e}")
        await asyncio.sleep(2)

@clan_monitor.before_loop
async def before_cm(): await bot.wait_until_ready()

@tasks.loop(minutes=30)
async def competition_sync():
    """Auto-sync active competitions with clan roster"""
    for g in bot.guilds:
        try:
            comp = await get_competition(g.id)
            if not comp:
                continue
            
            comp_id, skill, title, start_time, end_time, created_by = comp
            
            # Get clan members
            async with aiosqlite.connect(DATABASE) as db:
                cursor = await db.execute("SELECT rsn FROM clan_members WHERE guild_id = ?", (g.id,))
                members = await cursor.fetchall()
            
            if not members:
                continue
            
            clan_rsns = {rsn for (rsn,) in members}
            
            # Get existing participants
            async with aiosqlite.connect(DATABASE) as db:
                cursor = await db.execute(
                    "SELECT rsn FROM competition_participants WHERE competition_id = ?",
                    (comp_id,)
                )
                existing = {row[0] for row in await cursor.fetchall()}
            
            # Find new members
            new_members = list(clan_rsns - existing)
            
            if new_members:
                print(f"Competition sync: Adding {len(new_members)} new members to {title}")
                xp_data = await fetch_skill_xp_batch(new_members, skill, batch_size=10)
                
                async with aiosqlite.connect(DATABASE) as db:
                    for rsn, xp in xp_data.items():
                        if xp is not None:
                            await db.execute(
                                "INSERT OR IGNORE INTO competition_participants (competition_id, rsn, start_xp, current_xp) VALUES (?, ?, ?, ?)",
                                (comp_id, rsn, xp, xp)
                            )
                    await db.commit()
        except Exception as e:
            print(f"Competition sync error {g.name}: {e}")
        await asyncio.sleep(2)

@competition_sync.before_loop
async def before_cs(): await bot.wait_until_ready()

@tasks.loop(minutes=1)
async def wildy_flash_announcer():
    if datetime.now(timezone.utc).minute == 0:
        flash = get_next_wildy_flash()
        embed = create_embed(f"{flash['current']['icon']} Wilderness Flash Event", f"**{flash['current']['name']}** is now active!", 0xFF4500)
        embed.add_field(name="Type", value=flash['current']['type'].title(), inline=True)
        embed.add_field(name="Duration", value="1 Hour", inline=True)
        for g in bot.guilds:
            cid = await get_world_events_channel(g.id)
            if cid:
                ch = bot.get_channel(cid)
                if ch:
                    try: await ch.send(embed=embed)
                    except: pass

@wildy_flash_announcer.before_loop
async def before_wf(): await bot.wait_until_ready()

# ==================== WELCOME SYSTEM ====================
WELCOME_CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "welcome_config.json")

DEFAULT_WELCOME_CONFIG = {
    "enabled": True,
    "ping_user": True,
    "ping_role": None,  # Role ID to ping (e.g., Welcoming Committee)
    "title": "Welcome to Statuesque! 🎉",
    "description": "We're glad you're here!",
    "color": "2ECC71",  # Hex color without #
    "fields": [
        {"name": "📋 Getting Started", "value": "• Please let us know if you will be guesting or joining our clan.\n• Tell us your RSN here: <#CHANNEL_ID>\n• Introduce yourself here: <#CHANNEL_ID>", "inline": False},
        {"name": "🎭 Roles & Info", "value": "• Self-Assign Roles here: <#CHANNEL_ID>\n• Current Event Schedule here: <#CHANNEL_ID>", "inline": False},
        {"name": "🤖 Bot Commands", "value": "• Use the `/help` command from our bot to see all available options.\n• Link your RSN with `/link YourRSN`", "inline": False}
    ],
    "footer": {"text": "We're glad you're here!", "icon": True},
    "thumbnail": "user",  # "user" for user avatar, "server" for server icon, or a URL
    "image": None  # Optional large image URL
}

def get_welcome_config(guild_id: int) -> dict:
    """Load welcome config for a guild from JSON file"""
    try:
        with open(WELCOME_CONFIG_FILE, "r", encoding="utf-8") as f:
            configs = json.load(f)
            return configs.get(str(guild_id), DEFAULT_WELCOME_CONFIG.copy())
    except (FileNotFoundError, json.JSONDecodeError):
        return DEFAULT_WELCOME_CONFIG.copy()

def save_welcome_config(guild_id: int, config: dict):
    """Save welcome config for a guild to JSON file"""
    try:
        with open(WELCOME_CONFIG_FILE, "r", encoding="utf-8") as f:
            configs = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        configs = {}
    
    configs[str(guild_id)] = config
    
    with open(WELCOME_CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(configs, f, indent=2, ensure_ascii=False)

def init_welcome_config(guild_id: int):
    """Initialize welcome config for a guild if it doesn't exist"""
    try:
        with open(WELCOME_CONFIG_FILE, "r", encoding="utf-8") as f:
            configs = json.load(f)
            if str(guild_id) not in configs:
                configs[str(guild_id)] = DEFAULT_WELCOME_CONFIG.copy()
                with open(WELCOME_CONFIG_FILE, "w", encoding="utf-8") as f2:
                    json.dump(configs, f2, indent=2, ensure_ascii=False)
    except (FileNotFoundError, json.JSONDecodeError):
        configs = {str(guild_id): DEFAULT_WELCOME_CONFIG.copy()}
        with open(WELCOME_CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(configs, f, indent=2, ensure_ascii=False)

@bot.event
async def on_member_join(member):
    async with aiosqlite.connect(DATABASE) as db:
        c = await db.execute("SELECT welcome_channel FROM guild_settings WHERE guild_id = ?", (member.guild.id,))
        r = await c.fetchone()
    
    if not r or not r[0]:
        return
    
    ch = bot.get_channel(r[0])
    if not ch:
        return
    
    config = get_welcome_config(member.guild.id)
    
    if not config.get("enabled", True):
        return
    
    # Build the ping message
    ping_parts = []
    if config.get("ping_user", True):
        ping_parts.append(member.mention)
    if config.get("ping_role"):
        ping_parts.append(f"<@&{config['ping_role']}>")
    
    ping_message = " ".join(ping_parts) if ping_parts else None
    
    # Build the embed
    try:
        color = int(config.get("color", "2ECC71"), 16)
    except:
        color = BOT_CONFIG["success_color"]
    
    title = config.get("title", "Welcome!").replace("{user}", member.display_name).replace("{server}", member.guild.name)
    description = config.get("description", "").replace("{user}", member.mention).replace("{server}", member.guild.name)
    
    embed = discord.Embed(title=title, description=description, color=color)
    
    # Add fields
    for field in config.get("fields", []):
        name = field.get("name", "Info")
        value = field.get("value", "").replace("{user}", member.mention).replace("{server}", member.guild.name)
        inline = field.get("inline", False)
        embed.add_field(name=name, value=value, inline=inline)
    
    # Thumbnail
    thumbnail = config.get("thumbnail", "user")
    if thumbnail == "user":
        embed.set_thumbnail(url=member.display_avatar.url)
    elif thumbnail == "server" and member.guild.icon:
        embed.set_thumbnail(url=member.guild.icon.url)
    elif thumbnail and thumbnail.startswith("http"):
        embed.set_thumbnail(url=thumbnail)
    
    # Image
    if config.get("image"):
        embed.set_image(url=config["image"])
    
    # Footer
    footer_config = config.get("footer", {})
    if footer_config:
        footer_text = footer_config.get("text", "").replace("{user}", member.display_name).replace("{server}", member.guild.name)
        if footer_config.get("icon") and member.guild.icon:
            embed.set_footer(text=footer_text, icon_url=member.guild.icon.url)
        else:
            embed.set_footer(text=footer_text)
    
    # Send the message
    if ping_message:
        await ch.send(content=ping_message, embed=embed)
    else:
        await ch.send(embed=embed)

@bot.tree.command(name="help", description="View all commands")
async def help_cmd(i: discord.Interaction):
    embed = create_embed("Commands", f"**{BOT_CONFIG['clan_name']}** Bot")
    embed.add_field(name="Account", value="`/link` `/unlink` `/accounts` `/setprimary`", inline=False)
    embed.add_field(name="Stats", value="`/stats` `/skill` `/compare`", inline=False)
    embed.add_field(name="Boss & Drops", value="`/drop` `/drops` `/kc` `/bosslog` `/bossboard`", inline=False)
    embed.add_field(name="Schedule", value="`/schedule start/add/view/remove/generate/cancel`", inline=False)
    embed.add_field(name="Competition", value="`/compstart` `/compleaderboard` `/compinfo` `/compend`", inline=False)
    embed.add_field(name="Clan Tracking", value="`/setclan` `/clanlist` `/maprank` `/rankmaps` `/syncme` `/toggleautorole`", inline=False)
    embed.add_field(name="World Events", value="`/wildyflash` `/gametime` `/event`", inline=False)
    embed.add_field(name="Other", value="`/price` `/leaderboard` `/claninfo`", inline=False)
    embed.add_field(name="Admin", value="`/setchannel` `/welcome init/preview/toggle/title/...`", inline=False)
    await i.response.send_message(embed=embed)

@bot.tree.command(name="claninfo", description="View clan information")
async def claninfo(i: discord.Interaction):
    async with aiosqlite.connect(DATABASE) as db:
        c = await db.execute("SELECT COUNT(DISTINCT discord_id) FROM linked_accounts"); mem = (await c.fetchone())[0]
        c = await db.execute("SELECT COUNT(*) FROM drop_log"); drops = (await c.fetchone())[0]
        c = await db.execute("SELECT SUM(kill_count) FROM boss_kills"); kc = (await c.fetchone())[0] or 0
        c = await db.execute("SELECT COUNT(*) FROM clan_members WHERE guild_id = ?", (i.guild.id,)); clan = (await c.fetchone())[0]
    embed = create_embed(BOT_CONFIG['clan_name'], f"*{BOT_CONFIG['clan_motto']}*")
    embed.add_field(name="Discord Linked", value=str(mem), inline=True)
    embed.add_field(name="Clan Members", value=str(clan), inline=True)
    embed.add_field(name="Drops Logged", value=format_number(drops), inline=True)
    embed.add_field(name="Total KC", value=format_number(kc), inline=True)
    await i.response.send_message(embed=embed)

@bot.tree.command(name="link", description="Link RS account")
@app_commands.describe(rsn="Your RuneScape username")
async def link(i: discord.Interaction, rsn: str):
    await i.response.defer()
    data = await fetch_runemetrics(rsn)
    if not data: await i.followup.send(embed=create_error_embed(f"Could not find **{rsn}**"), ephemeral=True); return
    name = data.get("name", rsn)
    async with aiosqlite.connect(DATABASE) as db:
        c = await db.execute("SELECT COUNT(*) FROM linked_accounts WHERE discord_id = ?", (i.user.id,))
        first = (await c.fetchone())[0] == 0
        try:
            await db.execute("INSERT INTO linked_accounts (discord_id, rsn, is_primary) VALUES (?, ?, ?)", (i.user.id, name, first))
            await db.commit()
            embed = create_success_embed("Linked!", f"**{name}** linked!")
            embed.add_field(name="Stats", value=f"Level: **{data.get('totalskill', 'N/A')}** | Combat: **{data.get('combatlevel', 'N/A')}**", inline=False)
            await i.followup.send(embed=embed)
            if await is_auto_role_enabled(i.guild.id):
                async with aiosqlite.connect(DATABASE) as db:
                    c = await db.execute("SELECT clan_rank FROM clan_members WHERE guild_id = ? AND LOWER(rsn) = LOWER(?)", (i.guild.id, name))
                    r = await c.fetchone()
                    if r: await sync_member_role(i.guild, name, r[0])
        except: await i.followup.send(embed=create_embed("Already Linked", f"**{name}** already linked.", BOT_CONFIG["warning_color"]), ephemeral=True)

@bot.tree.command(name="unlink", description="Unlink RS account")
@app_commands.describe(rsn="RSN to unlink")
async def unlink(i: discord.Interaction, rsn: str):
    async with aiosqlite.connect(DATABASE) as db:
        c = await db.execute("DELETE FROM linked_accounts WHERE discord_id = ? AND LOWER(rsn) = LOWER(?)", (i.user.id, rsn))
        await db.commit()
        if c.rowcount > 0: await i.response.send_message(embed=create_success_embed("Unlinked", f"**{rsn}** unlinked."))
        else: await i.response.send_message(embed=create_error_embed(f"**{rsn}** not linked."), ephemeral=True)

@bot.tree.command(name="accounts", description="View linked accounts")
async def accounts(i: discord.Interaction):
    async with aiosqlite.connect(DATABASE) as db:
        c = await db.execute("SELECT rsn, is_primary FROM linked_accounts WHERE discord_id = ? ORDER BY is_primary DESC", (i.user.id,))
        rows = await c.fetchall()
    if not rows: await i.response.send_message(embed=create_embed("No Accounts", "Use `/link`", BOT_CONFIG["warning_color"]), ephemeral=True); return
    embed = create_embed("Your Accounts", f"{len(rows)} linked")
    for rsn, prim in rows: embed.add_field(name=rsn, value="⭐ Primary" if prim else "Linked", inline=True)
    await i.response.send_message(embed=embed)

@bot.tree.command(name="setprimary", description="Set primary account")
@app_commands.describe(rsn="RSN to set primary")
async def setprimary(i: discord.Interaction, rsn: str):
    async with aiosqlite.connect(DATABASE) as db:
        c = await db.execute("SELECT id FROM linked_accounts WHERE discord_id = ? AND LOWER(rsn) = LOWER(?)", (i.user.id, rsn))
        if not await c.fetchone(): await i.response.send_message(embed=create_error_embed(f"**{rsn}** not linked."), ephemeral=True); return
        await db.execute("UPDATE linked_accounts SET is_primary = 0 WHERE discord_id = ?", (i.user.id,))
        await db.execute("UPDATE linked_accounts SET is_primary = 1 WHERE discord_id = ? AND LOWER(rsn) = LOWER(?)", (i.user.id, rsn))
        await db.commit()
    await i.response.send_message(embed=create_success_embed("Primary Set", f"**{rsn}** is now primary!"))

@bot.tree.command(name="stats", description="Player stats")
@app_commands.describe(rsn="RSN (optional)")
async def stats(i: discord.Interaction, rsn: Optional[str] = None):
    await i.response.defer()
    if not rsn: rsn = await get_linked_rsn(i.user.id)
    if not rsn: await i.followup.send(embed=create_error_embed("Provide RSN or link"), ephemeral=True); return
    rm, hs = await fetch_runemetrics(rsn), await fetch_hiscores(rsn)
    if not rm and not hs: await i.followup.send(embed=create_error_embed(f"Could not find **{rsn}**"), ephemeral=True); return
    name = rm.get("name", rsn) if rm else rsn
    embed = discord.Embed(title=f"📊 {name}", url=f"https://apps.runescape.com/runemetrics/app/overview/player/{name.replace(' ', '%20')}", color=BOT_CONFIG["primary_color"])
    embed.set_thumbnail(url=SKILL_ICONS["Overall"])
    if rm:
        embed.add_field(name="Overview", value=f"```\nTotal Level   │ {rm.get('totalskill', 0):,}/3,060\nCombat Level  │ {rm.get('combatlevel', 0)}\nTotal XP      │ {format_number(rm.get('totalxp', 0))}\n```", inline=False)
    if hs:
        for cat, skills in [("⚔️ Combat", ["Attack", "Strength", "Defence", "Constitution", "Ranged", "Prayer", "Magic", "Summoning", "Necromancy"]), ("🌿 Gathering", ["Mining", "Fishing", "Woodcutting", "Farming", "Hunter", "Archaeology", "Divination"]), ("🔨 Artisan", ["Herblore", "Crafting", "Fletching", "Smithing", "Cooking", "Firemaking", "Runecrafting"]), ("🎯 Support", ["Agility", "Thieving", "Slayer", "Dungeoneering", "Construction", "Invention"])]:
            lines = [f"{s:<12} {hs[s]['level']:>3}" for s in skills if s in hs]
            if lines: embed.add_field(name=cat, value="```\n" + "\n".join(lines) + "\n```", inline=True)
    embed.set_footer(text=BOT_CONFIG['clan_name'], icon_url=BOT_CONFIG["logo_url"])
    embed.timestamp = datetime.now(timezone.utc)
    await i.followup.send(embed=embed)

async def skill_ac(i, c): return [app_commands.Choice(name=s, value=s) for s in ([s for s in SKILLS[1:] if c.lower() in s.lower()] if c else SKILLS[1:])[:25]]

@bot.tree.command(name="skill", description="Skill info")
@app_commands.describe(skill="Skill", rsn="RSN (optional)")
@app_commands.autocomplete(skill=skill_ac)
async def skill(i: discord.Interaction, skill: str, rsn: Optional[str] = None):
    await i.response.defer()
    if not rsn: rsn = await get_linked_rsn(i.user.id)
    if not rsn: await i.followup.send(embed=create_error_embed("Provide RSN or link"), ephemeral=True); return
    hs = await fetch_hiscores(rsn)
    if not hs or skill not in hs: await i.followup.send(embed=create_error_embed(f"No {skill} data for **{rsn}**"), ephemeral=True); return
    d = hs[skill]
    embed = discord.Embed(title=f"{skill} - {rsn}", color=BOT_CONFIG["primary_color"])
    embed.set_thumbnail(url=SKILL_ICONS.get(skill, SKILL_ICONS["Overall"]))
    embed.add_field(name="Stats", value=f"**Level:** {d['level']}\n**XP:** {format_number(d['xp'])}\n**Rank:** {d['rank']:,}", inline=True)
    if d['level'] < 99:
        goal = get_xp_for_level(99)
        embed.add_field(name="To 99", value=f"{get_progress_bar(d['xp'], goal, 12)}\n**{format_number(max(0, goal-d['xp']))}** XP", inline=True)
    elif d['level'] < 120:
        goal = ELITE_XP[120]
        embed.add_field(name="To 120", value=f"{get_progress_bar(d['xp'], goal, 12)}\n**{format_number(max(0, goal-d['xp']))}** XP", inline=True)
    await i.followup.send(embed=embed)

@bot.tree.command(name="compare", description="Compare two players")
@app_commands.describe(rsn1="First player", rsn2="Second player")
async def compare(i: discord.Interaction, rsn1: str, rsn2: str):
    await i.response.defer()
    d1, d2 = await asyncio.gather(fetch_runemetrics(rsn1), fetch_runemetrics(rsn2))
    if not d1 or not d2: await i.followup.send(embed=create_error_embed("Could not find one or both players"), ephemeral=True); return
    embed = create_embed(f"{d1['name']} vs {d2['name']}")
    s1, s2 = 0, 0
    for label, key in [("Total XP", "totalxp"), ("Level", "totalskill"), ("Combat", "combatlevel"), ("Quests", "questscomplete")]:
        v1, v2 = d1.get(key, 0), d2.get(key, 0)
        if v1 > v2: s1 += 1
        elif v2 > v1: s2 += 1
        embed.add_field(name=label, value=f"{format_number(v1) if key=='totalxp' else f'{v1:,}'}\nvs\n{format_number(v2) if key=='totalxp' else f'{v2:,}'}", inline=True)
    embed.add_field(name="Result", value=f"**{d1['name']}** wins!" if s1 > s2 else f"**{d2['name']}** wins!" if s2 > s1 else "Tie!", inline=False)
    await i.followup.send(embed=embed)

@bot.tree.command(name="drop", description="Log a drop")
@app_commands.describe(item="Item", boss="Boss (optional)", value="GP value (optional)")
async def drop(i: discord.Interaction, item: str, boss: Optional[str] = None, value: Optional[int] = None):
    rsn = await get_linked_rsn(i.user.id)
    if not rsn: await i.response.send_message(embed=create_error_embed("Link an account first"), ephemeral=True); return
    async with aiosqlite.connect(DATABASE) as db:
        await db.execute("INSERT INTO drop_log (discord_id, rsn, item_name, boss_name, value) VALUES (?, ?, ?, ?, ?)", (i.user.id, rsn, item, boss, value or 0))
        await db.commit()
    embed = create_embed("Rare Drop!", f"**{rsn}** received **{item}**!", BOT_CONFIG["gold_color"])
    embed.set_thumbnail(url=f"https://runescape.wiki/images/{item.replace(' ', '_')}_detail.png")
    if boss: embed.add_field(name="Boss", value=boss, inline=True)
    if value: embed.add_field(name="Value", value=f"{format_number(value)} GP", inline=True)
    await i.response.send_message(embed=embed)

@bot.tree.command(name="drops", description="View drops")
@app_commands.describe(rsn="Filter by RSN (optional)")
async def drops(i: discord.Interaction, rsn: Optional[str] = None):
    async with aiosqlite.connect(DATABASE) as db:
        if rsn: c = await db.execute("SELECT rsn, item_name, boss_name, value FROM drop_log WHERE LOWER(rsn) = LOWER(?) ORDER BY timestamp DESC LIMIT 15", (rsn,))
        else: c = await db.execute("SELECT rsn, item_name, boss_name, value FROM drop_log ORDER BY timestamp DESC LIMIT 15")
        rows = await c.fetchall()
    if not rows: await i.response.send_message(embed=create_embed("No Drops", "Use `/drop`", BOT_CONFIG["warning_color"]), ephemeral=True); return
    embed = create_embed(f"Recent Drops{f' - {rsn}' if rsn else ''}")
    for r, item, boss, val in rows: embed.add_field(name=item, value=f"**{r}**" + (f" ({boss})" if boss else "") + (f" • {format_number(val)} GP" if val else ""), inline=True)
    await i.response.send_message(embed=embed)

async def boss_ac(i, c): return [app_commands.Choice(name=b, value=b) for b in ([b for b in BOSSES if c.lower() in b.lower()] if c else BOSSES)[:25]]

@bot.tree.command(name="kc", description="Update boss KC")
@app_commands.describe(boss="Boss", count="Kill count", pb="Personal best (optional)")
@app_commands.autocomplete(boss=boss_ac)
async def kc(i: discord.Interaction, boss: str, count: int, pb: Optional[str] = None):
    rsn = await get_linked_rsn(i.user.id)
    if not rsn: await i.response.send_message(embed=create_error_embed("Link an account first"), ephemeral=True); return
    async with aiosqlite.connect(DATABASE) as db:
        await db.execute("INSERT INTO boss_kills (discord_id, rsn, boss_name, kill_count, personal_best) VALUES (?, ?, ?, ?, ?) ON CONFLICT(discord_id, rsn, boss_name) DO UPDATE SET kill_count=excluded.kill_count, personal_best=COALESCE(excluded.personal_best, boss_kills.personal_best), last_updated=CURRENT_TIMESTAMP", (i.user.id, rsn, boss, count, pb))
        await db.commit()
    await i.response.send_message(embed=create_success_embed("KC Updated", f"**{rsn}** - {boss}\n\nKC: **{count:,}**" + (f"\nPB: **{pb}**" if pb else "")))

@bot.tree.command(name="bosslog", description="View boss KC")
@app_commands.describe(rsn="RSN (optional)")
async def bosslog(i: discord.Interaction, rsn: Optional[str] = None):
    if not rsn: rsn = await get_linked_rsn(i.user.id)
    if not rsn: await i.response.send_message(embed=create_error_embed("Provide RSN or link"), ephemeral=True); return
    async with aiosqlite.connect(DATABASE) as db:
        c = await db.execute("SELECT boss_name, kill_count, personal_best FROM boss_kills WHERE LOWER(rsn) = LOWER(?) ORDER BY kill_count DESC", (rsn,))
        rows = await c.fetchall()
    if not rows: await i.response.send_message(embed=create_embed(f"Boss Log - {rsn}", "No kills. Use `/kc`", BOT_CONFIG["warning_color"])); return
    embed = create_embed(f"Boss Log - {rsn}", f"Total KC: **{sum(r[1] for r in rows):,}**")
    for boss, kc, pb in rows[:12]: embed.add_field(name=boss, value=f"**{kc:,}**" + (f" (PB: {pb})" if pb else ""), inline=True)
    await i.response.send_message(embed=embed)

@bot.tree.command(name="bossboard", description="Boss leaderboard")
@app_commands.describe(boss="Boss")
@app_commands.autocomplete(boss=boss_ac)
async def bossboard(i: discord.Interaction, boss: str):
    await i.response.defer()
    async with aiosqlite.connect(DATABASE) as db:
        c = await db.execute("SELECT rsn, kill_count, personal_best FROM boss_kills WHERE boss_name = ? ORDER BY kill_count DESC LIMIT 10", (boss,))
        rows = await c.fetchall()
    if not rows: await i.followup.send(embed=create_embed(f"{boss} Leaderboard", "No kills logged!", BOT_CONFIG["warning_color"])); return
    medals = ["🥇", "🥈", "🥉"]
    board = "\n".join([f"{medals[j] if j < 3 else f'**{j+1}.**'} **{r}** - {k:,} KC" + (f" *(PB: {p})*" if p else "") for j, (r, k, p) in enumerate(rows)])
    await i.followup.send(embed=create_embed(f"{boss} Leaderboard", board))

@bot.tree.command(name="leaderboard", description="Clan XP leaderboard")
async def leaderboard(i: discord.Interaction):
    await i.response.defer()
    async with aiosqlite.connect(DATABASE) as db:
        c = await db.execute("SELECT DISTINCT rsn FROM linked_accounts")
        accs = await c.fetchall()
    if not accs: await i.followup.send(embed=create_embed("Leaderboard", "No accounts linked!", BOT_CONFIG["warning_color"])); return
    players = []
    for (rsn,) in accs:
        d = await fetch_runemetrics(rsn)
        if d: players.append({"name": d.get("name", rsn), "xp": d.get("totalxp", 0), "level": d.get("totalskill", 0)})
    players.sort(key=lambda x: x["xp"], reverse=True)
    medals = ["🥇", "🥈", "🥉"]
    board = "\n".join([f"{medals[j] if j < 3 else f'**{j+1}.**'} **{p['name']}**\n    {format_number(p['xp'])} XP • Level {p['level']}" for j, p in enumerate(players[:10])])
    await i.followup.send(embed=create_embed(f"{BOT_CONFIG['clan_name']} Leaderboard", board or "No data"))

@bot.tree.command(name="setclan", description="Set RS3 clan to track (Admin)")
@app_commands.describe(clan_name="Exact clan name")
@app_commands.default_permissions(administrator=True)
async def setclan(i: discord.Interaction, clan_name: str):
    await i.response.defer()
    members = await fetch_clan_members(clan_name)
    if not members: await i.followup.send(embed=create_error_embed(f"Could not find clan **{clan_name}**"), ephemeral=True); return
    async with aiosqlite.connect(DATABASE) as db:
        await db.execute("INSERT INTO guild_settings (guild_id, clan_name) VALUES (?, ?) ON CONFLICT(guild_id) DO UPDATE SET clan_name=excluded.clan_name", (i.guild.id, clan_name))
        for m in members:
            await db.execute("INSERT INTO clan_members (guild_id, rsn, clan_rank, clan_xp, kills) VALUES (?, ?, ?, ?, ?) ON CONFLICT(guild_id, rsn) DO UPDATE SET clan_rank=excluded.clan_rank, clan_xp=excluded.clan_xp, kills=excluded.kills, last_seen=CURRENT_TIMESTAMP", (i.guild.id, m["rsn"], m["rank"], m["clan_xp"], m["kills"]))
        await db.commit()
    embed = create_success_embed("Clan Set!", f"Tracking **{clan_name}**\n\n**{len(members)}** members found.")
    embed.add_field(name="Channels", value=f"Public (joins/promos): <#{BOT_CONFIG['clan_public_channel']}>\nPrivate (leaves/demotes): <#{BOT_CONFIG['clan_private_channel']}>", inline=False)
    await i.followup.send(embed=embed)

@bot.tree.command(name="clanlist", description="View clan members")
async def clanlist(i: discord.Interaction):
    await i.response.defer()
    async with aiosqlite.connect(DATABASE) as db:
        c = await db.execute("SELECT clan_name FROM guild_settings WHERE guild_id = ?", (i.guild.id,))
        r = await c.fetchone()
        if not r or not r[0]: await i.followup.send(embed=create_error_embed("No clan set. Use `/setclan`"), ephemeral=True); return
        clan_name = r[0]
        c = await db.execute("SELECT rsn, clan_rank FROM clan_members WHERE guild_id = ? ORDER BY rsn", (i.guild.id,))
        members = await c.fetchall()
    if not members: await i.followup.send(embed=create_error_embed("No members found."), ephemeral=True); return
    by_rank = {}
    for rsn, rank in members:
        if rank not in by_rank: by_rank[rank] = []
        by_rank[rank].append(rsn)
    embed = create_embed(clan_name, f"**{len(members)}** members")
    for rank in CLAN_RANKS:
        if rank in by_rank:
            names = by_rank[rank][:10]
            extra = f" (+{len(by_rank[rank])-10})" if len(by_rank[rank]) > 10 else ""
            embed.add_field(name=f"{rank} ({len(by_rank[rank])})", value=", ".join(names) + extra, inline=False)
    await i.followup.send(embed=embed)

async def rank_ac(i, c): return [app_commands.Choice(name=r, value=r) for r in ([r for r in CLAN_RANKS if c.lower() in r.lower()] if c else CLAN_RANKS)[:25]]

@bot.tree.command(name="maprank", description="Map clan rank to Discord role (Admin)")
@app_commands.describe(clan_rank="RS3 clan rank", discord_role="Discord role")
@app_commands.autocomplete(clan_rank=rank_ac)
@app_commands.default_permissions(administrator=True)
async def maprank(i: discord.Interaction, clan_rank: str, discord_role: discord.Role):
    if clan_rank not in CLAN_RANKS: await i.response.send_message(embed=create_error_embed(f"Invalid rank. Valid: {', '.join(CLAN_RANKS)}"), ephemeral=True); return
    async with aiosqlite.connect(DATABASE) as db:
        await db.execute("INSERT INTO rank_mappings (guild_id, clan_rank, discord_role_id) VALUES (?, ?, ?) ON CONFLICT(guild_id, clan_rank) DO UPDATE SET discord_role_id=excluded.discord_role_id", (i.guild.id, clan_rank, discord_role.id))
        await db.commit()
    await i.response.send_message(embed=create_success_embed("Rank Mapped!", f"**{clan_rank}** → {discord_role.mention}"))

@bot.tree.command(name="rankmaps", description="View rank mappings")
async def rankmaps(i: discord.Interaction):
    async with aiosqlite.connect(DATABASE) as db:
        c = await db.execute("SELECT clan_rank, discord_role_id FROM rank_mappings WHERE guild_id = ?", (i.guild.id,))
        rows = await c.fetchall()
    if not rows: await i.response.send_message(embed=create_embed("No Rank Mappings", "Use `/maprank`", BOT_CONFIG["warning_color"]), ephemeral=True); return
    embed = create_embed("Rank → Role Mappings")
    for rank, rid in rows:
        role = i.guild.get_role(rid)
        embed.add_field(name=rank, value=role.mention if role else f"*Deleted ({rid})*", inline=True)
    await i.response.send_message(embed=embed)

@bot.tree.command(name="toggleautorole", description="Toggle auto role sync (Admin)")
@app_commands.default_permissions(administrator=True)
async def toggleautorole(i: discord.Interaction):
    async with aiosqlite.connect(DATABASE) as db:
        c = await db.execute("SELECT auto_role_sync FROM guild_settings WHERE guild_id = ?", (i.guild.id,))
        r = await c.fetchone()
        new_val = not (bool(r[0]) if r else False)
        await db.execute("INSERT INTO guild_settings (guild_id, auto_role_sync) VALUES (?, ?) ON CONFLICT(guild_id) DO UPDATE SET auto_role_sync=excluded.auto_role_sync", (i.guild.id, new_val))
        await db.commit()
    await i.response.send_message(embed=create_success_embed("Auto Role Sync", f"Now **{'enabled' if new_val else 'disabled'}**.\n\nWhen enabled, Discord roles auto-update with clan rank changes."))

@bot.tree.command(name="checkautorole", description="Check auto role sync status")
@app_commands.default_permissions(administrator=True)
async def checkautorole(i: discord.Interaction):
    enabled = await is_auto_role_enabled(i.guild.id)
    status = "✅ **Enabled**" if enabled else "❌ **Disabled**"
    await i.response.send_message(embed=create_embed("Auto Role Sync Status", status))

@bot.tree.command(name="syncme", description="Sync your Discord role with clan rank")
async def syncme(i: discord.Interaction):
    rsn = await get_linked_rsn(i.user.id)
    if not rsn: await i.response.send_message(embed=create_error_embed("Link your account first"), ephemeral=True); return
    async with aiosqlite.connect(DATABASE) as db:
        c = await db.execute("SELECT clan_rank FROM clan_members WHERE guild_id = ? AND LOWER(rsn) = LOWER(?)", (i.guild.id, rsn))
        r = await c.fetchone()
    if not r: await i.response.send_message(embed=create_error_embed(f"**{rsn}** not in tracked clan."), ephemeral=True); return
    await sync_member_role(i.guild, rsn, r[0])
    await i.response.send_message(embed=create_success_embed("Role Synced!", f"Your role now matches clan rank: **{r[0]}**"))

schedule_group = app_commands.Group(name="schedule", description="Event scheduling", default_permissions=discord.Permissions(administrator=True))

# Event categories with colored square emojis
EVENT_CATEGORIES = {
    "hard_pvm": {"name": "Hard PvM", "emoji": "🟥", "description": "Kerapac, Nex: AOD, Raids, ROTS, Solak, Vorago, ED4, etc."},
    "medium_pvm": {"name": "Medium PvM", "emoji": "🟧", "description": "Godwars Dungeon 2, Kalphite King, Nex, Rex Matriarchs, ED1-3, etc."},
    "easy_pvm": {"name": "Easy PvM", "emoji": "🟩", "description": "Arch-Glacor, Croesus, Corporeal Beast, Godwars Dungeon 1, etc."},
    "skilling": {"name": "Skilling", "emoji": "🟦", "description": "Portables, Clan Gatherings, General Skilling, Artisan's Workshop, etc."},
    "minigames": {"name": "Minigames", "emoji": "🟪", "description": "Barbarian Assault, Castle Wars, Pest Control, Penguin Hide & Seek, PvP, etc."},
    "discord_events": {"name": "Discord Events", "emoji": "🟥", "description": "Jackbox, Karaoke, Movie Nights, Cards Against Humanity, etc."},
    "clan_events": {"name": "Clan Events", "emoji": "⬜", "description": "Citadel, Clan Gatherings, Specials, etc."},
    "giveaways": {"name": "Giveaways", "emoji": "🟫", "description": "Drop Parties, Raffles, General Giveaways, etc."},
    "game_nexus": {"name": "Game Nexus", "emoji": "🔵", "description": "Non-RuneScape games (Fall Guys, CS, Call of Duty, etc.)"},
}

DAYS_OF_WEEK = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

@schedule_group.command(name="start", description="Start schedule session")
@app_commands.describe(title="Schedule title", week_start="Week starting date (DD/MM/YYYY) - defaults to next Monday")
async def sch_start(i: discord.Interaction, title: Optional[str] = "Clan Events", week_start: Optional[str] = None):
    # Parse week_start or default to next Monday
    if week_start:
        try:
            start_date = datetime.strptime(week_start, "%d/%m/%Y")
        except ValueError:
            await i.response.send_message(embed=create_error_embed("Invalid date format. Use DD/MM/YYYY"), ephemeral=True)
            return
    else:
        today = datetime.now(timezone.utc)
        days_until_monday = (7 - today.weekday()) % 7
        if days_until_monday == 0:
            days_until_monday = 7
        start_date = today + timedelta(days=days_until_monday)
    
    async with aiosqlite.connect(DATABASE) as db:
        c = await db.execute("SELECT session_id FROM schedule_sessions WHERE guild_id = ? AND is_active = 1", (i.guild.id,))
        if await c.fetchone():
            await i.response.send_message(embed=create_embed("Session Active", "Use `/schedule view` or `/schedule cancel`", BOT_CONFIG["warning_color"]), ephemeral=True)
            return
        sid = str(uuid.uuid4())[:8]
        await db.execute("INSERT INTO schedule_sessions (session_id, guild_id, started_by, title, week_start) VALUES (?, ?, ?, ?, ?)",
                        (sid, i.guild.id, i.user.id, title, start_date.strftime("%Y-%m-%d")))
        await db.commit()
    
    week_end = start_date + timedelta(days=6)
    await i.response.send_message(embed=create_success_embed("Schedule Started!",
        f"**{title}**\n\n"
        f"📅 Week: **{start_date.strftime('%A %d %b')}** → **{week_end.strftime('%A %d %b %Y')}**\n\n"
        f"Session: `{sid}`\n\n"
        f"`/schedule add` - Add event\n"
        f"`/schedule view` - View events\n"
        f"`/schedule generate` - Finish & post"))

@schedule_group.command(name="add", description="Add event to schedule")
@app_commands.describe(
    day="Day of the week",
    event="Event name",
    host="Host RSN",
    time="Game Time (HH:MM)",
    category="Event category/difficulty",
    world="World number (optional)",
    tags="Tags like [L] [E] [LS] [K] [S] (optional)"
)
@app_commands.choices(
    day=[app_commands.Choice(name=d, value=d) for d in DAYS_OF_WEEK],
    category=[app_commands.Choice(name=f"{v['emoji']} {v['name']}", value=k) for k, v in EVENT_CATEGORIES.items()]
)
async def sch_add(i: discord.Interaction, day: str, event: str, host: str, time: str, category: str, world: Optional[int] = None, tags: Optional[str] = None):
    if not re.match(r'^([01]?[0-9]|2[0-3]):[0-5][0-9]$', time):
        await i.response.send_message(embed=create_error_embed("Invalid time. Use HH:MM format."), ephemeral=True)
        return
    
    async with aiosqlite.connect(DATABASE) as db:
        c = await db.execute("SELECT session_id FROM schedule_sessions WHERE guild_id = ? AND is_active = 1", (i.guild.id,))
        s = await c.fetchone()
        if not s:
            await i.response.send_message(embed=create_error_embed("No active session. Use `/schedule start`"), ephemeral=True)
            return
        
        await db.execute(
            "INSERT INTO schedule_entries (session_id, event_name, host_rsn, event_day, game_time, category, world_number, tags, added_by) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (s[0], event, host, day, time, category, world, tags, i.user.id)
        )
        await db.commit()
        
        c = await db.execute("SELECT COUNT(*) FROM schedule_entries WHERE session_id = ?", (s[0],))
        cnt = (await c.fetchone())[0]
    
    cat_info = EVENT_CATEGORIES.get(category, {"emoji": "⬜", "name": "Event"})
    await i.response.send_message(embed=create_success_embed("Event Added!",
        f"{cat_info['emoji']} **{event}**\n"
        f"📅 {day}\n"
        f"🕐 {time} GT" + (f" | W{world}" if world else "") +
        (f"\n🏷️ {tags}" if tags else "") +
        f"\n👤 Host: {host}\n\n"
        f"Total: {cnt} events"))

@schedule_group.command(name="view", description="View current schedule")
async def sch_view(i: discord.Interaction):
    async with aiosqlite.connect(DATABASE) as db:
        c = await db.execute("SELECT session_id, title, week_start FROM schedule_sessions WHERE guild_id = ? AND is_active = 1", (i.guild.id,))
        s = await c.fetchone()
        if not s:
            await i.response.send_message(embed=create_error_embed("No active session."), ephemeral=True)
            return
        
        c = await db.execute(
            "SELECT id, event_name, host_rsn, event_day, game_time, category, world_number, tags FROM schedule_entries WHERE session_id = ? ORDER BY CASE event_day WHEN 'Monday' THEN 1 WHEN 'Tuesday' THEN 2 WHEN 'Wednesday' THEN 3 WHEN 'Thursday' THEN 4 WHEN 'Friday' THEN 5 WHEN 'Saturday' THEN 6 WHEN 'Sunday' THEN 7 END, game_time",
            (s[0],)
        )
        entries = await c.fetchall()
    
    embed = create_embed(f"📅 {s[1]}", f"Session: `{s[0]}` • {len(entries)} event(s)")
    
    if s[2]:
        week_start = datetime.strptime(s[2], "%Y-%m-%d")
        week_end = week_start + timedelta(days=6)
        embed.description += f"\n📆 {week_start.strftime('%d %b')} → {week_end.strftime('%d %b %Y')}"
    
    if entries:
        # Group by day
        by_day = {}
        for eid, ev, host, day, t, cat, w, tags in entries:
            if day not in by_day:
                by_day[day] = []
            cat_info = EVENT_CATEGORIES.get(cat, {"emoji": "⬜"})
            by_day[day].append(f"`{eid}` {cat_info['emoji']} **{t}** - {ev[:20]}")
        
        for day in DAYS_OF_WEEK:
            if day in by_day:
                embed.add_field(name=day, value="\n".join(by_day[day]), inline=False)
    else:
        embed.add_field(name="No Events", value="Use `/schedule add`", inline=False)
    
    await i.response.send_message(embed=embed)

@schedule_group.command(name="remove", description="Remove event by ID")
@app_commands.describe(entry_id="Entry ID (shown in /schedule view)")
async def sch_remove(i: discord.Interaction, entry_id: int):
    async with aiosqlite.connect(DATABASE) as db:
        c = await db.execute(
            "SELECT e.event_name FROM schedule_entries e JOIN schedule_sessions s ON e.session_id = s.session_id WHERE e.id = ? AND s.guild_id = ? AND s.is_active = 1",
            (entry_id, i.guild.id)
        )
        e = await c.fetchone()
        if not e:
            await i.response.send_message(embed=create_error_embed(f"Entry `{entry_id}` not found."), ephemeral=True)
            return
        await db.execute("DELETE FROM schedule_entries WHERE id = ?", (entry_id,))
        await db.commit()
    await i.response.send_message(embed=create_success_embed("Removed", f"Removed **{e[0]}**"))

@schedule_group.command(name="generate", description="Generate final schedule embed")
async def sch_generate(i: discord.Interaction):
    async with aiosqlite.connect(DATABASE) as db:
        c = await db.execute("SELECT session_id, title, week_start FROM schedule_sessions WHERE guild_id = ? AND is_active = 1", (i.guild.id,))
        s = await c.fetchone()
        if not s:
            await i.response.send_message(embed=create_error_embed("No active session."), ephemeral=True)
            return
        
        c = await db.execute(
            "SELECT event_name, host_rsn, event_day, game_time, category, world_number, tags FROM schedule_entries WHERE session_id = ? ORDER BY CASE event_day WHEN 'Monday' THEN 1 WHEN 'Tuesday' THEN 2 WHEN 'Wednesday' THEN 3 WHEN 'Thursday' THEN 4 WHEN 'Friday' THEN 5 WHEN 'Saturday' THEN 6 WHEN 'Sunday' THEN 7 END, game_time",
            (s[0],)
        )
        entries = await c.fetchall()
        
        if not entries:
            await i.response.send_message(embed=create_error_embed("No events to generate!"), ephemeral=True)
            return
        
        await db.execute("UPDATE schedule_sessions SET is_active = 0 WHERE session_id = ?", (s[0],))
        await db.commit()
    
    # Build the schedule embed
    week_start = datetime.strptime(s[2], "%Y-%m-%d") if s[2] else datetime.now(timezone.utc)
    week_end = week_start + timedelta(days=6)
    
    embed = discord.Embed(
        title=f"📅 {s[1]}",
        description=f"**{week_start.strftime('%A %d %B')}** → **{week_end.strftime('%A %d %B %Y')}**\n\nAll times are **Game Time (UTC)**",
        color=BOT_CONFIG["primary_color"]
    )
    embed.set_thumbnail(url=BOT_CONFIG["logo_url"])
    
    # Group events by day
    by_day = {}
    for ev, host, day, t, cat, w, tags in entries:
        if day not in by_day:
            by_day[day] = []
        by_day[day].append((ev, host, t, cat, w, tags))
    
    # Add each day as a field
    for day in DAYS_OF_WEEK:
        if day in by_day:
            day_events = []
            for ev, host, t, cat, w, tags in by_day[day]:
                cat_info = EVENT_CATEGORIES.get(cat, {"emoji": "⬜"})
                line = f"{cat_info['emoji']} **{t}** - {ev}"
                if tags:
                    line += f" {tags}"
                line += f"\n┗ *Host: {host}*" + (f" *| W{w}*" if w else "")
                day_events.append(line)
            embed.add_field(name=f"━━━ {day} ━━━", value="\n".join(day_events), inline=False)
    
    # Add legend
    legend = "**Legend:**\n`[L]` Learner Friendly · `[E]` Experienced · `[LS]` LootShare\n`[K]` Keeps · `[S]` Splits"
    embed.add_field(name="\u200b", value=legend, inline=False)
    
    embed.set_footer(text=f"{BOT_CONFIG['clan_name']} • {len(entries)} events", icon_url=BOT_CONFIG["logo_url"])
    embed.timestamp = datetime.now(timezone.utc)
    
    await i.response.send_message(embed=embed)

@schedule_group.command(name="categories", description="Show event categories and their emojis")
async def sch_categories(i: discord.Interaction):
    embed = create_embed("📋 Event Categories", "Available categories for scheduling:")
    
    for key, cat in EVENT_CATEGORIES.items():
        embed.add_field(
            name=f"{cat['emoji']} {cat['name']}",
            value=f"*{cat['description']}*",
            inline=False
        )
    
    await i.response.send_message(embed=embed, ephemeral=True)

@schedule_group.command(name="cancel", description="Cancel current session")
async def sch_cancel(i: discord.Interaction):
    async with aiosqlite.connect(DATABASE) as db:
        c = await db.execute("SELECT session_id FROM schedule_sessions WHERE guild_id = ? AND is_active = 1", (i.guild.id,))
        s = await c.fetchone()
        if not s:
            await i.response.send_message(embed=create_error_embed("No active session."), ephemeral=True)
            return
        await db.execute("DELETE FROM schedule_entries WHERE session_id = ?", (s[0],))
        await db.execute("DELETE FROM schedule_sessions WHERE session_id = ?", (s[0],))
        await db.commit()
    await i.response.send_message(embed=create_success_embed("Cancelled", "Schedule session cancelled."))

bot.tree.add_command(schedule_group)

@bot.tree.command(name="wildyflash", description="Current Wilderness Flash Event")
async def wildyflash(i: discord.Interaction):
    f = get_next_wildy_flash()
    embed = create_embed(f"{f['current']['icon']} Wilderness Flash Event", color=0xFF4500)
    embed.add_field(name="Current", value=f"**{f['current']['name']}**\n{f['current']['type'].title()}", inline=True)
    embed.add_field(name="Time Left", value=f"**{f['minutes_left']}** min", inline=True)
    embed.add_field(name="Next", value=f"{f['next']['icon']} {f['next']['name']}", inline=False)
    await i.response.send_message(embed=embed)

@bot.tree.command(name="gametime", description="Current Game Time (UTC)")
async def gametime(i: discord.Interaction):
    now = datetime.now(timezone.utc)
    reset = now.replace(hour=0, minute=0, second=0) + timedelta(days=1)
    to_reset = reset - now
    f = get_next_wildy_flash()
    embed = create_embed("🕐 Game Time", f"**{now.strftime('%H:%M')}** GT\n*{now.strftime('%A, %d %B %Y')}*")
    embed.add_field(name="Daily Reset", value=f"In **{int(to_reset.total_seconds()//3600)}h {int((to_reset.total_seconds()%3600)//60)}m**", inline=True)
    embed.add_field(name="Wildy Flash", value=f"{f['current']['icon']} {f['current']['name']}\n{f['minutes_left']}m left", inline=True)
    await i.response.send_message(embed=embed)

@bot.tree.command(name="event", description="Announce world event")
@app_commands.describe(event_type="Event type", world="World number (optional)", details="Extra details (optional)")
@app_commands.choices(event_type=[app_commands.Choice(name=v["name"], value=k) for k, v in WORLD_EVENTS.items()])
async def event(i: discord.Interaction, event_type: str, world: Optional[int] = None, details: Optional[str] = None):
    e = WORLD_EVENTS.get(event_type)
    if not e: await i.response.send_message("Unknown event.", ephemeral=True); return
    embed = create_embed(f"{e['icon']} {e['name']}", details or "Event active!", 0x9B59B6)
    embed.add_field(name="Reported by", value=i.user.mention, inline=True)
    embed.add_field(name="Game Time", value=get_game_time() + " GT", inline=True)
    if world: embed.add_field(name="World", value=f"**W{world}**", inline=True)
    cid = await get_world_events_channel(i.guild.id)
    if cid:
        ch = bot.get_channel(cid)
        if ch: await ch.send(embed=embed); await i.response.send_message(f"Announced in {ch.mention}!", ephemeral=True); return
    await i.response.send_message(embed=embed)

@bot.tree.command(name="vos", description="Current Voice of Seren")
async def vos(i: discord.Interaction):
    await i.response.defer()
    vos_data = await fetch_vos()
    now = datetime.now(timezone.utc)
    mins_until_change = 60 - now.minute
    
    embed = create_embed("🔮 Voice of Seren", f"Active clans in Prifddinas\nChanges in **{mins_until_change}** minutes", 0x9B59B6)
    
    if vos_data and isinstance(vos_data, dict):
        # API returns {"district1": "Clan1", "district2": "Clan2"} or similar
        clans = []
        for key, clan in vos_data.items():
            if isinstance(clan, str) and clan in VOS_BENEFITS:
                clans.append(clan)
        
        if not clans:
            clans = list(vos_data.values()) if vos_data else []
        
        for clan in clans[:2]:
            clan_name = clan if isinstance(clan, str) else str(clan)
            benefits = VOS_BENEFITS.get(clan_name, {})
            embed.add_field(
                name=f"🏛️ {clan_name}",
                value=f"**Skills:** {benefits.get('skills', 'Various')}\n**Benefit:** {benefits.get('benefit', 'XP boost')}\n**Location:** {benefits.get('location', 'Prifddinas')}",
                inline=False
            )
    else:
        # Fallback - show general info
        embed.add_field(name="⚠️ API Unavailable", value="Check in-game or use Alt1 toolkit.\nVoS changes every hour on the hour.", inline=False)
    
    embed.add_field(name="📍 All Clans", value="Amlodd • Cadarn • Crwys • Hefin\nIorwerth • Ithell • Meilyr • Trahaearn", inline=False)
    embed.set_footer(text="Same VoS on all worlds • Requires Plague's End")
    await i.followup.send(embed=embed)

@bot.tree.command(name="merchant", description="Travelling Merchant's current stock")
async def merchant(i: discord.Interaction):
    await i.response.defer()
    tms_data = await fetch_travelling_merchant()
    
    embed = create_embed("🛒 Travelling Merchant", "Deep Sea Fishing Hub", 0x3498DB)
    embed.add_field(name="📍 Location", value="**Deep Sea Fishing Hub**\nFishing Guild → Rowboat", inline=False)
    
    if tms_data and isinstance(tms_data, list):
        stock_txt = ""
        for item in tms_data:
            if isinstance(item, dict):
                name = item.get("name", item.get("item", "Unknown"))
                cost = item.get("cost", item.get("price", "?"))
                stock_txt += f"• **{name}** - {cost:,} coins\n" if isinstance(cost, int) else f"• **{name}** - {cost}\n"
            else:
                stock_txt += f"• {item}\n"
        embed.add_field(name="📦 Today's Stock", value=stock_txt or "Check in-game", inline=False)
    else:
        embed.add_field(name="⚠️ API Unavailable", value="Stock resets at 00:00 UTC daily.\nCheck wiki: runescape.wiki/w/Travelling_Merchant", inline=False)
    
    now = datetime.now(timezone.utc)
    reset = now.replace(hour=0, minute=0, second=0) + timedelta(days=1)
    hrs_left = int((reset - now).total_seconds() // 3600)
    embed.add_field(name="⏰ Resets", value=f"In **{hrs_left}** hours (00:00 UTC)", inline=True)
    await i.followup.send(embed=embed)

@bot.tree.command(name="warbands", description="Warbands timing and locations")
async def warbands(i: discord.Interaction):
    wb = get_warbands_times()
    embed = create_embed("⚔️ Warbands", "Wilderness PvP D&D", 0xE74C3C)
    embed.add_field(name="⏰ Next Wave", value=f"**{wb['next']}**\nIn **{wb['minutes_until']}** minutes", inline=False)
    embed.add_field(name="📍 Camp Locations", value="\n".join(f"• {c}" for c in wb['camps']), inline=False)
    embed.add_field(name="ℹ️ Info", value="• Occurs every **7 hours** (00:00, 07:00, 14:00, 21:00 UTC)\n• 3 camps spawn randomly\n• Loot supplies for XP (75 per type/day)\n• **PvP enabled** - bring minimal risk!", inline=False)
    embed.set_footer(text="⚠️ Wilderness PvP - You can be attacked!")
    await i.response.send_message(embed=embed)

@bot.tree.command(name="cache", description="Guthixian Cache timing")
async def cache(i: discord.Interaction):
    c = get_cache_times()
    embed = create_embed("💚 Guthixian Cache", "Divination D&D", 0x2ECC71)
    embed.add_field(name="⏰ Next Cache", value=f"**{c['next']}**\nIn **{c['minutes_until']}** minutes", inline=False)
    embed.add_field(name="📍 Location", value=c['location'], inline=False)
    embed.add_field(name="ℹ️ Info", value="• Occurs **every hour** on the hour\n• 10 minute duration\n• Max 200 points (100 pts = daily cap bonus)\n• Great Divination XP!", inline=False)
    await i.response.send_message(embed=embed)

@bot.tree.command(name="sinkholes", description="Sinkholes timing")
async def sinkholes(i: discord.Interaction):
    sh = get_sinkhole_times()
    embed = create_embed("🕳️ Sinkholes", "Dungeoneering D&D", 0x9B59B6)
    embed.add_field(name="⏰ Next Sinkhole", value=f"**{sh['next']}**\nIn **{sh['minutes_until']}** minutes", inline=False)
    embed.add_field(name="📍 Location", value=sh['location'], inline=False)
    embed.add_field(name="ℹ️ Info", value="• Occurs every **30 minutes** (:00 and :30)\n• 5 players per game\n• 2 games per day limit\n• Cards affect rewards!", inline=False)
    await i.response.send_message(embed=embed)

@bot.tree.command(name="spotlight", description="Current Minigame Spotlight")
async def spotlight(i: discord.Interaction):
    sp = get_spotlight_game()
    embed = create_embed("🎮 Minigame Spotlight", "Boosted Thaler & Rewards", 0xF39C12)
    embed.add_field(name="🌟 Current Spotlight", value=f"**{sp['game']}**", inline=False)
    embed.add_field(name="⏰ Days Remaining", value=f"**{sp['days_remaining']}** days", inline=True)
    embed.add_field(name="💰 Bonus", value="• **3x Thaler** earnings\n• Increased rewards\n• More players active!", inline=False)
    await i.response.send_message(embed=embed)

@bot.tree.command(name="events", description="All current game events")
async def events(i: discord.Interaction):
    await i.response.defer()
    
    # Gather all event data
    flash = get_next_wildy_flash()
    wb = get_warbands_times()
    cache = get_cache_times()
    sh = get_sinkhole_times()
    sp = get_spotlight_game()
    vos_data = await fetch_vos()
    
    embed = create_embed("🗓️ Current Events", f"Game Time: **{get_game_time()} GT**", 0x3498DB)
    
    # Wilderness Flash
    embed.add_field(
        name=f"{flash['current']['icon']} Wildy Flash",
        value=f"**{flash['current']['name']}**\n{flash['minutes_left']}m left",
        inline=True
    )
    
    # Voice of Seren
    vos_txt = "Check `/vos`"
    if vos_data and isinstance(vos_data, dict):
        clans = [str(v) for v in vos_data.values() if isinstance(v, str)][:2]
        if clans:
            vos_txt = " & ".join(clans)
    embed.add_field(name="🔮 Voice of Seren", value=vos_txt, inline=True)
    
    # Spotlight
    embed.add_field(name="🎮 Spotlight", value=f"**{sp['game']}**\n{sp['days_remaining']}d left", inline=True)
    
    # Warbands
    embed.add_field(name="⚔️ Warbands", value=f"Next: **{wb['next']}**\n{wb['minutes_until']}m", inline=True)
    
    # Cache
    embed.add_field(name="💚 Cache", value=f"Next: **{cache['next']}**\n{cache['minutes_until']}m", inline=True)
    
    # Sinkholes
    embed.add_field(name="🕳️ Sinkholes", value=f"Next: **{sh['next']}**\n{sh['minutes_until']}m", inline=True)
    
    embed.add_field(name="📋 Commands", value="`/vos` `/merchant` `/warbands` `/cache` `/sinkholes` `/spotlight` `/wildyflash`", inline=False)
    await i.followup.send(embed=embed)

@bot.tree.command(name="price", description="Check GE prices")
@app_commands.describe(item="Item name (supports shortcuts like FSOA, ECB, SGB, etc.)")
async def price(i: discord.Interaction, item: str):
    await i.response.defer()
    
    # Check for alias first
    original_input = item
    item_lower = item.lower().strip()
    if item_lower in ITEM_ALIASES:
        item = ITEM_ALIASES[item_lower]
    
    pd, ed = await fetch_wiki_price(item), await fetch_ely_price(item)
    wp = None
    # Check pd is actually a dict with items
    if pd and isinstance(pd, dict):
        for k in pd:
            if isinstance(pd[k], dict) and k.lower() == item.lower():
                wp = pd[k].get("price", 0)
                item = k
                break
        if not wp:
            for k in pd:
                if isinstance(pd[k], dict):
                    wp = pd[k].get("price", 0)
                    item = k
                    break
    ep = ed.get("price") or ed.get("value") if ed and isinstance(ed, dict) else None
    if not wp and not ep:
        # Check if there's a similar alias they might have meant
        similar_aliases = [f"**{alias}** → {full}" for alias, full in ITEM_ALIASES.items() if original_input.lower() in alias.lower() or alias.lower() in original_input.lower()]
        
        results = await search_wiki_items(item)
        if similar_aliases:
            await i.followup.send(embed=create_embed("Not Found", f"**{original_input}** not found.\n\n**Did you mean:**\n" + "\n".join(f"• {a}" for a in similar_aliases[:5]), BOT_CONFIG["warning_color"]), ephemeral=True)
        elif results:
            await i.followup.send(embed=create_embed("Not Found", f"**{original_input}** not found.\n\n**Did you mean:**\n" + "\n".join(f"• {r}" for r in results[:5]), BOT_CONFIG["warning_color"]), ephemeral=True)
        else:
            await i.followup.send(embed=create_error_embed(f"No items matching **{original_input}**"), ephemeral=True)
        return
    
    # Build embed
    embed = create_embed(item, f"[Wiki](https://runescape.wiki/w/{item.replace(' ', '_')})")
    
    # Use wiki's special:filepath for more reliable images
    wiki_image_name = item.replace(' ', '_').replace("'", "%27")
    embed.set_thumbnail(url=f"https://runescape.wiki/images/{wiki_image_name}_detail.png")
    
    if wp: embed.add_field(name="Wiki Price", value=f"{wp:,} GP", inline=True)
    if ep: embed.add_field(name="Ely.gg", value=f"{ep:,} GP", inline=True)
    
    # Show if alias was used
    if original_input.lower() != item.lower():
        embed.set_footer(text=f"Searched: {original_input} → {item}")
    
    await i.followup.send(embed=embed)

@bot.tree.command(name="setchannel", description="Set announcement channel (Admin)")
@app_commands.describe(channel_type="Channel type", channel="Channel")
@app_commands.choices(channel_type=[app_commands.Choice(name="Drops", value="drops"), app_commands.Choice(name="Achievements", value="achievements"), app_commands.Choice(name="Events", value="events"), app_commands.Choice(name="Welcome", value="welcome"), app_commands.Choice(name="World Events", value="world_events")])
@app_commands.default_permissions(administrator=True)
async def setchannel(i: discord.Interaction, channel_type: str, channel: discord.TextChannel):
    async with aiosqlite.connect(DATABASE) as db:
        await db.execute(f"INSERT INTO guild_settings (guild_id, {channel_type}_channel) VALUES (?, ?) ON CONFLICT(guild_id) DO UPDATE SET {channel_type}_channel=excluded.{channel_type}_channel", (i.guild.id, channel.id))
        await db.commit()
    await i.response.send_message(embed=create_success_embed("Channel Set", f"**{channel_type.replace('_', ' ').title()}** → {channel.mention}"))

# Welcome command group
welcome_group = app_commands.Group(name="welcome", description="Welcome message configuration", default_permissions=discord.Permissions(administrator=True))

@welcome_group.command(name="init", description="Initialize/reset welcome config to defaults")
async def welcome_init(i: discord.Interaction):
    init_welcome_config(i.guild.id)
    await i.response.send_message(embed=create_success_embed("Welcome Config Initialized", 
        f"Default config created in `{WELCOME_CONFIG_FILE}`\n\n"
        f"Use `/welcome preview` to see current config\n"
        f"Use `/welcome edit` to modify settings\n"
        f"Or edit the JSON file directly and use `/welcome reload`"))

@welcome_group.command(name="preview", description="Preview the current welcome message")
async def welcome_preview(i: discord.Interaction):
    config = get_welcome_config(i.guild.id)
    
    # Simulate the welcome message
    ping_parts = []
    if config.get("ping_user", True):
        ping_parts.append(i.user.mention)
    if config.get("ping_role"):
        ping_parts.append(f"<@&{config['ping_role']}>")
    
    ping_message = " ".join(ping_parts) if ping_parts else "*No ping configured*"
    
    try:
        color = int(config.get("color", "2ECC71"), 16)
    except:
        color = BOT_CONFIG["success_color"]
    
    title = config.get("title", "Welcome!").replace("{user}", i.user.display_name).replace("{server}", i.guild.name)
    description = config.get("description", "").replace("{user}", i.user.mention).replace("{server}", i.guild.name)
    
    embed = discord.Embed(title=title, description=description, color=color)
    
    for field in config.get("fields", []):
        name = field.get("name", "Info")
        value = field.get("value", "").replace("{user}", i.user.mention).replace("{server}", i.guild.name)
        inline = field.get("inline", False)
        embed.add_field(name=name, value=value, inline=inline)
    
    thumbnail = config.get("thumbnail", "user")
    if thumbnail == "user":
        embed.set_thumbnail(url=i.user.display_avatar.url)
    elif thumbnail == "server" and i.guild.icon:
        embed.set_thumbnail(url=i.guild.icon.url)
    elif thumbnail and thumbnail.startswith("http"):
        embed.set_thumbnail(url=thumbnail)
    
    if config.get("image"):
        embed.set_image(url=config["image"])
    
    footer_config = config.get("footer", {})
    if footer_config:
        footer_text = footer_config.get("text", "").replace("{user}", i.user.display_name).replace("{server}", i.guild.name)
        if footer_config.get("icon") and i.guild.icon:
            embed.set_footer(text=footer_text, icon_url=i.guild.icon.url)
        else:
            embed.set_footer(text=footer_text)
    
    await i.response.send_message(content=f"**Preview** (Ping: {ping_message})\n─────────────────────", embed=embed)

@welcome_group.command(name="toggle", description="Enable/disable welcome messages")
async def welcome_toggle(i: discord.Interaction):
    config = get_welcome_config(i.guild.id)
    config["enabled"] = not config.get("enabled", True)
    save_welcome_config(i.guild.id, config)
    
    status = "✅ Enabled" if config["enabled"] else "❌ Disabled"
    await i.response.send_message(embed=create_success_embed("Welcome Messages", status))

@welcome_group.command(name="title", description="Set welcome embed title")
@app_commands.describe(title="Title text ({user} = username, {server} = server name)")
async def welcome_title(i: discord.Interaction, title: str):
    config = get_welcome_config(i.guild.id)
    config["title"] = title
    save_welcome_config(i.guild.id, config)
    await i.response.send_message(embed=create_success_embed("Title Updated", f"New title: **{title}**"))

@welcome_group.command(name="description", description="Set welcome embed description")
@app_commands.describe(description="Description text ({user} = mention, {server} = server name)")
async def welcome_description(i: discord.Interaction, description: str):
    config = get_welcome_config(i.guild.id)
    config["description"] = description
    save_welcome_config(i.guild.id, config)
    await i.response.send_message(embed=create_success_embed("Description Updated", f"New description:\n{description}"))

@welcome_group.command(name="color", description="Set welcome embed color")
@app_commands.describe(hex_color="Hex color code (e.g., 2ECC71 for green)")
async def welcome_color(i: discord.Interaction, hex_color: str):
    hex_color = hex_color.replace("#", "").upper()
    try:
        int(hex_color, 16)
    except:
        await i.response.send_message(embed=create_error_embed("Invalid hex color. Use format like: 2ECC71"), ephemeral=True)
        return
    
    config = get_welcome_config(i.guild.id)
    config["color"] = hex_color
    save_welcome_config(i.guild.id, config)
    await i.response.send_message(embed=create_success_embed("Color Updated", f"New color: `#{hex_color}`"))

@welcome_group.command(name="footer", description="Set welcome embed footer")
@app_commands.describe(text="Footer text", show_icon="Show server icon in footer")
async def welcome_footer(i: discord.Interaction, text: str, show_icon: bool = True):
    config = get_welcome_config(i.guild.id)
    config["footer"] = {"text": text, "icon": show_icon}
    save_welcome_config(i.guild.id, config)
    await i.response.send_message(embed=create_success_embed("Footer Updated", f"New footer: **{text}**"))

@welcome_group.command(name="pingrole", description="Set a role to ping on new joins")
@app_commands.describe(role="Role to ping (leave empty to disable)")
async def welcome_pingrole(i: discord.Interaction, role: Optional[discord.Role] = None):
    config = get_welcome_config(i.guild.id)
    config["ping_role"] = role.id if role else None
    save_welcome_config(i.guild.id, config)
    
    if role:
        await i.response.send_message(embed=create_success_embed("Ping Role Set", f"Will ping {role.mention} on new joins"))
    else:
        await i.response.send_message(embed=create_success_embed("Ping Role Removed", "No role will be pinged"))

@welcome_group.command(name="pinguser", description="Toggle pinging the new user")
async def welcome_pinguser(i: discord.Interaction):
    config = get_welcome_config(i.guild.id)
    config["ping_user"] = not config.get("ping_user", True)
    save_welcome_config(i.guild.id, config)
    
    status = "✅ Will ping user" if config["ping_user"] else "❌ Won't ping user"
    await i.response.send_message(embed=create_success_embed("User Ping", status))

@welcome_group.command(name="addfield", description="Add a field to the welcome embed")
@app_commands.describe(name="Field title", value="Field content (use \\n for new lines)", inline="Display inline")
async def welcome_addfield(i: discord.Interaction, name: str, value: str, inline: bool = False):
    config = get_welcome_config(i.guild.id)
    if "fields" not in config:
        config["fields"] = []
    
    # Replace literal \n with actual newlines
    value = value.replace("\\n", "\n")
    
    config["fields"].append({"name": name, "value": value, "inline": inline})
    save_welcome_config(i.guild.id, config)
    await i.response.send_message(embed=create_success_embed("Field Added", f"**{name}**\n{value}"))

@welcome_group.command(name="clearfields", description="Remove all fields from welcome embed")
async def welcome_clearfields(i: discord.Interaction):
    config = get_welcome_config(i.guild.id)
    config["fields"] = []
    save_welcome_config(i.guild.id, config)
    await i.response.send_message(embed=create_success_embed("Fields Cleared", "All fields removed from welcome embed"))

@welcome_group.command(name="reload", description="Reload config from JSON file")
async def welcome_reload(i: discord.Interaction):
    config = get_welcome_config(i.guild.id)
    await i.response.send_message(embed=create_success_embed("Config Reloaded", 
        f"Loaded from `{WELCOME_CONFIG_FILE}`\n\n"
        f"**Title:** {config.get('title', 'N/A')}\n"
        f"**Enabled:** {config.get('enabled', True)}\n"
        f"**Fields:** {len(config.get('fields', []))}\n"
        f"**Ping User:** {config.get('ping_user', True)}\n"
        f"**Ping Role:** {'<@&' + str(config.get('ping_role')) + '>' if config.get('ping_role') else 'None'}"))

@welcome_group.command(name="export", description="Show the current JSON config")
async def welcome_export(i: discord.Interaction):
    config = get_welcome_config(i.guild.id)
    json_str = json.dumps(config, indent=2)
    
    if len(json_str) > 1900:
        # Send as file if too long
        await i.response.send_message(
            content=f"Config too long for message. File: `{WELCOME_CONFIG_FILE}`",
            ephemeral=True
        )
    else:
        await i.response.send_message(f"```json\n{json_str}\n```", ephemeral=True)

bot.tree.add_command(welcome_group)

# ==================== HALL OF FAME IMAGE GENERATOR ====================
try:
    from PIL import Image, ImageDraw, ImageFont
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    print("WARNING: Pillow not installed. Hall of Fame image generation disabled. Install with: pip install Pillow")

# Hall of Fame categories with icons
# emoji_id: Discord custom emoji ID (numeric string) - set to None for no emoji in image
# icon: Unicode emoji for Discord text display
HOF_CATEGORIES = {
    "the_statuesque": {"name": "the Statuesque", "icon": "🏆", "emoji_id": "1463607824885088520", "color": (255, 215, 0)},
    "trimmed_comp": {"name": "Trimmed Completionist", "icon": "🎖️", "emoji_id": "977222749263122495", "color": (255, 105, 180)},
    "master_quest": {"name": "Master Quest Cape", "icon": "📜", "emoji_id": "977224698423291934", "color": (100, 149, 237)},
    "ultimate_slayer": {"name": "the Ultimate Slayer", "icon": "🗡️", "emoji_id": None, "color": (50, 205, 50)},
    "the_wikian": {"name": "The Wikian", "icon": "📚", "emoji_id": "1463618471421018348", "color": (255, 140, 0)},
    "master_of_all": {"name": "Master of All", "icon": "⭐", "emoji_id": "1068597304401076324", "color": (255, 215, 0)},
    "120_all": {"name": "120 All", "icon": "🔥", "emoji_id": "1068597304401076324", "color": (255, 69, 0)},
    "200m_all": {"name": "200M All", "icon": "💎", "emoji_id": "1068597631141556224", "color": (0, 191, 255)},
    "1kc_pet": {"name": "1KC Pet", "icon": "🐾", "emoji_id": None, "color": (255, 215, 0)},
    "4k_telos": {"name": "4K% God/Goddess of Destruction", "icon": "🏆", "emoji_id": "1463605390737408322", "color": (255, 215, 0)},
    "the_warden": {"name": "the Warden", "icon": "🛡️", "emoji_id": "1463605390737408322", "color": (0, 255, 127)},
    "telos_200ks": {"name": "Telos 200 Killstreak", "icon": "💀", "emoji_id": "1463605390737408322", "color": (138, 43, 226)},
    "the_iceborn": {"name": "the Iceborn", "icon": "❄️", "emoji_id": "997855866424393738", "color": (135, 206, 250)},
    "glacor_200ks": {"name": "Arch-Glacor 200 Killstreak", "icon": "🧊", "emoji_id": "997855866424393738", "color": (135, 206, 250)},
    "lord_of_chaos": {"name": "Lord/Lady of Chaos", "icon": "😈", "emoji_id": None, "color": (220, 20, 60)},
    "wrath_of_chaos": {"name": "Wrath of Chaos", "icon": "🔥", "emoji_id": None, "color": (255, 69, 0)},
    "of_the_praesul": {"name": "of the Praesul", "icon": "✨", "emoji_id": None, "color": (255, 105, 180)},
    "insane_final_boss": {"name": "Insane Final Boss", "icon": "👑", "emoji_id": None, "color": (255, 215, 0)},
    "the_reaper": {"name": "the Reaper", "icon": "💀", "emoji_id": None, "color": (128, 0, 128)},
    "the_daredevil": {"name": "the Daredevil", "icon": "⚡", "emoji_id": None, "color": (255, 165, 0)},
    "the_defeater": {"name": "the Defeater", "icon": "⚔️", "emoji_id": None, "color": (255, 215, 0)},
    "combat_mastery": {"name": "Master Combat Mastery", "icon": "🏅", "emoji_id": None, "color": (192, 192, 192)},
    "gm_combat": {"name": "Grandmaster Combat Mastery", "icon": "🥇", "emoji_id": None, "color": (255, 215, 0)},
    "gold_digger": {"name": "Gold Digger", "icon": "💰", "emoji_id": "1068597030676615168", "color": (255, 215, 0)},
    "clueless": {"name": "Clueless", "icon": "📦", "emoji_id": "1068597030676615168", "color": (139, 69, 19)},
    "double_agent": {"name": "Double Agent", "icon": "🕵️", "emoji_id": "1068597030676615168", "color": (75, 0, 130)},
    "clue_chaser": {"name": "the Clue Chaser", "icon": "🗺️", "emoji_id": "1068597030676615168", "color": (210, 105, 30)},
    "master_of_clues": {"name": "Master of Clues", "icon": "📜", "emoji_id": "1068597030676615168", "color": (255, 215, 0)},
    "seasonal_high": {"name": "Seasonal High Scores", "icon": "🏆", "emoji_id": None, "color": (255, 215, 0)},
    "tavias_rod": {"name": "Tavia's Fishing Rod", "icon": "🎣", "emoji_id": "1463616963107360838", "color": (0, 191, 255)},
    "hazelmere_ring": {"name": "Hazelmere's Signet Ring", "icon": "💍", "emoji_id": "1463616731800141854", "color": (50, 205, 50)},
    "tonys_mattock": {"name": "Tony's Mattock", "icon": "⛏️", "emoji_id": "1463616369844162605", "color": (255, 215, 0)},
    "orlando_hat": {"name": "Orlando Smith's Hat", "icon": "🎩", "emoji_id": "1463616098502180939", "color": (139, 69, 19)},
    "black_partyhat": {"name": "Black Partyhat", "icon": "🎉", "emoji_id": "1463615788828332198", "color": (75, 75, 75)},
    "leagues_dragon": {"name": "Leagues: Dragon (60,000)", "icon": "🐉", "emoji_id": None, "color": (255, 69, 0)},
    "nex": {"name": "Nex", "icon": "⚔️", "emoji_id": "997855976097071185", "color": (128, 0, 128)},
    "nex_aod": {"name": "Nex: Angel of Death", "icon": "👼", "emoji_id": "997855854311243906", "color": (255, 105, 180)},
}

# Cache for downloaded Discord emoji images {emoji_id: PIL.Image}
hof_emoji_cache = {}

# Store HOF data per guild (includes emoji overrides per category)
# Format: {guild_id: {cat_key: {"members": [...], "emoji_id": "123456789"}}}
hof_data_store = {}

async def fetch_discord_emoji(emoji_id: str, animated: bool = False) -> Optional[Image.Image]:
    """Fetch a Discord emoji by ID and return as PIL Image"""
    if not PIL_AVAILABLE:
        return None
    
    # Check cache first
    if emoji_id in hof_emoji_cache:
        return hof_emoji_cache[emoji_id]
    
    # Discord CDN URL for custom emojis
    ext = "gif" if animated else "png"
    url = f"https://cdn.discordapp.com/emojis/{emoji_id}.{ext}?size=48"
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.read()
                    img = Image.open(io.BytesIO(data))
                    # Convert to RGBA if needed
                    if img.mode != 'RGBA':
                        img = img.convert('RGBA')
                    # Resize to 24x24 for header icons
                    img = img.resize((24, 24), Image.Resampling.LANCZOS)
                    hof_emoji_cache[emoji_id] = img
                    return img
    except Exception as e:
        print(f"Failed to fetch emoji {emoji_id}: {e}")
    
    return None

def parse_emoji_string(emoji_str: str) -> Optional[tuple]:
    """Parse a Discord emoji string like <:name:123456789> or <a:name:123456789>
    Returns (emoji_id, is_animated) or None"""
    if not emoji_str:
        return None
    
    # Match custom emoji format: <:name:id> or <a:name:id>
    match = re.match(r'<(a)?:([^:]+):(\d+)>', emoji_str.strip())
    if match:
        is_animated = match.group(1) == 'a'
        emoji_id = match.group(3)
        return (emoji_id, is_animated)
    
    # Also accept raw emoji ID
    if emoji_str.strip().isdigit():
        return (emoji_str.strip(), False)
    
    return None

async def generate_hof_image_async(categories_data: dict, guild_id: int = None, title: str = "Hall of Fame") -> io.BytesIO:
    """Generate a Hall of Fame image from category data with Discord emoji support"""
    if not PIL_AVAILABLE:
        return None
    
    # Image settings
    bg_color = (30, 30, 35)
    border_color = (255, 215, 0)
    text_color = (255, 255, 255)
    title_color = (255, 215, 0)
    bullet_color = (255, 215, 0)  # Gold bullet points
    
    # Filter out empty categories
    filtered_data = {}
    for k, v in categories_data.items():
        # Handle both old format (list) and new format (dict with members/emoji_id)
        if isinstance(v, dict):
            members = v.get("members", [])
            if members:
                filtered_data[k] = v
        elif v:  # Old format: direct list
            filtered_data[k] = {"members": v, "emoji_id": None}
    
    if not filtered_data:
        return None
    
    # Pre-fetch all emoji images
    emoji_images = {}
    for cat_key, cat_data in filtered_data.items():
        emoji_id = None
        # Check for category-specific emoji override
        if isinstance(cat_data, dict) and cat_data.get("emoji_id"):
            parsed = parse_emoji_string(cat_data["emoji_id"])
            if parsed:
                emoji_id, animated = parsed
        # Fall back to default category emoji
        elif cat_key in HOF_CATEGORIES and HOF_CATEGORIES[cat_key].get("emoji_id"):
            emoji_id = HOF_CATEGORIES[cat_key]["emoji_id"]
            animated = False
        
        if emoji_id:
            img = await fetch_discord_emoji(emoji_id, animated if 'animated' in dir() else False)
            if img:
                emoji_images[cat_key] = img
    
    # Calculate dimensions - increased sizes
    num_cols = 3
    col_width = 450  # Wider columns
    padding = 50
    title_height = 100
    emoji_size = 32  # Larger emoji
    emoji_padding = 8
    member_line_height = 28  # More spacing between members
    category_spacing = 35  # Space between categories
    header_height = 38  # Height for category header
    
    # Calculate height needed for each column
    col_heights = [0, 0, 0]
    col_assignments = [[], [], []]
    
    for cat_key, cat_data in filtered_data.items():
        members = cat_data.get("members", []) if isinstance(cat_data, dict) else cat_data
        if not members:
            continue
        # Find shortest column
        min_col = col_heights.index(min(col_heights))
        member_count = len(members) if isinstance(members, list) else len(members.split('\n'))
        cat_height = header_height + (member_count * member_line_height) + category_spacing
        col_heights[min_col] += cat_height
        col_assignments[min_col].append((cat_key, cat_data))
    
    max_col_height = max(col_heights) if col_heights else 400
    img_width = (col_width * num_cols) + (padding * 2)
    img_height = title_height + max_col_height + (padding * 2)
    img_height = max(img_height, 600)
    
    # Create image
    img = Image.new('RGBA', (img_width, img_height), bg_color)
    draw = ImageDraw.Draw(img)
    
    # Load fonts - check fonts/ directory first (relative to bot), then system fonts
    bot_dir = os.path.dirname(os.path.abspath(__file__))
    font_paths = [
        (os.path.join(bot_dir, "fonts", "DejaVuSans-Bold.ttf"), os.path.join(bot_dir, "fonts", "DejaVuSans.ttf")),
        ("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
        ("arial.ttf", "arial.ttf"),
    ]
    
    title_font = header_font = text_font = None
    for bold_path, regular_path in font_paths:
        try:
            title_font = ImageFont.truetype(bold_path, 48)
            header_font = ImageFont.truetype(bold_path, 22)
            text_font = ImageFont.truetype(regular_path, 18)
            break
        except:
            continue
    
    if not title_font:
        title_font = ImageFont.load_default()
        header_font = ImageFont.load_default()
        text_font = ImageFont.load_default()
    
    # Draw border
    draw.rectangle([8, 8, img_width-9, img_height-9], outline=border_color, width=4)
    draw.rectangle([15, 15, img_width-16, img_height-16], outline=(80, 80, 80), width=2)
    
    # Draw title
    title_text = f"~ Hall of Fame ~"
    try:
        bbox = draw.textbbox((0, 0), title_text, font=title_font)
        title_w = bbox[2] - bbox[0]
    except:
        title_w = len(title_text) * 24
    
    # Draw centered title
    draw.text(((img_width - title_w) // 2, 30), title_text, fill=title_color, font=title_font)
    
    # Draw categories in columns
    x_positions = [padding, padding + col_width, padding + (col_width * 2)]
    
    for col_idx, assignments in enumerate(col_assignments):
        x = x_positions[col_idx]
        y = title_height + padding
        
        for cat_key, cat_data in assignments:
            cat_info = HOF_CATEGORIES.get(cat_key, {"name": cat_key.replace("_", " ").title(), "icon": "🏆", "color": (255, 215, 0)})
            members = cat_data.get("members", []) if isinstance(cat_data, dict) else cat_data
            
            # Draw emoji if available
            text_x = x
            if cat_key in emoji_images:
                emoji_img = emoji_images[cat_key]
                # Resize emoji to match new size
                emoji_img_resized = emoji_img.resize((emoji_size, emoji_size), Image.Resampling.LANCZOS)
                # Paste emoji with alpha channel
                img.paste(emoji_img_resized, (x, y - 4), emoji_img_resized)
                text_x = x + emoji_size + emoji_padding
            
            # Draw category header
            header_text = f"{cat_info['name']}"
            draw.text((text_x, y), header_text, fill=cat_info['color'], font=header_font)
            y += header_height
            
            # Draw members with proper bullet points
            if isinstance(members, list):
                for member in members:
                    # Draw gold dash/bullet
                    draw.text((x, y), "-", fill=bullet_color, font=text_font)
                    # Draw member name with offset
                    draw.text((x + 18, y), member, fill=text_color, font=text_font)
                    y += member_line_height
            elif isinstance(members, str):
                for member in members.split('\n'):
                    if member.strip():
                        draw.text((x, y), "-", fill=bullet_color, font=text_font)
                        draw.text((x + 18, y), member.strip(), fill=text_color, font=text_font)
                        y += member_line_height
            
            y += category_spacing  # Space between categories
    
    # Convert to RGB for PNG saving (remove alpha)
    rgb_img = Image.new('RGB', img.size, bg_color)
    rgb_img.paste(img, mask=img.split()[3] if img.mode == 'RGBA' else None)
    
    # Save to BytesIO
    output = io.BytesIO()
    rgb_img.save(output, format='PNG', quality=95)
    output.seek(0)
    return output

def generate_hof_image(categories_data: dict, title: str = "Hall of Fame") -> io.BytesIO:
    """Generate a Hall of Fame image from category data (sync version, no emoji support)"""
    if not PIL_AVAILABLE:
        return None
    
    # Image settings
    bg_color = (30, 30, 35)
    border_color = (255, 215, 0)
    text_color = (255, 255, 255)
    title_color = (255, 215, 0)
    bullet_color = (255, 215, 0)
    
    # Filter out empty categories
    categories_data = {k: v for k, v in categories_data.items() if v}
    
    if not categories_data:
        return None
    
    # Calculate dimensions - increased sizes
    num_cols = 3
    col_width = 450
    padding = 50
    title_height = 100
    member_line_height = 28
    category_spacing = 35
    header_height = 38
    
    # Calculate height needed for each column
    col_heights = [0, 0, 0]
    col_assignments = [[], [], []]
    
    for cat_key, members in categories_data.items():
        if not members:
            continue
        # Find shortest column
        min_col = col_heights.index(min(col_heights))
        member_count = len(members) if isinstance(members, list) else len(members.split('\n'))
        cat_height = header_height + (member_count * member_line_height) + category_spacing
        col_heights[min_col] += cat_height
        col_assignments[min_col].append((cat_key, members))
    
    max_col_height = max(col_heights) if col_heights else 400
    img_width = (col_width * num_cols) + (padding * 2)
    img_height = title_height + max_col_height + (padding * 2)
    img_height = max(img_height, 600)
    
    # Create image
    img = Image.new('RGB', (img_width, img_height), bg_color)
    draw = ImageDraw.Draw(img)
    
    # Load fonts - check fonts/ directory first (relative to bot), then system fonts
    bot_dir = os.path.dirname(os.path.abspath(__file__))
    font_paths = [
        (os.path.join(bot_dir, "fonts", "DejaVuSans-Bold.ttf"), os.path.join(bot_dir, "fonts", "DejaVuSans.ttf")),
        ("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
        ("arial.ttf", "arial.ttf"),
    ]
    
    title_font = header_font = text_font = None
    for bold_path, regular_path in font_paths:
        try:
            title_font = ImageFont.truetype(bold_path, 48)
            header_font = ImageFont.truetype(bold_path, 26)
            text_font = ImageFont.truetype(regular_path, 22)
            break
        except:
            continue
    
    if not title_font:
        title_font = ImageFont.load_default()
        header_font = ImageFont.load_default()
        text_font = ImageFont.load_default()
    
    # Draw border
    draw.rectangle([8, 8, img_width-9, img_height-9], outline=border_color, width=4)
    draw.rectangle([15, 15, img_width-16, img_height-16], outline=(80, 80, 80), width=2)
    
    # Draw title
    title_text = f"~ Hall of Fame ~"
    try:
        bbox = draw.textbbox((0, 0), title_text, font=title_font)
        title_w = bbox[2] - bbox[0]
    except:
        title_w = len(title_text) * 24
    
    # Draw centered title
    draw.text(((img_width - title_w) // 2, 30), title_text, fill=title_color, font=title_font)
    
    # Draw categories in columns
    x_positions = [padding, padding + col_width, padding + (col_width * 2)]
    
    for col_idx, assignments in enumerate(col_assignments):
        x = x_positions[col_idx]
        y = title_height + padding
        
        for cat_key, members in assignments:
            cat_info = HOF_CATEGORIES.get(cat_key, {"name": cat_key.replace("_", " ").title(), "icon": "🏆", "color": (255, 215, 0)})
            
            # Draw category header
            header_text = f"{cat_info['name']}"
            draw.text((x, y), header_text, fill=cat_info['color'], font=header_font)
            y += header_height
            
            # Draw members with proper bullet points
            if isinstance(members, list):
                for member in members:
                    draw.text((x, y), "-", fill=bullet_color, font=text_font)
                    draw.text((x + 18, y), member, fill=text_color, font=text_font)
                    y += member_line_height
            elif isinstance(members, str):
                for member in members.split('\n'):
                    if member.strip():
                        draw.text((x, y), "-", fill=bullet_color, font=text_font)
                        draw.text((x + 18, y), member.strip(), fill=text_color, font=text_font)
                        y += member_line_height
            
            y += category_spacing  # Space between categories
    
    # Save to BytesIO
    output = io.BytesIO()
    img.save(output, format='PNG', quality=95)
    output.seek(0)
    return output

# HOF Editor Modal
class HofEditModal(discord.ui.Modal):
    def __init__(self, guild_id: int, cat_key: str, cat_name: str, current_members: list, current_emoji: str = None):
        super().__init__(title="Edit Hall of Fame Category")
        self.guild_id = guild_id
        self.cat_key = cat_key
        
        self.members_input = discord.ui.TextInput(
            label=f"{cat_name} Members",
            style=discord.TextStyle.paragraph,
            placeholder="Player1\nPlayer2 | Alt\nPlayer3",
            required=False,
            max_length=2000,
            default="\n".join(current_members) if current_members else ""
        )
        self.add_item(self.members_input)
        
        # Add emoji input field
        self.emoji_input = discord.ui.TextInput(
            label="Category Emoji (Discord custom emoji)",
            style=discord.TextStyle.short,
            placeholder="<:emoji_name:123456789> or emoji ID",
            required=False,
            max_length=100,
            default=current_emoji or ""
        )
        self.add_item(self.emoji_input)
    
    async def on_submit(self, interaction: discord.Interaction):
        if self.guild_id not in hof_data_store:
            hof_data_store[self.guild_id] = {}
        
        members = [m.strip() for m in self.members_input.value.split('\n') if m.strip()]
        emoji_str = self.emoji_input.value.strip() if self.emoji_input.value else None
        
        # Store in new format with members and emoji
        hof_data_store[self.guild_id][self.cat_key] = {
            "members": members,
            "emoji_id": emoji_str
        }
        
        count = len(members)
        emoji_msg = f"\nEmoji: {emoji_str}" if emoji_str else ""
        await interaction.response.send_message(
            f"✅ **{self.cat_key.replace('_', ' ').title()}** updated with **{count}** members!{emoji_msg}\n"
            f"Use `/hofpreview` to see the current image or `/hofpost` to post it publicly.",
            ephemeral=True
        )

# Create category choices for slash commands (first 25)
HOF_CHOICES_1 = [
    app_commands.Choice(name=info["name"], value=key) 
    for key, info in list(HOF_CATEGORIES.items())[:25]
]
HOF_CHOICES_2 = [
    app_commands.Choice(name=info["name"], value=key) 
    for key, info in list(HOF_CATEGORIES.items())[25:]
]

@bot.tree.command(name="hofedit", description="Edit a Hall of Fame category")
@app_commands.describe(category="Select category to edit")
@app_commands.choices(category=HOF_CHOICES_1)
async def hofedit(i: discord.Interaction, category: str):
    cat_info = HOF_CATEGORIES.get(category, {"name": category})
    current_data = hof_data_store.get(i.guild.id, {}).get(category, {})
    # Handle both old format (list) and new format (dict)
    if isinstance(current_data, dict):
        current_members = current_data.get("members", [])
        current_emoji = current_data.get("emoji_id", "")
    else:
        current_members = current_data if isinstance(current_data, list) else []
        current_emoji = ""
    modal = HofEditModal(i.guild.id, category, cat_info["name"], current_members, current_emoji)
    await i.response.send_modal(modal)

@bot.tree.command(name="hofedit2", description="Edit Hall of Fame (more categories)")
@app_commands.describe(category="Select category to edit")
@app_commands.choices(category=HOF_CHOICES_2)
async def hofedit2(i: discord.Interaction, category: str):
    cat_info = HOF_CATEGORIES.get(category, {"name": category})
    current_data = hof_data_store.get(i.guild.id, {}).get(category, {})
    # Handle both old format (list) and new format (dict)
    if isinstance(current_data, dict):
        current_members = current_data.get("members", [])
        current_emoji = current_data.get("emoji_id", "")
    else:
        current_members = current_data if isinstance(current_data, list) else []
        current_emoji = ""
    modal = HofEditModal(i.guild.id, category, cat_info["name"], current_members, current_emoji)
    await i.response.send_modal(modal)

@bot.tree.command(name="hofcustom", description="Add a custom Hall of Fame category")
@app_commands.describe(
    category_name="Name for the custom category", 
    members="Members (comma separated)",
    emoji="Discord custom emoji (e.g. <:emoji:123456789>)"
)
async def hofcustom(i: discord.Interaction, category_name: str, members: str, emoji: str = None):
    if i.guild.id not in hof_data_store:
        hof_data_store[i.guild.id] = {}
    
    cat_key = category_name.lower().replace(" ", "_")
    if cat_key not in HOF_CATEGORIES:
        HOF_CATEGORIES[cat_key] = {"name": category_name, "icon": "🏆", "emoji_id": None, "color": (255, 215, 0)}
    
    member_list = [m.strip() for m in members.split(',') if m.strip()]
    hof_data_store[i.guild.id][cat_key] = {
        "members": member_list,
        "emoji_id": emoji.strip() if emoji else None
    }
    
    emoji_msg = f"\nEmoji: {emoji}" if emoji else ""
    await i.response.send_message(
        f"✅ Custom category **{category_name}** added with **{len(member_list)}** members!{emoji_msg}",
        ephemeral=True
    )

@bot.tree.command(name="hofpreview", description="Preview the Hall of Fame image (only you can see)")
async def hofpreview(i: discord.Interaction):
    if not PIL_AVAILABLE:
        await i.response.send_message("❌ Pillow library not installed. Run: `pip install Pillow`", ephemeral=True)
        return
    
    await i.response.defer(ephemeral=True)
    
    data = hof_data_store.get(i.guild.id, {})
    if not data or not any(data.values()):
        await i.followup.send("❌ No Hall of Fame data yet! Use `/hofedit` to add categories.", ephemeral=True)
        return
    
    # Use async generator to support Discord emoji fetching
    img_buffer = await generate_hof_image_async(data, i.guild.id)
    if not img_buffer:
        await i.followup.send("❌ Failed to generate image.", ephemeral=True)
        return
    
    file = discord.File(img_buffer, filename="hall_of_fame_preview.png")
    
    # Count stats - handle both old and new data formats
    total_entries = 0
    total_cats = 0
    for v in data.values():
        if isinstance(v, dict):
            members = v.get("members", [])
            if members:
                total_entries += len(members)
                total_cats += 1
        elif v:
            total_entries += len(v)
            total_cats += 1
    
    await i.followup.send(
        f"🏆 **Hall of Fame Preview**\n"
        f"Categories: **{total_cats}** | Total Entries: **{total_entries}**\n"
        f"Use `/hofpost` to post publicly!",
        file=file,
        ephemeral=True
    )

@bot.tree.command(name="hofpost", description="Post the Hall of Fame image publicly")
@app_commands.describe(channel="Channel to post in (optional, defaults to current)")
async def hofpost(i: discord.Interaction, channel: Optional[discord.TextChannel] = None):
    if not PIL_AVAILABLE:
        await i.response.send_message("❌ Pillow library not installed. Run: `pip install Pillow`", ephemeral=True)
        return
    
    await i.response.defer()
    
    data = hof_data_store.get(i.guild.id, {})
    if not data or not any(data.values()):
        await i.followup.send("❌ No Hall of Fame data yet! Use `/hofedit` to add categories.")
        return
    
    # Use async generator to support Discord emoji fetching
    img_buffer = await generate_hof_image_async(data, i.guild.id)
    if not img_buffer:
        await i.followup.send("❌ Failed to generate image.")
        return
    
    target_channel = channel or i.channel
    
    # Check bot permissions
    if not target_channel.permissions_for(i.guild.me).send_messages:
        await i.followup.send(f"❌ I don't have permission to send messages in {target_channel.mention}!")
        return
    if not target_channel.permissions_for(i.guild.me).attach_files:
        await i.followup.send(f"❌ I don't have permission to attach files in {target_channel.mention}!")
        return
    
    try:
        file = discord.File(img_buffer, filename="hall_of_fame.png")
        embed = create_embed("🏆 Hall of Fame 🏆", f"**{BOT_CONFIG['clan_name']}** Achievements", BOT_CONFIG["gold_color"])
        embed.set_image(url="attachment://hall_of_fame.png")
        
        await target_channel.send(embed=embed, file=file)
        
        if channel and channel != i.channel:
            await i.followup.send(f"✅ Hall of Fame posted in {channel.mention}!")
        else:
            await i.followup.send("✅ Hall of Fame posted!", ephemeral=True)
    except discord.Forbidden:
        await i.followup.send(f"❌ I don't have permission to post in {target_channel.mention}!")
    except Exception as e:
        await i.followup.send(f"❌ Failed to post: {e}")

@bot.tree.command(name="hofclear", description="Clear all Hall of Fame data")
async def hofclear(i: discord.Interaction):
    if i.guild.id in hof_data_store:
        hof_data_store[i.guild.id] = {}
    await i.response.send_message("✅ Hall of Fame data cleared!", ephemeral=True)

@bot.tree.command(name="hofemoji", description="Set a Discord emoji for a Hall of Fame category")
@app_commands.describe(
    category="Select category to set emoji for",
    emoji="Discord custom emoji (e.g. <:emoji:123456789>) or leave blank to clear"
)
@app_commands.choices(category=HOF_CHOICES_1)
async def hofemoji(i: discord.Interaction, category: str, emoji: str = None):
    if i.guild.id not in hof_data_store:
        hof_data_store[i.guild.id] = {}
    
    cat_info = HOF_CATEGORIES.get(category, {"name": category})
    current_data = hof_data_store.get(i.guild.id, {}).get(category, {})
    
    # Handle both old format (list) and new format (dict)
    if isinstance(current_data, dict):
        members = current_data.get("members", [])
    else:
        members = current_data if isinstance(current_data, list) else []
    
    # Update with emoji
    emoji_str = emoji.strip() if emoji else None
    hof_data_store[i.guild.id][category] = {
        "members": members,
        "emoji_id": emoji_str
    }
    
    if emoji_str:
        # Validate emoji format
        parsed = parse_emoji_string(emoji_str)
        if parsed:
            await i.response.send_message(
                f"✅ Emoji for **{cat_info['name']}** set to {emoji_str}\n"
                f"Use `/hofpreview` to see it in the image!",
                ephemeral=True
            )
        else:
            await i.response.send_message(
                f"⚠️ Emoji set to `{emoji_str}` but format may be invalid.\n"
                f"Use format: `<:name:123456789>` or just the emoji ID.\n"
                f"Use `/hofpreview` to test!",
                ephemeral=True
            )
    else:
        await i.response.send_message(
            f"✅ Emoji for **{cat_info['name']}** cleared.",
            ephemeral=True
        )

@bot.tree.command(name="hofemoji2", description="Set emoji for more Hall of Fame categories")
@app_commands.describe(
    category="Select category to set emoji for",
    emoji="Discord custom emoji (e.g. <:emoji:123456789>) or leave blank to clear"
)
@app_commands.choices(category=HOF_CHOICES_2)
async def hofemoji2(i: discord.Interaction, category: str, emoji: str = None):
    if i.guild.id not in hof_data_store:
        hof_data_store[i.guild.id] = {}
    
    cat_info = HOF_CATEGORIES.get(category, {"name": category})
    current_data = hof_data_store.get(i.guild.id, {}).get(category, {})
    
    # Handle both old format (list) and new format (dict)
    if isinstance(current_data, dict):
        members = current_data.get("members", [])
    else:
        members = current_data if isinstance(current_data, list) else []
    
    # Update with emoji
    emoji_str = emoji.strip() if emoji else None
    hof_data_store[i.guild.id][category] = {
        "members": members,
        "emoji_id": emoji_str
    }
    
    if emoji_str:
        parsed = parse_emoji_string(emoji_str)
        if parsed:
            await i.response.send_message(
                f"✅ Emoji for **{cat_info['name']}** set to {emoji_str}\n"
                f"Use `/hofpreview` to see it in the image!",
                ephemeral=True
            )
        else:
            await i.response.send_message(
                f"⚠️ Emoji set to `{emoji_str}` but format may be invalid.\n"
                f"Use format: `<:name:123456789>` or just the emoji ID.\n"
                f"Use `/hofpreview` to test!",
                ephemeral=True
            )
    else:
        await i.response.send_message(
            f"✅ Emoji for **{cat_info['name']}** cleared.",
            ephemeral=True
        )

@bot.tree.command(name="hoflist", description="List current Hall of Fame entries")
async def hoflist(i: discord.Interaction):
    data = hof_data_store.get(i.guild.id, {})
    if not data or not any(data.values()):
        await i.response.send_message("❌ No Hall of Fame data yet! Use `/hofedit` to add categories.", ephemeral=True)
        return
    
    embed = create_embed("🏆 Hall of Fame Data", "Current entries:")
    
    for cat_key, cat_data in data.items():
        # Handle both old format (list) and new format (dict)
        if isinstance(cat_data, dict):
            members = cat_data.get("members", [])
            emoji_id = cat_data.get("emoji_id", "")
        else:
            members = cat_data if isinstance(cat_data, list) else []
            emoji_id = ""
        
        if members:
            cat_info = HOF_CATEGORIES.get(cat_key, {"name": cat_key.replace("_", " ").title(), "icon": "🏆"})
            # Bullet point each member
            member_text = "\n".join(f"• {m}" for m in members[:10])
            if len(members) > 10:
                member_text += f"\n• ... (+{len(members) - 10} more)"
            
            # Show emoji info if set
            emoji_indicator = f" {emoji_id}" if emoji_id else ""
            embed.add_field(
                name=f"{cat_info.get('icon', '🏆')} {cat_info['name']} ({len(members)}){emoji_indicator}", 
                value=member_text or "None", 
                inline=False
            )
    
    await i.response.send_message(embed=embed, ephemeral=True)

# ==================== DUEL ARENA MINIGAME ====================

# Combat styles and their strengths/weaknesses
COMBAT_STYLES = {
    "melee": {"name": "Melee", "emoji": "⚔️", "strong": "ranged", "weak": "magic", "color": (255, 69, 0)},
    "ranged": {"name": "Ranged", "emoji": "🏹", "strong": "magic", "weak": "melee", "color": (0, 255, 127)},
    "magic": {"name": "Magic", "emoji": "✨", "strong": "melee", "weak": "ranged", "color": (138, 43, 226)},
}

# Special attacks
SPECIAL_ATTACKS = [
    {"name": "Dragon Claw Spec", "emoji": "🐉", "damage": (30, 50), "style": "melee"},
    {"name": "Dark Bow Spec", "emoji": "🌑", "damage": (25, 45), "style": "ranged"},
    {"name": "Guthix Staff Spec", "emoji": "💚", "damage": (20, 40), "style": "magic"},
    {"name": "AGS Spec", "emoji": "⚡", "damage": (35, 55), "style": "melee"},
    {"name": "Zaryte Bow Spec", "emoji": "🔮", "damage": (28, 48), "style": "ranged"},
    {"name": "Ice Barrage", "emoji": "❄️", "damage": (22, 38), "style": "magic"},
]

# Hit splats
HIT_SPLATS = ["💥", "⚡", "🔥", "💫", "✨"]

# Pending duel challenges
pending_duels = {}

class DuelView(View):
    def __init__(self, challenger: discord.Member, opponent: discord.Member):
        super().__init__(timeout=60)
        self.challenger = challenger
        self.opponent = opponent
        self.accepted = False
    
    @discord.ui.button(label="Accept Duel", style=discord.ButtonStyle.success, emoji="⚔️")
    async def accept(self, interaction: discord.Interaction, button: Button):
        if interaction.user.id != self.opponent.id:
            await interaction.response.send_message("This duel isn't for you!", ephemeral=True)
            return
        
        self.accepted = True
        self.stop()
        await interaction.response.defer()
    
    @discord.ui.button(label="Decline", style=discord.ButtonStyle.danger, emoji="❌")
    async def decline(self, interaction: discord.Interaction, button: Button):
        if interaction.user.id != self.opponent.id:
            await interaction.response.send_message("This duel isn't for you!", ephemeral=True)
            return
        
        self.accepted = False
        self.stop()
        await interaction.response.send_message(f"{self.opponent.display_name} declined the duel!", ephemeral=False)

def generate_duel_frame(
    player1_name: str, player2_name: str,
    player1_hp: int, player2_hp: int,
    max_hp: int, frame_num: int,
    action_text: str = "", hit_damage: int = 0,
    attacker: int = 0, winner: int = 0
) -> Image.Image:
    """Generate a single frame of the duel animation"""
    width, height = 500, 300
    
    # Create base image
    img = Image.new('RGB', (width, height), (20, 20, 30))
    draw = ImageDraw.Draw(img)
    
    # Try to load a font, fall back to default
    try:
        font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24)
        font_medium = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
        font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14)
    except:
        font_large = ImageFont.load_default()
        font_medium = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # Draw arena background - sand colored
    draw.rectangle([15, 50, width-15, height-15], fill=(194, 178, 128))
    
    # Draw arena border - wooden frame
    draw.rectangle([5, 5, width-5, height-5], outline=(101, 67, 33), width=5)
    draw.rectangle([12, 12, width-12, height-12], outline=(139, 90, 43), width=3)
    
    # Title bar
    draw.rectangle([0, 0, width, 45], fill=(50, 50, 60))
    title = "- DUEL ARENA -"
    draw.text((width//2, 25), title, fill=(255, 215, 0), font=font_large, anchor="mm")
    
    # Draw crossed swords icon (simple)
    draw.line([20, 15, 40, 35], fill=(192, 192, 192), width=3)
    draw.line([40, 15, 20, 35], fill=(192, 192, 192), width=3)
    draw.line([width-40, 15, width-20, 35], fill=(192, 192, 192), width=3)
    draw.line([width-20, 15, width-40, 35], fill=(192, 192, 192), width=3)
    
    # Player 1 (left side)
    p1_x, p1_y = 100, 150
    # Character color based on health
    p1_color = (0, 200, 0) if player1_hp > max_hp * 0.3 else (255, 100, 0) if player1_hp > 0 else (100, 100, 100)
    
    # Draw player 1 figure
    draw.ellipse([p1_x-20, p1_y-40, p1_x+20, p1_y], fill=p1_color)  # Head
    draw.rectangle([p1_x-15, p1_y, p1_x+15, p1_y+50], fill=p1_color)  # Body
    
    # Attack animation offset
    attack_offset = 0
    if attacker == 1 and frame_num % 2 == 0:
        attack_offset = 20
    
    # Sword for player 1
    draw.line([p1_x+15+attack_offset, p1_y+10, p1_x+45+attack_offset, p1_y-10], fill=(192, 192, 192), width=4)
    
    # Player 1 name and HP bar
    draw.text((p1_x, p1_y+70), player1_name[:12], fill=(50, 50, 50), font=font_medium, anchor="mm")
    
    # HP bar player 1
    hp_bar_width = 80
    hp_fill = int((player1_hp / max_hp) * hp_bar_width)
    draw.rectangle([p1_x-40, p1_y+85, p1_x+40, p1_y+100], fill=(50, 50, 50))
    draw.rectangle([p1_x-40, p1_y+85, p1_x+40, p1_y+100], outline=(0, 0, 0), width=2)
    if hp_fill > 0:
        hp_color = (0, 200, 0) if player1_hp > max_hp * 0.5 else (255, 165, 0) if player1_hp > max_hp * 0.25 else (200, 0, 0)
        draw.rectangle([p1_x-39, p1_y+86, p1_x-39+hp_fill, p1_y+99], fill=hp_color)
    draw.text((p1_x, p1_y+92), f"{player1_hp}/{max_hp}", fill=(255, 255, 255), font=font_small, anchor="mm")
    
    # Player 2 (right side)
    p2_x, p2_y = 400, 150
    p2_color = (0, 200, 0) if player2_hp > max_hp * 0.3 else (255, 100, 0) if player2_hp > 0 else (100, 100, 100)
    
    # Draw player 2 figure
    draw.ellipse([p2_x-20, p2_y-40, p2_x+20, p2_y], fill=p2_color)  # Head
    draw.rectangle([p2_x-15, p2_y, p2_x+15, p2_y+50], fill=p2_color)  # Body
    
    # Attack animation offset for player 2
    attack_offset2 = 0
    if attacker == 2 and frame_num % 2 == 0:
        attack_offset2 = -20
    
    # Sword for player 2 (facing left)
    draw.line([p2_x-15+attack_offset2, p2_y+10, p2_x-45+attack_offset2, p2_y-10], fill=(192, 192, 192), width=4)
    
    # Player 2 name and HP bar
    draw.text((p2_x, p2_y+70), player2_name[:12], fill=(50, 50, 50), font=font_medium, anchor="mm")
    
    # HP bar player 2
    hp_fill2 = int((player2_hp / max_hp) * hp_bar_width)
    draw.rectangle([p2_x-40, p2_y+85, p2_x+40, p2_y+100], fill=(50, 50, 50))
    draw.rectangle([p2_x-40, p2_y+85, p2_x+40, p2_y+100], outline=(0, 0, 0), width=2)
    if hp_fill2 > 0:
        hp_color2 = (0, 200, 0) if player2_hp > max_hp * 0.5 else (255, 165, 0) if player2_hp > max_hp * 0.25 else (200, 0, 0)
        draw.rectangle([p2_x-39, p2_y+86, p2_x-39+hp_fill2, p2_y+99], fill=hp_color2)
    draw.text((p2_x, p2_y+92), f"{player2_hp}/{max_hp}", fill=(255, 255, 255), font=font_small, anchor="mm")
    
    # VS text in center
    draw.text((width//2, p1_y), "VS", fill=(255, 50, 50), font=font_large, anchor="mm")
    
    # Draw hit splat if damage dealt
    if hit_damage > 0:
        target_x = p2_x if attacker == 1 else p1_x
        target_y = p1_y - 50 if attacker == 2 else p2_y - 50
        
        # Red hit splat - pointed star shape
        splat_size = 22
        draw.ellipse([target_x-splat_size, target_y-splat_size, target_x+splat_size, target_y+splat_size], fill=(180, 0, 0))
        # Inner circle
        draw.ellipse([target_x-splat_size+4, target_y-splat_size+4, target_x+splat_size-4, target_y+splat_size-4], fill=(220, 0, 0))
        draw.text((target_x, target_y), str(hit_damage), fill=(255, 255, 255), font=font_medium, anchor="mm")
    
    # Action text at bottom
    if action_text:
        # Draw text background
        draw.rectangle([20, height-55, width-20, height-20], fill=(40, 40, 50))
        draw.rectangle([20, height-55, width-20, height-20], outline=(100, 100, 100), width=1)
        draw.text((width//2, height-38), action_text, fill=(255, 255, 100), font=font_medium, anchor="mm")
    
    # Winner banner
    if winner > 0:
        winner_name = player1_name if winner == 1 else player2_name
        # Semi-transparent overlay effect
        draw.rectangle([40, 110, 460, 190], fill=(0, 80, 0))
        draw.rectangle([40, 110, 460, 190], outline=(255, 215, 0), width=4)
        draw.rectangle([45, 115, 455, 185], outline=(200, 170, 0), width=2)
        draw.text((width//2, 135), "VICTORY!", fill=(255, 215, 0), font=font_large, anchor="mm")
        draw.text((width//2, 165), f"{winner_name} WINS!", fill=(255, 255, 255), font=font_medium, anchor="mm")
    
    return img

def generate_duel_gif(player1_name: str, player2_name: str, battle_log: list) -> io.BytesIO:
    """Generate an animated GIF of the duel"""
    frames = []
    max_hp = 100
    p1_hp = max_hp
    p2_hp = max_hp
    
    # Opening frame
    frame = generate_duel_frame(player1_name, player2_name, p1_hp, p2_hp, max_hp, 0, "Fight!")
    frames.append(frame)
    
    # Battle frames
    for i, action in enumerate(battle_log):
        attacker = action["attacker"]
        damage = action["damage"]
        text = action["text"]
        
        if attacker == 1:
            p2_hp = max(0, p2_hp - damage)
        else:
            p1_hp = max(0, p1_hp - damage)
        
        # Attack frame with hit splat
        frame = generate_duel_frame(player1_name, player2_name, p1_hp, p2_hp, max_hp, i, text, damage, attacker)
        frames.append(frame)
        
        # Pause frame (no hit splat)
        frame = generate_duel_frame(player1_name, player2_name, p1_hp, p2_hp, max_hp, i+1, "")
        frames.append(frame)
    
    # Winner frame
    winner = 1 if p2_hp <= 0 else 2 if p1_hp <= 0 else 0
    if winner:
        for _ in range(3):  # Hold winner frame
            frame = generate_duel_frame(player1_name, player2_name, p1_hp, p2_hp, max_hp, 0, "", 0, 0, winner)
            frames.append(frame)
    
    # Save as GIF
    gif_buffer = io.BytesIO()
    frames[0].save(
        gif_buffer,
        format='GIF',
        save_all=True,
        append_images=frames[1:],
        duration=700,  # ms per frame
        loop=0
    )
    gif_buffer.seek(0)
    return gif_buffer

def simulate_duel(player1_name: str, player2_name: str) -> tuple:
    """Simulate a duel and return battle log and winner"""
    battle_log = []
    p1_hp = 100
    p2_hp = 100
    turn = random.choice([1, 2])  # Random first attacker
    
    attack_messages = [
        "{attacker} lands a solid hit!",
        "{attacker} strikes with fury!",
        "{attacker} attacks!",
        "{attacker} deals damage!",
        "{attacker} connects!",
    ]
    
    special_messages = [
        "{attacker} uses {special}!",
        "{attacker} unleashes {special}!",
    ]
    
    while p1_hp > 0 and p2_hp > 0:
        attacker_name = player1_name if turn == 1 else player2_name
        
        # 20% chance of special attack
        if random.random() < 0.2:
            special = random.choice(SPECIAL_ATTACKS)
            damage = random.randint(special["damage"][0], special["damage"][1])
            text = random.choice(special_messages).format(attacker=attacker_name[:10], special=special["name"])
        else:
            damage = random.randint(5, 25)
            text = random.choice(attack_messages).format(attacker=attacker_name[:10])
        
        # Apply damage
        if turn == 1:
            p2_hp = max(0, p2_hp - damage)
        else:
            p1_hp = max(0, p1_hp - damage)
        
        battle_log.append({
            "attacker": turn,
            "damage": damage,
            "text": f"{text} ({damage})"
        })
        
        # Switch turns
        turn = 2 if turn == 1 else 1
        
        # Limit battle length
        if len(battle_log) > 15:
            break
    
    winner = 1 if p2_hp <= 0 else 2
    return battle_log, winner

@bot.tree.command(name="duel", description="Challenge someone to a duel!")
@app_commands.describe(opponent="Who do you want to duel?")
async def duel(i: discord.Interaction, opponent: discord.Member):
    if not PIL_AVAILABLE:
        await i.response.send_message("❌ Duel system requires image generation (PIL not available).", ephemeral=True)
        return
    
    if opponent.id == i.user.id:
        await i.response.send_message("❌ You can't duel yourself!", ephemeral=True)
        return
    
    if opponent.bot:
        await i.response.send_message("❌ You can't duel a bot!", ephemeral=True)
        return
    
    # Create challenge embed
    embed = create_embed("⚔️ Duel Challenge!", 
        f"**{i.user.display_name}** has challenged **{opponent.display_name}** to a duel!\n\n"
        f"Do you accept the challenge?",
        0xFF4500
    )
    embed.set_thumbnail(url="https://runescape.wiki/images/Duel_Arena_icon.png")
    
    view = DuelView(i.user, opponent)
    await i.response.send_message(content=opponent.mention, embed=embed, view=view)
    
    # Wait for response
    await view.wait()
    
    if not view.accepted:
        return
    
    # Start the duel!
    await i.followup.send("⚔️ **The duel begins!** Generating battle...")
    
    # Simulate the duel
    battle_log, winner = simulate_duel(i.user.display_name, opponent.display_name)
    
    # Generate the GIF
    try:
        gif_buffer = generate_duel_gif(i.user.display_name, opponent.display_name, battle_log)
        
        winner_user = i.user if winner == 1 else opponent
        loser_user = opponent if winner == 1 else i.user
        
        # Create result embed
        result_embed = create_embed("⚔️ Duel Results",
            f"🏆 **{winner_user.display_name}** defeated **{loser_user.display_name}**!\n\n"
            f"Total hits: **{len(battle_log)}**",
            0xFFD700
        )
        
        file = discord.File(gif_buffer, filename="duel.gif")
        result_embed.set_image(url="attachment://duel.gif")
        
        await i.followup.send(embed=result_embed, file=file)
    except Exception as e:
        print(f"Duel GIF error: {e}")
        # Fallback to text-based result
        winner_user = i.user if winner == 1 else opponent
        await i.followup.send(f"⚔️ **{winner_user.display_name}** wins the duel!")

@bot.tree.command(name="quickduel", description="Instant duel result (no GIF)")
@app_commands.describe(opponent="Who do you want to duel?")
async def quickduel(i: discord.Interaction, opponent: discord.Member):
    if opponent.id == i.user.id:
        await i.response.send_message("❌ You can't duel yourself!", ephemeral=True)
        return
    
    if opponent.bot:
        await i.response.send_message("❌ You can't duel a bot!", ephemeral=True)
        return
    
    # Instant random result
    winner = random.choice([i.user, opponent])
    loser = opponent if winner == i.user else i.user
    
    damage_dealt = random.randint(50, 150)
    
    embed = create_embed("⚔️ Quick Duel!",
        f"**{i.user.display_name}** vs **{opponent.display_name}**\n\n"
        f"🏆 **{winner.display_name}** wins!\n"
        f"💀 {loser.display_name} was defeated\n"
        f"💥 Total damage: **{damage_dealt}**",
        0xFF4500
    )
    
    await i.response.send_message(embed=embed)


# ==================== SKILLING COMPETITION ====================

async def fetch_skill_xp(rsn: str, skill: str) -> Optional[int]:
    """Fetch current XP for a specific skill from hiscores"""
    data = await fetch_hiscores(rsn)
    if not data:
        return None
    
    if skill in data and "xp" in data[skill]:
        return data[skill]["xp"]
    return None

async def get_competition(guild_id: int):
    """Get active competition for a guild"""
    async with aiosqlite.connect(DATABASE) as db:
        cursor = await db.execute(
            "SELECT id, skill, title, start_time, end_time, created_by FROM competitions WHERE guild_id = ? AND end_time > ? ORDER BY start_time DESC LIMIT 1",
            (guild_id, datetime.now(timezone.utc).isoformat())
        )
        return await cursor.fetchone()

async def get_competition_participants(comp_id: int):
    """Get all participants and their XP data for a competition"""
    async with aiosqlite.connect(DATABASE) as db:
        cursor = await db.execute(
            "SELECT rsn, start_xp, current_xp FROM competition_participants WHERE competition_id = ?",
            (comp_id,)
        )
        return await cursor.fetchall()

@bot.tree.command(name="compstart", description="Start a new skilling competition")
@app_commands.describe(
    skill="The skill to track",
    title="Competition title",
    end_date="End date (DD/MM/YYYY format)",
    end_time="End time in game time (HH:MM format, e.g. 23:59)"
)
@app_commands.autocomplete(skill=skill_ac)
@app_commands.checks.has_permissions(administrator=True)
async def compstart(i: discord.Interaction, skill: str, title: str, end_date: str, end_time: str = "23:59"):
    # Validate skill
    if skill not in SKILLS[1:]:  # Exclude "Overall"
        await i.response.send_message(f"❌ Invalid skill. Choose from: {', '.join(SKILLS[1:])}", ephemeral=True)
        return
    
    # Parse end date/time
    try:
        end_dt = datetime.strptime(f"{end_date} {end_time}", "%d/%m/%Y %H:%M")
        end_dt = end_dt.replace(tzinfo=timezone.utc)
    except ValueError:
        await i.response.send_message("❌ Invalid date format. Use DD/MM/YYYY for date and HH:MM for time.", ephemeral=True)
        return
    
    if end_dt <= datetime.now(timezone.utc):
        await i.response.send_message("❌ End date must be in the future!", ephemeral=True)
        return
    
    # Check for existing active competition
    existing = await get_competition(i.guild.id)
    if existing:
        await i.response.send_message("❌ There's already an active competition! Use `/compend` to end it first.", ephemeral=True)
        return
    
    start_dt = datetime.now(timezone.utc)
    
    # Create competition
    async with aiosqlite.connect(DATABASE) as db:
        cursor = await db.execute(
            "INSERT INTO competitions (guild_id, skill, title, start_time, end_time, created_by) VALUES (?, ?, ?, ?, ?, ?)",
            (i.guild.id, skill, title, start_dt.isoformat(), end_dt.isoformat(), i.user.id)
        )
        comp_id = cursor.lastrowid
        await db.commit()
    
    # Get member count
    async with aiosqlite.connect(DATABASE) as db:
        cursor = await db.execute("SELECT COUNT(*) FROM clan_members WHERE guild_id = ?", (i.guild.id,))
        member_count = (await cursor.fetchone())[0]
    
    embed = create_embed(
        f"🏆 {title}",
        f"A new **{skill}** competition has started!",
        BOT_CONFIG["gold_color"]
    )
    embed.add_field(name="📊 Scope", value=skill, inline=True)
    embed.add_field(name="🕐 Start", value=f"{start_dt.strftime('%A, %d %B %Y %H:%M')}", inline=True)
    embed.add_field(name="🏁 End", value=f"{end_dt.strftime('%A, %d %B %Y %H:%M')}", inline=True)
    embed.add_field(name="👥 Clan Members", value=str(member_count), inline=True)
    embed.set_footer(text=f"Bot Created by Oogle. • Use /comprefresh to enroll all members!")
    
    if skill in SKILL_ICONS:
        embed.set_thumbnail(url=SKILL_ICONS[skill])
    
    await i.response.send_message(embed=embed)
    
    # Start background enrollment
    if member_count > 0:
        asyncio.create_task(enroll_clan_members_fast(i.guild.id, comp_id, skill, i.channel))

async def fetch_skill_xp_batch(rsns: list, skill: str, batch_size: int = 10) -> dict:
    """Fetch XP for multiple players concurrently"""
    results = {}
    
    async def fetch_one(rsn):
        xp = await fetch_skill_xp(rsn, skill)
        return rsn, xp
    
    # Process in batches
    for i in range(0, len(rsns), batch_size):
        batch = rsns[i:i + batch_size]
        tasks = [fetch_one(rsn) for rsn in batch]
        batch_results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for result in batch_results:
            if isinstance(result, tuple):
                rsn, xp = result
                results[rsn] = xp
        
        # Small delay between batches to avoid rate limiting
        if i + batch_size < len(rsns):
            await asyncio.sleep(1)
    
    return results

async def enroll_clan_members_fast(guild_id: int, comp_id: int, skill: str, channel):
    """Background task to enroll clan members using concurrent requests"""
    # Get all clan members
    async with aiosqlite.connect(DATABASE) as db:
        cursor = await db.execute("SELECT rsn FROM clan_members WHERE guild_id = ?", (guild_id,))
        members = await cursor.fetchall()
    
    if not members:
        try:
            await channel.send("❌ No clan members found! Use `/setclan` first.")
        except:
            pass
        return
    
    rsn_list = [rsn for (rsn,) in members]
    total = len(rsn_list)
    
    try:
        await channel.send(f"🔄 Enrolling **{total}** clan members... This may take a few minutes.")
    except:
        pass
    
    # Fetch all XP concurrently (10 at a time)
    xp_data = await fetch_skill_xp_batch(rsn_list, skill, batch_size=10)
    
    # Insert all into database
    registered = 0
    failed = 0
    
    async with aiosqlite.connect(DATABASE) as db:
        for rsn, xp in xp_data.items():
            if xp is not None:
                try:
                    await db.execute(
                        "INSERT OR IGNORE INTO competition_participants (competition_id, rsn, start_xp, current_xp) VALUES (?, ?, ?, ?)",
                        (comp_id, rsn, xp, xp)
                    )
                    registered += 1
                except:
                    failed += 1
            else:
                failed += 1
        await db.commit()
    
    try:
        await channel.send(f"✅ **Competition enrollment complete!**\n**Enrolled:** {registered} players\n**Failed:** {failed}")
    except:
        pass

@bot.tree.command(name="compupdate", description="Update competition XP for all participants")
@app_commands.checks.has_permissions(administrator=True)
async def compupdate(i: discord.Interaction):
    comp = await get_competition(i.guild.id)
    if not comp:
        await i.response.send_message("❌ No active competition!", ephemeral=True)
        return
    
    comp_id, skill, title, start_time, end_time, created_by = comp
    
    participants = await get_competition_participants(comp_id)
    
    await i.response.send_message(f"🔄 Updating XP for **{len(participants)}** participants in **{title}**...\nThis runs in the background.")
    
    asyncio.create_task(background_xp_update_fast(i.channel, comp_id, skill, participants))

async def background_xp_update_fast(channel, comp_id: int, skill: str, participants: list):
    """Background task to update XP for all participants using concurrent requests"""
    rsn_list = [rsn for rsn, _, _ in participants]
    
    # Fetch all XP concurrently
    xp_data = await fetch_skill_xp_batch(rsn_list, skill, batch_size=10)
    
    # Update database
    updated = 0
    failed = 0
    
    async with aiosqlite.connect(DATABASE) as db:
        for rsn, new_xp in xp_data.items():
            if new_xp is not None:
                try:
                    await db.execute(
                        "UPDATE competition_participants SET current_xp = ? WHERE competition_id = ? AND rsn = ?",
                        (new_xp, comp_id, rsn)
                    )
                    updated += 1
                except:
                    failed += 1
            else:
                failed += 1
        await db.commit()
    
    try:
        await channel.send(f"✅ **XP Update complete!**\n**Updated:** {updated}\n**Failed:** {failed}")
    except:
        pass

@bot.tree.command(name="compleaderboard", description="Show the competition leaderboard")
@app_commands.describe(top="Number of players to show (default 25)")
async def compleaderboard(i: discord.Interaction, top: int = 25):
    comp = await get_competition(i.guild.id)
    if not comp:
        await i.response.send_message("❌ No active competition!", ephemeral=True)
        return
    
    comp_id, skill, title, start_time, end_time, created_by = comp
    
    await i.response.defer()
    
    # Get current data (no inline update - use /compupdate for that)
    async with aiosqlite.connect(DATABASE) as db:
        cursor = await db.execute(
            "SELECT rsn, start_xp, current_xp FROM competition_participants WHERE competition_id = ? ORDER BY (current_xp - start_xp) DESC",
            (comp_id,)
        )
        results = await cursor.fetchall()
    
    if not results:
        await i.followup.send("❌ No participants yet! Use `/comprefresh` to enroll clan members.")
        return
    
    # Parse dates
    start_dt = datetime.fromisoformat(start_time)
    end_dt = datetime.fromisoformat(end_time)
    
    # Build leaderboard text
    embed = create_embed(f"🏆 {title}", f"**Scope:** {skill}", BOT_CONFIG["gold_color"])
    embed.add_field(name="Start", value=start_dt.strftime("%A, %d %B %Y %H:%M"), inline=True)
    embed.add_field(name="End", value=end_dt.strftime("%A, %d %B %Y %H:%M"), inline=True)
    embed.add_field(name="Players", value=str(len(results)), inline=True)
    
    # Create ASCII table - fixed formatting
    table_lines = ["```"]
    table_lines.append(f"{'#':<4} {'RSN':<14} {'XP Gained':>12}")
    table_lines.append("=" * 32)
    
    for idx, (rsn, start_xp, current_xp) in enumerate(results[:top], 1):
        xp_gained = (current_xp or 0) - (start_xp or 0)
        table_lines.append(f"{idx:<4} {rsn[:14]:<14} {xp_gained:>12,}")
    
    table_lines.append("```")
    
    embed.description += f"\n\n**Leaderboard (Top {min(top, len(results))})**\n" + "\n".join(table_lines)
    
    # Top 3 winners
    if len(results) >= 1:
        winners = []
        medals = ["🥇", "🥈", "🥉"]
        for idx, (rsn, start_xp, current_xp) in enumerate(results[:3]):
            xp_gained = (current_xp or 0) - (start_xp or 0)
            winners.append(f"{medals[idx]} **{rsn}** — **{xp_gained:,}** XP")
        embed.add_field(name="Winners", value="\n".join(winners), inline=False)
    
    if skill in SKILL_ICONS:
        embed.set_thumbnail(url=SKILL_ICONS[skill])
    
    embed.set_footer(text=f"Use /compupdate to refresh XP • {datetime.now(timezone.utc).strftime('%d/%m/%Y %H:%M')}")
    
    await i.followup.send(embed=embed)

@bot.tree.command(name="compinfo", description="Show current competition info")
async def compinfo(i: discord.Interaction):
    comp = await get_competition(i.guild.id)
    if not comp:
        await i.response.send_message("❌ No active competition!", ephemeral=True)
        return
    
    comp_id, skill, title, start_time, end_time, created_by = comp
    
    start_dt = datetime.fromisoformat(start_time)
    end_dt = datetime.fromisoformat(end_time)
    now = datetime.now(timezone.utc)
    
    time_left = end_dt - now
    days_left = time_left.days
    hours_left = time_left.seconds // 3600
    
    participants = await get_competition_participants(comp_id)
    
    embed = create_embed(f"🏆 {title}", "Competition Info", BOT_CONFIG["gold_color"])
    embed.add_field(name="📊 Scope", value=skill, inline=True)
    embed.add_field(name="👥 Players", value=str(len(participants)), inline=True)
    embed.add_field(name="⏰ Time Left", value=f"{days_left}d {hours_left}h", inline=True)
    embed.add_field(name="🕐 Start", value=start_dt.strftime("%a, %d %b %Y %H:%M"), inline=True)
    embed.add_field(name="🏁 End", value=end_dt.strftime("%a, %d %b %Y %H:%M"), inline=True)
    
    if skill in SKILL_ICONS:
        embed.set_thumbnail(url=SKILL_ICONS[skill])
    
    embed.set_footer(text="Use /compleaderboard to see rankings")
    
    await i.response.send_message(embed=embed)

@bot.tree.command(name="compcheck", description="Check your XP data in the competition")
@app_commands.describe(rsn="RSN to check (optional)")
async def compcheck(i: discord.Interaction, rsn: Optional[str] = None):
    if not rsn:
        rsn = await get_linked_rsn(i.user.id)
        if not rsn:
            await i.response.send_message("❌ No linked RSN. Provide one or use `/link` first.", ephemeral=True)
            return
    
    comp = await get_competition(i.guild.id)
    if not comp:
        await i.response.send_message("❌ No active competition!", ephemeral=True)
        return
    
    comp_id, skill, title, start_time, end_time, created_by = comp
    
    await i.response.defer(ephemeral=True)
    
    # Get stored data - try case insensitive match
    async with aiosqlite.connect(DATABASE) as db:
        cursor = await db.execute(
            "SELECT start_xp, current_xp, rsn FROM competition_participants WHERE competition_id = ? AND LOWER(rsn) = LOWER(?)",
            (comp_id, rsn)
        )
        row = await cursor.fetchone()
    
    if not row:
        # Show what RSNs we do have that are similar
        async with aiosqlite.connect(DATABASE) as db:
            cursor = await db.execute(
                "SELECT rsn FROM competition_participants WHERE competition_id = ? AND LOWER(rsn) LIKE ?",
                (comp_id, f"%{rsn.lower()[:5]}%")
            )
            similar = await cursor.fetchall()
        
        similar_text = ", ".join([r[0] for r in similar[:5]]) if similar else "None found"
        await i.followup.send(f"❌ **{rsn}** is not in the competition!\n\nSimilar RSNs in competition: {similar_text}", ephemeral=True)
        return
    
    start_xp, stored_current_xp, stored_rsn = row
    
    # Fetch live XP
    live_xp = await fetch_skill_xp(rsn, skill)
    
    # Also fetch raw hiscores data for debug
    raw_data = await fetch_hiscores(rsn)
    
    embed = create_embed(f"🔍 Competition Check: {stored_rsn}", f"**{title}** - {skill}", BOT_CONFIG["primary_color"])
    embed.add_field(name="Starting XP", value=f"{start_xp:,}" if start_xp else "N/A", inline=True)
    embed.add_field(name="Stored Current XP", value=f"{stored_current_xp:,}" if stored_current_xp else "N/A", inline=True)
    embed.add_field(name="Live XP (API)", value=f"{live_xp:,}" if live_xp else "Failed to fetch", inline=True)
    
    if start_xp and live_xp:
        gained = live_xp - start_xp
        embed.add_field(name="XP Gained", value=f"{gained:,}", inline=True)
    
    # Debug info
    if raw_data and skill in raw_data:
        embed.add_field(name="Debug - API Response", value=f"Skill: {skill}\nXP: {raw_data[skill].get('xp', 'N/A')}", inline=False)
    elif raw_data:
        embed.add_field(name="Debug - API Response", value=f"Skill '{skill}' not found in data. Available: {list(raw_data.keys())[:5]}...", inline=False)
    else:
        embed.add_field(name="Debug - API Response", value="Failed to fetch hiscores data", inline=False)
    
    await i.followup.send(embed=embed, ephemeral=True)

@bot.tree.command(name="testxp", description="Test XP fetch for a player (debug)")
@app_commands.describe(rsn="RSN to test", skill="Skill to check")
async def testxp(i: discord.Interaction, rsn: str, skill: str = "Fishing"):
    await i.response.defer(ephemeral=True)
    
    # Fetch hiscores
    data = await fetch_hiscores(rsn)
    
    if not data:
        await i.followup.send(f"❌ Failed to fetch hiscores for **{rsn}**", ephemeral=True)
        return
    
    if skill in data:
        xp = data[skill]["xp"]
        level = data[skill]["level"]
        rank = data[skill]["rank"]
        await i.followup.send(f"✅ **{rsn}** - {skill}\n**Level:** {level}\n**XP:** {xp:,}\n**Rank:** {rank:,}", ephemeral=True)
    else:
        await i.followup.send(f"❌ Skill **{skill}** not found. Available skills: {', '.join(list(data.keys())[:10])}...", ephemeral=True)

@bot.tree.command(name="compend", description="End the current competition and show final results")
@app_commands.describe(channel="Channel to post final results (optional)")
@app_commands.checks.has_permissions(administrator=True)
async def compend(i: discord.Interaction, channel: Optional[discord.TextChannel] = None):
    comp = await get_competition(i.guild.id)
    if not comp:
        await i.response.send_message("❌ No active competition!", ephemeral=True)
        return
    
    comp_id, skill, title, start_time, end_time, created_by = comp
    
    participants = await get_competition_participants(comp_id)
    
    await i.response.send_message(f"🔄 Finalizing **{title}**... Updating XP for **{len(participants)}** participants.")
    
    # Run final update in background then post results
    target_channel = channel or i.channel
    asyncio.create_task(finalize_competition(i.channel, target_channel, comp_id, skill, title, start_time, participants))

async def finalize_competition(notify_channel, results_channel, comp_id: int, skill: str, title: str, start_time: str, participants: list):
    """Background task to finalize competition with fast batch update"""
    # Fast batch XP update
    rsn_list = [rsn for rsn, _, _ in participants]
    xp_data = await fetch_skill_xp_batch(rsn_list, skill, batch_size=10)
    
    # Update database
    async with aiosqlite.connect(DATABASE) as db:
        for rsn, new_xp in xp_data.items():
            if new_xp is not None:
                await db.execute(
                    "UPDATE competition_participants SET current_xp = ? WHERE competition_id = ? AND rsn = ?",
                    (new_xp, comp_id, rsn)
                )
        
        # Mark competition as ended
        await db.execute("UPDATE competitions SET ended = 1, end_time = ? WHERE id = ?", 
                        (datetime.now(timezone.utc).isoformat(), comp_id))
        await db.commit()
    
    # Get final results
    async with aiosqlite.connect(DATABASE) as db:
        cursor = await db.execute(
            "SELECT rsn, start_xp, current_xp FROM competition_participants WHERE competition_id = ? ORDER BY (current_xp - start_xp) DESC",
            (comp_id,)
        )
        results = await cursor.fetchall()
    
    start_dt = datetime.fromisoformat(start_time)
    end_dt = datetime.now(timezone.utc)
    
    # Build final results embed
    embed = create_embed(f"🏆 {title} — Final Results", f"**Scope:** {skill}", BOT_CONFIG["gold_color"])
    embed.add_field(name="Start", value=start_dt.strftime("%A, %d %B %Y %H:%M"), inline=True)
    embed.add_field(name="End", value=end_dt.strftime("%A, %d %B %Y %H:%M"), inline=True)
    embed.add_field(name="Players", value=str(len(results)), inline=True)
    
    # ASCII table - fixed formatting
    table_lines = ["```"]
    table_lines.append(f"{'#':<4} {'RSN':<14} {'XP Gained':>12}")
    table_lines.append("=" * 32)
    
    for idx, (rsn, start_xp, current_xp) in enumerate(results[:25], 1):
        xp_gained = (current_xp or 0) - (start_xp or 0)
        table_lines.append(f"{idx:<4} {rsn[:14]:<14} {xp_gained:>12,}")
    
    table_lines.append("```")
    
    embed.description += f"\n\n**Final Leaderboard (Top 25)**\n" + "\n".join(table_lines)
    
    # Winners section
    if len(results) >= 1:
        winners = []
        medals = ["🥇", "🥈", "🥉"]
        for idx, (rsn, start_xp, current_xp) in enumerate(results[:3]):
            xp_gained = (current_xp or 0) - (start_xp or 0)
            winners.append(f"{medals[idx]} **{rsn}** — **{xp_gained:,}** XP")
        embed.add_field(name="Winners", value="\n".join(winners), inline=False)
    
    if skill in SKILL_ICONS:
        embed.set_thumbnail(url=SKILL_ICONS[skill])
    
    embed.set_footer(text=f"Competition Ended • Bot Created by Oogle. • {end_dt.strftime('%d/%m/%Y %H:%M')}")
    
    try:
        await results_channel.send(embed=embed)
        if notify_channel != results_channel:
            await notify_channel.send(f"✅ Competition ended! Final results posted in {results_channel.mention}")
    except Exception as e:
        print(f"Error posting competition results: {e}")

@bot.tree.command(name="compadd", description="Add a player to the active competition")
@app_commands.describe(rsn="RSN to add")
@app_commands.checks.has_permissions(administrator=True)
async def compadd(i: discord.Interaction, rsn: str):
    comp = await get_competition(i.guild.id)
    if not comp:
        await i.response.send_message("❌ No active competition!", ephemeral=True)
        return
    
    comp_id, skill, title, start_time, end_time, created_by = comp
    
    await i.response.defer(ephemeral=True)
    
    # Get current XP
    xp = await fetch_skill_xp(rsn, skill)
    if xp is None:
        await i.followup.send(f"❌ Couldn't fetch {skill} XP for **{rsn}**. Check the name is correct.", ephemeral=True)
        return
    
    async with aiosqlite.connect(DATABASE) as db:
        try:
            await db.execute(
                "INSERT INTO competition_participants (competition_id, rsn, start_xp, current_xp) VALUES (?, ?, ?, ?)",
                (comp_id, rsn, xp, xp)
            )
            await db.commit()
            await i.followup.send(f"✅ **{rsn}** added to **{title}**!\nStarting {skill} XP: **{xp:,}**", ephemeral=True)
        except aiosqlite.IntegrityError:
            await i.followup.send(f"⚠️ **{rsn}** is already in this competition!", ephemeral=True)

@bot.tree.command(name="comprefresh", description="Sync competition with clan roster (add new, remove left)")
@app_commands.checks.has_permissions(administrator=True)
async def comprefresh(i: discord.Interaction):
    comp = await get_competition(i.guild.id)
    if not comp:
        await i.response.send_message("❌ No active competition!", ephemeral=True)
        return
    
    comp_id, skill, title, start_time, end_time, created_by = comp
    
    # Get all clan members
    async with aiosqlite.connect(DATABASE) as db:
        cursor = await db.execute("SELECT rsn FROM clan_members WHERE guild_id = ?", (i.guild.id,))
        members = await cursor.fetchall()
    
    if not members:
        await i.response.send_message("❌ No clan members found! Use `/setclan` first to populate the clan list.", ephemeral=True)
        return
    
    clan_rsns = {rsn for (rsn,) in members}
    
    # Get existing participants
    async with aiosqlite.connect(DATABASE) as db:
        cursor = await db.execute(
            "SELECT rsn FROM competition_participants WHERE competition_id = ?",
            (comp_id,)
        )
        existing = {row[0] for row in await cursor.fetchall()}
    
    # Find new members and members who left
    new_members = clan_rsns - existing
    left_members = existing - clan_rsns
    
    await i.response.send_message(
        f"🔄 **Syncing competition with clan roster...**\n"
        f"**New members to add:** {len(new_members)}\n"
        f"**Left members to remove:** {len(left_members)}\n"
        f"This runs in the background."
    )
    
    asyncio.create_task(background_sync_fast(i.channel, comp_id, skill, list(new_members), list(left_members)))

async def background_sync_fast(channel, comp_id: int, skill: str, new_members: list, left_members: list):
    """Background task to sync competition with clan roster"""
    added = 0
    failed = 0
    removed = 0
    
    # Remove members who left the clan
    if left_members:
        async with aiosqlite.connect(DATABASE) as db:
            for rsn in left_members:
                await db.execute(
                    "DELETE FROM competition_participants WHERE competition_id = ? AND rsn = ?",
                    (comp_id, rsn)
                )
                removed += 1
            await db.commit()
    
    # Add new members using fast batch fetch
    if new_members:
        xp_data = await fetch_skill_xp_batch(new_members, skill, batch_size=10)
        
        async with aiosqlite.connect(DATABASE) as db:
            for rsn, xp in xp_data.items():
                if xp is not None:
                    try:
                        await db.execute(
                            "INSERT OR IGNORE INTO competition_participants (competition_id, rsn, start_xp, current_xp) VALUES (?, ?, ?, ?)",
                            (comp_id, rsn, xp, xp)
                        )
                        added += 1
                    except:
                        failed += 1
                else:
                    failed += 1
            await db.commit()
    
    try:
        await channel.send(
            f"✅ **Competition sync complete!**\n"
            f"**Added:** {added}\n"
            f"**Removed:** {removed}\n"
            f"**Failed:** {failed}"
        )
    except:
        pass

@bot.tree.command(name="compcancel", description="Cancel the current competition without posting results")
@app_commands.checks.has_permissions(administrator=True)
async def compcancel(i: discord.Interaction):
    comp = await get_competition(i.guild.id)
    if not comp:
        await i.response.send_message("❌ No active competition!", ephemeral=True)
        return
    
    comp_id, skill, title, start_time, end_time, created_by = comp
    
    async with aiosqlite.connect(DATABASE) as db:
        await db.execute("DELETE FROM competition_participants WHERE competition_id = ?", (comp_id,))
        await db.execute("DELETE FROM competitions WHERE id = ?", (comp_id,))
        await db.commit()
    
    await i.response.send_message(f"✅ Competition **{title}** has been cancelled.", ephemeral=True)

def main():
    if BOT_TOKEN == "YOUR_BOT_TOKEN_HERE": print("ERROR: Set your bot token!"); return
    bot.run(BOT_TOKEN)

if __name__ == "__main__": main()
