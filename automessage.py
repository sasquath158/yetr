from pyrogram import Client, filters
import time
import os
import asyncio
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, KeyboardButton
import random
from pyrogram.types import InputMediaPhoto
import json 
import string
import types

# Telegram API bilgilerinizi burada ayarlayın
api_id = '28146275'
api_hash = 'ea9aca8caf15a6e62d71ecca5b6a404d'
bot_token = '6972869235:AAEH3tdTIcQi2VN8ItdWa6fCfbEQXfPzQBQ'
app = Client('my_bot', api_id=api_id, api_hash=api_hash, bot_token=bot_token)

saved_photos = []
photo_captions = {}


@app.on_message(filters.command("start"))
def start_command(client, message):
    user = message.from_user
    
    #Asagidaki, url yerine baska bir fotograf urlsi koyarsaniz, start komutunda o fotografi gosterir.
    photo_url = "https://cdn-icons-png.flaticon.com/512/6134/6134346.png"
    caption = f"{user.mention} Naber? 🪂"

    keyboard = [
        [InlineKeyboardButton("🛠️ Kullanım", callback_data="button3")]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    client.send_photo(
        chat_id=message.chat.id,
        photo=photo_url,
        caption=caption,
        reply_markup=reply_markup
    )


@app.on_callback_query(filters.regex("button3"))
def button3_callback(client, callback_query):
    caption = "**⚙️ Kullanım kılavuzu:\n\n/ekle - fotoğraf eklemek için: ekle komutu gönderdikten sonra, fotoğraf gönderin. Daha sonra, mesajın başına C: yazarak, fotoğraf açıklaması yazın örnek: C: fotoğraf açıklaması daha sonra B: yazarak button ismi ve linki belirtin. Örnek: B:Buton ismi-Buton_linki  DİKKAT: button ismi ve buton linki arasinda - işareti koyun ve oan bitişik yazın aksi halde hata olur ve botunuz çöker \n/oto - bu komutu kullandığınızda, bota eklediğiniz, fotoğraflar, 20 dakika ara ile gruba gönderilir.\n/soto - bu komut ile aktiv bir gönderi paylaşımı varsa, onu durdura bilirsiniz\n/sil - bu komutla, bota eklediğiniz her-hangi bir fotoğrafı sile bilirsiniz. Bunun için /sil resim_ismi yazmanız yeterli.\n/listele bu komut ile, botda ekli olan fotoğrafları isimleri ile birlikte göre bilirsiniz**"

    keyboard = [
        [InlineKeyboardButton("👨🏻‍💻 yapımcı", url="https://t.me/Sananebekardesim"), InlineKeyboardButton("👈🏻 Geri", callback_data="button6")]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    callback_query.message.edit_caption(
        caption=caption,
        reply_markup=reply_markup
    )
  
@app.on_callback_query(filters.regex("button6"))
def button6_callback(client, callback_query):
    caption = "**Naber? 🪂**"

    keyboard = [
        [InlineKeyboardButton("🛠️ Kullanım", callback_data="button3")] ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    callback_query.message.edit_caption(
        caption=caption,
        reply_markup=reply_markup
    )



auto_sender_active = False

def oto(client, message):
    global auto_sender_active
    # Buraya kimin id sini koyarsaniz botu yalnizca o kullana bilir.
    if message.from_user.id == 6214828761:
        
        auto_sender_active = True

        photos = [f for f in os.listdir("auto_sender/downloads") if f.endswith(".jpg")]
        sphotos = len(photos)
        pnumber = 0

        while auto_sender_active:
            if not photos:
                break

            photo = photos.pop(0)
            photo_path = os.path.join("auto_sender/downloads", photo)

            caption_file_path = os.path.join("auto_sender/downloads", f"{photo.split('.')[0]}.txt")
            caption = ""
            if os.path.exists(caption_file_path):
                with open(caption_file_path, "r") as file:
                    caption = file.read()
                    
            # Buton adını ve linkini JSON dosyasından al
            json_data = open(f"auto_sender/downloads/{photo.split('.')[0]}.json", "r")
            json_data = json.load(json_data)
            button_name = json_data["button_name"]
            button_link = json_data["button_link"]

            # InlineKeyboardMarkup nesnesi oluştur
            keyboard = [
            [InlineKeyboardButton(button_name, url=button_link)] ]
            
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            client.send_photo(
               chat_id=message.chat.id,
               photo=photo_path,
               caption=caption,
               reply_markup=reply_markup
    )
            time.sleep(600)
            pnumber += 1
            
            if not auto_sender_active:
                break
                
            elif pnumber == sphotos: 
                oto(client, message)
           
                

@app.on_message(filters.command("oto"))
def oto_message(client, message):
    
    if message.from_user.id == 6214828761:
        if auto_sender_active == True:
            message.reply("**🫨 Zaten aktif bir oto mesaj gönderimi var**")
            return
        oto(client, message)



        
@app.on_message(filters.command("soto"))
def soto(client, message):
    global auto_sender_active
    
    if auto_sender_active == False:
        message.reply("**🫨 Zaten aktif bir oto mesaj gönderimi yok**")
        return
    # Sadece belirli kişi kullanabilir
    if message.from_user.id == 6214828761:

        auto_sender_active = False
        time.sleep(0.6)
        message.reply("**❌ Otomatik gönderimi durdurdum**")


@app.on_message(filters.command("listele"))
async def listele(client, message):
    # Sadece belirli bir kişi kullanabilir
    if message.from_user.id == 6214828761:
        await message.reply("**Hemen listeliyorumm ✍🏻**")
        photo_folder = "auto_sender/downloads"
        photo_files = [f for f in os.listdir(photo_folder) if f.endswith(".jpg")]
        
        for photo in photo_files:
            photo_path = os.path.join(photo_folder, photo)
            await client.send_photo(message.chat.id, photo_path, caption=photo)
            await asyncio.sleep(2)


@app.on_message(filters.command("sil"))
async def sil(client, message):
    # Sadece belirli bir kişi kullanabilir
    if message.from_user.id == 6214828761:
        
        command_parts = message.text.split()
        if len(command_parts) != 2:
            await message.reply("**❔ Doğru kullanım:\n /sil resim_ismi**")
        else:
            resim_ismi = command_parts[1]
            photo_folder = "auto_sender/downloads"
            photo_path = os.path.join(photo_folder, f"{resim_ismi}.jpg")
            caption_file_path = os.path.join(photo_folder, f"{resim_ismi}.txt")
            buttonn_path = os.path.join(photo_folder, f"{resim_ismi}.json")

            if os.path.exists(photo_path) and photo_path.endswith(".jpg"):
                os.remove(photo_path)
                if os.path.exists(caption_file_path):
                    os.remove(caption_file_path)
                if os.path.exists(buttonn_path):
                    os.remove(buttonn_path)
                    
                await message.reply(f"**{resim_ismi} isimli fotoğrafı sildim 🚮**")
            else:
                await message.reply(f"**{resim_ismi} isimli fotoğrafı bulamadım 🤷🏻‍♀️**")


resim_ismi = None

@app.on_message(filters.user(6214828761))
async def on_message(client, message):

    if message.text == "/ekle":
        
        if auto_sender_active == True:
            await message.reply("**aktif bir gönderim var, onu /soto ile durdurup daha sonra ekleme yapın!**")
            return
        
        await message.reply("**📸 Lütfen fotoğrafı gönderin**")

        return

    if message.photo:
        
        if auto_sender_active == True:
            await message.reply("**aktif bir gönderim var, onu /soto ile durdurup daha sonra ekleme yapın!**")
            return
            
        global resim_ismi

        characters = string.ascii_lowercase + string.ascii_uppercase + string.digits
        resim_ismi = ''.join(random.choice(characters) for _ in range(12))

        file_path = os.path.join("downloads", f"{resim_ismi}.jpg")
        await client.download_media(message.photo, file_path)

        await message.reply("**✍🏻 Bir açıklama yazın\n\n💢NOT: mesajın başına, C: yazmayı unutma**")

    if message.text and message.text.startswith("C:"):
        if auto_sender_active == True:
            await message.reply("**aktif bir gönderim var, onu /soto ile durdurup daha sonra ekleme yapın!**")
            return
        caption = message.text[2:]
        file_path = os.path.join(f"auto_sender/downloads", f"{resim_ismi}.txt")
        with open(file_path, "w") as f:
            f.write(caption)
            
        await message.reply("**Buton için ad ve link yazın doğru yazım şekli 👇🏻\n\nbutton_ismi-button_linki\n\n💢NOT: mesajın başına B: yazmayı unutma. Ve button linkini - işaretine Birleşik yaz yoksa bot çöker!**")

    if message.text and message.text.startswith("B:"):
        if auto_sender_active == True:
            await message.reply("**aktif bir gönderim var, onu /soto ile durdurup daha sonra ekleme yapın!**")
            return
        button_data = message.text[2:].split("-")

        button_name = button_data[0]
        button_link = button_data[1]

        await client.send_message(message.chat.id, f"**İşlem tamamlandı 😼**")
        button_data = {
            "button_name":button_name,
            "button_link":button_link,
        }

        with open(f"auto_sender/downloads/{resim_ismi}.json", "w") as f:
            json.dump(button_data, f, indent=4)


app.run()
