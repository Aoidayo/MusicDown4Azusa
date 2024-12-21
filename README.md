# MusicDown4Azusa
阿梓歌下载器

看见了nooblong 网易云的阿梓播客，所以也想下载自己喜欢的阿梓的歌。

参考：
- [nooblong/bilibili-to-netease-cloud-music: b站视频一键转网易云播客](https://github.com/nooblong/bilibili-to-netease-cloud-music?tab=readme-ov-file)
- [Nemo2011/bilibili-api](https://github.com/Nemo2011/bilibili-api)
	- 基于[asyncio --- 异步 I/O — Python 3.13.1 文档](https://docs.python.org/zh-cn/3/library/asyncio.html)
	- 获取基础cookies：[获取 Credential 类所需信息](https://nemo2011.github.io/bilibili-api/#/get-credential)

# 1 指定bv下载视频

## 1.1 环境安装
```bash
pip3 install git+https://github.com/Nemo2011/bilibili-api.git@dev
```


## 1.2 cookies
使用之前，从b站网页的cookies中获取如下字段的值，并写入`pre.json`中
- `SESSDATA` ：session，跳过登录
- `bili_jct` ：操作用户数据的POST请求 需要
- `buvid3` ：设备验证码
- `dedeuserid` ：可以不提供，一般是用户id


## 1.3 使用示例

```bash
python music.py -b BV1nek6YcEsJ
python music.py -b BV1nek6YcEsJ -v # 下载视频
```

