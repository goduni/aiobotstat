import io
from pathlib import Path
from typing import Optional, Union

from aiobotstat.base import BaseClient
from aiobotstat.const import HTTPMethods
from aiobotstat.models import BotInfo, TaskID, TaskStatus


class BotStatAPI(BaseClient):
    BASE_URL = 'https://api.botstat.io'

    def __init__(self, token: Optional[str] = None, access_key: Optional[str] = None):
        """
        :param token: Telegram Bot API token (https://core.telegram.org/bots#6-botfather)
        """

        super().__init__()
        self.__token = token
        self.__access_key = access_key

    async def get_bot_info(self, username: str) -> BotInfo:
        """
        Return bot info.

        :param username: Bot id or username (case-insensitive)
        :return: bot profile object or not found exception
        """
        method = HTTPMethods.GET
        url = f"{self.BASE_URL}/get/{username}"

        data = await self._make_request(method, url)
        return BotInfo(**data.result)

    async def create_task(
            self,
            file: Union[str, Path, io.IOBase],
            token: Optional[str] = None,
            notify_id: Optional[int] = None
    ) -> TaskID:
        """
        Init new bot checking.

        :param file: Any format of user_id array (csv, one-per-line or other).
        :param token: Telegram Bot API token
        :param notify_id: User chat_id to receive notification from @BotSafeRobot
        :return: new object with task id
        """
        token = token or self.__token
        if token is None:
            raise RuntimeError(
                "Please provide `token` for `BotStatAPI` instance "
                "or pass it as a `create_task` request param."
            )
        method = HTTPMethods.POST
        url = f"{self.BASE_URL}/create/{token}"
        form = self._prepare_form(file)

        params = {}
        if notify_id:
            params['notify_id'] = notify_id

        data = await self._make_request(method, url, data=form, params=params)
        return TaskID(**data.result)

    async def cancel_task(self, task_id: str) -> bool:
        """
        Cancel task
        :param task_id: id of task
        :return: bool
        """

        method = HTTPMethods.DELETE
        url = f"{self.BASE_URL}/cancel/{task_id}"

        data = await self._make_request(method, url)
        return data.ok

    async def get_task_status(self, task_id: str) -> TaskStatus:
        """
        Get task status
        :param task_id: id of task
        :return: task status object
        """

        method = HTTPMethods.GET
        url = f"{self.BASE_URL}/status/{task_id}"

        data = await self._make_request(method, url)
        return TaskStatus(**data.result)

    async def send_stat(self, username: str, access_key: Optional[str] = None,
                        owner: Optional[int] = None,
                        users_live: Optional[int] = None,
                        users_die: Optional[int] = None,
                        groups_live: Optional[int] = None,
                        groups_die: Optional[int] = None,
                        users_in_groups: Optional[int] = None) -> bool:
        """
        Get task status

        :param username: Username bot
        :param access_key: the key from @BotStatSupport
        :param owner: Chat_id owner to bind a bot to an id
        :param users_live: Count live users
        :param users_die: Count die users
        :param groups_live: Count live groups
        :param groups_die: Count die groups
        :param users_in_groups: Count users in groups
        :return: ok
        """

        access_key = access_key or self.__access_key
        if access_key is None:
            raise RuntimeError(
                "Please provide `access_key` for `BotStatAPI` instance "
                "or pass it as a `send_stat` request param."
            )

        method = HTTPMethods.GET
        url = f"{self.BASE_URL}/send-stat/{access_key}"

        params = {'username': username}
        if owner is not None:
            params['owner'] = owner
        if users_live:
            params['users_live'] = users_live
        if users_die:
            params['users_die'] = users_die
        if groups_live:
            params['groups_live'] = groups_live
        if groups_die:
            params['groups_die'] = groups_die
        if users_in_groups:
            params['users_in_groups'] = users_in_groups

        data = await self._make_request(method, url, params=params)
        return data.ok
