# -*- coding: utf-8 -*-

import telebot
# import database
from telebot import types
import config
from bot_db import DBManager
import translator

bot = telebot.TeleBot(config.BOT_TOKEN)

db = DBManager('kinorepa', 'postgres', 'postgres')
print("Database opened successfully")

genres = ['2_1_inline', '2_2_inline', '2_3_inline', '2_4_inline', '2_5_inline']
durations = ['3_1_inline', '3_2_inline', '3_3_inline']
ratings = ['4_1_inline', '4_2_inline', '4_3_inline', '4_4_inline']
years = ['5_1_inline', '5_2_inline', '5_3_inline', '5_4_inline']
result = []
genre_kb = None
duration_kb = None
rating_kb = None
year_kb = None

for i in range(4):
    a = set()
    result.append(a)

def change_keyboard(kb, call_back):
    new_kb = {}
    print(kb.to_dict())
    for i in range(len(kb.to_dict()['inline_keyboard'])):
        for item in kb.to_dict()['inline_keyboard'][i]:
            new_kb[item['callback_data']] = item['text']
    if new_kb[call_back][-1] == '+':
        new_kb[call_back] = new_kb[call_back][:-1]
        result[int(call_back[0]) - 2].remove(new_kb[call_back])
    else:
        result[int(call_back[0]) - 2].add(new_kb[call_back])
        new_kb[call_back] += '+'

    final_kb = types.InlineKeyboardMarkup()

    for val in new_kb.keys():
        if new_kb[val] != 'next' and new_kb[val] != 'find' and new_kb[val] != 'back':
            final_kb.add(types.InlineKeyboardButton(text=new_kb[val], callback_data=val))
    kb_1 = types.InlineKeyboardButton(text='next',
                                      callback_data=list(new_kb.keys())[list(new_kb.values()).index('next')])
    kb_2 = types.InlineKeyboardButton(text='back',
                                      callback_data=list(new_kb.keys())[list(new_kb.values()).index('back')])
    kb_3 = types.InlineKeyboardButton(text='find',
                                      callback_data=list(new_kb.keys())[list(new_kb.values()).index('find')])
    final_kb.add(kb_2, kb_3, kb_1)
    return final_kb


