# video-to-wechat-article

把一个视频改写成一篇可直接复制到公众号编辑器的独立成稿 HTML。

**视频是原材料，文章是最终表达。** 输出的文章像独立创作的公众号文章——读者不需要知道、也不应该感觉到它来源于一个视频。

## 输出

一个文件：`<video-name>-wechat.html`

用浏览器打开，全选复制，粘贴到公众号编辑器。格式已适配。

## 安装

### Claude Code

```bash
git clone https://github.com/<your-username>/video-to-wechat-article.git ~/.claude/skills/video-to-wechat-article
```

### Codex

```bash
git clone https://github.com/<your-username>/video-to-wechat-article.git ~/.codex/skills/video-to-wechat-article
```

### 双端共用

装到一边，另一边建符号链接：

```bash
git clone https://github.com/<your-username>/video-to-wechat-article.git ~/.codex/skills/video-to-wechat-article
ln -s ~/.codex/skills/video-to-wechat-article ~/.claude/skills/video-to-wechat-article
```

## 依赖

| 工具 | 用途 | 安装 |
|------|------|------|
| ffmpeg | 音频提取、关键帧提取 | `brew install ffmpeg` |
| Python 3 | 辅助脚本 | 系统自带或 `brew install python3` |
| 转录工具 | 语音转文字 | 自适应——Whisper API / whisper-cpp / 本地 Whisper / 用户提供 |

转录工具至少装一个：

```bash
# 方案 A: whisper-cpp（推荐，本地运行，速度快）
brew install whisper-cpp
# 首次使用下载模型
curl -L https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-base.bin -o ~/.cache/whisper-cpp/ggml-base.bin

# 方案 B: OpenAI Whisper API（需要 API Key）
export OPENAI_API_KEY="sk-..."

# 方案 C: Python whisper（本地，需要 GPU）
pip3 install openai-whisper
```

## 使用

对 agent 说：

> 帮我把 `~/Videos/my-talk.mp4` 转成公众号文章

agent 会自动走完整流程：

1. 提取音频 → 转录
2. 提取关键帧辅助理解
3. 用 dbs 文案规则重写成独立文章
4. 可选：用 huashu-design 规则设计封面和配图
5. 输出一个浏览器打开就能复制粘贴的 HTML

## 文件结构

```
video-to-wechat-article/
  SKILL.md                        # 技能定义
  README.md                       # 本文件
  scripts/
    extract_audio.py              # 提取音频（需 ffmpeg）
    extract_keyframes.py          # 提取关键帧（需 ffmpeg）
    render_wechat_html.py         # 生成公众号 HTML
  references/
    dbs-copywriting.md            # 文案规则（从 dbs 蒸馏）
    huashu-design.md              # 视觉设计规则（从 huashu-design 蒸馏）
    wechat-html-format.md         # 公众号 HTML 格式规范
```

## 设计理念

- **文章不是视频整理稿** — 禁止「视频里提到」「视频约 00:03」，禁止字幕腔和时间戳
- **单一 HTML 输出** — 不是一堆 md/txt 文件包，就是一个能复制的 HTML
- **默认纯文字** — 好文章不需要图片撑场面。用户要求配图时才做
- **配图三种模式** — 对比图 / 卡片网格 / 比喻插图（详见 `references/huashu-design.md`）

## 参考

本 skill 集成了 dontbesilent（dbs）文案方法论和花叔Design（huashu-design）视觉设计方法论。参考文件均为蒸馏后的操作指南，不是原文搬运。

## License

MIT
