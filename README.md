# video-to-wechat-article

> 让视频直接变成公众号文章

<p align="center">
  <img src="https://img.shields.io/badge/license-MIT-green" alt="License: MIT">
  <img src="https://img.shields.io/badge/standard-Agent%20Skills-blue" alt="Agent Skills Standard">
  <img src="https://img.shields.io/badge/runtime-Claude%20Code%20%7C%20Codex-orange" alt="Multi-Runtime">
</p>

---

拍视频的人都有一个共同的痛——素材在手里，但不想写文章。

口播、课程切片、播客录像、直播回放……你知道这里面有好的观点，但把它变成一篇公众号文章，至少要搭进去两三个小时：听一遍、记笔记、理结构、写初稿、打磨、配图、排版。

**现在不用了。** 把视频丢进来，出来的是一篇能直接复制粘贴到公众号编辑器的独立成稿 HTML。

不是字幕整理。不是"视频约 00:03 提到"。不是素材笔记。是一篇真正的文章——有结构、有观点、有节奏，读者不会感觉到它来源于一个视频。

---

## 它到底做了什么

**输入：** 一个本地视频文件。

**输出：** 一个 `<视频名>-wechat.html`。

中间发生了什么：

```
你的视频
  → 提取音频
  → 转录文字
  → 用 dbs 文案规则重写成独立文章（去字幕腔、去 AI 味、去"视频里提到"）
  → 可选：用 huashu-design 设计封面和配图
  → 生成干净的 HTML——打开、复制、粘贴到公众号编辑器
```

你只需要说一句话：

> 帮我把这个视频转成公众号文章

---

## 安装

### 方法一：一句话安装（推荐）

直接告诉你的 agent：

> 帮我安装这个 skill：https://github.com/BlackFast/video-to-wechat-article

### 方法二：npx

```bash
npx skills add BlackFast/video-to-wechat-article
```

### 方法三：手动安装

| Runtime | 路径 |
|---------|------|
| Claude Code | `git clone https://github.com/BlackFast/video-to-wechat-article.git ~/.claude/skills/video-to-wechat-article` |
| Codex | `git clone https://github.com/BlackFast/video-to-wechat-article.git ~/.codex/skills/video-to-wechat-article` |
| 双端共用 | 装到一处，另一个建符号链接 |

### 方法四：不用安装也能用

即使你的 agent 不支持 Agent Skills，直接把 `SKILL.md` 的内容粘贴到对话里，它就能按流程走。

---

## 依赖

这个 skill 不依赖任何云服务。它用你本机的工具：

| 工具 | 干什么 | 怎么装 |
|------|--------|--------|
| ffmpeg | 提取音频和关键帧 | `brew install ffmpeg` |
| Python 3 | 跑辅助脚本 | 系统自带 |
| 一个转录工具 | 语音转文字 | 三选一，见下 |

转录选一个就行：

```bash
# 推荐：whisper-cpp（本地跑，2 秒转完 1 分钟音频）
brew install whisper-cpp
curl -L https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-base.bin \
  -o ~/.cache/whisper-cpp/ggml-base.bin

# 或者：OpenAI Whisper API
export OPENAI_API_KEY="sk-..."

# 或者：Python whisper
pip3 install openai-whisper
```

---

## 设计原则

这个 skill 有几个硬性信念：

**文章不是视频整理稿。** 文章里禁止出现「视频里提到」「视频约 00:03」「本文根据视频整理」。读者不需要知道它来自一个视频。

**单一输出，不是文件包。** 旧版本输出 7 个文件（transcript.md、article.md、title_candidates.md……），你还要一个个打开看。现在只有一个 HTML，打开就能用。

**默认纯文字。** 一篇好文章不需要图片撑场面。只有你要求配图时才做——而且不是放几张视频截图了事，是用 CSS 画出来的独立插图。

**配图不是文字排版的变体。** 封面可以给几个排版方向让你选。但内文配图是另一回事——每张图对应一个具体的观点或比喻，画面各不相同。目前验证过的三种配图模式：对比图、卡片网格、比喻插图。

---

## 配图模式速览

| 模式 | 长什么样 | 什么时候用 |
|------|---------|-----------|
| 对比图 | 左右分屏，左=错误做法，右=正确做法 | 文章有 A vs B 的论点 |
| 卡片网格 | 色块卡片排成词典格子，最后一张虚线空卡 | 提出"收集/分类/体系"概念 |
| 比喻插图 | CSS 几何形状搭建场景，关键数字用 UI 元素 | 文章有强比喻（F1 赛车、登山） |

---

## 文件结构

```
video-to-wechat-article/
  SKILL.md                    # 技能定义——agent 读这个就知道怎么干活
  README.md                   # 你在看的这个文件
  scripts/
    extract_audio.py          # ffmpeg 提取音频 → mono 16k WAV
    extract_keyframes.py      # ffmpeg 定时抽取关键帧
    render_wechat_html.py     # 把内容拼成干净的公众号 HTML
  references/
    dbs-copywriting.md        # 文案操作手册（从 dontbesilent 蒸馏）
    huashu-design.md          # 视觉设计手册（从 花叔Design 蒸馏）
    wechat-html-format.md     # 公众号 HTML 标签白名单和格式规范
```

---

## 背景

这个 skill 来源于一个真实的痛点：我拍了不少视频，有些观点值得写成文章，但每次都卡在"写完第一段就不想写了"。

已有的 AI 工具能转录，转录完还是素材——离"一篇能发的文章"差得远。

差在哪？三个东西：
1. **文案判断**——什么该留、什么该删、怎么把口语变成书面语但不丢掉说话人的味道
2. **结构重构**——视频是线性的，文章需要骨架。小标题、节奏、重点句——这些视频里没有
3. **视觉完整**——封面和配图不是为了好看，是为了读者在信息流里停下来、在正文里读下去

这三个东西，分别由 dbs 和 huashu-design 两个方法论解决。这个 skill 把它们蒸馏成操作手册，agent 读一遍就知道怎么做。

---

## 作者

**BlackFast**

---

## License

MIT — 随便用，随便改，随便造。

---

> 视频是原材料，文章是最终表达。让视频直接变成公众号文章。
