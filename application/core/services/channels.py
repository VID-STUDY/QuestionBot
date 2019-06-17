from application import db
from application.core.models import Channel


def create_channel(channel_name, channel_title, chat_id):
    channel = Channel(channel_name=channel_name, channel_title=channel_title, chat_id=chat_id)
    db.session.add(channel)
    db.session.commit()
    return channel


def remove_channel(channel_id):
    channel = Channel.query.get_or_404(channel_id)
    db.session.delete(channel)
    db.session.commit()
