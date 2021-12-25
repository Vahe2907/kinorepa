import telebot


def change_keyboard(kb, call_back):
    new_kb = {}
    for i in range(len(kb.to_dict()["inline_keyboard"])):
        for item in kb.to_dict()["inline_keyboard"][i]:
            new_kb[item["callback_data"]] = item["text"]
    if new_kb[call_back][-1] == "+":
        new_kb[call_back] = new_kb[call_back][:-1]
        result[int(call_back[0]) - 2].remove(new_kb[call_back])
    else:
        result[int(call_back[0]) - 2].add(new_kb[call_back])
        new_kb[call_back] += "+"

    final_kb = telebot.types.InlineKeyboardMarkup()

    for val in new_kb.keys():
        if new_kb[val] != "next" and new_kb[val] != "find" and new_kb[val] != "back":
            final_kb.add(
                telebot.types.InlineKeyboardButton(text=new_kb[val], callback_data=val)
            )
    kb_1 = telebot.types.InlineKeyboardButton(
        text="next",
        callback_data=list(new_kb.keys())[list(new_kb.values()).index("next")],
    )
    kb_2 = telebot.types.InlineKeyboardButton(
        text="back",
        callback_data=list(new_kb.keys())[list(new_kb.values()).index("back")],
    )
    kb_3 = telebot.types.InlineKeyboardButton(
        text="find",
        callback_data=list(new_kb.keys())[list(new_kb.values()).index("find")],
    )
    final_kb.add(kb_2, kb_3, kb_1)
    return final_kb


def keyboard(where_call):
    kb = telebot.types.InlineKeyboardMarkup()

    if where_call == "start":
        kb_11 = telebot.types.InlineKeyboardButton(
            text="my_filters", callback_data="1_1_inline"
        )
        kb_12 = telebot.types.InlineKeyboardButton(
            text="rand", callback_data="1_2_inline"
        )
        kb.add(kb_11, kb_12)
        return kb

    elif where_call == "genre":
        kb_21 = telebot.types.InlineKeyboardButton(
            text="genre1", callback_data="2_1_inline"
        )
        kb_22 = telebot.types.InlineKeyboardButton(
            text="genre2", callback_data="2_2_inline"
        )
        kb_23 = telebot.types.InlineKeyboardButton(
            text="genre3", callback_data="2_3_inline"
        )
        kb_24 = telebot.types.InlineKeyboardButton(
            text="genre4", callback_data="2_4_inline"
        )
        kb_25 = telebot.types.InlineKeyboardButton(
            text="genre5", callback_data="2_5_inline"
        )
        kb.add(kb_21)
        kb.add(kb_22)
        kb.add(kb_23)
        kb.add(kb_24)
        kb.add(kb_25)
        kb_26 = telebot.types.InlineKeyboardButton(
            text="next", callback_data="2_6_inline"
        )
        kb_27 = telebot.types.InlineKeyboardButton(
            text="back", callback_data="2_7_inline"
        )
        kb_28 = telebot.types.InlineKeyboardButton(
            text="find", callback_data="2_8_inline"
        )
        kb.add(kb_27, kb_28, kb_26)
        return kb

    elif where_call == "duration":
        # duration1 - time < 90 min
        # duration2 - 90 min <= time <120 min
        # duration - time >= 120 min
        kb_31 = telebot.types.InlineKeyboardButton(
            text="duration1", callback_data="3_1_inline"
        )
        kb_32 = telebot.types.InlineKeyboardButton(
            text="duration2", callback_data="3_2_inline"
        )
        kb_33 = telebot.types.InlineKeyboardButton(
            text="duration3", callback_data="3_3_inline"
        )
        kb_34 = telebot.types.InlineKeyboardButton(
            text="next", callback_data="3_4_inline"
        )
        kb_35 = telebot.types.InlineKeyboardButton(
            text="back", callback_data="3_5_inline"
        )
        kb_36 = telebot.types.InlineKeyboardButton(
            text="find", callback_data="3_6_inline"
        )
        kb.add(kb_31)
        kb.add(kb_32)
        kb.add(kb_33)
        kb.add(kb_35, kb_36, kb_34)
        return kb

    elif where_call == "rating":
        kb_41 = telebot.types.InlineKeyboardButton(
            text="rating_1", callback_data="4_1_inline"
        )
        kb_42 = telebot.types.InlineKeyboardButton(
            text="rating_2", callback_data="4_2_inline"
        )
        kb_43 = telebot.types.InlineKeyboardButton(
            text="rating_3", callback_data="4_3_inline"
        )
        kb_44 = telebot.types.InlineKeyboardButton(
            text="rating_4", callback_data="4_4_inline"
        )
        kb_45 = telebot.types.InlineKeyboardButton(
            text="next", callback_data="4_5_inline"
        )
        kb_46 = telebot.types.InlineKeyboardButton(
            text="back", callback_data="4_6_inline"
        )
        kb_47 = telebot.types.InlineKeyboardButton(
            text="find", callback_data="4_7_inline"
        )
        kb.add(kb_41)
        kb.add(kb_42)
        kb.add(kb_43)
        kb.add(kb_44)
        kb.add(kb_46, kb_47, kb_45)
        return kb

    elif where_call == "production_year":
        kb_51 = telebot.types.InlineKeyboardButton(
            text="year_1", callback_data="5_1_inline"
        )
        kb_52 = telebot.types.InlineKeyboardButton(
            text="year_2", callback_data="5_2_inline"
        )
        kb_53 = telebot.types.InlineKeyboardButton(
            text="year_3", callback_data="5_3_inline"
        )
        kb_54 = telebot.types.InlineKeyboardButton(
            text="year_4", callback_data="5_4_inline"
        )
        kb_55 = telebot.types.InlineKeyboardButton(
            text="next", callback_data="5_5_inline"
        )
        kb_56 = telebot.types.InlineKeyboardButton(
            text="back", callback_data="5_6_inline"
        )
        kb_57 = telebot.types.InlineKeyboardButton(
            text="find", callback_data="5_7_inline"
        )
        kb.add(kb_51)
        kb.add(kb_52)
        kb.add(kb_53)
        kb.add(kb_54)
        kb.add(kb_56, kb_57, kb_55)
        return kb
