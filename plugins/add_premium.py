import pytz
import os
import asyncio
from datetime import time, datetime, timedelta
from info import *
from Script import script
from utils import get_seconds
from database.users_chats_db import db
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors.exceptions.bad_request_400 import MessageTooLong
from pyrogram.errors import FloodWait

@Client.on_message(filters.command("remove_premium") & filters.user(ADMINS))
async def remove_premium(client, message):
    if len(message.command) == 2:
        user_id = int(message.command[1])
        user = await client.get_users(user_id)
        if await db.has_premium_access(user_id):
            await db.remove_premium_access(user_id)
            await message.reply_text(f"<b>Sᴜᴄᴄᴇssꜰᴜʟʟy Rᴇᴍᴏᴠᴇᴅ {user.mention}'s Pʀᴇᴍɪᴜᴍ Sᴜʙꜱᴄʀɪᴘᴛɪᴏɴ ❗</b>")
            try:
                await client.send_message(chat_id=user_id, text=f"<b><i>Hᴇʏ Tʜᴇʀᴇ {user.mention} 👋</i>\n\nYᴏᴜʀ Pʀᴇᴍɪᴜᴍ Sᴜʙꜱᴄʀɪᴘᴛɪᴏɴ Hᴀs Bᴇᴇɴ Rᴇᴍᴏᴠᴇᴅ ❌</b>\n\n<b>Fᴏʀ Aɴʏ Hᴇʟᴘ Cᴏɴᴛᴀᴄᴛ Aᴅᴍɪɴ @TheKunalPMBot</b>")
            except:
                pass
        else:
            await message.reply_text(f"<b>idk who is this {user.mention} ❓</b>")
    else:
        await message.reply_text("<b>Cᴏᴍᴍᴀɴᴅ Iɴᴄᴏᴍᴘʟᴇᴛᴇ...</b>")

@Client.on_message(filters.private & filters.command("myplan"))
async def myplan(client, message):
    user = message.from_user.mention
    user_id = message.from_user.id
    data = await db.get_user(message.from_user.id)
    if data and data.get("expiry_time"):
        expiry = data.get("expiry_time") 
        expiry_ist = expiry.astimezone(pytz.timezone(TIMEZONE))
        expiry_str_in_ist = expiry.astimezone(pytz.timezone(TIMEZONE)).strftime("%d-%m-%Y %I:%M:%S %p")            

        current_time = datetime.now(pytz.timezone(TIMEZONE))
        time_left = expiry_ist - current_time

        days = time_left.days
        hours, remainder = divmod(time_left.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        time_left_str = f"{days} days, {hours} hours, {minutes} minutes"
        await message.reply_text(f"<b><u>Cᴜʀʀᴇɴᴛ Pʟᴀɴ Dᴇᴛᴀɪʟs 📊</u>\n\nUꜱᴇʀ : {user}\n\nUꜱᴇʀ Iᴅ : <code>{user_id}</code>\n\nTɪᴍᴇ Lᴇꜰᴛ : <code>{time_left_str}</code>\n\nExᴘ Tɪᴍᴇ : <code>{expiry_str_in_ist}</code></b>", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("💰 Uᴘɢʀᴀᴅᴇ", url="t.me/J_shree_ram"), InlineKeyboardButton("Cʟᴏsᴇ ❌", callback_data="close_data")]])) 
    else:
        await message.reply_text(f"<b>ʜᴇʏ {user},\n\nʏᴏᴜ ᴅᴏ ɴᴏᴛ ʜᴀᴠᴇ ᴀɴʏ ᴀᴄᴛɪᴠᴇ ᴘʀᴇᴍɪᴜᴍ ᴘʟᴀɴs, ɪꜰ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴛᴀᴋᴇ ᴘʀᴇᴍɪᴜᴍ ᴛʜᴇɴ ᴄʟɪᴄᴋ ᴏɴ /plans ᴛᴏ ᴋɴᴏᴡ ᴀʙᴏᴜᴛ ᴛʜᴇ ᴘʟᴀɴs...</b>")

