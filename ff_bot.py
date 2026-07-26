import requests
import telebot
from telebot import types
from datetime import datetime
import time
import logging
import json
import urllib.parse
import os
import sys
import threading

# ============================================================
# CONFIGURATION
# ============================================================
API_TOKEN = "8965483066:AAEhcH7o2TwOGfufQIKDOnJSgXbh3T0I0n4"  # <-- Apna token yahan daalo
BOT_USERNAME = "ffcollectioninfo_bot"   # <-- Apna bot username (without @)

# ============================================================
# LOGGING
# ============================================================
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# ============================================================
# PREMIUM EMOJI MAPPING (Complete)
# ============================================================
EMOJI_MAPPING = {
    "✅": ["6246537187614005254", "6246782404476803545", "6010060634803148161", "6010498532488778300"],
    "✔️": ["6246871001062185760", "6010264538375525668", "6010487760710800947"],
    "☑️": ["6246537187614005254", "6010097953773983121"],
    "👁️": ["6035338338406242050", "6035051267087143217", "6034945975963881533", "6034845323405299835"],
    "👁": ["6035338338406242050", "6035051267087143217"],
    "👀": ["6035225389356290238", "6035081585261287115", "6035243995154616907", "6035173858338672933"],
    "🔥": ["4956222745814762495", "4956606007221421405", "4956429969396859866", "6086954744268460848"],
    "💥": ["6032673796530377389", "4958479549265347295"],
    "⚡": ["5791970059597386804", "6087079590377820415", "6095843123252957701"],
    "❤️": ["5783157259152397008", "5801084710343938087", "6010280773351904888"],
    "💙": ["5780496071645991525", "6104780447684757396"],
    "💚": ["5888789252493283486"],
    "💛": ["5840261097719148872"],
    "🧡": ["5840263144212529797"],
    "💜": ["5840265018655703965"],
    "🖤": ["5840266939932994956"],
    "⭐": ["6244496562752331516", "5904618938578243567", "6010193314932855525"],
    "🌟": ["6010156854955480259", "6086924086791902713"],
    "✨": ["6010338729640596556", "6010086134023985536", "5801044672658805468"],
    "🧛": ["6034871295072539452", "6035251193519805118", "6032673796530377389"],
    "👑": ["5794422335599546668", "6089003761496232797", "6247039939305808563"],
    "💰": ["6089104607328342288", "6086730718774300509", "6086664791026307819"],
    "💵": ["6089140105233044310"],
    "💎": ["6086778246882399112", "5791697221799907788"],
    "👍": ["6089313931149448495", "4958626617535497157", "4956582500865410174"],
    "👎": ["6088789257285988672"],
    "👏": ["6093744967304352336", "4956582500865410174"],
    "😀": ["6093864814071780526", "6093922327978840798"],
    "😁": ["6035060329468137931"],
    "😂": ["5782741660936966676", "5782746664573867142"],
    "😃": ["6035337951859184840"],
    "😄": ["5782942227319756256"],
    "😅": ["5782670102486848559"],
    "😆": ["5782670102486848559"],
    "😉": ["6089024570612781324"],
    "😊": ["5780690182692935276"],
    "😍": ["6010179687001625256"],
    "🥰": ["6044369013952222465", "6044359320211034681"],
    "😘": ["6044373012566774137"],
    "😎": ["6032853480782172520", "6044373012566774137"],
    "😢": ["5780793884678296697"],
    "😭": ["5783024321324651865"],
    "😤": ["6034865170449175739", "6034855438053282213"],
    "😠": ["6035355642829475999", "6034843326245508065"],
    "😡": ["6035355642829475999"],
    "🤔": ["5782756916660802905", "5783034045130610245", "6093666528316625608"],
}

