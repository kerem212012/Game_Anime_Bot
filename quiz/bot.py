import os
import random

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quiz_bot.settings')
django.setup()

import telebot
from environs import Env
from quiz.models import *
from telebot import types

env = Env()
env.read_env()
bot = telebot.TeleBot(env.str("TG_TOKEN"))
user_state = {}
user_data = {}


def create_user(tg_id, name):
    CustomUser.objects.update_or_create(tg_id=tg_id, first_name=name, username=tg_id)


def start_code(message):
    user_id = message.chat.id
    user_state[user_id] = "code"
    user_data[user_id] = {}
    bot.send_message(user_id, text="Enter code:")


@bot.message_handler(func=lambda msg: msg.chat.id in user_state)
def handle_pay_steps(message):
    markup = types.InlineKeyboardMarkup()
    user_id = message.chat.id
    user = CustomUser.objects.get(tg_id=user_id)
    state = user_state.get(user_id)
    if state == "code":
        user_data[user_id]["code"] = message.text.strip()
        del user_state[user_id]
        if not (user.admin or user.owner):
            if user_data[message.chat.id]["code"] == "sub_2_chipsinka":
                user.admin = True
                user.save()
                panel_btn = types.InlineKeyboardButton(text="Admin Panel",callback_data="panel")
                markup.row(panel_btn)
                bot.send_message(message.chat.id, "Now you admin!", reply_markup=markup)
            else:
                bot.send_message(message.chat.id, "Invalid code!")
        else:
            bot.send_message(message.chat.id, "You almost Admin or Owner!")


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    create_user(message.chat.id, message.chat.first_name)
    bot.send_message(message.chat.id, text=f"Hello!{message.chat.first_name}")
    bot.send_message(message.chat.id, text=f"Write /score for view your score!")
    start_btn = types.InlineKeyboardButton(text="Start", callback_data="start")
    code_btn = types.InlineKeyboardButton(text="Code", callback_data="code")
    markup.row(code_btn)
    markup.row(start_btn)
    user = CustomUser.objects.get(tg_id=message.chat.id)
    if user.admin or user.owner:
        code_btn = types.InlineKeyboardButton(text="Admin Panel", callback_data="panel")
        markup.row(code_btn)
    info_btn = types.InlineKeyboardButton(text="Info", callback_data="info")
    markup.row(info_btn)
    bot.send_message(message.chat.id, "Let's start!", reply_markup=markup)