def keyboard(where_call):
    kb = types.InlineKeyboardMarkup()

    if where_call == 'start':
        kb_11 = types.InlineKeyboardButton(text='my_filters', callback_data='1_1_inline')
        kb_12 = types.InlineKeyboardButton(text='rand', callback_data='1_2_inline')
        kb.add(kb_11, kb_12)
        return kb

    elif where_call == 'genre':
        kb_21 = types.InlineKeyboardButton(text='genre1', callback_data='2_1_inline')
        kb_22 = types.InlineKeyboardButton(text='genre2', callback_data='2_2_inline')
        kb_23 = types.InlineKeyboardButton(text='genre3', callback_data='2_3_inline')
        kb_24 = types.InlineKeyboardButton(text='genre4', callback_data='2_4_inline')
        kb_25 = types.InlineKeyboardButton(text='genre5', callback_data='2_5_inline')
        kb.add(kb_21)
        kb.add(kb_22)
        kb.add(kb_23)
        kb.add(kb_24)
        kb.add(kb_25)
        kb_26 = types.InlineKeyboardButton(text='next', callback_data='2_6_inline')
        kb_27 = types.InlineKeyboardButton(text='back', callback_data='2_7_inline')
        kb_28 = types.InlineKeyboardButton(text='find', callback_data='2_8_inline')
        kb.add(kb_27, kb_28, kb_26)
        return kb

    elif where_call == 'duration':
        # duration1 - time < 90 min
        # duration2 - 90 min <= time <120 min
        # duration - time >= 120 min
        kb_31 = types.InlineKeyboardButton(text='duration1', callback_data='3_1_inline')
        kb_32 = types.InlineKeyboardButton(text='duration2', callback_data='3_2_inline')
        kb_33 = types.InlineKeyboardButton(text='duration3', callback_data='3_3_inline')
        kb_34 = types.InlineKeyboardButton(text='next', callback_data='3_4_inline')
        kb_35 = types.InlineKeyboardButton(text='back', callback_data='3_5_inline')
        kb_36 = types.InlineKeyboardButton(text='find', callback_data='3_6_inline')
        kb.add(kb_31)
        kb.add(kb_32)
        kb.add(kb_33)
        kb.add(kb_35, kb_36, kb_34)
        return kb

    elif where_call == 'rating':
        kb_41 = types.InlineKeyboardButton(text='rating_1', callback_data='4_1_inline')
        kb_42 = types.InlineKeyboardButton(text='rating_2', callback_data='4_2_inline')
        kb_43 = types.InlineKeyboardButton(text='rating_3', callback_data='4_3_inline')
        kb_44 = types.InlineKeyboardButton(text='rating_4', callback_data='4_4_inline')
        kb_45 = types.InlineKeyboardButton(text='next', callback_data='4_5_inline')
        kb_46 = types.InlineKeyboardButton(text='back', callback_data='4_6_inline')
        kb_47 = types.InlineKeyboardButton(text='find', callback_data='4_7_inline')
        kb.add(kb_41)
        kb.add(kb_42)
        kb.add(kb_43)
        kb.add(kb_44)
        kb.add(kb_46, kb_47, kb_45)
        return kb

    elif where_call == 'production_year':
        kb_51 = types.InlineKeyboardButton(text='year_1', callback_data='5_1_inline')
        kb_52 = types.InlineKeyboardButton(text='year_2', callback_data='5_2_inline')
        kb_53 = types.InlineKeyboardButton(text='year_3', callback_data='5_3_inline')
        kb_54 = types.InlineKeyboardButton(text='year_4', callback_data='5_4_inline')
        kb_55 = types.InlineKeyboardButton(text='next', callback_data='5_5_inline')
        kb_56 = types.InlineKeyboardButton(text='back', callback_data='5_6_inline')
        kb_57 = types.InlineKeyboardButton(text='find', callback_data='5_7_inline')
        kb.add(kb_51)
        kb.add(kb_52)
        kb.add(kb_53)
        kb.add(kb_54)
        kb.add(kb_56, kb_57, kb_55)
        return kb


@bot.message_handler(commands=['start', 'help'])
def category(message):
    global result, genre_kb, duration_kb, rating_kb, year_kb
    genre_kb = keyboard('genre')
    duration_kb = keyboard('duration')
    rating_kb = keyboard('rating')
    year_kb = keyboard('production_year')
    bot.reply_to(message, "Привет! Я помогу тебе выбрать фильм!", reply_markup=keyboard('start'))



@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    global result, genre_kb, duration_kb, rating_kb, year_kb

    if call.data == '2_7_inline':
        genre_kb = keyboard('genre')
        duration_kb = keyboard('duration')
        rating_kb = keyboard('rating')
        year_kb = keyboard('production_year')
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='Привет! Я помогу тебе выбрать фильм!', reply_markup=keyboard('start'))
    elif call.data == '1_1_inline' or call.data == '3_5_inline':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='жанр', reply_markup=genre_kb)
    elif call.data in genres:
        genre_kb = change_keyboard(genre_kb, call.data)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='жанр', reply_markup=genre_kb)
    elif call.data == '2_6_inline' or call.data == '4_6_inline':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='длительность', reply_markup=duration_kb)
    elif call.data in durations:
        duration_kb = change_keyboard(duration_kb, call.data)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='длительность', reply_markup=duration_kb)
    elif call.data == '3_4_inline' or call.data == '5_6_inline':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='рейтинг', reply_markup=rating_kb)
    elif call.data in ratings:
        rating_kb = change_keyboard(rating_kb, call.data)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='рейтинг', reply_markup=rating_kb)
    elif call.data == '4_5_inline':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='год выпуска', reply_markup=year_kb)
    elif call.data in years:
        year_kb = change_keyboard(year_kb, call.data)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='год выпуска', reply_markup=year_kb)
    elif call.data == '2_8_inline' or call.data == '3_6_inline' or call.data == '4_7_inline' or call.data == '5_7_inline':
        print(db.find_by_filters(','.join(map(str, map(lambda x: '\'{}\''.format(x), result[0]))),
                                 'NULL', 'NULL', 'NULL', 'NULL'))

bot.polling()