FLAG_MAPPING = {
    "🇺🇸": "5433865586356531140", "🇬🇧": "5433827537241258614", "🇫🇷": "5433636707549331311",
    "🇩🇪": "5433845881046578644", "🇮🇳": "5433601609076586221", "🇯🇵": "5434147542369579483",
    "🇨🇳": "5435996255207567113", "🇷🇺": "5433674924168328689", "🇧🇷": "5433825269498525925",
    "🇮🇹": "5433627189901801019", "🇨🇦": "5433979415874779870", "🇦🇺": "5434067655977874913",
    "🇰🇷": "5434142701941437163", "🇪🇸": "5434026158003862063", "🇲🇽": "5434131139889478358",
    "🇮🇩": "5431739800883312139", "🇳🇱": "5431656358258685474", "🇹🇷": "5433792911214917126",
    "🇸🇦": "5433991338703991663", "🇦🇪": "5434013938821902926", "🇿🇦": "5431489619038320862",
    "🇵🇰": "5434064563601421981", "🇧🇩": "5433854239052935880",
    "🇱🇰": "5433609855413794108", "🇳🇵": "5433852744404317916", "🇲🇾": "5431620340662940910",
    "🇸🇬": "5433884376838454074", "🇵🇭": "5434119663736862995", "🇻🇳": "5431676201007592926",
    "🇹🇭": "5433814347396692144", "🇪🇬": "5433643519367461444", "🇳🇬": "5433982207603520017",
    "🇰🇪": "5433845881046578644", "🇦🇷": "5433845881046578644", "🇨🇱": "5433827537241258614",
    "🇵🇪": "5433827537241258614", "🇨🇴": "5433825269498525925", "🇻🇪": "5433767976937585990",
    "🇵🇹": "5433598722858562967", "🇸🇪": "5433628435442316429", "🇳🇴": "5434098446598419585",
    "🇩🇰": "5434129692485498098", "🇫🇮": "5434115081006756195", "🇮🇪": "5434012796360604182",
    "🇨🇭": "5433902785068283672", "🇦🇹": "5434027579638035690", "🇧🇪": "5431755073787016798",
    "🇬🇷": "5433972762970437003", "🇨🇿": "5434115081006756195", "🇭🇺": "5434001565021123877",
    "🇵🇱": "5433833485770964033", "🇷🇴": "5434132406904830055", "🇺🇦": "5434132406904830055",
}

ALL_PREMIUM_EMOJIS = list(set(
    [id for ids in EMOJI_MAPPING.values() for id in ids] +
    [id for ids in FLAG_MAPPING.values() for id in ids]
))

DEFAULT_EMOJI_ID = "6035338338406242050"

def get_premium_emoji_for_normal_emoji(normal_emoji: str) -> str:
    # Direct lookup
    if normal_emoji in EMOJI_MAPPING:
        return EMOJI_MAPPING[normal_emoji][0]
    if normal_emoji in FLAG_MAPPING:
        return FLAG_MAPPING[normal_emoji]
    # Try without variation selector
    norm = normal_emoji.replace('\ufe0f', '').replace('\ufe0e', '').replace('\u200d', '')
    if norm in EMOJI_MAPPING:
        return EMOJI_MAPPING[norm][0]
    if norm in FLAG_MAPPING:
        return FLAG_MAPPING[norm]
    return DEFAULT_EMOJI_ID

def format_premium(text: str) -> str:
    """Convert normal emojis to premium telegram emojis"""
    import re
    emoji_pattern = re.compile(
        "(["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F1E0-\U0001F1FF"  # flags (iOS)
        "\U00002702-\U000027B0"
        "\U000024C2-\U0001F251"
        "]+)"
    )
    def replace_emoji(match):
        emoji = match.group(0)
        premium_id = get_premium_emoji_for_normal_emoji(emoji)
        return f'<tg-emoji emoji-id="{premium_id}">{emoji}</tg-emoji>'
    return emoji_pattern.sub(replace_emoji, text)

