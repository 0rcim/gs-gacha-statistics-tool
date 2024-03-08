# [ADB] Genshin Impact gacha statistics tool (Based on ADB)

安卓平台祈愿记录抓取分析工具，基于ADB，需要设备打开USB debugging。

## Install dependencies

```sh
python -m pip install adbutils peewee
```

## Usage

```sh
# 给文件赋予可执行权限
chmod +x ./gs-statistics

# 仅进行本地统计分析
./gs-statistics

# 进行抓取操作，进入游戏，打开祈愿页面，然后点击历史记录
# 根据提示，等待获取到url后，按下回车，之后便开始抓取记录更新至到本地并打印统计结果
# 祈愿记录保存在项目根目录下的SQLite数据库文件gs-gacha-log.db中
./gs-statistics update

# utils/import.py UIGF.json 导入历史抽卡记录
python utils/import.py path/to/your_GS_UIGF_file.json
```
