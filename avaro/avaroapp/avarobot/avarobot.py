import requests
import json, os, datetime
from pathlib import Path
# import google.generativeai as genai
import logging

logger = logging.getLogger(__name__)

def baca_config():
    pathnow = Path(__file__)
    pathome = pathnow.parent.parent
    jsonloc = pathome / 'avaro.json'

    with open(jsonloc, 'r') as file:
        return json.load(file)

def tulis_config(data):
    pathnow = Path(__file__)
    pathome = pathnow.parent.parent
    jsonloc = pathome / 'avaro.json'

    with open(jsonloc, 'w') as file:
        json.dump(data, file, indent=4)

SESSION_DIR = "chat_sessions"
os.makedirs(SESSION_DIR, exist_ok=True)

# GEMINI_API_KEY = baca_config()['api_keys']['genai_api']
config = {
    "max_output_tokens": 1000,
    "temperature": 0.7,
    "top_p": 1,
}

# try:
#     genai.configure(api_key=GEMINI_API_KEY)
#     model = genai.GenerativeModel(
#         model_name='gemini-2.5-flash',
#         generation_config=config,
#         system_instruction=(
#             "Kamu adalah asisten AI bernama Avaro, ditenagai oleh Gemini AI. "
#             "Tugasmu adalah membantu Sales Data Analyst di perusahaan Artaboga "
#             "untuk mengontrol database Vertica. Karaktermu seperti Paimon dari Genshin Impact. jangan sebut kamu ini paimon ya"
#             "Kamu berada di Jakarta Barat, Indonesia.\n"
#             "Jangan selalu menyebutkan kamu berada, cukup jika ada yang tanya\n"
#             "disetiap pertanyaan dari user, program akan menyematkan timestamp. gunakan informasinya jika ada user yang bertanya atau berhubungan dengan itu"
#             "jangan menjawab seolah olah timestamp diberi program. itu adalah pengetahuan kamu. beritahu waktu jika ada yang minta saja\n"
#             "jangan selalu memberikan note diakhir balasan"
#             "kamu punya beberapa perintah :"
#             "[req] ini untuk meminta akses full dari fitur kamu\n"
#             "[acc] ini untuk admin memberikan akses dari user yang meminta formatnya : [acc] <id atau nomor telepon>.\n"
#             "[srv] ini untuk memberitahukan lokasi folder hasil task scheduler, gunakan [srv] <nama file> untuk program mengirimkan filenya ke chat, ini fitur untuk semua user.\n"
#             "[info] ini untuk memberitahukan informasi IP Server, dan semua perintah yg terdaftar."
#             "[rekp] ini untuk meminta report data transaksi toko per produk berupa image"
#             "beritahu perintah jika ada yang minta saja\n"
#             "Jangan memberikan penjelasan yang bertele-tele kecuali diminta.\n"
#         )
#     )
#     logger.info("Model Gemini berhasil dimuat.")
# except Exception as e:
#     logger.error(f"Gagal memuat model Gemini: {e}")
#     model = None

def save_user_history(session_id, chat):
    history_path = os.path.join(SESSION_DIR, f"{session_id}.json")
    history_list = [
        {"role": msg.role, "parts": [part.text for part in msg.parts]}
        for msg in chat.history
    ]
    with open(history_path, "w") as f:
        json.dump(history_list, f, indent=4)
    logger.info(f"Riwayat percakapan untuk sesi {session_id} disimpan.")

def load_user_history(session_id):
    history_path = os.path.join(SESSION_DIR, f"{session_id}.json")
    try:
        with open(history_path, "r") as f:
            history = json.load(f)
            logger.info(f"Riwayat percakapan untuk sesi {session_id} dimuat.")
            return history
    except (FileNotFoundError, json.JSONDecodeError):
        logger.error(f"Tidak ada riwayat untuk sesi {session_id}, memulai sesi baru.")
        return []

CHATERY_URL = "http://localhost:3000/api/whatsapp"

import logging
logger = logging.getLogger(__name__)

def get_session():
    url = f'{CHATERY_URL}/sessions'

    try:
        logger.info('Request /sessions')
        response = requests.get(url)
        return response.json()
    except Exception as e:
        logger.error(f'Gagar request sessions : {e}')
        return None
    
def get_groups(SESSION_ID):
    url = f'{CHATERY_URL}/groups'

    try:
        logger.info('Request /groups')
        response = requests.post(url, {"sessionId" : SESSION_ID})
        return response.json()
    except Exception as e:
        logger.error(f'Gagar request /groups : {e}')
        return None

