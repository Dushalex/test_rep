from aiogram import Router, Bot
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from dotenv import load_dotenv
from generators import AI

router = Router()
load_dotenv()

class Generate(StatesGroup):
    text = State()
    generate = State()
    process_message = State()

'''
async def generate(message: Message, state: FSMContext):
    # Обрабатываем сообщения с текстом, фото или видео
    if message.text or message.photo or message.video:
        await message.answer('Подождите, ваше сообщение обрабатывается...')
        await process_message(message, state)
'''

@router.message(Generate.process_message)
async def process_message(message: Message, state: FSMContext):
    # Берём исходный текст: если есть text, иначе caption
    original_text = message.text or message.caption or ""
    # Вызываем функцию для переписывания текста (через ChatGPT API)
    rewritten_text = AI(original_text)
    #rewritten_text = original_text
    
    # Если сообщение содержит фотографию, отправляем её с новым описанием
    if message.photo:
        photo_file_id = message.photo[-1].file_id
        await message.answer_photo(photo=photo_file_id, caption=rewritten_text)
    # Если сообщение содержит видео
    elif message.video:
        video_file_id = message.video.file_id
        await message.answer_video(video=video_file_id, caption=rewritten_text)
    # Если сообщение только с текстом
    else:
        await message.answer(rewritten_text)

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await message.answer('Добро пожаловать в бот!')
    await state.update_data(
        abstract_name=[''],
        abstracts=['']
    )

@router.message()
async def generate(message: Message, state: FSMContext):
    if message.text or message.photo:
        await state.set_state(Generate.text)
        await process_message(message, state)

@router.message(Generate.text)
async def genera_error(message: Message):
    await message.answer('Подождите, ваше сообщение обрабатывается...')
