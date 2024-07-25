import asyncio
from flask import Flask, request, jsonify
from aiogram import Bot
from config import BOT_TOKEN
from database.base import DataBase


bot = Bot(token=BOT_TOKEN)
app = Flask(__name__)
event_loop = None


async def send_message(tgid, message):
    await bot.send_message(tgid, message)


def run_async(coroutine):
    global event_loop
    if event_loop is None:
        event_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(event_loop)
    event_loop.run_until_complete(coroutine)


@app.route('/telegram/send', methods=['GET'])
def send_notification():
    userid = request.args.get('userid')
    message = request.args.get('message')
    if not userid or not message:
        return jsonify({'error': 'Missing userid or message'}), 400
    tgid = DataBase.get_user_tgid(userid)
    if tgid is None:
        return jsonify({'error': 'User not found or Telegram ID not linked'}), 404
    run_async(send_message(int(tgid), message))
    return jsonify({'status': 'Message sent'}), 200


@app.route('/telegram/add', methods=['GET'])
def add_user():
    userid = request.args.get('userid')
    if not userid:
        return jsonify({'error': 'Missing userid'}), 400
    if DataBase.add_userid(userid):
        return jsonify({'status': 'User was added'}), 200
    else:
        return jsonify({'error': 'User already exists'}), 400


@app.route('/telegram/check', methods=['GET'])
def check_user():
    userid = request.args.get('userid')
    if not userid:
        return jsonify({'error': 'Missing userid'}), 400
    user = DataBase.check_user(userid)
    if user is None:
        return jsonify({'status': 'User does not exist'}), 200
    else:
        return jsonify({'status': 'User exists', 'userid': user.userid,
                        'tgid': user.tgid, 'name': user.name}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
