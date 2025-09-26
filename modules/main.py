import os
import re
import sys
import m3u8
import json
import time
import pytz
import asyncio
import requests
import subprocess
import urllib
import urllib.parse
import yt_dlp
import tgcrypto
import cloudscraper
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from base64 import b64encode, b64decode
from logs import logging
from bs4 import BeautifulSoup
import saini as helper
from html_handler import html_handler
from drm_handler import drm_handler
import globals
from authorisation import add_auth_user, list_auth_users, remove_auth_user
from broadcast import broadcast_handler, broadusers_handler
from text_handler import text_to_txt
from youtube_handler import ytm_handler, y2t_handler, getcookies_handler, cookies_handler
from utils import progress_bar
from vars import api_url, api_token, token_cp, adda_token, photologo, photoyt, photocp, photozip
from vars import API_ID, API_HASH, BOT_TOKEN, OWNER, CREDIT, AUTH_USERS, TOTAL_USERS, cookies_file_path
from aiohttp import ClientSession
from subprocess import getstatusoutput
from pytube import YouTube
from aiohttp import web
import random
from pyromod import listen
from pyrogram import Client, filters
from pyrogram.types import Message, InputMediaPhoto
from pyrogram.errors import FloodWait, PeerIdInvalid, UserIsBlocked, InputUserDeactivated
from pyrogram.errors.exceptions.bad_request_400 import StickerEmojiInvalid
from pyrogram.types.messages_and_media import message
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import aiohttp
import aiofiles
import zipfile
import shutil
import ffmpeg

# Initialize the bot
bot = Client(
    "bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,
# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,
@bot.on_message(filters.command("start"))
async def start(bot, m: Message):
    user_id = m.chat.id
    if user_id not in TOTAL_USERS:
        TOTAL_USERS.append(user_id)
    user = await bot.get_me()

    mention = user.mention
    caption = f"🌟 Welcome {m.from_user.mention} ! 🌟"
    start_message = await bot.send_photo(
        chat_id=m.chat.id,
        photo="https://iili.io/KuCBoV2.jpg",
        caption=caption
    )

    await asyncio.sleep(1)
    await start_message.edit_text(
        f"🌟 Welcome {m.from_user.first_name}! 🌟\n\n" +
        f"Initializing Uploader bot... 🤖\n\n"
        f"Progress: [⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️] 0%\n\n"
    )

    await asyncio.sleep(1)
    await start_message.edit_text(
        f"🌟 Welcome {m.from_user.first_name}! 🌟\n\n" +
        f"Loading features... ⏳\n\n"
        f"Progress: [🟥🟥🟥⬜️⬜️⬜️⬜️⬜️⬜️⬜️] 25%\n\n"
    )
    
    await asyncio.sleep(1)
    await start_message.edit_text(
        f"🌟 Welcome {m.from_user.first_name}! 🌟\n\n" +
        f"This may take a moment, sit back and relax! 😊\n\n"
        f"Progress: [🟧🟧🟧🟧🟧⬜️⬜️⬜️⬜️⬜️] 50%\n\n"
    )

    await asyncio.sleep(1)
    await start_message.edit_text(
        f"🌟 Welcome {m.from_user.first_name}! 🌟\n\n" +
        f"Checking subscription status... 🔍\n\n"
        f"Progress: [🟨🟨🟨🟨🟨🟨🟨🟨⬜️⬜️] 75%\n\n"
    )

    await asyncio.sleep(1)
    if m.chat.id in AUTH_USERS:
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("✨ Commands", callback_data="cmd_command")],
            [InlineKeyboardButton("💎 Features", callback_data="feat_command"), InlineKeyboardButton("⚙️ Settings", callback_data="setttings")],
            [InlineKeyboardButton("💳 Plans", callback_data="upgrade_command")],
            [InlineKeyboardButton(text="📞 Contact", url=f"tg://openmessage?user_id={OWNER}"), InlineKeyboardButton(text="🛠️ Repo", url="https://github.com/nikhilsainiop/saini-txt-direct")],
        ])
        
        await start_message.edit_text(
            f"🌟 Welcome {m.from_user.first_name}! 🌟\n\n" +
            f"Great! You are a premium member!\n"
            f"Use button : **✨ Commands** to get started 🌟\n\n"
            f"If you face any problem contact -  [{CREDIT}⁬](tg://openmessage?user_id={OWNER})\n", disable_web_page_preview=True, reply_markup=keyboard
        )
    else:
        await asyncio.sleep(2)
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("✨ Commands", callback_data="cmd_command")],
            [InlineKeyboardButton("💎 Features", callback_data="feat_command"), InlineKeyboardButton("⚙️ Settings", callback_data="setttings")],
            [InlineKeyboardButton("💳 Plans", callback_data="upgrade_command")],
            [InlineKeyboardButton(text="📞 Contact", url=f"tg://openmessage?user_id={OWNER}"), InlineKeyboardButton(text="🛠️ Repo", url="https://github.com/nikhilsainiop/saini-txt-direct")],
        ])
        await start_message.edit_text(
           f" 🎉 Welcome {m.from_user.first_name} to DRM Bot! 🎉\n\n"
           f"**You are currently using the free version.** 🆓\n\n<blockquote expandable>I'm here to make your life easier by downloading videos from your **.txt** file 📄 and uploading them directly to Telegram!</blockquote>\n\n**Want to get started? Press /id**\n\n💬 Contact : [{CREDIT}⁬](tg://openmessage?user_id={OWNER}) to Get The Subscription 🎫 and unlock the full potential of your new bot! 🔓\n", disable_web_page_preview=True, reply_markup=keyboard
    )

# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,
# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,
@bot.on_callback_query(filters.regex("back_to_main_menu"))
async def back_to_main_menu(client, callback_query):
    user_id = callback_query.from_user.id
    first_name = callback_query.from_user.first_name
    caption = f"✨ **Welcome [{first_name}](tg://user?id={user_id}) in My uploader bot**"
    keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("✨ Commands", callback_data="cmd_command")],
            [InlineKeyboardButton("💎 Features", callback_data="feat_command"), InlineKeyboardButton("⚙️ Settings", callback_data="setttings")],
            [InlineKeyboardButton("💳 Plans", callback_data="upgrade_command")],
            [InlineKeyboardButton(text="📞 Contact", url=f"tg://openmessage?user_id={OWNER}"), InlineKeyboardButton(text="🛠️ Repo", url="https://github.com/nikhilsainiop/saini-txt-direct")],
        ])
    
    await callback_query.message.edit_media(
      InputMediaPhoto(
        media="https://envs.sh/GVI.jpg",
        caption=caption
      ),
      reply_markup=keyboard
    )
    await callback_query.answer()  

# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,
# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,
@bot.on_callback_query(filters.regex("cmd_command"))
async def cmd(client, callback_query):
    user_id = callback_query.from_user.id
    first_name = callback_query.from_user.first_name
    caption = f"✨ **Welcome [{first_name}](tg://user?id={user_id})\nChoose Button to select Commands**"
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🚻 User", callback_data="user_command"), InlineKeyboardButton("🚹 Owner", callback_data="owner_command")],
        [InlineKeyboardButton("🔙 Back to Main Menu", callback_data="back_to_main_menu")]
    ])
    await callback_query.message.edit_media(
    InputMediaPhoto(
      media="https://tinypic.host/images/2025/07/14/file_00000000fc2461fbbdd6bc500cecbff8_conversation_id6874702c-9760-800e-b0bf-8e0bcf8a3833message_id964012ce-7ef5-4ad4-88e0-1c41ed240c03-1-1.jpg",
      caption=caption
    ),
    reply_markup=keyboard
    )
# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,
@bot.on_callback_query(filters.regex("user_command"))
async def help_button(client, callback_query):
  user_id = callback_query.from_user.id
  first_name = callback_query.from_user.first_name
  keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back to Commands", callback_data="cmd_command")]])
  caption = (
        f"💥 𝐁𝐎𝐓𝐒 𝐂𝐎𝐌𝐌𝐀𝐍𝐃𝐒\n"
        f"▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰\n" 
        f"📌 𝗠𝗮𝗶𝗻 𝗙𝗲𝗮𝘁𝘂𝗿𝗲𝘀:\n\n"  
        f"➥ /start – Bot Status Check\n"
        f"➥ /y2t – YouTube → .txt Converter\n"  
        f"➥ /ytm – YouTube → .mp3 downloader\n"  
        f"➥ /t2t – Text → .txt Generator\n"
        f"➥ /t2h – .txt → .html Converter\n" 
        f"➥ /stop – Cancel Running Task\n"
        f"▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰ \n" 
        f"⚙️ 𝗧𝗼𝗼𝗹𝘀 & 𝗦𝗲𝘁𝘁𝗶𝗻𝗴𝘀: \n\n" 
        f"➥ /cookies – Update YT Cookies\n" 
        f"➥ /id – Get Chat/User ID\n"  
        f"➥ /info – User Details\n"  
        f"➥ /logs – View Bot Activity\n"
        f"▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰\n"
        f"💡 𝗡𝗼𝘁𝗲:\n\n"  
        f"• Send any link for auto-extraction\n"
        f"• Send direct .txt file for auto-extraction\n"
        f"• Supports batch processing\n\n"  
        f"╭────────⊰◆⊱────────╮\n"   
        f" ➠ 𝐌𝐚𝐝𝐞 𝐁𝐲 : {CREDIT} 💻\n"
        f"╰────────⊰◆⊱────────╯\n"
  )
    
  await callback_query.message.edit_media(
    InputMediaPhoto(
      media="https://tinypic.host/images/2025/07/14/file_00000000fc2461fbbdd6bc500cecbff8_conversation_id6874702c-9760-800e-b0bf-8e0bcf8a3833message_id964012ce-7ef5-4ad4-88e0-1c41ed240c03-1-1.jpg",
      caption=caption
    ),
    reply_markup=keyboard
    )
# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,
@bot.on_callback_query(filters.regex("owner_command"))
async def help_button(client, callback_query):
  user_id = callback_query.from_user.id
  first_name = callback_query.from_user.first_name
  keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back to Commands", callback_data="cmd_command")]])
  caption = (
        f"👤 𝐁𝐨𝐭 𝐎𝐰𝐧𝐞𝐫 𝐂𝐨𝐦𝐦𝐚𝐧𝐝𝐬\n\n" 
        f"➥ /addauth xxxx – Add User ID\n" 
        f"➥ /rmauth xxxx – Remove User ID\n"  
        f"➥ /users – Total User List\n"  
        f"➥ /broadcast – For Broadcasting\n"  
        f"➥ /broadusers – All Broadcasting Users\n"  
        f"➥ /reset – Reset Bot\n"
        f"▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰\n"  
        f"╭────────⊰◆⊱────────╮\n"   
        f" ➠ 𝐌𝐚𝐝𝐞 𝐁𝐲 : {CREDIT} 💻\n"
        f"╰────────⊰◆⊱────────╯\n"
  )
    
  await callback_query.message.edit_media(
    InputMediaPhoto(
      media="https://tinypic.host/images/2025/07/14/file_00000000fc2461fbbdd6bc500cecbff8_conversation_id6874702c-9760-800e-b0bf-8e0bcf8a3833message_id964012ce-7ef5-4ad4-88e0-1c41ed240c03-1-1.jpg",
      caption=caption
    ),
    reply_markup=keyboard
  )

# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,
# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,
@bot.on_callback_query(filters.regex("upgrade_command"))
async def upgrade_button(client, callback_query):
  user_id = callback_query.from_user.id
  first_name = callback_query.from_user.first_name
  keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back to Main Menu", callback_data="back_to_main_menu")]])
  caption = (
           f" 🎉 Welcome [{first_name}](tg://user?id={user_id}) to DRM Bot! 🎉\n\n"
           f"You can have access to download all Non-DRM+AES Encrypted URLs 🔐 including\n\n"
           f"<blockquote>• 📚 Appx Zip+Encrypted Url\n"
           f"• 🎓 Classplus DRM+ NDRM\n"
           f"• 🧑‍🏫 PhysicsWallah DRM\n"
           f"• 📚 CareerWill + PDF\n"
           f"• 🎓 Khan GS\n"
           f"• 🎓 Study Iq DRM\n"
           f"• 🚀 APPX + APPX Enc PDF\n"
           f"• 🎓 Vimeo Protection\n"
           f"• 🎓 Brightcove Protection\n"
           f"• 🎓 Visionias Protection\n"
           f"• 🎓 Zoom Video\n"
           f"• 🎓 Utkarsh Protection(Video + PDF)\n"
           f"• 🎓 All Non DRM+AES Encrypted URLs\n"
           f"• 🎓 MPD URLs if the key is known (e.g., Mpd_url?key=key XX:XX)</blockquote>\n\n"
           f"<b>💵 Monthly Plan: 100 INR</b>\n\n"
           f"If you want to buy membership of the bot, feel free to contact [{CREDIT}](tg://user?id={OWNER})\n"
    )  
    
  await callback_query.message.edit_media(
    InputMediaPhoto(
      media="https://envs.sh/GVI.jpg",
      caption=caption
    ),
    reply_markup=keyboard
    )
# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,
# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,
@bot.on_callback_query(filters.regex("setttings"))
async def settings_button(client, callback_query):
    caption = "✨ <b>My Premium BOT Settings Panel</b> ✨"
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("📝 Caption Style", callback_data="caption_style_command"), InlineKeyboardButton("🖋️ File Name", callback_data="file_name_command")],
        [InlineKeyboardButton("🌅 Thumbnail", callback_data="thummbnail_command")],
        [InlineKeyboardButton("✍️ Add Credit", callback_data="add_credit_command"), InlineKeyboardButton("🔏 Set Token", callback_data="set_token_command")],
        [InlineKeyboardButton("💧 Watermark", callback_data="wattermark_command")],
        [InlineKeyboardButton("📽️ Video Quality", callback_data="quality_command"), InlineKeyboardButton("🏷️ Topic", callback_data="topic_command")],
        [InlineKeyboardButton("🔄 Reset", callback_data="resset_command")],
        [InlineKeyboardButton("🔙 Back to Main Menu", callback_data="back_to_main_menu")]
    ])

    await callback_query.message.edit_media(
    InputMediaPhoto(
      media="https://envs.sh/GVI.jpg",
      caption=caption
    ),
    reply_markup=keyboard
    )
# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,
@bot.on_callback_query(filters.regex("thummbnail_command"))
async def cmd(client, callback_query):
    user_id = callback_query.from_user.id
    first_name = callback_query.from_user.first_name
    caption = f"✨ **Welcome [{first_name}](tg://user?id={user_id})\nChoose Button to set Thumbnail**"
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🎥 Video", callback_data="viideo_thumbnail_command"), InlineKeyboardButton("📑 PDF", callback_data="pddf_thumbnail_command")],
        [InlineKeyboardButton("🔙 Back to Settings", callback_data="setttings")]
    ])
    await callback_query.message.edit_media(
    InputMediaPhoto(
      media="https://tinypic.host/images/2025/07/14/file_00000000fc2461fbbdd6bc500cecbff8_conversation_id6874702c-9760-800e-b0bf-8e0bcf8a3833message_id964012ce-7ef5-4ad4-88e0-1c41ed240c03-1-1.jpg",
      caption=caption
    ),
    reply_markup=keyboard
    )
# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,
@bot.on_callback_query(filters.regex("wattermark_command"))
async def cmd(client, callback_query):
    user_id = callback_query.from_user.id
    first_name = callback_query.from_user.first_name
    caption = f"✨ **Welcome [{first_name}](tg://user?id={user_id})\nChoose Button to set Watermark**"
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🎥 Video", callback_data="video_watermark_command"), InlineKeyboardButton("📑 PDF", callback_data="pdf_watermark_command")],
        [InlineKeyboardButton("🔙 Back to Settings", callback_data="setttings")]
    ])
    await callback_query.message.edit_media(
    InputMediaPhoto(
      media="https://tinypic.host/images/2025/07/14/file_00000000fc2461fbbdd6bc500cecbff8_conversation_id6874702c-9760-800e-b0bf-8e0bcf8a3833message_id964012ce-7ef5-4ad4-88e0-1c41ed240c03-1-1.jpg",
      caption=caption
    ),
    reply_markup=keyboard
    )
# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,
@bot.on_callback_query(filters.regex("set_token_command"))
async def cmd(client, callback_query):
    user_id = callback_query.from_user.id
    first_name = callback_query.from_user.first_name
    caption = f"✨ **Welcome [{first_name}](tg://user?id={user_id})\nChoose Button to set Token**"
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Classplus", callback_data="cp_token_command")],
        [InlineKeyboardButton("Physics Wallah", callback_data="pw_token_command"), InlineKeyboardButton("Carrerwill", callback_data="cw_token_command")],
        [InlineKeyboardButton("🔙 Back to Settings", callback_data="setttings")]
    ])
    await callback_query.message.edit_media(
    InputMediaPhoto(
      media="https://tinypic.host/images/2025/07/14/file_00000000fc2461fbbdd6bc500cecbff8_conversation_id6874702c-9760-800e-b0bf-8e0bcf8a3833message_id964012ce-7ef5-4ad4-88e0-1c41ed240c03-1-1.jpg",
      caption=caption
    ),
    reply_markup=keyboard
    )
# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,
@bot.on_callback_query(filters.regex("caption_style_command"))
async def handle_caption(client, callback_query):
    user_id = callback_query.from_user.id
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back to Settings", callback_data="setttings")]])
    editable = await callback_query.message.edit(
        "**Caption Style 1**\n"
        "<blockquote expandable><b>[🎥]Vid Id</b> : {str(count).zfill(3)}\n"
        "**Video Title :** `{name1} [{res}p].{ext}`\n"
        "<blockquote><b>Batch Name :</b> {b_name}</blockquote>\n\n"
        "**Extracted by➤**{CR}</blockquote>\n\n"
        "**Caption Style 2**\n"
        "<blockquote expandable>**——— ✦ {str(count).zfill(3)} ✦ ———**\n\n"
        "🎞️ **Title** : `{name1}`\n"
        "**├── Extention :  {extension}.{ext}**\n"
        "**├── Resolution : [{res}]**\n"
        "📚 **Course : {b_name}**\n\n"
        "🌟 **Extracted By : {credit}**</blockquote>\n\n"
        "**Caption Style 3**\n"
        "<blockquote expandable>**{str(count).zfill(3)}.** {name1} [{res}p].{ext}</blockquote>\n\n"
        "**Send Your Caption Style eg. /cc1 or /cc2 or /cc3**", reply_markup=keyboard)
    input_msg = await bot.listen(editable.chat.id)
    try:
        if input_msg.text.lower() == "/cc1":
            globals.caption = '/cc1'
            await editable.edit(f"✅ Caption Style 1 Updated!", reply_markup=keyboard)
        elif input_msg.text.lower() == "/cc2":
            globals.caption = '/cc2'
            await editable.edit(f"✅ Caption Style 2 Updated!", reply_markup=keyboard)
        else:
            globals.caption = input_msg.text
            await editable.edit(f"✅ Caption Style 3 Updated!", reply_markup=keyboard)
            
    except Exception as e:
        await editable.edit(f"<b>❌ Failed to set Caption Style:</b>\n<blockquote expandable>{str(e)}</blockquote>", reply_markup=keyboard)
    finally:
        await input_msg.delete()
# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,
@bot.on_callback_query(filters.regex("file_name_command"))
async def handle_caption(client, callback_query):
    user_id = callback_query.from_user.id
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back to Settings", callback_data="setttings")]])
    editable = await callback_query.message.edit("**Send End File Name or Send /d**", reply_markup=keyboard)
    input_msg = await bot.listen(editable.chat.id)
    try:
        if input_msg.text.lower() == "/d":
            globals.endfilename = '/d'
            await editable.edit(f"✅ End File Name Disabled !", reply_markup=keyboard)
        else:
            globals.endfilename = input_msg.text
            await editable.edit(f"✅ End File Name `{globals.endfilename}` is enabled!", reply_markup=keyboard)
            
    except Exception as e:
        await editable.edit(f"<b>❌ Failed to set End File Name:</b>\n<blockquote expandable>{str(e)}</blockquote>", reply_markup=keyboard)
    finally:
        await input_msg.delete()
# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,
@bot.on_callback_query(filters.regex("viideo_thumbnail_command"))
async def video_thumbnail(client, callback_query):
    user_id = callback_query.from_user.id
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back to Settings", callback_data="thummbnail_command")]])
    editable = await callback_query.message.edit(f"Send the Video Thumb URL or Send /d \n<blockquote><b>Note </b>- For document format send : No</blockquote>", reply_markup=keyboard)
    input_msg = await bot.listen(editable.chat.id)

    try:
        if input_msg.text.startswith("http://") or input_msg.text.startswith("https://"):
            globals.thumb = input_msg.text
            await editable.edit(f"✅ Thumbnail set successfully from the URL !", reply_markup=keyboard)

        elif input_msg.text.lower() == "/d":
            globals.thumb = "/d"
            await editable.edit(f"✅ Thumbnail set to default !", reply_markup=keyboard)

        else:
            globals.thumb = input_msg.text
            await editable.edit(f"✅ Video in Document Format is enabled !", reply_markup=keyboard)

    except Exception as e:
        await editable.edit(f"<b>❌ Failed to set thumbnail:</b>\n<blockquote expandable>{str(e)}</blockquote>", reply_markup=keyboard)
    finally:
        await input_msg.delete()
# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,
@bot.on_callback_query(filters.regex("pddf_thumbnail_command"))
async def pdf_thumbnail_button(client, callback_query):
  keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back to Settings", callback_data="thummbnail_command")]])
  caption = ("<b>⋅ This Feature is Not Working Yet ⋅</b>")
  await callback_query.message.edit_media(
    InputMediaPhoto(
        media="https://envs.sh/GVI.jpg",
        caption=caption
    ),
    reply_markup=keyboard
  )
# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,
@bot.on_callback_query(filters.regex("add_credit_command"))
async def credit(client, callback_query):
    user_id = callback_query.from_user.id
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back to Settings", callback_data="setttings")]])
    editable = await callback_query.message.edit(f"Send Credit Name or Send /d", reply_markup=keyboard)
    input_msg = await bot.listen(editable.chat.id)

    try:
        if input_msg.text.lower() == "/d":
            globals.CR = f"{CREDIT}"
            await editable.edit(f"✅ Credit set to default !", reply_markup=keyboard)

        else:
            globals.CR = input_msg.text
            await editable.edit(f"✅ Credit set as {globals.CR} !", reply_markup=keyboard)

    except Exception as e:
        await editable.edit(f"<b>❌ Failed to set Credit:</b>\n<blockquote expandable>{str(e)}</blockquote>", reply_markup=keyboard)
    finally:
        await input_msg.delete()
# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,
@bot.on_callback_query(filters.regex("cp_token_command"))
async def handle_token(client, callback_query):
    user_id = callback_query.from_user.id
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back to Settings", callback_data="set_token_command")]])
    editable = await callback_query.message.edit("**Send Classplus Token**", reply_markup=keyboard)
    input_msg = await bot.listen(editable.chat.id)
    try:
        globals.cptoken = input_msg.text
        await editable.edit(f"✅ Classplus Token set successfully !\n\n<blockquote expandable>`{globals.cptoken}`</blockquote>", reply_markup=keyboard)
            
    except Exception as e:
        await editable.edit(f"<b>❌ Failed to set Classplus Token:</b>\n<blockquote expandable>{str(e)}</blockquote>", reply_markup=keyboard)
    finally:
        await input_msg.delete()
# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,
@bot.on_callback_query(filters.regex("pw_token_command"))
async def handle_token(client, callback_query):
    user_id = callback_query.from_user.id
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back to Settings", callback_data="set_token_command")]])
    editable = await callback_query.message.edit("**Send Physics Wallah Same Batch Token**", reply_markup=keyboard)
    input_msg = await bot.listen(editable.chat.id)
    try:
        globals.pwtoken = input_msg.text
        await editable.edit(f"✅ Physics Wallah Token set successfully !\n\n<blockquote expandable>`{globals.pwtoken}`</blockquote>", reply_markup=keyboard)
            
    except Exception as e:
        await editable.edit(f"<b>❌ Failed to set Physics Wallah Token:</b>\n<blockquote expandable>{str(e)}</blockquote>", reply_markup=keyboard)
    finally:
        await input_msg.delete()
# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,
@bot.on_callback_query(filters.regex("cw_token_command"))
async def handle_token(client, callback_query):
    user_id = callback_query.from_user.id
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back to Settings", callback_data="set_token_command")]])
    editable = await callback_query.message.edit("**Send Carrerwill Token**", reply_markup=keyboard)
    input_msg = await bot.listen(editable.chat.id)
    try:
        if input_msg.text.lower() == "/d":
            globals.cwtoken = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE3MjQyMzg3OTEsImNvbiI6eyJpc0FkbWluIjpmYWxzZSwiYXVzZXIiOiJVMFZ6TkdGU2NuQlZjR3h5TkZwV09FYzBURGxOZHowOSIsImlkIjoiZEUxbmNuZFBNblJqVEROVmFWTlFWbXhRTkhoS2R6MDkiLCJmaXJzdF9uYW1lIjoiYVcxV05ITjVSemR6Vm10ak1WUlBSRkF5ZVNzM1VUMDkiLCJlbWFpbCI6Ik5Ga3hNVWhxUXpRNFJ6VlhiR0ppWTJoUk0wMVdNR0pVTlU5clJXSkRWbXRMTTBSU2FHRnhURTFTUlQwPSIsInBob25lIjoiVUhVMFZrOWFTbmQ1ZVcwd1pqUTViRzVSYVc5aGR6MDkiLCJhdmF0YXIiOiJLM1ZzY1M4elMwcDBRbmxrYms4M1JEbHZla05pVVQwOSIsInJlZmVycmFsX2NvZGUiOiJOalZFYzBkM1IyNTBSM3B3VUZWbVRtbHFRVXAwVVQwOSIsImRldmljZV90eXBlIjoiYW5kcm9pZCIsImRldmljZV92ZXJzaW9uIjoiUShBbmRyb2lkIDEwLjApIiwiZGV2aWNlX21vZGVsIjoiU2Ftc3VuZyBTTS1TOTE4QiIsInJlbW90ZV9hZGRyIjoiNTQuMjI2LjI1NS4xNjMsIDU0LjIyNi4yNTUuMTYzIn19.snDdd-PbaoC42OUhn5SJaEGxq0VzfdzO49WTmYgTx8ra_Lz66GySZykpd2SxIZCnrKR6-R10F5sUSrKATv1CDk9ruj_ltCjEkcRq8mAqAytDcEBp72-W0Z7DtGi8LdnY7Vd9Kpaf499P-y3-godolS_7ixClcYOnWxe2nSVD5C9c5HkyisrHTvf6NFAuQC_FD3TzByldbPVKK0ag1UnHRavX8MtttjshnRhv5gJs5DQWj4Ir_dkMcJ4JaVZO3z8j0OxVLjnmuaRBujT-1pavsr1CCzjTbAcBvdjUfvzEhObWfA1-Vl5Y4bUgRHhl1U-0hne4-5fF0aouyu71Y6W0eg'
            await editable.edit(f"✅ Carrerwill Token set successfully as default !", reply_markup=keyboard)

        else:
            globals.cwtoken = input_msg.text
            await editable.edit(f"✅ Carrerwill Token set successfully !\n\n<blockquote expandable>`{globals.cwtoken}`</blockquote>", reply_markup=keyboard)
            
    except Exception as e:
        await editable.edit(f"<b>❌ Failed to set Careerwill Token:</b>\n<blockquote expandable>{str(e)}</blockquote>", reply_markup=keyboard)
    finally:
        await input_msg.delete()
# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,
@bot.on_callback_query(filters.regex("video_watermark_command"))
async def video_watermark(client, callback_query):
    user_id = callback_query.from_user.id
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back to Settings", callback_data="wattermark_command")]])
    editable = await callback_query.message.edit(f"**Send Video Watermark text or Send /d**", reply_markup=keyboard)
    input_msg = await bot.listen(editable.chat.id)

    try:
        if input_msg.text.lower() == "/d":
            globals.vidwatermark = "/d"
            await editable.edit(f"**Video Watermark Disabled ✅** !", reply_markup=keyboard)

        else:
            globals.vidwatermark = input_msg.text
            await editable.edit(f"Video Watermark `{globals.vidwatermark}` enabled ✅!", reply_markup=keyboard)

    except Exception as e:
        await editable.edit(f"<b>❌ Failed to set Watermark:</b>\n<blockquote expandable>{str(e)}</blockquote>", reply_markup=keyboard)
    finally:
        await input_msg.delete()
# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,
@bot.on_callback_query(filters.regex("pdf_watermark_command"))
async def pdf_watermark_button(client, callback_query):
  keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back to Settings", callback_data="wattermark_command")]])
  caption = ("<b>⋅ This Feature is Not Working Yet ⋅</b>")
  await callback_query.message.edit_media(
    InputMediaPhoto(
        media="https://envs.sh/GVI.jpg",
        caption=caption
    ),
    reply_markup=keyboard
  )
# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,
@bot.on_callback_query(filters.regex("quality_command"))
async def handle_quality(client, callback_query):
    user_id = callback_query.from_user.id
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back to Settings", callback_data="setttings")]])
    editable = await callback_query.message.edit("__**Enter resolution or Video Quality (`144`, `240`, `360`, `480`, `720`, `1080`) or Send /d**__", reply_markup=keyboard)
    input_msg = await bot.listen(editable.chat.id)
    try:
        if input_msg.text.lower() == "144":
            globals.raw_text2 = '144'
            globals.quality = f"{globals.raw_text2}p"
            globals.res = '256x144'
            await editable.edit(f"✅ Video Quality set {globals.quality} !", reply_markup=keyboard)
        elif input_msg.text.lower() == "240":
            globals.raw_text2 = '240'
            globals.quality = f"{globals.raw_text2}p"
            globals.res = '426x240'
            await editable.edit(f"✅ Video Quality set {globals.quality} !", reply_markup=keyboard)
        elif input_msg.text.lower() == "360":
            globals.raw_text2 = '360'
            globals.quality = f"{globals.raw_text2}p"
            globals.res = '640x360'
            await editable.edit(f"✅ Video Quality set {globals.quality} !", reply_markup=keyboard)
        elif input_msg.text.lower() == "480":
            globals.raw_text2 = '480'
            globals.quality = f"{globals.raw_text2}p"
            globals.res = '854x480'
            await editable.edit(f"✅ Video Quality set {globals.quality} !", reply_markup=keyboard)
        elif input_msg.text.lower() == "720":
            globals.raw_text2 = '720'
            globals.quality = f"{globals.raw_text2}p"
            globals.res = '1280x720'
            await editable.edit(f"✅ Video Quality set {globals.quality} !", reply_markup=keyboard)
        elif input_msg.text.lower() == "1080":
            globals.raw_text2 = '1080'
            globals.quality = f"{globals.raw_text2}p"
            globals.res = '1920x1080'
            await editable.edit(f"✅ Video Quality set {globals.quality} !", reply_markup=keyboard)
        else:
            globals.raw_text2 = '480'
            globals.quality = f"{globals.raw_text2}p"
            globals.res = '854x480'
            await editable.edit(f"✅ Video Quality set {globals.quality} as Default !", reply_markup=keyboard)
            
    except Exception as e:
        await editable.edit(f"<b>❌ Failed to set Video Quality:</b>\n<blockquote expandable>{str(e)}</blockquote>", reply_markup=keyboard)
    finally:
        await input_msg.delete()
# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,
@bot.on_callback_query(filters.regex("topic_command"))
async def video_watermark(client, callback_query):
    user_id = callback_query.from_user.id
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back to Settings", callback_data="setttings")]])
    editable = await callback_query.message.edit(f"**If you want to enable topic in caption: send /yes or send /d**\n\n<blockquote><b>Topic fetch from (bracket) in title</b></blockquote>", reply_markup=keyboard)
    input_msg = await bot.listen(editable.chat.id)

    try:
        if input_msg.text.lower() == "/yes":
            globals.topic = "/yes"
            await editable.edit(f"**Topic enabled in Caption ✅** !", reply_markup=keyboard)

        else:
            globals.topic = input_msg.text
            await editable.edit(f"Topic disabled in Caption ✅!", reply_markup=keyboard)

    except Exception as e:
        await editable.edit(f"<b>❌ Failed to set Topic in Caption:</b>\n<blockquote expandable>{str(e)}</blockquote>", reply_markup=keyboard)
    finally:
        await input_msg.delete()
# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,
@bot.on_callback_query(filters.regex("resset_command"))
async def credit(client, callback_query):
    user_id = callback_query.from_user.id
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back to Settings", callback_data="setttings")]])
    editable = await callback_query.message.edit(f"If you want to reset settings send /yes or Send /no", reply_markup=keyboard)
    input_msg = await bot.listen(editable.chat.id)

    try:
        if input_msg.text.lower() == "/yes":
            globals.caption = '/cc1'
            globals.endfilename = '/d'
            globals.thumb = '/d'
            globals.CR = f"{CREDIT}"
            globals.cwtoken = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE3MjQyMzg3OTEsImNvbiI6eyJpc0FkbWluIjpmYWxzZSwiYXVzZXIiOiJVMFZ6TkdGU2NuQlZjR3h5TkZwV09FYzBURGxOZHowOSIsImlkIjoiZEUxbmNuZFBNblJqVEROVmFWTlFWbXhRTkhoS2R6MDkiLCJmaXJzdF9uYW1lIjoiYVcxV05ITjVSemR6Vm10ak1WUlBSRkF5ZVNzM1VUMDkiLCJlbWFpbCI6Ik5Ga3hNVWhxUXpRNFJ6VlhiR0ppWTJoUk0wMVdNR0pVTlU5clJXSkRWbXRMTTBSU2FHRnhURTFTUlQwPSIsInBob25lIjoiVUhVMFZrOWFTbmQ1ZVcwd1pqUTViRzVSYVc5aGR6MDkiLCJhdmF0YXIiOiJLM1ZzY1M4elMwcDBRbmxrYms4M1JEbHZla05pVVQwOSIsInJlZmVycmFsX2NvZGUiOiJOalZFYzBkM1IyNTBSM3B3VUZWbVRtbHFRVXAwVVQwOSIsImRldmljZV90eXBlIjoiYW5kcm9pZCIsImRldmljZV92ZXJzaW9uIjoiUShBbmRyb2lkIDEwLjApIiwiZGV2aWNlX21vZGVsIjoiU2Ftc3VuZyBTTS1TOTE4QiIsInJlbW90ZV9hZGRyIjoiNTQuMjI2LjI1NS4xNjMsIDU0LjIyNi4yNTUuMTYzIn19.snDdd-PbaoC42OUhn5SJaEGxq0VzfdzO49WTmYgTx8ra_Lz66GySZykpd2SxIZCnrKR6-R10F5sUSrKATv1CDk9ruj_ltCjEkcRq8mAqAytDcEBp72-W0Z7DtGi8LdnY7Vd9Kpaf499P-y3-godolS_7ixClcYOnWxe2nSVD5C9c5HkyisrHTvf6NFAuQC_FD3TzByldbPVKK0ag1UnHRavX8MtttjshnRhv5gJs5DQWj4Ir_dkMcJ4JaVZO3z8j0OxVLjnmuaRBujT-1pavsr1CCzjTbAcBvdjUfvzEhObWfA1-Vl5Y4bUgRHhl1U-0hne4-5fF0aouyu71Y6W0eg'
            globals.cptoken = "cptoken"
            globals.pwtoken = "pwtoken"
            globals.vidwatermark = '/d'
            globals.raw_text2 = '480'
            globals.quality = '480p'
            globals.res = '854x480'
            globals.topic = '/d'
            await editable.edit(f"✅ Settings reset as default !", reply_markup=keyboard)

        else:
            await editable.edit(f"✅ Settings Not Changed !", reply_markup=keyboard)

    except Exception as e:
        await editable.edit(f"<b>❌ Failed to Change Settings:</b>\n<blockquote expandable>{str(e)}</blockquote>", reply_markup=keyboard)
    finally:
        await input_msg.delete()

# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,
# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,
@bot.on_callback_query(filters.regex("feat_command"))
async def feature_button(client, callback_query):
  caption = "**✨ My Premium BOT Features :**"
  keyboard = InlineKeyboardMarkup([
      [InlineKeyboardButton("📌 Auto Pin Batch Name", callback_data="pin_command")],
      [InlineKeyboardButton("💧 Watermark", callback_data="watermark_command"), InlineKeyboardButton("🔄 Reset", callback_data="reset_command")],
      [InlineKeyboardButton("🖨️ Bot Working Logs", callback_data="logs_command")],
      [InlineKeyboardButton("🖋️ File Name", callback_data="custom_command"), InlineKeyboardButton("🏷️ Title", callback_data="titlle_command")],
      [InlineKeyboardButton("🎥 YouTube", callback_data="yt_command")],
      [InlineKeyboardButton("🌐 HTML", callback_data="html_command")],
      [InlineKeyboardButton("📝 Text File", callback_data="txt_maker_command"), InlineKeyboardButton("📢 Broadcast", callback_data="broadcast_command")],
      [InlineKeyboardButton("🔙 Back to Main Menu", callback_data="back_to_main_menu")]
  ])
  await callback_query.message.edit_media(
    InputMediaPhoto(
      media="https://tinypic.host/images/2025/07/14/file_000000002d44622f856a002a219cf27aconversation_id68747543-56d8-800e-ae47-bb6438a09851message_id8e8cbfb5-ea6c-4f59-974a-43bdf87130c0.png",
      caption=caption
    ),
    reply_markup=keyboard
  )
# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,
@bot.on_callback_query(filters.regex("pin_command"))
async def pin_button(client, callback_query):
  keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back to Feature", callback_data="feat_command")]])
  caption = f"**Auto Pin 📌 Batch Name :**\n\nAutomatically Pins the Batch Name in Channel or Group, If Starting from the First Link."
  await callback_query.message.edit_media(
    InputMediaPhoto(
      media="https://tinypic.host/images/2025/07/14/file_000000002d44622f856a002a219cf27aconversation_id68747543-56d8-800e-ae47-bb6438a09851message_id8e8cbfb5-ea6c-4f59-974a-43bdf87130c0.png",
      caption=caption
      ),
      reply_markup=keyboard
  )
# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,
@bot.on_callback_query(filters.regex("watermark_command"))
async def watermark_button(client, callback_query):
  keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back to Feature", callback_data="feat_command")]])
  caption = f"**Custom Watermark :**\n\nSet Your Own Custom Watermark on Videos for Added Personalization."
  await callback_query.message.edit_media(
    InputMediaPhoto(
      media="https://tinypic.host/images/2025/07/14/file_000000002d44622f856a002a219cf27aconversation_id68747543-56d8-800e-ae47-bb6438a09851message_id8e8cbfb5-ea6c-4f59-974a-43bdf87130c0.png",
      caption=caption
      ),
      reply_markup=keyboard
  )
# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,
@bot.on_callback_query(filters.regex("reset_command"))
async def restart_button(client, callback_query):
  keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back to Feature", callback_data="feat_command")]])
  caption = f"**🔄 Reset Command:**\n\nIf You Want to Reset or Restart Your Bot, Simply Use Command /reset."
  await callback_query.message.edit_media(
    InputMediaPhoto(
      media="https://tinypic.host/images/2025/07/14/file_000000002d44622f856a002a219cf27aconversation_id68747543-56d8-800e-ae47-bb6438a09851message_id8e8cbfb5-ea6c-4f59-974a-43bdf87130c0.png",
      caption=caption
      ),
      reply_markup=keyboard
  )
# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,
@bot.on_callback_query(filters.regex("logs_command"))
async def pin_button(client, callback_query):
  keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back to Feature", callback_data="feat_command")]])
  caption = f"**🖨️ Bot Working Logs:**\n\n◆/logs - Bot Send Working Logs in .txt File."
  await callback_query.message.edit_media(
    InputMediaPhoto(
      media="https://tinypic.host/images/2025/07/14/file_000000002d44622f856a002a219cf27aconversation_id68747543-56d8-800e-ae47-bb6438a09851message_id8e8cbfb5-ea6c-4f59-974a-43bdf87130c0.png",
      caption=caption
      ),
      reply_markup=keyboard
    )
# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,
@bot.on_callback_query(filters.regex("custom_command"))
async def custom_button(client, callback_query):
  keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back to Feature", callback_data="feat_command")]])
  caption = f"**🖋️ Custom File Name:**\n\nSupport for Custom Name before the File Extension.\nAdd name ..when txt is uploading"
  await callback_query.message.edit_media(
    InputMediaPhoto(
      media="https://tinypic.host/images/2025/07/14/file_000000002d44622f856a002a219cf27aconversation_id68747543-56d8-800e-ae47-bb6438a09851message_id8e8cbfb5-ea6c-4f59-974a-43bdf87130c0.png",
      caption=caption
      ),
      reply_markup=keyboard
  )
# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,
@bot.on_callback_query(filters.regex("titlle_command"))
async def titlle_button(client, callback_query):
  keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back to Feature", callback_data="feat_command")]])
  caption = f"**Custom Title Feature :**\nAdd and customize titles at the starting\n**NOTE 📍 :** The Titile must enclosed within (Title), Best For appx's .txt file."
  await callback_query.message.edit_media(
    InputMediaPhoto(
      media="https://tinypic.host/images/2025/07/14/file_000000002d44622f856a002a219cf27aconversation_id68747543-56d8-800e-ae47-bb6438a09851message_id8e8cbfb5-ea6c-4f59-974a-43bdf87130c0.png",
      caption=caption
      ),
      reply_markup=keyboard
  )
# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,
@bot.on_callback_query(filters.regex("broadcast_command"))
async def pin_button(client, callback_query):
  keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back to Feature", callback_data="feat_command")]])
  caption = f"**📢 Broadcasting Support:**\n\n◆/broadcast - 📢 Broadcast to All Users.\n◆/broadusers - 👁️ To See All Broadcasting User"
  await callback_query.message.edit_media(
    InputMediaPhoto(
      media="https://tinypic.host/images/2025/07/14/file_000000002d44622f856a002a219cf27aconversation_id68747543-56d8-800e-ae47-bb6438a09851message_id8e8cbfb5-ea6c-4f59-974a-43bdf87130c0.png",
      caption=caption
      ),
      reply_markup=keyboard
  )
# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,
@bot.on_callback_query(filters.regex("txt_maker_command"))
async def editor_button(client, callback_query):
  keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back to Feature", callback_data="feat_command")]])
  caption = f"**🤖 Available Commands 🗓️**\n◆/t2t for text to .txt file\n"
  await callback_query.message.edit_media(
    InputMediaPhoto(
      media="https://tinypic.host/images/2025/07/14/file_000000002d44622f856a002a219cf27aconversation_id68747543-56d8-800e-ae47-bb6438a09851message_id8e8cbfb5-ea6c-4f59-974a-43bdf87130c0.png",
      caption=caption
      ),
      reply_markup=keyboard
  )
# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,
@bot.on_callback_query(filters.regex("yt_command"))
async def y2t_button(client, callback_query):
  keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back to Feature", callback_data="feat_command")]])
  caption = f"**YouTube Commands:**\n\n◆/y2t - 🔪 YouTube Playlist → .txt Converter\n◆/ytm - 🎶 YouTube → .mp3 downloader\n\n<blockquote><b>◆YouTube → .mp3 downloader\n01. Send YouTube Playlist.txt file\n02. Send single or multiple YouTube links set\neg.\n`https://www.youtube.com/watch?v=xxxxxx\nhttps://www.youtube.com/watch?v=yyyyyy`</b></blockquote>"
  await callback_query.message.edit_media(
    InputMediaPhoto(
      media="https://envs.sh/GVi.jpg",
      caption=caption
      ),
      reply_markup=keyboard
  )

# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,
@bot.on_callback_query(filters.regex("html_command"))
async def y2t_button(client, callback_query):
  keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back to Feature", callback_data="feat_command")]])
  caption = f"**HTML Commands:**\n\n◆/t2h - 🌐 .txt → .html Converter"
  await callback_query.message.edit_media(
    InputMediaPhoto(
      media="https://envs.sh/GVI.jpg",
      caption=caption
      ),
      reply_markup=keyboard
  )

# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,



# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,

@bot.on_message(filters.command(["id"]))
async def id_command(client, message: Message):
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton(text="Send to Owner", url=f"tg://openmessage?user_id={OWNER}")]])
    chat_id = message.chat.id
    text = f"<blockquote expandable><b>The ID of this chat id is:</b></blockquote>\n`{chat_id}`"
    
    if str(chat_id).startswith("-100"):
        await message.reply_text(text)
    else:
        await message.reply_text(text, reply_markup=keyboard)

# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,

@bot.on_message(filters.private & filters.command(["info"]))
async def info(bot: Client, update: Message):
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton(text="📞 Contact", url=f"tg://openmessage?user_id={OWNER}")]])
    text = (
        f"╭────────────────╮\n"
        f"│✨ **Your Telegram Info**✨ \n"
        f"├────────────────\n"
        f"├🔹**Name :** `{update.from_user.first_name} {update.from_user.last_name if update.from_user.last_name else 'None'}`\n"
        f"├🔹**User ID :** @{update.from_user.username}\n"
        f"├🔹**TG ID :** `{update.from_user.id}`\n"
        f"├🔹**Profile :** {update.from_user.mention}\n"
        f"╰────────────────╯"
    )
    
    await update.reply_text(        
        text=text,
        disable_web_page_preview=True,
        reply_markup=keyboard
    )

# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,
@bot.on_message(filters.command(["logs"]))
async def send_logs(client: Client, m: Message):  # Correct parameter name
    try:
        with open("logs.txt", "rb") as file:
            sent = await m.reply_text("**📤 Sending you ....**")
            await m.reply_document(document=file)
            await sent.delete()
    except Exception as e:
        await m.reply_text(f"**Error sending logs:**\n<blockquote>{e}</blockquote>")

# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,
@bot.on_message(filters.command(["reset"]))
async def restart_handler(_, m):
    if m.chat.id != OWNER:
        return
    else:
        await m.reply_text("𝐁𝐨𝐭 𝐢𝐬 𝐑𝐞𝐬𝐞𝐭𝐢𝐧𝐠...", True)
        os.execl(sys.executable, sys.executable, *sys.argv)

# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,
@bot.on_message(filters.command("stop") & filters.private)
async def cancel_handler(client: Client, m: Message):
    if m.chat.id not in AUTH_USERS:
        print(f"User ID not in AUTH_USERS", m.chat.id)
        await bot.send_message(
            m.chat.id, 
            f"<blockquote>__**Oopss! You are not a Premium member**__\n"
            f"__**PLEASE /upgrade YOUR PLAN**__\n"
            f"__**Send me your user id for authorization**__\n"
            f"__**Your User id** __- `{m.chat.id}`</blockquote>\n\n"
        )
    else:
        if globals.processing_request:
            globals.cancel_requested = True
            await m.delete()
            cancel_message = await m.reply_text("**🚦 Process cancel request received. Stopping after current process...**")
            await asyncio.sleep(30)  # 30 second wait
            await cancel_message.delete()
        else:
            await m.reply_text("**⚡ No active process to cancel.**")
            
# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,
@bot.on_message(filters.command("addauth") & filters.private)
async def call_add_auth_user(client: Client, message: Message):
    await add_auth_user(client, message)

# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,
@bot.on_message(filters.command("users") & filters.private)
async def call_list_auth_users(client: Client, message: Message):
    await list_auth_users(client, message)
    
# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,
@bot.on_message(filters.command("rmauth") & filters.private)
async def call_remove_auth_user(client: Client, message: Message):
    await remove_auth_user(client, message)
    
# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,
@bot.on_message(filters.command("broadcast") & filters.private)
async def call_broadcast_handler(client: Client, message: Message):
    await broadcast_handler(client, message)
    
# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,
@bot.on_message(filters.command("broadusers") & filters.private)
async def call_broadusers_handler(client: Client, message: Message):
    await broadusers_handler(client, message)
    
# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,
@bot.on_message(filters.command("cookies") & filters.private)
async def call_cookies_handler(client: Client, m: Message):
    await cookies_handler(client, m)

# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,
@bot.on_message(filters.command(["t2t"]))
async def call_text_to_txt(bot: Client, m: Message):
    await text_to_txt(bot, m)

# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,
@bot.on_message(filters.command(["y2t"]))
async def call_y2t_handler(bot: Client, m: Message):
    await y2t_handler(bot, m)

# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,
@bot.on_message(filters.command(["ytm"]))
async def call_ytm_handler(bot: Client, m: Message):
    await ytm_handler(bot, m)

# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....
@bot.on_message(filters.command("getcookies") & filters.private)
async def call_getcookies_handler(client: Client, m: Message):
    await getcookies_handler(client, m)

#...............…........# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,
@bot.on_message(filters.command(["t2h"]))
async def call_html_handler(bot: Client, message: Message):
    await html_handler(bot, message)
    
# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,
@bot.on_message(filters.private & (filters.document | filters.text))
async def call_drm_handler(bot: Client, m: Message):
    await drm_handler(bot, m)
                          
# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,

def notify_owner():
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": OWNER,
        "text": "𝐁𝐨𝐭 𝐑𝐞𝐬𝐭𝐚𝐫𝐭𝐞𝐝 𝐒𝐮𝐜𝐜𝐞𝐬𝐬𝐟𝐮𝐥𝐥𝐲 ✅"
    }
    requests.post(url, data=data)


def reset_and_set_commands():
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/setMyCommands"
    # Reset
    requests.post(url, json={"commands": []})
    # Set new
    commands = [
        {"command": "start", "description": "✅ Check Alive the Bot"},
        {"command": "stop", "description": "🚫 Stop the ongoing process"},
        {"command": "id", "description": "🆔 Get Your ID"},
        {"command": "info", "description": "ℹ️ Check Your Information"},
        {"command": "cookies", "description": "📁 Upload YT Cookies"},
        {"command": "y2t", "description": "🔪 YouTube → .txt Converter"},
        {"command": "ytm", "description": "🎶 YouTube → .mp3 downloader"},
        {"command": "t2t", "description": "📟 Text → .txt Generator"},
        {"command": "t2h", "description": "🌐 .txt → .html Converter"},
        {"command": "logs", "description": "👁️ View Bot Activity"},
        {"command": "broadcast", "description": "📢 Broadcast to All Users"},
        {"command": "broadusers", "description": "👨‍❤️‍👨 All Broadcasting Users"},
        {"command": "addauth", "description": "▶️ Add Authorisation"},
        {"command": "rmauth", "description": "⏸️ Remove Authorisation "},
        {"command": "users", "description": "👨‍👨‍👧‍👦 All Premium Users"},
        {"command": "reset", "description": "✅ Reset the Bot"}
    ]
    requests.post(url, json={"commands": commands})
    



if __name__ == "__main__":
    reset_and_set_commands()
    notify_owner() 


bot.run()
