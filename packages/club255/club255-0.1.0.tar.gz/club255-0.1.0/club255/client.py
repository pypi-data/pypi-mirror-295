from typing import Any, Union, Optional
from collections.abc import Callable

from yarl import URL
from httpx import Response, AsyncClient
from pydantic import HttpUrl, TypeAdapter

from .const import FID, MID, PID, UID, T
from .model import (
    User,
    Level,
    NavInfo,
    RawUser,
    BaseLike,
    BasePost,
    ChatList,
    LikeInfo,
    LiveInfo,
    PostInfo,
    SignInfo,
    UserData,
    BaseReply,
    LoginInfo,
    UploadKey,
    VideoInfo,
    BaseNotice,
    PostResult,
    NoticeCount,
    PostDetails,
    ReplyResult,
    VersionInfo,
    FollowResult,
    UploadResult,
    UserPostInfo,
    SystemNoticeMessage,
    RawUserWithContribution,
)
from .exception import ActionFailed


class Client:
    def __init__(
        self,
        url: Union[str, URL],
        account: str,
        password: str,
        token: Optional[str] = None,
        headers: Optional[dict[str, str]] = None,
        httpx_config: dict[str, Any] = None,
    ):
        if headers is None:
            headers = {}
        if isinstance(url, str):
            url = URL(url)
        if httpx_config is None:
            httpx_config = {}
        self.url = url
        self.httpx_config = httpx_config
        self.headers = headers
        self.account = account
        self.password = password
        self.token = token
        if self.token:
            self.set_token(token)

    def get_token(self) -> str:
        return self.token

    def set_token(self, token: str):
        self.token = token
        self.headers["cookie"] = f"token={token};"

    async def check_token(self) -> bool:
        try:
            await self.get_self_info()
            return True
        except ActionFailed:
            return False

    async def _call_api(self, api: str, method: str = "GET", **data: Any) -> Any:
        async with AsyncClient(headers=self.headers, **self.httpx_config) as client:
            return await client.request(
                method,
                str(self.url / api),
                json=data,
            )

    async def call_api(self, api: str, method: str = "GET", **data: Any) -> Any:
        if data.get("raw") and data.get("raw") is True:
            data.pop("raw")
            return await self._call_api(api, method, **data)
        resp: Response = await self._call_api(api, method, **data)
        return resp.json()

    async def call_api_get(self, api: str, **data: Any) -> Any:
        return await self.call_api(api, method=data.pop("method") if data.get("method") else "GET", **data)

    async def call_api_post(self, api: str, **data: Any) -> Any:
        return await self.call_api(api, method=data.pop("method") if data.get("method") else "POST", **data)

    async def post(
        self,
        api: str,
        type_: type[T],
        strict=True,
        data_from: Union[str, Callable, None] = None,
        **data: Any,
    ) -> T:
        res = await self.call_api_post(api, **data)
        if strict and res.get("code", 0) != 0:
            raise ActionFailed(f"API调用失败: {res.get('msg', '未知错误')}")
        return TypeAdapter(type_).validate_python(
            (res[data_from] if isinstance(data_from, str) else data_from(res)) if data_from else res
        )

    async def get(
        self,
        api: str,
        type_: type[T],
        strict: bool = True,
        data_from: Union[str, Callable, None] = None,
        **data: Any,
    ) -> T:
        res = await self.call_api_get(api, **data)
        if strict and res.get("code", 0) != 0:
            raise ActionFailed(f"API调用失败: {res.get('msg', '未知错误')}")
        return TypeAdapter(type_).validate_python(
            (res[data_from] if isinstance(data_from, str) else data_from(res)) if data_from else res,
        )

    async def login(self, account: str = "", password: str = "") -> LoginInfo:
        data = await self.call_api(
            "auth/login",
            "POST",
            **{
                "account": account or self.account,
                "password": password or self.password,
            },
        )

        info = LoginInfo.model_validate(data)

        if info.code == 0:
            self.set_token(info.token)

        return info

    async def get_live_info(self) -> LiveInfo:
        """
        获取hanser直播间信息
        :return:
        """
        return await self.get("forward/getRoomInfo", LiveInfo, data_from="data")

    async def get_version(self) -> VersionInfo:
        return await self.get("get_version", VersionInfo)

    async def get_level_list(self) -> list[Level]:
        return await self.get("level/list", list[Level])

    async def get_manager(self) -> list[RawUser]:
        return await self.get("user/manager", list[RawUser])

    async def get_nav_list(self) -> list[NavInfo]:
        """
        获取公告列表
        """
        return await self.get("post/nav-list", list[NavInfo])

    async def get_week_rank(self, page: int = 1, pageSize: int = 10) -> list[RawUserWithContribution]:
        return await self.get(
            f"contribution/rank?page={page}&pageSize={pageSize}&sort=week",
            list[RawUserWithContribution],
        )

    async def get_month_rank(self, page: int = 1, pageSize: int = 10) -> list[RawUserWithContribution]:
        return await self.get(
            f"contribution/rank?page={page}&pageSize={pageSize}&sort=month",
            list[RawUserWithContribution],
        )

    async def get_video_info(self, bv: str) -> VideoInfo:
        return await self.get(f"forward/get-video-info?bv={bv}", VideoInfo)

    async def get_post_list_brief(
        self, *, page: int = 1, _order: int = 1, _filter: int = 0, page_size=20
    ) -> list[BasePost]:
        """
        获取帖子列表，无详细内容
        :param page: 页数
        :param page_size: 帖子数量
        :param _order: 0->最后回复 1->最新发贴
        :param _filter: 帖子分类类型: 0->新帖 1->精华帖
        :return: List[PostInfo]
        """
        return await self.get(
            f"post/list?page={page}&pageSize={page_size}" f"&order={_order}&filter={_filter}",
            list[BasePost],
            data_from="result",
        )

    async def get_post_list_brief_by_time(self, *, page: int = 1, page_size=20) -> list[BasePost]:
        return await self.get_post_list_brief(page=page, _order=1, _filter=0, page_size=page_size)

    async def get_post_list_brief_by_reply(self, *, page: int = 1, page_size=20) -> list[BasePost]:
        return await self.get_post_list_brief(page=page, _order=0, _filter=0, page_size=page_size)

    async def get_nice_post_list_brief_by_time(self, *, page: int = 1, page_size=20) -> list[BasePost]:
        return await self.get_post_list_brief(page=page, _order=1, _filter=1, page_size=page_size)

    async def get_nice_post_list_brief_by_replay(self, *, page: int = 1, page_size=20) -> list[BasePost]:
        return await self.get_post_list_brief(page=page, _order=0, _filter=1, page_size=page_size)

    """
    下面是登录后可用的api
    """

    async def get_post_list(self, *, page: int = 1, _order: int = 1, _filter: int = 0, page_size=20) -> list[PostInfo]:
        """
        获取帖子列表
        :param page: 页数
        :param page_size: 帖子数量
        :param _order: 0->最后回复 1->最新发贴
        :param _filter: 帖子分类类型: 0->新帖 1->精华帖
        :return: List[PostInfo]
        """
        return await self.get(
            f"post/list?page={page}&pageSize={page_size}" f"&order={_order}&filter={_filter}",
            list[PostInfo],
            data_from="result",
        )

    async def get_post_list_by_time(self, *, page: int = 1, page_size=20) -> list[PostInfo]:
        return await self.get_post_list(page=page, _order=1, _filter=0, page_size=page_size)

    async def get_post_list_by_reply(self, *, page: int = 1, page_size=20) -> list[PostInfo]:
        return await self.get_post_list(page=page, _order=0, _filter=0, page_size=page_size)

    async def get_nice_post_list_by_time(self, *, page: int = 1, page_size=20) -> list[PostInfo]:
        return await self.get_post_list(page=page, _order=1, _filter=1, page_size=page_size)

    async def get_nice_post_list_by_replay(self, *, page: int = 1, page_size=20) -> list[PostInfo]:
        return await self.get_post_list(page=page, _order=0, _filter=1, page_size=page_size)

    async def get_upload_key(self) -> UploadKey:
        return await self.get("auth/upload", UploadKey)

    async def upload_image(self, *, url: HttpUrl, self_uid: UID, img_msg: Any) -> UploadResult:
        pass

    async def dispose_msg(self, url: HttpUrl, self_uid: UID, message: str) -> str:
        return message

    async def send_post(
        self,
        url: HttpUrl,
        self_uid: UID,
        title: str,
        message: str,
    ) -> PostResult:
        message = await self.dispose_msg(url, self_uid, message)
        return await self.post("post/hansering", PostResult, title=title, content=message)

    async def send_floor_reply(
        self,
        *,
        message: str,
        pid: PID,
        fid: FID,
        upload_url: HttpUrl,
        self_uid: UID,
    ) -> ReplyResult:
        message = await self.dispose_msg(self_uid=self_uid, message=message, url=upload_url)
        return await self.post(
            f"reply/floor/{fid}",
            ReplyResult,
            **{"content": message, "postId": int(pid)},
        )

    async def send_post_reply(
        self,
        *,
        upload_url: HttpUrl,
        self_uid: UID,
        message: str,
        pid: PID,
        author: UID,
    ) -> ReplyResult:
        message = await self.dispose_msg(self_uid=self_uid, message=message, url=upload_url)
        return await self.post(
            f"reply/{pid}",
            ReplyResult,
            **{"author": int(author), "content": message, "postId": int(pid)},
        )

    async def like_post(self, pid: PID, uid: UID) -> LikeInfo:
        """
        点赞/取消点赞帖子
        :param pid: 帖子id
        :param uid: 作者id
        :return:
        """
        return await self.post(f"post/like/{pid}", LikeInfo, author=int(uid))

    async def get_user_data(self, uid: UID) -> UserData:
        """
        获取指定用户的积分，粉丝，收藏等信息
        :param uid: self_uid
        :return: UserData
        """
        return await self.get(f"user/data/count?self_uid={uid}", UserData, data_from="data")

    async def get_self_data(self, self_uid: UID) -> UserData:
        """
        获取自己的积分，粉丝，收藏等信息
        :return: UserData
        """
        return await self.get_user_data(self_uid)

    async def sign_now(self) -> SignInfo:
        return await self.get("sign", SignInfo)

    async def get_chat_list(self) -> list[ChatList]:
        return await self.get("chat/list", list[ChatList], data_from="list")

    async def get_chat_newest(self, uid: UID, mid: MID) -> dict:
        return await self.call_api(f"chat/chat-newest?self_uid={uid}&id={mid}", method="GET")

    async def get_self_info(self) -> User:
        return await self.get("user/info", User, data_from="info")

    async def get_user_info(self, uid: UID) -> User:
        return await self.get(f"user/user-info?self_uid={uid}", User, data_from="info")

    async def get_newest_post_id(self) -> int:
        data = await self.get_post_list_by_time()
        # data.sort(key=lambda x:-x.id)
        return data[0].id

    async def get_newest_nice_post_id(self) -> int:
        data = await self.get_nice_post_list_by_time()
        # data.sort(key=lambda x:-x.id)
        return data[0].id

    async def get_vision_info(self) -> VersionInfo:
        return await self.get("version", VersionInfo)

    async def check_if_sign(self) -> bool:
        data = await self.call_api("sign/signed", method="GET")
        return data["signed"]

    async def get_sign_days(self) -> int:
        data = await self.call_api("sign/days", method="GET")
        return data["day"]

    async def get_reply_list(self, *, page: int = 1, pageSize: int = 20) -> list[BaseReply]:
        return await self.get(
            f"notice/reply/list?page={page}&pageSize={pageSize}",
            list[BaseReply],
            data_from="list",
        )

    async def get_like_list(self, *, page: int = 1, pageSize: int = 20) -> list[BaseLike]:
        """
        点赞列表
        :param page:
        :param pageSize: 由于点赞数量大，较小的club255_page_size可能会导致错失部分点赞信息
        :return:
        """
        return await self.get(
            f"notice/like/list?page={page}&pageSize={pageSize}",
            list[BaseLike],
            data_from="list",
        )

    async def get_self_level(self) -> Level:
        return await self.get("level/info", Level, data_from="levelInfo")

    async def get_next_level(self) -> Level:
        return await self.get("level/info", Level, data_from="nextLevel")

    async def get_notice_count(self) -> NoticeCount:
        return await self.get("notice/count", NoticeCount, data_from="count")

    async def get_system_notice_message(self, page: int = 1, pageSize=20) -> list[SystemNoticeMessage]:
        return await self.get(
            f"notice/system?page={page}&pageSize={pageSize}",
            list[SystemNoticeMessage],
            data_from="list",
        )

    async def get_site_notice(self, page: int = 0, pageSize=20) -> list[BaseNotice]:
        return await self.get(
            f"notice/site?page={page}&pageSize={pageSize}",
            list[BaseNotice],
            data_from="list",
        )

    async def get_post_details(self, pid: PID) -> PostDetails:
        return await self.get(f"post/detail/{pid}", PostDetails, data_from="info")

    async def follow_user(self, uid: UID) -> FollowResult:
        """
        关注/取关
        :param uid:
        :return: FollowResult relation：0:取关 1:关注
        """
        return await self.post(f"user/follow/{uid}", FollowResult, uid=int(uid))

    async def edit_post(
        self,
        url: HttpUrl,
        self_uid: UID,
        pid: PID,
        title: str,
        message: str,
    ) -> Response:
        """
        修改帖子
        没有返回值
        """
        message = await self.dispose_msg(url, self_uid, message)
        return await self.call_api(
            f"post/edit/{pid}",
            method="POST",
            raw=True,
            title=title,
            content=message,
        )

    async def get_post_by_user(self, uid: UID, *, page: int = 1, page_size=20) -> list[UserPostInfo]:
        """
        获取帖子列表
        :param page_size: 帖子数量
        :param page: 页数
        :param uid: 用户id
        :return: List[PostInfo]
        """
        return await self.get(
            f"post/user/list?page={page}&pageSize={page_size}&self_uid={uid}",
            list[UserPostInfo],
            data_from="list",
        )

    async def set_floor_top(self, pid: PID, fid: FID) -> None:
        """
        这个api不会返回信息
        """
        return await self.call_api("reply/set-top", method="POST", raw=True, postId=pid, replyId=fid)


__all__ = ["Client"]
