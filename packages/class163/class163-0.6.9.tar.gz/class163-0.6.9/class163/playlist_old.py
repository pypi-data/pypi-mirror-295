"""
class163/playlist_old.py
Version: 0.5.2
Author: CooooldWind_
E-Mail: 3091868003@qq.com
Copyright @CooooldWind_ / Following GNU_AGPLV3+ License
"""

import time
from netease_encode_api import EncodeSession
from class163.music import Music
from urllib.parse import urlparse, parse_qs
from class163.global_args import *


class Playlist:
    def __init__(self, id: int | str) -> None:
        self.id = id
        if self.id.__class__ == str and self.id.find("music.163.com") != -1:
            self.id = url_to_id(self.id)
        self.encode_session = EncodeSession()  #  解码会话
        self.__encode_data = {
            "id": self.id,
        }
        self.creator: str = None
        self.create_time = None
        self.last_update_time = None
        self.title: str = None
        self.track_count: int = None
        self.description: str = None
        self.track: list[Music] = []
        self.track_id: list[int] = []
        self.info_raw: dict = {}
        self.info_sorted: dict = {}
        self.detail_info_raw: dict = {}
        self.detail_info_sorted: dict = {}

    def get(
        self,
        detail: bool = True,
        session: EncodeSession = None,
        mode: MODE = "d",
        level: LEVEL = "standard",
    ) -> dict:
        if session == None:
            session = self.encode_session
        result: dict = {}
        result = self.get_info(session=session)
        if detail:
            result = self.get_detail(mode=mode, level=level)
        return result

    def get_info(self, session: EncodeSession = None) -> dict:
        if session == None:
            session = self.encode_session
        self.info_raw = session.get_response(
            url="https://music.163.com/weapi/v6/playlist/detail",
            encode_data=self.__encode_data,
        )["playlist"]
        self.title = self.info_raw["name"]
        self.description = self.info_raw["description"]
        self.track_count = self.info_raw["trackCount"]
        self.last_update_time = time.localtime(
            int(self.info_raw["updateTime"]) / 1000
        )
        self.last_update_time = self.last_update_time[0:5]
        self.create_time = time.localtime(int(self.info_raw["createTime"]) / 1000)
        self.create_time = self.create_time[0:5]
        self.creator = self.info_raw["creator"]["nickname"]
        for i in self.info_raw["trackIds"]:
            self.track.append(Music(i["id"]))
            self.track_id.append(i["id"])
        self.info_sorted = {
            "title": self.title,
            "description": self.description,
            "track_count": self.track_count,
            "last_update_time": self.last_update_time,
            "create_time": self.create_time,
            "creator": self.creator,
            "track_id": self.track_id,
        }
        return self.info_sorted

    def get_detail(self, mode: MODE = "d", level: LEVEL = "standard") -> dict:
        self.detail_info_sorted = self.info_sorted
        sorted_track: list[dict] = []
        self.detail_info_raw = self.info_raw
        self.detail_info_raw["tracks"] = []
        for i in self.track:
            i.get(mode=mode, level=level)
            self.detail_info_raw["tracks"].append(i.detail_info_raw)
            sorted_track.append(i.info_dict())
        self.detail_info_sorted["track"] = sorted_track
        return self.detail_info_sorted


def url_to_id(url: str) -> int:
    try:
        # 手动分割URL，获取hash部分
        if url.find("#/") != -1: hash_fragment = url.split("#")[1]
        else: hash_fragment = url
        # 解析hash部分的查询参数
        query_params = parse_qs(hash_fragment.split("?")[1])

        # 提取ID并转换为整数
        playlist_id = int(query_params.get("id", [None])[0])
        return playlist_id
    except (IndexError, ValueError, TypeError):
        raise ValueError("URL 中未找到 'id' 参数")
