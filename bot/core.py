"""
Main core for inline queries handlers
"""
from application import telegram_bot
from telebot.types import CallbackQuery, User
from telebot.apihelper import ApiException
from application.core.models import Test, Option, Channel, BotUser, Answer
from application.resources import strings
import settings


@telegram_bot.callback_query_handler(func=lambda query: True)
def answer_handler(query: CallbackQuery):
    data = query.data
    data = data.split('@')
    test_id = data[0]
    option_id = data[1]
    user = query.from_user
    channel_id = query.message.chat.id
    answers_processor(test_id, option_id, user, channel_id, query)


def answers_processor(test_id, option_id, user: User, channel_chat_id, query: CallbackQuery):
    """
    Processor which process user answers
    :param test_id: The test id which the user given an answer
    :param option_id: The answer id
    :param user: The user
    :param channel_chat_id: Telegram chat id of channel
    :param query: Telegram Callback query
    :return: void
    """
    channel = Channel.get_by_chat_id(channel_chat_id)
    if not channel:
        # if channel is not registered just stop processing
        return
    # if user given answer in first time, add him to channel members
    current_user = BotUser.add_user(user.id, user.first_name, user.last_name, user.username)
    channel.add_member(current_user)
    test = Test.get_by_id(test_id)
    if test.user_given_right_answer(user_id=current_user.id):
        # if user already given the right answer send message to him and stop processing
        message = strings.get_string('answer.already_given')
        telegram_bot.answer_callback_query(query.id, message, show_alert=True)
        return
    right_answer = test.get_right_answer()
    target_message_id = query.message.message_id
    # if user given right answer
    if option_id == right_answer.id:
        answers_count = test.get_count_user_answers(user.id)
        # If user given right answer on first try in top 10 players
        # TODO: check caption messages by test file path
        if query.message.caption:
            current_message_text = query.message.caption
        else:
            current_message_text = query.message.text
        if test.get_top_10_answers_count() < 10 and answers_count == 0:
            new_message_text = add_user_to_top_10(current_user, current_message_text)
            answer_points = settings.get_top_10_points()
            message = strings.get_string('answer.right_answer_on_top_10').format(answer_points)
        else:
            if answers_count == 0:
                # If user not in top 10, but answered on first try
                answer_points = settings.get_first_try_points()
                message = strings.get_string('answer.right_answer_on_the_first_try').format(answer_points)
                new_message_text = add_user_to_first_try_answer(current_user, current_message_text)
            else:
                # if user answered not on first try
                answer_points = settings.get_not_first_try_points()
                message = strings.get_string('answer.right_answer_on_the_not_first_try').format(answers_count + 1,
                                                                                                answer_points)
                new_message_text = None
    else:
        answer_points = None
        new_message_text = None
        message = strings.get_string('answer.wrong_answer')
    answer = Answer(user_id=user.id, points=answer_points)
    test.add_answer(answer)
    # TODO: check caption messages by test file path
    if query.message.caption and new_message_text:
        telegram_bot.edit_message_caption(new_message_text,
                                          channel_chat_id, target_message_id, parse_mode='HTML')
    elif query.message.text and new_message_text:
        telegram_bot.edit_message_text(new_message_text, channel_chat_id,
                                       target_message_id, parse_mode='HTML')
    try:
        telegram_bot.answer_callback_query(query.id, message, show_alert=True)
    except ApiException:
        pass


def add_user_to_top_10(user: BotUser, message_text: str) -> str:
    # TODO: add username to list of top 10 players
    pass


def add_user_to_first_try_answer(user: BotUser, message_text: str) -> str:
    # TODO: add username to list of first try answers
    pass