# ============================================================
# STYLISH TEXT FUNCTION
# ============================================================
def stylish(text: str) -> str:
    STYLISH_MAP = {
        'A': '𝐀', 'B': '𝐁', 'C': '𝐂', 'D': '𝐃', 'E': '𝐄', 'F': '𝐅', 'G': '𝐆',
        'H': '𝐇', 'I': '𝐈', 'J': '𝐉', 'K': '𝐊', 'L': '𝐋', 'M': '𝐌', 'N': '𝐍',
        'O': '𝐎', 'P': '𝐏', 'Q': '𝐐', 'R': '𝐑', 'S': '𝐒', 'T': '𝐓', 'U': '𝐔',
        'V': '𝐕', 'W': '𝐖', 'X': '𝐗', 'Y': '𝐘', 'Z': '𝐙',
        'a': '𝐚', 'b': '𝐛', 'c': '𝐜', 'd': '𝐝', 'e': '𝐞', 'f': '𝐟',
        'g': '𝐠', 'h': '𝐡', 'i': '𝐢', 'j': '𝐣', 'k': '𝐤', 'l': '𝐥',
        'm': '𝐦', 'n': '𝐧', 'o': '𝐨', 'p': '𝐩', 'q': '𝐪', 'r': '𝐫',
        's': '𝐬', 't': '𝐭', 'u': '𝐮', 'v': '𝐯', 'w': '𝐰', 'x': '𝐱',
        'y': '𝐲', 'z': '𝐳',
        '0': '𝟎', '1': '𝟏', '2': '𝟐', '3': '𝟑', '4': '𝟒',
        '5': '𝟓', '6': '𝟔', '7': '𝟕', '8': '𝟖', '9': '𝟗'
    }
    return ''.join(STYLISH_MAP.get(c, c) for c in text)

# ============================================================
# API CONFIG
# ============================================================
PLAYER_INFO_API = "https://info.killersharmabot.online/player-info?uid={uid}"
OUTFIT_API_URL = "https://image.killersharmabot.online/outfit-image?avatar_id={avatar_id}&clothes={clothes}"
BANNER_API_URL = "https://image.killersharmabot.online/banner-image?headPic={headPic}&bannerId={bannerId}&name={name}&level={level}&guild={guild}&pinId={pinId}&celebrity={celebrity}&frame={frame}"
AVATAR_API_URL = "https://ffoutfitapis.vercel.app/avatar-image?uid={uid}&region={region}&key=99day"

# ============================================================
# HELPER FUNCTIONS
# ============================================================
def is_valid_uid(uid):
    return uid.isdigit() and 8 <= len(uid) <= 11

def escape_markdown(text):
    escape_chars = '_*[]()~`>#+-=|{}.!'
    return ''.join(['\\' + char if char in escape_chars else char for char in str(text)])

def format_timestamp(ts):
    try:
        if ts and ts != 'ɴ/ᴀ' and ts != '':
            return datetime.utcfromtimestamp(int(ts)).strftime('%d-%m-%Y %H:%M:%S')
        return 'ɴ/ᴀ'
    except:
        return 'ɴ/ᴀ'

def encode_for_url(text):
    if text and text != 'ɴ/ᴀ':
        return urllib.parse.quote(str(text))
    return ''

