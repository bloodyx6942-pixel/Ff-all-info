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
from http.server import HTTPServer, BaseHTTPRequestHandler

# ============================================================
# CONFIGURATION
# ============================================================
API_TOKEN = "8965483066:AAEhcH7o2TwOGfufQIKDOnJSgXbh3T0I0n4"
BOT_USERNAME = "ffcollectioninfo_bot"

# ============================================================
# LOGGING
# ============================================================
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

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
# DUMMY HTTP SERVER FOR RENDER HEALTH CHECKS
# ============================================================
class DummyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b'Bot is running!')
    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

def run_dummy_server():
    PORT = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', PORT), DummyHandler)
    logger.info(f"🌐 Dummy server running on port {PORT}")
    server.serve_forever()

# ============================================================
# BOT COMMANDS
# ============================================================
bot = telebot.TeleBot(API_TOKEN)
user_states = {}

@bot.message_handler(commands=['start'])
def start_command(message):
    try:
        chat_id = message.chat.id
        user_id = message.from_user.id
        first_name = message.from_user.first_name or "User"
        username = message.from_user.username or "NoUsername"

        welcome_text = f"""
🔥 {stylish('WELCOME TO FF INFO BOT!')} 🔥

👤 {stylish('User ID:')} <code>{user_id}</code>
👋 {stylish('Hello,')} {first_name}

📌 {stylish('Use the button below to get FF ID info.')}
        """

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
            msg = f"""
📝 {stylish('PLEASE ENTER FF UID')}

{stylish('Send your Free Fire UID as a reply to this message.')}
            """
            bot.send_message(chat_id, msg, parse_mode="HTML")
            user_states[chat_id] = 'awaiting_uid'
    except Exception as e:
        logger.error(f"Callback error: {e}")

@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    try:
        chat_id = message.chat.id
        text = message.text.strip()

        if chat_id in user_states and user_states[chat_id] == 'awaiting_uid':
            if is_valid_uid(text):
                bot.send_chat_action(chat_id, 'typing')
                process_uid(chat_id, text)
                del user_states[chat_id]
            else:
                bot.reply_to(
                    message,
                    f"""
❌ {stylish('INVALID UID!')}

{stylish('UID must be 8-11 digits.')}
{stylish('Please try again.')}
                    """,
                    parse_mode="HTML"
                )
        else:
            if is_valid_uid(text):
                bot.send_chat_action(chat_id, 'typing')
                process_uid(chat_id, text)
            else:
                bot.reply_to(
                    message,
                    f"""
❓ {stylish('Unknown command!')}

{stylish('Use /start to see available options.')}
                    """,
                    parse_mode="HTML"
                )
    except Exception as e:
        logger.error(f"Message handler error: {e}")

def process_uid(chat_id, uid):
    try:
        processing_msg = bot.send_message(
            chat_id,
            f"⏳ {stylish('FETCHING PLAYER INFO...')}",
            parse_mode="HTML"
        )

        info = get_player_info(uid)

        if not info['success']:
            bot.edit_message_text(
                f"""
❌ {stylish('FAILED TO FETCH PLAYER INFO')}

{stylish('Error:')} {info.get('error', 'Unknown error')}
                """,
                chat_id,
                processing_msg.message_id,
                parse_mode="HTML"
            )
            return

        region = info['region']
        nickname = info['nickname']
        last_login = format_timestamp(info.get('last_login'))
        create_at = format_timestamp(info.get('create_at'))
        ban_status = "✅ Not Banned" if info.get('ban_status') == 'Not Banned' else "❌ Banned"

        info_text = f"""
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
        """

        bot.delete_message(chat_id, processing_msg.message_id)
        bot.send_message(chat_id, info_text, parse_mode="HTML")

        images_to_send = []
        clothes_ids = info.get('clothes_ids', [])
        clothes_str = ','.join(str(c) for c in clothes_ids) if clothes_ids else ''
        avatar_id = info.get('avatar_id', '')

        if avatar_id and clothes_str:
            outfit_url = OUTFIT_API_URL.format(avatar_id=avatar_id, clothes=clothes_str)
            outfit_img = download_image(outfit_url)
            if outfit_img:
                images_to_send.append(("👕 Outfit", outfit_img))

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

        if not images_to_send:
            avatar_url = AVATAR_API_URL.format(uid=uid, region=region)
            avatar_img = download_image(avatar_url)
            if avatar_img:
                images_to_send.append(("🖼️ Avatar", avatar_img))

        for caption, img in images_to_send:
            try:
                bot.send_photo(chat_id, img, caption=f"{caption}\n👤 {nickname}", parse_mode="HTML")
            except Exception as e:
                logger.error(f"Image send error: {e}")

    except Exception as e:
        logger.error(f"Process UID error: {e}")
        bot.send_message(chat_id, f"❌ {stylish('Error processing request')}", parse_mode="HTML")

# ============================================================
# START BOT (POLLING)
# ============================================================
if __name__ == "__main__":
    logger.info("🤖 Bot started successfully!")
    logger.info(f"📡 Bot: @{BOT_USERNAME}")
    logger.info("📝 Command: /start")
    logger.info("📋 Premium Emojis + Stylish Fonts enabled!")

    dummy_thread = threading.Thread(target=run_dummy_server, daemon=True)
    dummy_thread.start()

    try:
        bot.polling(none_stop=True, interval=0)
    except Exception as e:
        logger.error(f"❌ Bot error: {e}")