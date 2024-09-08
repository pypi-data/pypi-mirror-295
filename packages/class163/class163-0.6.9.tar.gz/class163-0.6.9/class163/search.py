"""
class163/music.py
Version: 0.6.0
Author: CooooldWind_/豆包@字节跳动
E-Mail: 3091868003@qq.com
Copyright @CooooldWind_ / Following GNU_AGPLV3+ License
"""

import time
from netease_encode_api import EncodeSession
from urllib.parse import urlparse, parse_qs
from class163.global_args import *
from requests import Session
from requests.cookies import cookiejar_from_dict
from class163.common import BasicMusicType, extract, extract_in_list
from typing import Optional, Dict, List, Union, Type


class Search:
    def __init__(
        self, key: str, cookie_dict: Optional[Dict], search_type: SEARCH_TYPE = "song"
    ):
        self.encode_session = EncodeSession()
        self.search_type = search_type
        if cookie_dict != None:
            self.encode_session.set_cookies(cookie_dict)
        encode_type = ""
        if search_type == "song":
            encode_type = "1"
        elif search_type == "album":
            encode_type = "10"
        elif search_type == "artist":
            encode_type = "100"
        elif search_type == "playlist":
            encode_type = "1000"
        self.offset = 0
        self.result_count = 0
        self.__encode_data = {
            "s": key,
            "type": encode_type,  # 歌曲-1 专辑-10 歌手-100 歌单-1000
            "offset": str(self.offset),
            "total": "true",
            "limit": "30",
        }
        self.search_result_raw = {}

    def get(
        self, encode_session: EncodeSession = None, end_index: int = 9999999
    ) -> Optional[Dict]:
        if encode_session is None:
            encode_session = self.encode_session
        if "MUSIC_U" not in dict(self.encode_session.session.cookies.get_dict()).keys():
            return None
        origin = encode_session.get_response(
            url=SEARCH_URL, encode_data=self.__encode_data
        )["result"]
        self.result_count = extract(origin, [f"{self.search_type}Count"], int)
        self.search_result_raw = origin
        while True:
            self.offset += 30
            if self.offset >= min(self.result_count, end_index):
                break
            self.__encode_data["offset"] = str(self.offset)
            self.__encode_data["total"] = "false"
            origin = encode_session.get_response(
                url=SEARCH_URL, encode_data=self.__encode_data
            )["result"]
            self.search_result_raw[f"{self.search_type}s"] += extract(
                origin, [f"{self.search_type}s"], list
            )
        self.search_result_raw[f"{self.search_type}s"] = self.search_result_raw[
            f"{self.search_type}s"
        ][0 : min(self.result_count, end_index)]
        return self.search_result_raw
