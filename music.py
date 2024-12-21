import asyncio
import argparse
from bilibili_api import video, Credential, HEADERS
import httpx
import os
import re
import json

data = json.load(open("./pre.json", "r", encoding="utf-8"))

SESSDATA = data["SESSDATA"]
BILI_JCT = data["BILI_CJT"]
BUVID3 = data["BUVID3"]

# FFMPEG 路径，查看：http://ffmpeg.org/
FFMPEG_PATH = "ffmpeg"


async def download_url(url: str, out: str, info: str):
    # 下载函数
    async with httpx.AsyncClient(headers=HEADERS) as sess:
        resp = await sess.get(url)
        length = resp.headers.get("content-length")
        with open(out, "wb") as f:
            process = 0
            for chunk in resp.iter_bytes(1024):
                if not chunk:
                    break

                process += len(chunk)
                print(f"下载 {info} {process} / {length}")
                f.write(chunk)


async def re2title(title: str) -> str:
    pattern = "《(.*?)》"
    match = re.search(pattern, title)
    if match is None:
        return title
    else:
        return match.group(1)


async def main(bv: str, ov: bool):
    # 实例化 Credential 类
    credential = Credential(sessdata=SESSDATA, bili_jct=BILI_JCT, buvid3=BUVID3)
    # 实例化 Video 类
    v = video.Video(bvid=bv, credential=credential)
    # 获取信息
    info = await v.get_info()
    title = await re2title(info["title"])

    # 获取视频下载链接
    download_url_data = await v.get_download_url(0)
    # 解析视频下载信息
    detecter = video.VideoDownloadURLDataDetecter(data=download_url_data)
    streams = detecter.detect_best_streams()

    cache_path = None
    # 有 MP4 流 / FLV 流两种可能
    if detecter.check_flv_stream() == True:
        await download_url(streams[0].url, "flv_temp.flv", "FLV 音视频流")
        if ov == False:
            os.system(
                f"{FFMPEG_PATH} -i flv_temp.flv -vn -acodec libmp3lame -ab 192k ./music/{title}.mp3"
            )
            os.remove("flv_temp.flv")
            cache_path = f"./music/{title}.mp3"
        else:
            os.system(f"mv flv_temp.flv ./video/{title}.mp4")
            cache_path = f"./video/{title}.mp4"
    else:
        await download_url(streams[1].url, "audio_temp.m4s", "音频流")
        if ov == True:
            await download_url(streams[0].url, "video_temp.m4s", "视频流")

            os.system(
                f"{FFMPEG_PATH} -i video_temp.m4s -i audio_temp.m4s -vcodec copy -acodec copy ./video/{title}.mp4"
            )
            os.remove("video_temp.m4s")
            cache_path = f"./video/{title}.mp4"
        else:
            os.system(
                f"{FFMPEG_PATH} -i audio_temp.m4s -vn -acodec libmp3lame -ar 44100 -ac 2 -ab 192k ./music/{title}.mp3"
            )
            cache_path = f"./music/{title}.mp3"
        os.remove("audio_temp.m4s")

    print(f"已下载为 {cache_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-b",
        "--bv",
        help="input bv id like BV1bL411h72w",
        type=str,
        required=True,
    )
    parser.add_argument(
        "-v",
        "--video",
        action="store_true",  # 指定时为True，否则默认就是False
        help="only video，default mp3 audio",
    )
    args = parser.parse_args()
    bv = args.bv
    onlyVideo = args.video

    os.makedirs("./video", exist_ok=True)
    os.makedirs("./music", exist_ok=True)

    # 主入口
    asyncio.get_event_loop().run_until_complete(main(bv=bv, ov=onlyVideo))