# ============================================================
# API FUNCTIONS
# ============================================================
def get_player_info(uid):
    try:
        url = PLAYER_INFO_API.format(uid=uid)
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            data = response.json()
            if 'basicInfo' in data:
                basic = data['basicInfo']
                captain = data.get('captainBasicInfo', {})
                clan = data.get('clanBasicInfo', {})
                credit = data.get('creditScoreInfo', {})
                pet = data.get('petInfo', {})
                profile = data.get('profileInfo', {})
                social = data.get('socialInfo', {})
                clothes_ids = profile.get('clothes', [])
                avatar_id = profile.get('avatarId', '')
                return {
                    "success": True,
                    "nickname": basic.get('nickname', 'ɴ/ᴀ'),
                    "region": basic.get('region', 'ɴ/ᴀ'),
                    "level": basic.get('level', 'ɴ/ᴀ'),
                    "likes": basic.get('liked', 'ɴ/ᴀ'),
                    "uid": basic.get('accountId', uid),
                    "rank": basic.get('rankingName', 'ɴ/ᴀ'),
                    "rank_points": basic.get('rankingPoints', 'ɴ/ᴀ'),
                    "ban_status": basic.get('banStatus', 'Not Banned'),
                    "title": basic.get('titleName', 'ɴ/ᴀ'),
                    "headpic": basic.get('headPic', 'ɴ/ᴀ'),
                    "headpic_name": basic.get('headPicName', 'ɴ/ᴀ'),
                    "banner": basic.get('bannerName', 'ɴ/ᴀ'),
                    "banner_id": basic.get('bannerId', 'ɴ/ᴀ'),
                    "last_login": basic.get('lastLoginAt', 'ɴ/ᴀ'),
                    "create_at": basic.get('createAt', 'ɴ/ᴀ'),
                    "exp": basic.get('exp', 'ɴ/ᴀ'),
                    "exp_needed": basic.get('expNeeded', 'ɴ/ᴀ'),
                    "level_progress": basic.get('levelProgress', 'ɴ/ᴀ'),
                    "badge_cnt": basic.get('badgeCnt', 'ɴ/ᴀ'),
                    "badge_id": basic.get('badgeId', 'ɴ/ᴀ'),
                    "pin_name": basic.get('pinName', 'ɴ/ᴀ'),
                    "pin_id": basic.get('pinId', 'ɴ/ᴀ'),
                    "equipped_gun": basic.get('equippedGunName', 'ɴ/ᴀ'),
                    "equipped_animation": basic.get('equippedAnimationName', 'ɴ/ᴀ'),
                    "release_version": basic.get('releaseVersion', 'ɴ/ᴀ'),
                    "season_id": basic.get('seasonId', 'ɴ/ᴀ'),
                    "cs_rank": basic.get('csRankingName', 'ɴ/ᴀ'),
                    "max_rank": basic.get('maxRank', 'ɴ/ᴀ'),
                    "prime_level": basic.get('primeLevel', {}).get('level', 'ɴ/ᴀ'),
                    "avatar_id": avatar_id,
                    "clothes_ids": clothes_ids,
                    "clothes_names": profile.get('clothesNames', []),
                    "captain_nickname": captain.get('nickname', 'ɴ/ᴀ'),
                    "captain_uid": captain.get('accountId', 'ɴ/ᴀ'),
                    "captain_level": captain.get('level', 'ɴ/ᴀ'),
                    "captain_likes": captain.get('liked', 'ɴ/ᴀ'),
                    "captain_rank": captain.get('rankingName', 'ɴ/ᴀ'),
                    "captain_banner": captain.get('bannerName', 'ɴ/ᴀ'),
                    "captain_headpic": captain.get('headPicName', 'ɴ/ᴀ'),
                    "clan_name": clan.get('clanName', 'ɴ/ᴀ'),
                    "clan_id": clan.get('clanId', 'ɴ/ᴀ'),
                    "clan_level": clan.get('clanLevel', 'ɴ/ᴀ'),
                    "clan_members": clan.get('memberNum', 'ɴ/ᴀ'),
                    "clan_captain": clan.get('captainId', 'ɴ/ᴀ'),
                    "credit_score": credit.get('creditScore', 'ɴ/ᴀ'),
                    "credit_status": credit.get('rewardState', 'ɴ/ᴀ'),
                    "pet_name": pet.get('petName', 'ɴ/ᴀ'),
                    "pet_level": pet.get('level', 'ɴ/ᴀ'),
                    "pet_skin": pet.get('skinName', 'ɴ/ᴀ'),
                    "pet_skill": pet.get('skillName', 'ɴ/ᴀ'),
                    "avatar_name": profile.get('avatarName', 'ɴ/ᴀ'),
                    "skills": profile.get('equippedSkillsNames', 'ɴ/ᴀ'),
                    "language": social.get('language', 'ɴ/ᴀ'),
                    "signature": social.get('signature', 'ɴ/ᴀ'),
                    "time_online": social.get('timeOnline', 'ɴ/ᴀ'),
                    "data": data
                }
            else:
                return {"success": False, "error": "Unknown response format"}
        else:
            return {"success": False, "error": f"API returned {response.status_code}"}
    except Exception as e:
        return {"success": False, "error": str(e)}

def download_image(url):
    try:
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            return response.content
        return None
    except:
        return None

# ============================================================
# BOT COMMANDS
# ============================================================
bot = telebot.TeleBot(API_TOKEN)
user_states = {}  # Store user states: {'chat_id': 'awaiting_uid'}

