---
license: openrail
task_categories:
- video-classification
language:
- zh
pretty_name: 软件教程数据集
size_categories:
- n<1K
---

# 软件教程数据集

本数据集包括从[bilibili](https://www.bilibili.com)收集的127个视频链接，存储在`SoftwareTutorialVideos.jsonl`中。大部分视频链接包含多个视频。本数据集总共有数千个视频，总时长超过一千小时。若按照最高清晰度下载，大小超过300G.

视频的主要内容是常用的软件教程，涵盖Word，Excel， Power Point，Visual Studio Code，python，C++，JavaScript，Java，Linux，MacOS，Unreal Engine，AutoCAD，Rhino，PhotoShop，After Effects， Vocaloid等。

本数据集既可用于个人学习，也可用于和桌面系统UI有关的计算机视觉任务，例如视频动作识别，视频理解，版面分析，图像分类，图像生成，机器人流程自动化（RPA）等。

## 下载视频

本数据集附带下载器`bilibili_download.py`，使用方法如下：

1. 下载安装[ffmpeg](https://ffmpeg.org/)并添加到环境变量。

2. 下载[lux](https://github.com/iawia002/lux)并把程序存放在同一文件夹下。

3. （可选）如果需要使用cookies（以下载更高清晰度的视频或下载仅会员可见的视频），在同一文件夹下新建`cookie.txt`. 使用浏览器打开bilibili网站并登录，然后使用开发者工具获取cookies，并且把内容保存在`cookie.txt`中。

4. 终端运行命令

   ```
   python bilibili_download.py
   ```

5. 选择第二个选项，开始下载视频。本脚本会把下载进度保留在`checkpoint.txt`中。若中途中断，会从中断处开始下载。

6. 如果看到感兴趣的视频需要添加，只需选择第一个选项，再输入相应的BV号即可。

## 视频时长统计

首先安装`opencv`:

```
pip install opencv-python
```

然后在终端运行脚本`duration.py`:

```
python duration.py
```

就会自动打印目前已经下载的视频的时长信息。