import tempfile
import time

import requests
import telepot
from openai import OpenAI
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardButton, InlineKeyboardMarkup

# Inicialização do cliente OpenAI
client = OpenAI()

# Substitua 'YOUR_TELEGRAM_TOKEN' pelo token do seu bot
TOKEN = "YOUR_TELEGRAM_TOKEN"
bot = telepot.Bot(TOKEN)

# Dicionário para manter o estado do usuário
user_state = {}


# Função para criar teclado de escolha de tamanho
def tamanho_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="1024x1024", callback_data="1024x1024")],
            [InlineKeyboardButton(text="1024x1792", callback_data="1024x1792")],
            [InlineKeyboardButton(text="1792x1024", callback_data="1792x1024")],
        ]
    )
    return keyboard


# Função para criar teclado de escolha de qualidade
def qualidade_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="HD", callback_data="hd")],
            [InlineKeyboardButton(text="Standard", callback_data="standard")],
        ]
    )
    return keyboard


# Função para lidar com mensagens de chat
def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type == "text":
        if msg["text"] == "/start":
            bot.sendMessage(chat_id, "Por favor, envie o prompt para a imagem.")
        else:
            user_state[chat_id] = {"prompt": msg["text"]}
            bot.sendMessage(
                chat_id, "Escolha o tamanho da imagem:", reply_markup=tamanho_keyboard()
            )


def pos_geracao_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Gerar outra imagem com o mesmo prompt",
                    callback_data="regerar_mesmo",
                )
            ],
            [
                InlineKeyboardButton(
                    text="Gerar imagem com novo prompt", callback_data="gerar_novo"
                )
            ],
        ]
    )
    return keyboard


# Função para lidar com queries de callback
def on_callback_query(msg):
    query_id, from_id, query_data = telepot.glance(msg, flavor="callback_query")
    bot.answerCallbackQuery(query_id)

    chat_id = msg["message"]["chat"]["id"]
    message_id = msg["message"]["message_id"]

    if chat_id not in user_state:
        user_state[chat_id] = {}

    if "size" not in user_state[chat_id]:
        # Escolha de tamanho
        user_state[chat_id]["size"] = query_data
        bot.sendMessage(
            chat_id, "Escolha a qualidade da imagem:", reply_markup=qualidade_keyboard()
        )
    elif "quality" not in user_state[chat_id]:
        # Escolha de qualidade
        user_state[chat_id]["quality"] = query_data

        # Geração da imagem
        bot.sendMessage(
            chat_id, "Sua solicitação está sendo processada. Aguarde um momento..."
        )
        generate_and_send_image(chat_id, user_state[chat_id])

        # Apresentar opções após enviar a imagem
        bot.sendMessage(
            chat_id,
            "O que gostaria de fazer agora?",
            reply_markup=pos_geracao_keyboard(),
        )

    elif query_data == "regerar_mesmo":
        # Regenerar imagem com o mesmo prompt
        bot.sendMessage(
            chat_id, "Gerando outra imagem com o mesmo prompt. Por favor, aguarde..."
        )
        generate_and_send_image(chat_id, user_state[chat_id])
        bot.sendMessage(
            chat_id,
            "O que gostaria de fazer agora?",
            reply_markup=pos_geracao_keyboard(),
        )

    elif query_data == "gerar_novo":
        # Solicitar um novo prompt
        bot.sendMessage(
            chat_id,
            "Prezado usuário, por favor, forneça a descrição para a imagem que deseja gerar. Inclua detalhes relevantes para obter o melhor resultado.",
        )
        user_state[chat_id] = {"prompt": None}  # Resetar para um novo prompt


def generate_and_send_image(chat_id, user_data):
    response = client.images.generate(
        model="dall-e-3",
        prompt=user_data["prompt"],
        n=1,
        size=user_data["size"],
        quality=user_data["quality"],
    )

    image_url = response.data[0].url
    image_content = requests.get(image_url).content

    with tempfile.NamedTemporaryFile(delete=False) as temp_image:
        temp_image.write(image_content)
        temp_image.flush()
        bot.sendPhoto(chat_id, photo=open(temp_image.name, "rb"))


# Configuração do loop de mensagens
MessageLoop(
    bot, {"chat": on_chat_message, "callback_query": on_callback_query}
).run_as_thread()

print("Listening...")

# Mantenha o programa rodando
while 1:
    time.sleep(10)