@bot.message_handler(commands=['start'])
def start_command(message):
    try:
        chat_id = message.chat.id
        user_id = message.from_user.id
        first_name = message.from_user.first_name or "User"
        username = message.from_user.username or "NoUsername"
        
        # Stylish welcome message with premium emojis
        welcome_text = format_premium(f"""
🔥 {stylish('WELCOME TO FF INFO BOT!')} 🔥

👤 {stylish('User ID:')} <code>{user_id}</code>
👋 {stylish('Hello,')} {first_name}

📌 {stylish('Use the button below to get FF ID info.')}
        """)
        
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🎯 FF ID INFO", callback_data="get_uid"))
        
        bot.send_message(
            chat_id,
            welcome_text,
            parse_mode="HTML",
            reply_markup=markup
        )
    except Exception as e:
        logger.error(f"Start command error: {e}")

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    try:
        chat_id = call.message.chat.id
        if call.data == "get_uid":
            # Ask for UID
            msg = format_premium(f"""
📝 {stylish('PLEASE ENTER FF UID')}

{stylish('Send your Free Fire UID as a reply to this message.')}
            """)
            bot.send_message(chat_id, msg, parse_mode="HTML")
            user_states[chat_id] = 'awaiting_uid'
    except Exception as e:
        logger.error(f"Callback error: {e}")

@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    try:
        chat_id = message.chat.id
        text = message.text.strip()
        
        # Check if user is in awaiting_uid state
        if chat_id in user_states and user_states[chat_id] == 'awaiting_uid':
            if is_valid_uid(text):
                # Valid UID - process
                bot.send_chat_action(chat_id, 'typing')
                process_uid(chat_id, text)
                del user_states[chat_id]
            else:
                bot.reply_to(
                    message,
                    format_premium(f"""
❌ {stylish('INVALID UID!')}

{stylish('UID must be 8-11 digits.')}
{stylish('Please try again.')}
                    """),
                    parse_mode="HTML"
                )
        else:
            # If user sends UID directly (without state)
            if is_valid_uid(text):
                bot.send_chat_action(chat_id, 'typing')
                process_uid(chat_id, text)
            else:
                bot.reply_to(
                    message,
                    format_premium(f"""
❓ {stylish('Unknown command!')}

{stylish('Use /start to see available options.')}
                    """),
                    parse_mode="HTML"
                )
    except Exception as e:
        logger.error(f"Message handler error: {e}")

