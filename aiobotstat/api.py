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
        if self.__access_key is None:
            raise RuntimeError(
                "Please provide `access_key` for `BotStatAPI` instance "
                "You can get the access key at https://botstat.io/dashboard/api"
            )
        method = HTTPMethods.GET
        url = f"{self.BASE_URL}/get/{username}/{self.__access_key}"

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
        if self.__access_key is None:
            raise RuntimeError(
                "Please provide `access_key` for `BotStatAPI` instance "
                "You can get the access key at https://botstat.io/dashboard/api"
            )
        method = HTTPMethods.POST
        url = f"{self.BASE_URL}/create/{token}/{self.__access_key}"
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

    async def check_sub(self, code: str, user_id: int) -> bool:
        """
        Check subscription via @BotMembersRobot

        :param code: Code from @BotMembersRobot
        :param user_id: User ID for verification
        :return: ok
        """

        method = HTTPMethods.GET
        url = f"{self.BASE_URL}/checksub/{code}/{user_id}"

        data = await self._make_request(method, url)
        return data.ok

    async def send_to_botman(
            self,
            owner_id: Optional[int],
            file: Union[str, Path, io.IOBase],
            token: Optional[str] = None,
            show_file_result: Optional[bool] = None
    ) -> bool:
        """
        Send database chat_ids to @BotManRobot

        :param owner_id: User chat_id owner to @BotManRobot
        :param file: File database users/groups. Allowed: txt, csv, xls, xlsx, json
        :param token: Telegram Bot API token
        :param show_file_result: Allow download file result after letter
        :return: bool
        """
        token = token or self.__token
        if token is None:
            raise RuntimeError(
                "Please provide `token` for `BotStatAPI` instance "
                "or pass it as a `send_to_botman` request param."
            )
        method = HTTPMethods.POST
        url = f"{self.BASE_URL}/botman/{token}"
        form = self._prepare_form(file)

        params = {
            "owner_id": owner_id
        }

        if show_file_result:
            params['show_file_result'] = show_file_result

        data = await self._make_request(method, url, data=form, params=params)
        return data.ok

    async def botman_pause(self, token: str) -> bool:
        """
        Set pause\continue job from @BotManRobot

        :param token: Telegram Bot API token
        :return: ok
        """

        token = token or self.__token
        if token is None:
            raise RuntimeError(
                "Please provide `token` for `BotStatAPI` instance "
                "or pass it as a `send_to_botman` request param."
            )

        method = HTTPMethods.GET
        url = f"{self.BASE_URL}/botman-pause/{token}"

        data = await self._make_request(method, url)
        return data.ok
