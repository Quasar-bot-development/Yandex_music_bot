from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup
import src.yandex_music_api as yandex


main_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Найти трек🔎')]],
    resize_keyboard=True)


def generate_tracks_keyboard(track_name):
    buttons = []
    tracks = yandex.get_tracks(track_name)
    for track in tracks[:5]:
        title, artists = yandex.get_info(track)        
        buttons.append([InlineKeyboardButton(text=f"{str(artists)}-{str(title)}"
                                                , callback_data='id')])
    tracks_keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return tracks_keyboard