def process_uid(chat_id, uid):
    """Process UID and send info with photos"""
    try:
        # Send processing message
        processing_msg = bot.send_message(
            chat_id,
            format_premium(f"⏳ {stylish('FETCHING PLAYER INFO...')}"),
            parse_mode="HTML"
        )
        
        # Get player info
        info = get_player_info(uid)
        
        if not info['success']:
            bot.edit_message_text(
                format_premium(f"""
❌ {stylish('FAILED TO FETCH PLAYER INFO')}

{stylish('Error:')} {info.get('error', 'Unknown error')}
                """),
                chat_id,
                processing_msg.message_id,
                parse_mode="HTML"
            )
            return
        
        # Format data
        region = info['region']
        nickname = info['nickname']
        last_login = format_timestamp(info.get('last_login'))
        create_at = format_timestamp(info.get('create_at'))
        ban_status = "✅ Not Banned" if info.get('ban_status') == 'Not Banned' else "❌ Banned"
        
        # Build info text with PREMIUM EMOJIS
        info_text = format_premium(f"""
🎮 {stylish('PLAYER INFORMATION')}
────────────────────
👤 {stylish('Nickname:')} <code>{escape_markdown(info.get('nickname', 'ɴ/ᴀ'))}</code>
🆔 {stylish('UID:')} <code>{uid}</code>
🌍 {stylish('Region:')} <code>{info.get('region', 'ɴ/ᴀ')}</code>
📊 {stylish('Level:')} <code>{info.get('level', 'ɴ/ᴀ')}</code>
📈 {stylish('Level Progress:')} <code>{info.get('level_progress', 'ɴ/ᴀ')}</code>
⭐ {stylish('EXP:')} <code>{info.get('exp', 'ɴ/ᴀ')}</code>
📌 {stylish('EXP Needed:')} <code>{info.get('exp_needed', 'ɴ/ᴀ')}</code>
👍 {stylish('Likes:')} <code>{info.get('likes', 'ɴ/ᴀ')}</code>
🏅 {stylish('Rank:')} <code>{info.get('rank', 'ɴ/ᴀ')}</code>
⭐ {stylish('Rank Points:')} <code>{info.get('rank_points', 'ɴ/ᴀ')}</code>
🔰 {stylish('Max Rank:')} <code>{info.get('max_rank', 'ɴ/ᴀ')}</code>
🏆 {stylish('CS Rank:')} <code>{info.get('cs_rank', 'ɴ/ᴀ')}</code>
🔒 {stylish('Ban Status:')} <code>{ban_status}</code>
📌 {stylish('Title:')} <code>{info.get('title', 'ɴ/ᴀ')}</code>
🖼️ {stylish('Headpic:')} <code>{info.get('headpic_name', 'ɴ/ᴀ')}</code>
🎨 {stylish('Banner:')} <code>{info.get('banner', 'ɴ/ᴀ')}</code>
📛 {stylish('Banner ID:')} <code>{info.get('banner_id', 'ɴ/ᴀ')}</code>
🎯 {stylish('Pin:')} <code>{info.get('pin_name', 'ɴ/ᴀ')}</code>
🔫 {stylish('Equipped Gun:')} <code>{info.get('equipped_gun', 'ɴ/ᴀ')}</code>
💫 {stylish('Equipped Animation:')} <code>{info.get('equipped_animation', 'ɴ/ᴀ')}</code>
🏅 {stylish('Badge Count:')} <code>{info.get('badge_cnt', 'ɴ/ᴀ')}</code>
📦 {stylish('Prime Level:')} <code>{info.get('prime_level', 'ɴ/ᴀ')}</code>
📱 {stylish('Release Version:')} <code>{info.get('release_version', 'ɴ/ᴀ')}</code>
📅 {stylish('Season:')} <code>{info.get('season_id', 'ɴ/ᴀ')}</code>
📅 {stylish('Last Login:')} <code>{last_login}</code>
📆 {stylish('Account Created:')} <code>{create_at}</code>

────────────────────
👑 {stylish('CLAN INFORMATION')}
🏠 {stylish('Clan Name:')} <code>{escape_markdown(info.get('clan_name', 'ɴ/ᴀ'))}</code>
🆔 {stylish('Clan ID:')} <code>{info.get('clan_id', 'ɴ/ᴀ')}</code>
📊 {stylish('Clan Level:')} <code>{info.get('clan_level', 'ɴ/ᴀ')}</code>
👥 {stylish('Members:')} <code>{info.get('clan_members', 'ɴ/ᴀ')}</code>

────────────────────
💳 {stylish('CREDIT SCORE')}
⭐ {stylish('Credit Score:')} <code>{info.get('credit_score', 'ɴ/ᴀ')}</code>
📌 {stylish('Status:')} <code>{info.get('credit_status', 'ɴ/ᴀ')}</code>

────────────────────
🐾 {stylish('PET INFORMATION')}
🐕 {stylish('Name:')} <code>{escape_markdown(info.get('pet_name', 'ɴ/ᴀ'))}</code>
📊 {stylish('Level:')} <code>{info.get('pet_level', 'ɴ/ᴀ')}</code>
🎨 {stylish('Skin:')} <code>{escape_markdown(info.get('pet_skin', 'ɴ/ᴀ'))}</code>
⚡ {stylish('Skill:')} <code>{escape_markdown(info.get('pet_skill', 'ɴ/ᴀ'))}</code>

────────────────────
🎭 {stylish('PROFILE INFORMATION')}
👤 {stylish('Avatar:')} <code>{escape_markdown(info.get('avatar_name', 'ɴ/ᴀ'))}</code>
🆔 {stylish('Avatar ID:')} <code>{info.get('avatar_id', 'ɴ/ᴀ')}</code>
👕 {stylish('Clothes:')} <code>{', '.join(info.get('clothes_names', [])) if info.get('clothes_names') else 'ɴ/ᴀ'}</code>
⚡ {stylish('Skills:')} <code>{escape_markdown(info.get('skills', 'ɴ/ᴀ'))}</code>

────────────────────
👤 {stylish('CAPTAIN INFORMATION')}
👤 {stylish('Name:')} <code>{escape_markdown(info.get('captain_nickname', 'ɴ/ᴀ'))}</code>
🆔 {stylish('UID:')} <code>{info.get('captain_uid', 'ɴ/ᴀ')}</code>
📊 {stylish('Level:')} <code>{info.get('captain_level', 'ɴ/ᴀ')}</code>
👍 {stylish('Likes:')} <code>{info.get('captain_likes', 'ɴ/ᴀ')}</code>
🏅 {stylish('Rank:')} <code>{info.get('captain_rank', 'ɴ/ᴀ')}</code>

────────────────────
🌐 {stylish('SOCIAL INFORMATION')}
💬 {stylish('Language:')} <code>{info.get('language', 'ɴ/ᴀ')}</code>
✍️ {stylish('Signature:')} <code>{escape_markdown(info.get('signature', 'ɴ/ᴀ'))}</code>
⏰ {stylish('Time Online:')} <code>{info.get('time_online', 'ɴ/ᴀ')}</code>
        """)
        
        # Delete processing message
        bot.delete_message(chat_id, processing_msg.message_id)
        
        # Send info text
        bot.send_message(chat_id, info_text, parse_mode="HTML")
        
        # --- Build images ---
        images_to_send = []
        clothes_ids = info.get('clothes_ids', [])
        clothes_str = ','.join(str(c) for c in clothes_ids) if clothes_ids else ''
        avatar_id = info.get('avatar_id', '')
        
        # 1. Outfit Image
        if avatar_id and clothes_str:
            outfit_url = OUTFIT_API_URL.format(avatar_id=avatar_id, clothes=clothes_str)
            outfit_img = download_image(outfit_url)
            if outfit_img:
                images_to_send.append(("👕 Outfit", outfit_img))
        
        # 2. Banner Image
        headpic = info.get('headpic', '')
        banner_id = info.get('banner_id', '')
        name = encode_for_url(nickname)
        level = info.get('level', '')
        guild = encode_for_url(info.get('clan_name', ''))
        pin_id = info.get('pin_id', '')
        if headpic and banner_id:
            banner_url = BANNER_API_URL.format(
                headPic=headpic, bannerId=banner_id, name=name, level=level,
                guild=guild, pinId=pin_id, celebrity='', frame=''
            )
            banner_img = download_image(banner_url)
            if banner_img:
                images_to_send.append(("🎨 Banner", banner_img))
        
        # 3. Avatar Image (fallback)
        if not images_to_send:
            avatar_url = AVATAR_API_URL.format(uid=uid, region=region)
            avatar_img = download_image(avatar_url)
            if avatar_img:
                images_to_send.append(("🖼️ Avatar", avatar_img))
        
        # Send images
        for caption, img in images_to_send:
            try:
                bot.send_photo(chat_id, img, caption=f"{caption}\n👤 {nickname}", parse_mode="HTML")
            except Exception as e:
                logger.error(f"Image send error: {e}")
                
    except Exception as e:
        logger.error(f"Process UID error: {e}")
        bot.send_message(chat_id, format_premium(f"❌ {stylish('Error processing request')}"), parse_mode="HTML")

# ============================================================
# START BOT (POLLING)
# ============================================================
if __name__ == "__main__":
    print("🤖 Bot started successfully!")
    print(f"📡 Bot Token: {API_TOKEN[:10]}...")
    print("📝 Command: /start")
    print("📋 Premium Emojis + Stylish Fonts enabled!")
    
    # Render: Use environment variable PORT for Render's port binding
    # Render requires a port to be open for health checks, so we start a dummy web server
    PORT = int(os.environ.get("PORT", 8080))
    
    # Start a dummy web server in a separate thread to satisfy Render's port requirement
    from http.server import HTTPServer, BaseHTTPRequestHandler
    
    class DummyHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'Bot is running!')
    
    def run_dummy_server():
        server = HTTPServer(('0.0.0.0', PORT), DummyHandler)
        print(f"🌐 Dummy server running on port {PORT} for Render health checks")
        server.serve_forever()
    
    dummy_thread = threading.Thread(target=run_dummy_server, daemon=True)
    dummy_thread.start()
    
    # Start bot polling
    try:
        bot.polling(none_stop=True, interval=0)
    except Exception as e:
        print(f"❌ Bot error: {e}")