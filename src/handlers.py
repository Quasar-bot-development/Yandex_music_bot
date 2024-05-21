from aiogram.filters.command import Command
from aiogram import F, Bot
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram import Router
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
import src.keyboards as kb
import src.db as db
from src.config import ADMIN_ID



router = Router()


class Track(StatesGroup):
    name = State()


@router.message(F.text, Command("start"))
async def start_loop(message: Message, bot: Bot):
    await message.answer(text=f"Привет, @{message.from_user.username}!\n"
        "Я бот-диджей🧑🏻‍💻, который поможет тебе быстро, просто и бесплатно находить треки любимых исполнителей \n"
        "и скачивать их прямиком с Яндекс Музыки🎧", reply_markup=kb.main_keyboard)
    if not db.is_old(message.from_user.id):
        db.add_new_user(message.from_user.id, message.from_user.username)
        
        
@router.message(F.text == "Найти трек🔎")  
async def find_track(message: Message, bot: Bot, state = FSMContext):  
    await state.set_state(Track.name)
    await message.answer(text="Введите название трека🎵") 
    
    

@router.message(Track.name)
async def get_name(message: Message,state = FSMContext):
    await state.update_data(name = message.text)
    data = await state.get_data()
    await message.answer(text="По твоему запросу я нашёл следующие треки:", reply_markup=kb.generate_tracks_keyboard(str(data["name"])))
    
    
        
        
@router.message(F.text == "/users")  
async def get_db(message: Message, bot: Bot):  
    if str(message.from_user.id) in ADMIN_ID:  
        db.get_xlsx()
        await message.answer_document(document=FSInputFile("./db/data.xlsx")) 
        # os.remove(f"data.xlsx") 
        

@router.callback_query(F.data == "balance")
async def send_random_value(callback: CallbackQuery, bot: Bot):
    user_balance = db.get_balance(callback.from_user.id)
    await callback.message.edit_caption(caption = f"Ваш текущий баланс: {user_balance} SHEIKH")
    await callback.message.edit_reply_markup(reply_markup = kb.main_keyboard)

