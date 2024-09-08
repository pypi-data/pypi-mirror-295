"""
class163/playlist.py
Version: 0.6.6
Author: CooooldWind_
E-Mail: 3091868003@qq.com
Copyright @CooooldWind_ / Following GNU_AGPLV3+ License
"""

import time
from netease_encode_api import EncodeSession
from class163.music import BasicMusicType, Music
from urllib.parse import urlparse, parse_qs
from class163.global_args import *
from class163.common import extract, extract_in_list
from typing import Optional, Dict, List, Union, Type


class BasicPlaylistType:
    def __init__(self):
        self.title = None
        self.creator = None
        self.create_time = None
        self.last_update_time = None
        self.description = None
        self.track_count = None
        self.track: List[Union[Music, BasicMusicType, None]] = []

    def info_dict(self) -> Optional[Dict]:
        track_result = [basic_music.info_dict() for basic_music in self.track]
        result = {
            "title": self.title,
            "creator": self.creator,
            "create_time": self.create_time,
            "last_update_time": self.last_update_time,
            "description": self.description,
            "track_count": self.track_count,
            "track_info": track_result,
        }
        return result

class Playlist(BasicPlaylistType):
    def __init__(self, id: int | str) -> None:
        super().__init__()
        self.id = id
        if self.id.__class__ == str and self.id.find("music.163.com") != -1:
            self.id = url_to_id(self.id)
        self.encode_session = EncodeSession()  #  解码会话
        self.__encode_data = {
            "id": self.id,
        }

    def get_detail(self, each_music: bool = True, session: EncodeSession = None) -> Optional[Dict]:
        if session == None:
            session = self.encode_session
        self.info_raw = session.get_response(
            url="https://music.163.com/weapi/v6/playlist/detail",
            encode_data=self.__encode_data,
        )["playlist"]
        origin = self.info_raw
        result = self.extract_detail(origin=origin)
        if each_music:
            for index in range(len(self.track)):
                if self.track[index].title == None:
                    appending_music = Music(self.track[index].id)
                    appending_music.get_detail(session)
                    self.track[index] = appending_music
        result = self.info_dict()
        return result

    def extract_detail(
        self,
        origin: Dict,
        title_keys: List[Union[str, int]] = ["name"],
        creator_keys: List[Union[str, int]] = ["creator", "nickname"],
        create_time_keys: List[Union[str, int]] = ["createTime"],
        last_update_time_keys: List[Union[str, int]] = ["updateTime"],
        description_keys: List[Union[str, int]] = ["description"],
        track_count_keys: List[Union[str, int]] = ["trackCount"],
        track_id_list_keys: List[Union[str, int]] = ["trackIds"],
        track_id_keys: List[Union[str, int]] = ["id"],
        track_list_keys: List[Union[str, int]] = ["tracks"],
    ) -> Optional[Dict]:
        self.title = extract(origin, title_keys, str)
        self.creator = extract(origin, creator_keys, str)
        create_time = time.localtime(int(extract(origin, create_time_keys, int)) / 1000)
        self.create_time = list(create_time[0:5])
        last_update_time = time.localtime(
            int(extract(origin, last_update_time_keys, int)) / 1000
        )
        self.last_update_time = list(last_update_time[0:5])
        self.description = extract(origin, description_keys, str)
        self.track_count = extract(origin, track_count_keys, int)
        track_id_list = extract_in_list(
            extract(origin, track_id_list_keys, list), track_id_keys, int
        )
        for id in track_id_list:
            self.track.append(Music(id))
        track_list = extract(origin, track_list_keys, list)
        for index in range(len(track_list)):
            appending_music = Music(0)
            appending_music.detail_info_raw = track_list[index]
            appending_music.extract_detail(origin=appending_music.detail_info_raw)
            self.track[index] = appending_music
        return self.info_dict()


def url_to_id(url: str) -> int:
    try:
        # 手动分割URL，获取hash部分
        if url.find("#/") != -1:
            hash_fragment = url.split("#")[1]
        else:
            hash_fragment = url
        # 解析hash部分的查询参数
        query_params = parse_qs(hash_fragment.split("?")[1])

        # 提取ID并转换为整数
        playlist_id = int(query_params.get("id", [None])[0])
        return playlist_id
    except (IndexError, ValueError, TypeError):
        raise ValueError("URL 中未找到 'id' 参数")
