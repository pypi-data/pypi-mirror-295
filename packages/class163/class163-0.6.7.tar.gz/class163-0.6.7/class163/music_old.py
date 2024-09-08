"""
class163/music.py
Version: 0.5.0
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

"""
Music 类用于处理音乐相关的信息，包括歌曲详情、歌词、音乐文件等
"""
class Music:
    def __init__(self, id: int | str) -> None:
        """
        初始化 Music 类的实例
        :param id: 歌曲的 ID 或包含 ID 的 URL
        """
        #  将 ID 转换为字符串格式，并处理 URL 中的 ID
        self.id = str(id)  
        if self.id.find("music.163.com")!= -1:
            self.id = url_to_id(self.id)
        self.encode_session = EncodeSession()  # 创建解码会话
        # 详细信息相关的初始化
        self.__detail_encode_data = {
            "c": str([{"id": self.id}]),
        }  
        self.title: str = None  # 歌曲标题
        self.subtitle: str = None  # 副标题
        self.album: str = None  # 专辑
        self.artist: list[str] = []  # 歌手列表
        self.publish_time = None  # 发布时间
        self.trans_title: str = None  # 标题译文
        self.trans_album: str = None  # 专辑译文
        self.trans_artist: dict = {}  # 歌手译文字典
        self.detail_info_raw: dict = {}  # 原始的详细信息数据
        self.detail_info_sorted: dict = {}  # 整理后的详细信息数据
        self.cover_url: str = None  # 封面 URL
        # 歌词相关的初始化
        self.__lyric_encode_data = {
            "id": self.id,
            "lv": -1,
            "tv": -1,
        }  
        self.lyric: str = None  # 歌词原文
        self.trans_lyric: str = None  # 歌词翻译
        self.trans_uploader: str = None  # 翻译歌词的网易云用户昵称
        self.trans_lyric_uptime = None  # 翻译的发布时间
        self.lyric_info_raw: dict = {}  # 原始的歌词信息数据
        self.lyric_info_sorted: dict = {}  # 整理后的歌词信息数据
        # 音乐文件相关的初始化
        """
        id 表示歌曲的 id 号, 
        level 是音乐品质, 
        标准为 standard, 
        较高音质为 higher, 
        极高音质 exhigh, 
        无损音质关键词为 lossless。
        """
        self.__file_encode_data = {
            "ids": str([self.id]),
            "level": None,  # standard/higher/exhigh/lossless
            "encodeType": None,  # 如果是 lossless 就用 aac, 其他是 mp3
        }  
        self.file_url: str = None
        self.file_md5: str = None
        self.file_size: int = None
        self.file_info_raw: dict = {}  # 原始的文件信息数据
        self.file_info_sorted: dict = {}  # 整理后的文件信息数据

    def get(
        self,
        mode: MODE = "d",
        encode_session: EncodeSession = None,
        url: str = None,
        offical: bool = True,
        level: LEVEL = "standard",
        cookies: dict = None,
        method: str = "get",
        url_key: list = [],
        md5_key: list = [],
        size_key: list = [],
        **kwargs
    ) -> dict:
        """
        根据指定的模式获取歌曲的详细信息、歌词或文件信息
        :param mode: 模式，'d'表示详细信息，'l'表示歌词，'f'表示文件
        :param encode_session: 编码会话，如果未提供则使用实例中的会话
        :param url: 第三方文件的 URL
        :param offical: 是否获取官方文件
        :param level: 音乐品质
        :param cookies: 用于请求的 Cookie 字典
        :param method: 请求方法，默认为'get'
        :param url_key: 用于提取文件 URL 的键列表
        :param md5_key: 用于提取文件 MD5 的键列表
        :param size_key: 用于提取文件大小的键列表
        :param kwargs: 其他关键字参数
        :return: 包含请求结果的字典
        """
        if encode_session is None:
            encode_session = self.encode_session
        is_detail, is_lyric, is_file = False, False, False
        if "d" in mode:
            is_detail = True
        if "l" in mode:
            is_lyric = True
        if "f" in mode:
            is_file = True
        result: dict = {}
        if is_detail:
            result.update(self.get_detail(encode_session=encode_session))
        if is_lyric:
            result.update(self.get_lyric(encode_session=encode_session))
        if is_file:
            result.update(
                self.get_file(
                    offical=offical,
                    encode_session=encode_session,
                    level=level,
                    url=url,
                    cookies=cookies,
                    method=method,
                    kwargs=kwargs,
                )
            )
        return result

    def file_info_sort(
        self, file_url: str = None, file_md5: str = None, file_size: int = None
    ) -> dict:
        """
        对文件信息进行整理
        :param file_url: 文件 URL
        :param file_md5: 文件 MD5
        :param file_size: 文件大小
        :return: 整理后的文件信息字典
        """
        self.file_info_sorted = {
            "file_url": file_url,
            "file_md5": file_md5,
            "file_size": file_size,
        }
        return self.file_info_sorted

    def get_file(
        self,
        url: str = None,
        offical: bool = True,
        level: LEVEL = "standard",
        encode_session: EncodeSession = None,
        cookies: dict = None,
        method: str = "get",
        url_key: list = [],
        md5_key: list = [],
        size_key: list = [],
        **kwargs
    ) -> dict:
        """
        获取音乐文件信息
        :param url: 第三方文件的 URL
        :param offical: 是否获取官方文件
        :param level: 音乐品质
        :param encode_session: 编码会话，如果未提供则使用实例中的会话
        :param cookies: Cookie 字典
        :param method: 请求方法
        :param url_key: 用于提取文件 URL 的键列表
        :param md5_key: 用于提取文件 MD5 的键列表
        :param size_key: 用于提取文件大小的键列表
        :param kwargs: 其他关键字参数
        :return: 文件信息字典
        """
        if encode_session is None:
            encode_session = self.encode_session
        if offical:
            return self.__get_file_offical(encode_session=encode_session, level=level)
        else:
            return self.__get_file_third_party(
                url=url,
                cookies=cookies,
                method=method,
                url_key=url_key,
                md5_key=md5_key,
                size_key=size_key,
                kwargs=kwargs,
            )

    def __get_file_third_party(
        self,
        method: str,
        url: str,
        cookies: dict,
        url_key: list,
        md5_key: list,
        size_key: list,
        **kwargs
    ) -> dict:
        """
        从第三方获取文件信息
        :param method: 请求方法
        :param url: URL
        :param cookies: Cookie 字典
        :param url_key: 用于提取文件 URL 的键列表
        :param md5_key: 用于提取文件 MD5 的键列表
        :param size_key: 用于提取文件大小的键列表
        :param kwargs: 其他关键字参数
        :return: 文件信息字典
        """
        session = Session()
        session.cookies = cookiejar_from_dict(cookie_dict=cookies)
        data = {}
        data.update(**kwargs)
        response = session.request(method=method, url=url, data=data).json()
        response = self.__extract_info(
            raw_info=response, url_key=url_key, md5_key=md5_key, size_key=size_key
        )
        return response

    def __find_key(
        self, nested: dict | str | float | int | bool | list | None, key: list
    ) -> str:
        """
        从嵌套的数据结构中根据给定的键列表查找值
        :param nested: 嵌套的数据结构
        :param key: 键列表
        :return: 查找到的值
        """
        if len(key) == 0:
            return nested
        else:
            return self.__find_key(nested=nested[key[0]], key=key[1:])

    def __extract_info(
        self, raw_info: dict, url_key: list, md5_key: list, size_key: list
    ):
        """
        从原始信息中提取文件的 URL、MD5 和大小
        :param raw_info: 原始信息字典
        :param url_key: 用于提取文件 URL 的键列表
        :param md5_key: 用于提取文件 MD5 的键列表
        :param size_key: 用于提取文件大小的键列表
        :return: 包含提取结果的字典
        """
        result = {
            "file_url": self.__find_key(nested=raw_info, key=url_key),
            "file_md5": self.__find_key(nested=raw_info, key=md5_key),
            "file_size": self.__find_key(nested=raw_info, key=size_key),
        }
        return result

    def __get_file_offical(
        self, encode_session: EncodeSession = None, level: LEVEL = "standard"
    ) -> dict:
        """
        从官方获取音乐文件信息
        :param encode_session: 编码会话，如果未提供则使用实例中的会话
        :param level: 音乐品质
        :return: 文件信息字典
        """
        if encode_session is None:
            encode_session = self.encode_session
        if level in ["standard", "higher", "exhigh"]:
            self.__file_encode_data["encodeType"] = "mp3"
        else:
            self.__file_encode_data["encodeType"] = "aac"
        self.__file_encode_data["level"] = level
        self.file_info_raw = encode_session.get_response(
            url=FILE_URL,
            encode_data=self.__file_encode_data,
        )["data"][0]
        self.file_url = str(self.file_info_raw["url"])
        if self.file_url.find("?authSecret")!= -1:
            self.file_url = self.file_url[: self.file_url.find("?authSecret")]
        self.file_md5 = str(self.file_info_raw["md5"])
        self.file_size = int(self.file_info_raw["size"])
        return self.file_info_sort(
            file_url=self.file_url, file_md5=self.file_md5, file_size=self.file_size
        )

    def get_lyric(self, encode_session: EncodeSession = None) -> dict:
        """
        获取歌词信息
        :param encode_session: 编码会话，如果未提供则使用实例中的会话
        :return: 歌词信息字典
        """
        if encode_session is None:
            encode_session = self.encode_session
        self.lyric_info_raw = encode_session.get_response(
            url=LYRIC_URL,
            encode_data=self.__lyric_encode_data,
        )
        # 歌词、歌词翻译、翻译上传者
        self.lyric = str(self.lyric_info_raw["lrc"]["lyric"])
        if "tlyric" in self.lyric_info_raw:
            if "lyric" in self.lyric_info_raw["tlyric"]:
                self.trans_lyric = str(self.lyric_info_raw["tlyric"]["lyric"])
        if "transUser" in self.lyric_info_raw:
            if "nickname" in self.lyric_info_raw["transUser"]:
                self.trans_uploader = str(self.lyric_info_raw["transUser"]["nickname"])
            # 翻译上传时间（精确到分钟）
            if "uptime" in self.lyric_info_raw["transUser"]:
                self.trans_lyric_uptime = time.localtime(
                    int(self.lyric_info_raw["transUser"]["uptime"]) / 1000
                )
                self.trans_lyric_uptime = self.trans_lyric_uptime[0:5]
        # 整理
        self.lyric_info_sorted = {
            "lyric": self.lyric,
            "trans_lyric": self.trans_lyric,
            "trans_uploader": self.trans_uploader,
            "trans_lyric_uptime": self.trans_lyric_uptime,
        }
        #
        return self.lyric_info_sorted

    def get_detail(self, encode_session: EncodeSession = None) -> dict:
        """
        获取歌曲的详细信息
        :param encode_session: 编码会话，如果未提供则使用实例中的会话
        :return: 详细信息字典
        """
        if encode_session is None:
            encode_session = self.encode_session
        self.detail_info_raw = encode_session.get_response(
            url=DETAIL_URL,
            encode_data=self.__detail_encode_data,
        )["songs"][0]
        # 标题和专辑
        self.title = str(self.detail_info_raw["name"])
        self.album = str(self.detail_info_raw["al"]["name"])
        # 发行日期
        self.publish_time = time.localtime(
            int(self.detail_info_raw["publishTime"]) / 1000
        )
        self.publish_time = self.publish_time[0:3]
        # 副标题
        if "alia" in self.detail_info_raw:
            if len(self.detail_info_raw["alia"]) > 0:
                self.subtitle = str(self.detail_info_raw["alia"][0])
        # 标题译文
        if "tns" in self.detail_info_raw:
            if len(self.detail_info_raw["tns"]) > 0:
                self.trans_title = str(self.detail_info_raw["tns"][0])
        # 专辑译文
        if "tns" in self.detail_info_raw["al"]:
            if len(self.detail_info_raw["al"]["tns"]) > 0:
                self.trans_album = str(self.detail_info_raw["al"]["tns"][0])
        # 歌手及歌手翻译
        for i in self.detail_info_raw["ar"]:
            self.artist.append(str(i["name"]))
            if "tns" in i:
                if len(i["tns"]) > 0:
                    self.trans_artist.update({str(i["name"]): str(i["tns"])})
        # 封面 URL
        self.cover_url = str(self.detail_info_raw["al"]["picUrl"])
        # 整理
        self.detail_info_sorted.update(
            {
                "id": self.id,
                "title": self.title,
                "album": self.album,
                "artist": self.artist,
                "publish_time": self.publish_time,
                "subtitle": self.subtitle,
                "trans_title": self.trans_title,
                "trans_album": self.trans_album,
                "trans_artist": self.trans_artist,
                "cover_url": self.cover_url,
            }
        )
        return self.detail_info_sorted


def url_to_id(url: str) -> str:
    """
    从给定的 URL 中提取歌曲 ID
    :param url: 包含歌曲 ID 的 URL
    :return: 提取出的歌曲 ID
    """
    try:
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)
        song_id = query_params.get("id", [None])[0]
        if song_id is not None:
            return str(song_id)
        else:
            raise ValueError("URL 中未找到 'id' 参数")
    except (ValueError, TypeError) as e:
        raise e


def artist_join(artist: list[str], separator: str = ", ") -> str:
    """
    将歌手列表连接为一个字符串
    :param artist: 歌手列表
    :param separator: 分隔符，默认为", "
    :return: 连接后的字符串
    """
    artist_str = ""
    for i in artist[:-1]:
        artist_str += i + separator
    artist_str += artist[-1]
    return artist_str