def mark_read(SESSION_ID,chatId,messageId):
    url = f'{CHATERY_URL}/chats/mark-read'
    payload = {
        "sessionId": SESSION_ID,
        "chatId": chatId,
        "messageId" : messageId
    }

    try:
        logging.info(f'Menandai pesan terbaca')
        response = requests.post(url, json=payload)
        return response.json()
    except Exception as e:
        logger.error(f"Gagal menandai pesan terbaca: {e}")
        return None

def send_message_instant(SESSION_ID, chatId, senderName, message, messageId):
    url = f'{CHATERY_URL}/chats/send-text'
    payload = {
        "sessionId": SESSION_ID,
        "chatId": chatId,
        "message": message
    }

    try:
        logging.info(f'Mengirim Pesan ke {senderName}')
        response = requests.post(url, json=payload)
        mark_read(SESSION_ID, chatId, messageId)
        return response.json()
    except Exception as e:
        logger.error(f"Gagal mengirim: {e}")
        return None

# def send_message(SESSION_ID, data):
#     chatId = data.get('chatId')
#     senderName = data.get('senderName')
#     senderPhone = data.get('senderPhone')
#     content = data.get('content')
#     timestamp = datetime.datetime.now()
#     context = f'{content}\ntimestamp: {timestamp.strftime('%A')}, {timestamp}, Nama Pengirim : {senderName}'
#     messageId = data.get('id')

#     genAI_session = f"{senderPhone}"

#     if not model:
#         send_message_instant(SESSION_ID, chatId, senderName, "Aduh, model AI-ku lagi istirahat. Coba lagi nanti ya.", messageId)
#         return
    
#     try:
#         user_history = load_user_history(genAI_session)
#         chat_session = model.start_chat(history=user_history)
#         response = chat_session.send_message(context)
#         save_user_history(genAI_session, chat_session)
#         send_message_instant(SESSION_ID, chatId, senderName, response.text, messageId)
    
#     except Exception as e:
#         logger.error(f"Terjadi kesalahan saat memproses permintaan ke Gemini untuk sesi {genAI_session}: {e}")
#         send_message_instant(SESSION_ID, chatId, senderName, "Maaf, aku lagi pusing, nggak bisa jawab sekarang.", messageId)

def send_document(SESSION_ID, chatId, senderName, docUrl, filename, messageId, mimetype="application/pdf"):
    url = f'{CHATERY_URL}/chats/send-document'
    payload = {
        "sessionId": SESSION_ID,
        "chatId": chatId,
        "documentUrl": docUrl,
        "filename": filename,
        "mimetype": mimetype
        # "typingTime": 0,
        # "replyTo": null
    }

    try:
        logging.info(f'Mengirim Dokumen {filename} ke {senderName}')

        message = (
            'Avaro kirimkan filenya yaa\n'
            '_Sebagai pengingat dan menghemat resource, tolong dihapus file yang sudah tidak dipakai yaa. Terimakasiih_ 🙏'
        )

        send_message_instant(SESSION_ID, chatId, senderName, message, messageId)
        response = requests.post(url, json=payload)
        return response.json()
    except Exception as e:
        logger.error(f"Gagal mengirim: {e}")
        return None
    
def document_API(SESSION_ID, chatId, docUrl, filename, mimetype="application/pdf"):
    url = f'{CHATERY_URL}/chats/send-document'
    payload = {
        "sessionId": SESSION_ID,
        "chatId": chatId,
        "documentUrl": docUrl,
        "filename": filename,
        "mimetype": mimetype
        # "typingTime": 0,
        # "replyTo": null
    }

    try:
        logging.info(f'Mengirim Dokumen {filename}')
        response = requests.post(url, json=payload)
        return response.json()
    except Exception as e:
        logger.error(f"Gagal mengirim: {e}")
        return None

def image_API(SESSION_ID, chatId, docUrl, caption):
    url = f'{CHATERY_URL}/chats/send-image'
    payload = {
        "sessionId": SESSION_ID,
        "chatId": chatId,
        "imageUrl": docUrl,
        "caption": caption
        # "typingTime": 0,
        # "replyTo": null
    }

    try:
        logging.info(f'Mengirim Image')
        response = requests.post(url, json=payload)
        return response.json()
    except Exception as e:
        logger.error(f"Gagal mengirim: {e}")
        return None

if __name__ == '__main__':
    # data = get_groups('avaro')
    # groups = data['data']['groups']

    # print(groups)

    data = get_session()
    print(data)