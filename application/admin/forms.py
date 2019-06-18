from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError
from application.core.services import channels
from application import telegram_bot
from telebot.apihelper import ApiException
import re


class NewChannelForm(FlaskForm):
    channel_name_url = StringField(validators=[DataRequired('Укажите ссылку на канал или его юзернейм')])
    submit = SubmitField('Сохранить')

    def validate_channel_name_url(self, field):
        if field.data.strip() != '':
            url_re = r'https?:\/\/(t(elegram)?\.me|telegram\.org)\/([a-z0-9\_])'
            if not (re.match(url_re, field.data) or field.data.startswith('@')):
                raise ValidationError('Указан неверный формат ссылки или юзернейма канала')
            if re.match(url_re, field.data):
                channel_name = '@' + field.data[field.data.rfind('/') + 1:]
            else:
                channel_name = field.data
            if channels.channel_exists(channel_name):
                raise ValidationError('Такой канал уже добавлен')
            try:
                channel_chat = telegram_bot.get_chat(channel_name)
            except ApiException:
                raise ValidationError('Указанный канал отсутствует, либо является привытаным')
            if channel_chat.type != 'channel':
                raise ValidationError('Указанный юзернейм не является каналом')
            try:
                sent_message = telegram_bot.send_message(channel_name, 'Test', disable_notification=True)
                telegram_bot.delete_message(sent_message.chat.id, sent_message.message_id)
            except ApiException:
                raise ValidationError('Бот не имеет доступа к отправке и удалению сообщений')
            self.chat_id = sent_message.chat.id
            self.channel = channel_chat

    def get_channel_chat_id(self):
        return self.chat_id

    def get_channel(self):
        return self.channel


class NewQuizForm(FlaskForm):
    start_date = StringField('Дата начала', validators=[DataRequired('Укажите дату начала викторины')])
    end_date = StringField('Дата конца', validators=[DataRequired('Укажите дату окончания')])
    top_count = StringField('Количество топ игроков', validators=[DataRequired("Укажите количество лучших игроков")])
    submit = SubmitField('Сохранить')

    def validate_top_count(self, field):
        if field.data != '':
            if not field.data.isdigit():
                raise ValidationError('Укажите число')
            if int(field.data) < 0:
                raise ValidationError('Укажите положительное число либо ноль')
