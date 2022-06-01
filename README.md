# aiobotstat

Mini library for [BotStat API](api.botstat.io).

Current API version: 0.1

Install

 - Git: `pip install git+https://github.com/viuipan/aiobotstat.git`
 

 - PyPi: `pip install aiobotstat`



Example:
```
import asyncio

from aiobotstat import BotStatAPI

BOT_TOKEN = ''
FILE_PATH = ''
BOT_USERNAME = ''

api = BotStatAPI(BOT_TOKEN)


async def main():
    bot_info = await api.get_bot_info(username=BOT_USERNAME)
    print(bot_info)

    task = await api.create_task(file=FILE_PATH)
    print(task)

    status = await api.get_task_status(task_id=task.id)
    print(status)

    cancel_result = await api.cancel_task(task_id=task.id)
    print(f'Cancel result is {cancel_result}')


asyncio.run(main())
```