@Client.on_message(filters.command("add_premium") & filters.user(ADMINS))
async def give_premium_cmd_handler(client, message):
    if len(message.command) == 4:
        time_zone = datetime.now(pytz.timezone(TIMEZONE))
        current_time = time_zone.strftime("%d-%m-%Y %I:%M:%S %p") 
        user_id = int(message.command[1])
        user = await client.get_users(user_id)
        time = message.command[2]+" "+message.command[3]
        seconds = await get_seconds(time)
        if seconds > 0:
            expiry_time = datetime.now() + timedelta(seconds=seconds)
            user_data = {"id": user_id, "expiry_time": expiry_time}
            await db.update_user(user_data)
            data = await db.get_user(user_id)
            expiry = data.get("expiry_time")
            expiry_str_in_ist = expiry.astimezone(pytz.timezone(TIMEZONE)).strftime("%d-%m-%Y %I:%M:%S %p")         
            await message.reply_text(f"<b>#PREMIUM_ADDED\n\nUsᴇʀ : {user.mention} <code>[{user_id}]</code>\n\nVᴀʟɪᴅɪᴛʏ : <code>{time}</code>\n\nExᴘ Tɪᴍᴇ : <code>{expiry_str_in_ist}</code></b>", disable_web_page_preview=True)
            try:
                await client.send_message(chat_id=user_id, text=f"<b><i>Hᴇʏ Tʜᴇʀᴇ {user.mention} 👋</i>\n\nYᴏᴜʀ {time} Pʀᴇᴍɪᴜᴍ Sᴜʙꜱᴄʀɪᴘᴛɪᴏɴ Aᴅᴅᴇᴅ ✅\n\nYᴏᴜʀ Pʟᴀɴ Dᴇᴀᴛᴀɪʟꜱ ⚠️\n\nSᴜʙ ᴛɪᴍᴇ : <code>{current_time}</code>\n\nExᴘ ᴛɪᴍᴇ : <code>{expiry_str_in_ist}</code>\n\nFᴏʀ Aɴʏ Hᴇʟᴘ Cᴏɴᴛᴀᴄᴛ Aᴅᴍɪɴ @J_shree_ram</b>", disable_web_page_preview=True) 
            except:
                pass
            await client.send_message(PREMIUM_LOGS, text=f"<b>#PREMIUM_ADDED\n\nUsᴇʀ : {user.mention} <code>[{user_id}]</code>\n\nVᴀʟɪᴅɪᴛʏ : <code>{time}</code>\n\nExᴘ Tɪᴍᴇ : <code>{expiry_str_in_ist}</code></b>", disable_web_page_preview=True)                
        else:
            await message.reply_text("<i>Iɴᴠᴀʟɪᴅ Tɪᴍᴇ Fᴏʀᴍᴀᴛ...</i>\n\n1 day for days\n1 hour for hours\n1 min for minutes\n1 month for months\n1 year for year")
    else:
        await message.reply_text("<b>Cᴏᴍᴍᴀɴᴅ Iɴᴄᴏᴍᴘʟᴇᴛᴇ...</b>")

@Client.on_message(filters.private & filters.command("plans"))
async def allplans(bot, message):
    btn = [[
            InlineKeyboardButton("❗ Bᴜʏ Pʀᴇᴍɪᴜᴍ Pʟᴀɴ / Sᴇɴᴅ Sᴄʀᴇᴇɴsʜᴏᴛ ❗", url="t.me/J_shree_ram")
          ]]
    await message.reply_photo(
        photo="https://graph.org/file/0b88dee3a5e6a7fb32505.jpg",
        caption="premium plans\n\n1 month plan\n3 month plan\n6 month plan",
        reply_markup=InlineKeyboardMarkup(btn)
    )