@bot.message_handler(commands=['score'])
def score(message):
    create_user(message.chat.id, message.chat.first_name)
    user = CustomUser.objects.get(tg_id=message.chat.id)
    bot.send_message(message.chat.id, text=f"Hello!{message.chat.first_name}")
    bot.send_message(message.chat.id,
                     text=f"Here is your score {message.chat.first_name} \nWrongs: {user.wrongs}\nCorrects: {user.corrects}")


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.data == "main":
        markup = types.InlineKeyboardMarkup()
        bot.send_message(call.message.chat.id, text=f"Hello!{call.message.chat.first_name}")
        bot.send_message(call.message.chat.id, text=f"Write /score for view your score!")
        start_btn = types.InlineKeyboardButton(text="Start", callback_data="start")
        code_btn = types.InlineKeyboardButton(text="Code", callback_data="code")
        markup.row(code_btn)
        markup.row(start_btn)
        user = CustomUser.objects.get(tg_id=call.message.chat.id)
        if user.admin or user.owner:
            code_btn = types.InlineKeyboardButton(text="Admin Panel", callback_data="panel")
            markup.row(code_btn)
        info_btn = types.InlineKeyboardButton(text="Info", callback_data="info")
        markup.row(info_btn)
        bot.send_message(call.message.chat.id, "Let's start!", reply_markup=markup)
    if call.data == "panel":
        markup = types.InlineKeyboardMarkup()
        wrong_btn = types.InlineKeyboardButton(text="Reset Someone's Wrongs", callback_data=f"list|reset_w")
        reset_btn = types.InlineKeyboardButton(text="Reset Someone", callback_data=f"list|reset")
        correct_btn = types.InlineKeyboardButton(text="Reset Someone's Corrects", callback_data=f"list|reset_c")
        spam_btn = types.InlineKeyboardButton(text="Spam Someone", callback_data=f"list|spam")
        if CustomUser.objects.get(tg_id=call.message.chat.id).owner:
            r_admin_btn = types.InlineKeyboardButton(text="Remove Admin", callback_data=f"list|r_admin")
            add_owner_btn = types.InlineKeyboardButton(text="Add Owner", callback_data=f"list|add_owner")
            spam_owner_btn = types.InlineKeyboardButton(text="Spam Owner", callback_data=f"list|spam_owner")
            r_owner_btn = types.InlineKeyboardButton(text="Remove Owner", callback_data=f"list|r_owner")
            markup.row(r_owner_btn)
            markup.row(spam_owner_btn)
            markup.row(add_owner_btn)
            markup.row(r_admin_btn)
        markup.row(reset_btn)
        markup.row(wrong_btn)
        markup.row(correct_btn)
        markup.row(spam_btn)
        bot.send_message(call.message.chat.id, "Choose something:", reply_markup=markup)
    if call.data.split("|", 1)[0] == "list" and (CustomUser.objects.get(tg_id=call.message.chat.id).admin or CustomUser.objects.get(tg_id=call.message.chat.id).owner):
        markup = types.InlineKeyboardMarkup()
        if call.data.split("|", 1)[1] == "r_admin":
            for user in CustomUser.objects.filter(is_staff=False,admin=True):
                btn = types.InlineKeyboardButton(text=user.first_name,
                                                 callback_data=f"{call.data.split('|', 1)[1]}|{user.tg_id}")
                markup.row(btn)
        elif call.data.split("|", 1)[1] == "spam_owner" or call.data.split("|", 1)[1] == "r_owner":
            for user in CustomUser.objects.filter(is_staff=False,owner=True):
                if user.tg_id == str(call.message.chat.id):
                    pass
                else:
                    btn = types.InlineKeyboardButton(text=user.first_name,
                                                     callback_data=f"{call.data.split('|', 1)[1]}|{user.tg_id}")
                    markup.row(btn)
        elif call.data.split("|", 1)[1] == "reset" or call.data.split("|", 1)[1] == "reset_c" or call.data.split("|", 1)[1] == "reset_w":
            for user in CustomUser.objects.filter(is_staff=False):
                if user.tg_id == str(call.message.chat.id):
                    btn = types.InlineKeyboardButton(text="You",
                                                     callback_data=f"{call.data.split('|', 1)[1]}|{user.tg_id}")
                else:
                    btn = types.InlineKeyboardButton(text=user.first_name,
                                                     callback_data=f"{call.data.split('|', 1)[1]}|{user.tg_id}")
                markup.row(btn)
        else:
            for user in CustomUser.objects.filter(is_staff=False,owner=False):
                if user.tg_id == str(call.message.chat.id):
                    pass
                else:
                    btn = types.InlineKeyboardButton(text=user.first_name,
                                                     callback_data=f"{call.data.split('|', 1)[1]}|{user.tg_id}")
                    markup.row(btn)
        bot.send_message(call.message.chat.id, "Choose someone:", reply_markup=markup)
    if call.data == "start":
        markup = types.InlineKeyboardMarkup()
        for quiz_type in QuizType.objects.all():
            btn = types.InlineKeyboardButton(text=quiz_type.title, callback_data=f"quiz|{quiz_type.id}")
            markup.row(btn)
        bot.send_message(call.message.chat.id, "Select type of quiz:", reply_markup=markup)
    if call.data.split("|", 1)[0] == "quiz":
        markup = types.InlineKeyboardMarkup()
        question = random.choice(Quiz.objects.filter(type=call.data.split("|", 1)[1]))
        answers = [question.wrong_answer_1, question.right_answer, question.wrong_answer_2, question.wrong_answer_3]
        for _ in range(4):
            answer = random.choice(answers)
            if answer == question.right_answer:
                btn = types.InlineKeyboardButton(text=answer, callback_data=f"right|{question.id}")
            else:
                btn = types.InlineKeyboardButton(text=answer, callback_data=f"wrong|{question.id}")
            markup.row(btn)
            answers.remove(answer)
        bot.send_message(call.message.chat.id, text=question.question, reply_markup=markup)
    if call.data.split("|", 1)[0] == "right":
        markup = types.InlineKeyboardMarkup()
        question = Quiz.objects.get(id=call.data.split("|", 1)[1])
        user = CustomUser.objects.get(tg_id=call.message.chat.id)
        user.corrects += 1
        user.save()
        continue_btn = types.InlineKeyboardButton(text="Continue", callback_data=f"quiz|{question.type.id}")
        quit_btn = types.InlineKeyboardButton(text="Quit", callback_data="main")
        markup.row(continue_btn)
        markup.row(quit_btn)
        bot.send_message(call.message.chat.id,
                         text=f"Congratulations!You clicked the correct answer:{question.right_answer}",
                         reply_markup=markup)
    if call.data.split("|", 1)[0] == "wrong":
        markup = types.InlineKeyboardMarkup()
        question = Quiz.objects.get(id=call.data.split("|", 1)[1])
        user = CustomUser.objects.get(tg_id=call.message.chat.id)
        user.wrongs += 1
        user.save()
        continue_btn = types.InlineKeyboardButton(text="Continue", callback_data=f"quiz|{question.type.id}")
        quit_btn = types.InlineKeyboardButton(text="Quit", callback_data="main")
        markup.row(continue_btn)
        markup.row(quit_btn)
        bot.send_message(call.message.chat.id,
                         text=f"Oh no!You clicked the wrong answer.Correct answer is {question.right_answer}",
                         reply_markup=markup)
    if call.data == "code":
        start_code(call.message)
    if call.data.split("|", 1)[0] == "reset":
        user = CustomUser.objects.get(tg_id=call.data.split("|", 1)[1])
        user.corrects = 0
        user.wrongs = 0
        user.save()
        bot.send_message(call.message.chat.id, text=f"{user.first_name}'s Corrects and Wrongs reseted")
    if call.data.split("|", 1)[0] == "reset_w":
        user = CustomUser.objects.get(tg_id=call.message.chat.id)
        user.wrongs = 0
        user.save()
        bot.send_message(call.message.chat.id, text=f"{user.first_name}'s Wrongs reseted")
    if call.data.split("|", 1)[0] == "reset_l":
        user = CustomUser.objects.get(tg_id=call.message.chat.id)
        user.corrects = 0
        user.save()
        bot.send_message(call.message.chat.id, text=f"{user.first_name}'s Corrects reseted")
    if call.data.split("|", 1)[0] == "spam":
        for _ in range(10):
            bot.send_message(call.data.split("|", 1)[1], text="You was pranked by admin or owner!")
        bot.send_message(call.message.chat.id, text="Spam completed!")
    if call.data.split("|", 1)[0] == "spam_owner":
        for _ in range(10):
            bot.send_message(call.data.split("|", 1)[1], text="You was pranked by owner!")
        bot.send_message(call.message.chat.id, text="Spam completed!")

    if call.data.split("|", 1)[0] == "r_admin":
        user = CustomUser.objects.get(tg_id=call.data.split("|", 1)[1])
        user.admin = False
        user.save()
        bot.send_message(call.message.chat.id, text=f"{user.first_name} Admin was removed!")
        bot.send_message(call.data.split("|", 1)[1], text="You removed from Admin!")
    if call.data.split("|", 1)[0] == "add_owner":
        user = CustomUser.objects.get(tg_id=call.data.split("|", 1)[1])
        user.admin = False
        user.owner = True
        user.save()
        bot.send_message(call.message.chat.id, text=f"{user.first_name} Owner was added!")
        bot.send_message(call.data.split("|", 1)[1], text="You added to Owner!")
    if call.data.split("|", 1)[0] == "r_owner":
        user = CustomUser.objects.get(tg_id=call.data.split("|", 1)[1])
        user.owner = False
        user.save()
        bot.send_message(call.message.chat.id, text=f"{user.first_name} Owner was removed!")
        bot.send_message(call.data.split("|", 1)[1], text="You removed from Owner!")
    if call.data == "info":
        bot.send_message(call.message.chat.id, text="Quiz Bot\n"
                                                    "Quizes are about Anime but later in Beta i will add more and more question(we have 25 now)\n"
                                                    "We have admin panel you need code from owner and after write /start!")
bot.infinity_polling()
