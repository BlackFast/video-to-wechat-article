---
name: video-to-wechat-article
description: Convert a local video into a single WeChat-ready HTML article. The article is an independent piece — not a video summary, not a transcript cleanup. No "视频里提到", no timestamps, no subtitle-speak. Output is one clean HTML file you copy-paste into the WeChat editor. Integrates dbs-style copywriting rules and huashu-design visual design patterns for cover images and inline illustrations. Use when the user asks to turn a video, recording, course clip, speech, or livestream replay into a 公众号 article.
---

# video-to-wechat-article

把一个视频改写成一篇可直接复制到公众号编辑器的独立成稿 HTML。

**核心定义：视频是原材料，文章是最终表达。** 输出的文章应该像一个独立创作的公众号文章，读者不需要知道、也不应该感觉到它来源于一个视频。

**你只交付一个文件：** `<video-name>-wechat.html`

**不做的事：** 自动发布到微信后台、生成视频复盘稿、生成素材整理稿。

## 最高优先级原则

### 文章是独立成稿，不是视频锚点

文章里**禁止**出现以下任何表述：

- 「视频里提到」「视频里说」「这个视频」
- 「视频约 00:03 提到」「在视频的开头」
- 「本文根据视频整理」「本视频说明」
- 「从这个视频可以看出」「视频中展示的」

也不要有：

- 字幕腔（短促、破碎、依赖画面才成立的句子）
- 时间戳引用
- 「以下是视频转写」式的结构

**应该怎么写：** 把视频里的观点、口气、信息密度，改写成一篇独立文章。就像一个作者在写公众号——他有自己的观点和表达，只是恰好和一个视频讲了同一件事。

### 单一 HTML 输出

用户最终只拿到一个文件：

```text
<video-name>-wechat.html
```

内部过程文件放到隐藏目录，不作为交付物：

```text
_work/
  audio.wav
  transcript.md
  keyframes/
  notes.md
```

## 脚本路径

所有脚本路径相对于本 SKILL.md 所在目录解析：

```bash
SKILL_DIR="<path-to-this-skill-folder>"
python3 "$SKILL_DIR/scripts/extract_audio.py" ...
python3 "$SKILL_DIR/scripts/extract_keyframes.py" ...
python3 "$SKILL_DIR/scripts/render_wechat_html.py" ...
```

不要假设 `python` 存在——用 `python3`。macOS 上即使装了 Python 3，`python` 也可能不在 PATH 里。

## 执行流程

### Step 1：确认输入

- 验证视频文件存在
- 创建工作目录 `_work/`（隐藏目录，不交付）

### Step 2：提取音频

```bash
python3 "$SKILL_DIR/scripts/extract_audio.py" input.mp4 --out _work/audio.wav
```

需要 ffmpeg。缺了会报清楚。

### Step 3：提取关键帧（辅助理解用）

```bash
python3 "$SKILL_DIR/scripts/extract_keyframes.py" input.mp4 --out _work/keyframes --interval 30
```

默认 30 秒间隔。关键帧只用于辅助理解视频内容（比如视频里有图表、演示、产品展示），不作为交付物。

### Step 4：转写

**自适应。** 按优先级选第一条可用的路：

1. 工作区已有转录工具 → 用它
2. 配了 `OPENAI_API_KEY` → Whisper API
3. 装了本地 Whisper → `whisper` CLI
4. 都没有 → 问用户提供 transcript 或批准装工具

输出：`_work/transcript.md`。不要硬编码某一家转录厂商。

### Step 5：理解内容

阅读 transcript，必要时参考 `_work/keyframes/` 里的帧来理解：
- 视频里展示的图表、数据、产品
- 说话人的表情和强调
- 演示的关键步骤

在 `_work/notes.md` 里记下：
- 核心观点（3-5 条）
- 关键数据或案例
- 说话人的语气特点（犀利/温和/幽默/严谨）
- 这篇文章的目标读者是谁

### Step 6：重写成文章

这是核心步骤。**先读 `references/dbs-copywriting.md`。** 然后基于 transcript 和 notes，写一篇独立成稿的公众号文章。

**结构：**

```text
标题
导语（摘要）
开头（冲突/误区/痛点/反常识引入）
核心内容（2-4 个小节，每节有小标题）
结尾（总结 + 轻 CTA）
```

**关键规则：**
- 口语转书面语（去填充词、去口误、去重复）
- 保留说话人独特的语气和风格——不要磨平
- 不确定的内容要标注，不要写成确信的事实
- 补充视频里假设读者知道但实际可能不知道的背景
- 用 `h2` 做小标题，用 `strong` 标重点句
- 段落要短，适合手机屏宽

### Step 7：生成 HTML

```bash
python3 "$SKILL_DIR/scripts/render_wechat_html.py" \
  --title "标题" \
  --digest "80-120 字的摘要" \
  --body article-body.md \
  --out output.html
```

或者 agent 直接手写 HTML——只要结构干净即可。详见 `references/wechat-html-format.md`。

### Step 8：设计封面和配图

**默认：纯文字 HTML，不配图。** 一篇好的公众号文章不需要图片撑场面。

如果用户要求配图，**不要只给封面文字的排版变体**——用户要的是跟文章内容对应的、各自独立的插图。

**先读 `references/huashu-design.md`**，里面有三个验证过的配图模式：

| 模式 | 适用场景 | 做法 |
|------|---------|------|
| 对比图 | 文章有 A vs B 的对比论点 | 左右分屏，左=错误/低效，右=正确/高效，中间分隔 |
| 卡片网格 | 文章提出收集/分类概念 | 色块卡片排成网格，最后一张虚线空卡 |
| 比喻插图 | 文章有强比喻 | CSS 几何形状构建场景，关键数字用 UI 元素呈现 |

**封面和配图是不同的事：**
- 封面：1 张，概括全文，信息流里抓注意力。可以给 3-4 个排版变体让用户选。
- 内文配图：2-4 张，每张对应一个具体观点或比喻，每张画面完全不同。

生成配图后，在 HTML 正文的对应位置插入配图占位块：

```html
<p><strong>配图：</strong>用 cover-design/illus-1-question-gap.html 的截图，插入此处。</p>
```

### Step 9：交付

最终只告诉用户一件事：

> 文章已生成：`<video-name>-wechat.html`
>
> 用浏览器打开，全选复制，粘贴到公众号编辑器即可。格式已适配。

## HTML 输出规范

详见 `references/wechat-html-format.md`。核心规则：

- 只用 `h1 h2 p blockquote strong section` 等基础标签
- 不用复杂 CSS、不用 JS、不用 div 堆叠
- 不用本地图片路径 `<img src="/Users/...">`
- 目标：复制到公众号编辑器后结构干净，不需要二次调整

## 质量检查（写入 HTML 前自检）

- 核心观点能不能一句话说清楚？
- 读者只扫小标题 + 粗体，能不能拿到 80% 的价值？
- 文章里有没有残留「视频里说」「视频约 xx 提到」？
- 开头是不是独立成立（读者不需要先看标题）？
- 有没有字幕腔？
- 不确定的论断有没有标注不确定？
- 配图占位块有没有用本地路径？

## 边界

- 不做微信后台登录
- 不调微信发布 API
- 不做浏览器自动化
- 不默认生成图片文件
- 转录自适应可用工具，不锁死一家

## 依赖

- **ffmpeg** — 音频提取和关键帧提取
- **Python 3** — 辅助脚本
- **转录工具** — 自适应（Whisper API / 本地 Whisper / 用户提供）

## 参考资料

- `references/dbs-copywriting.md` — 从 dbs 生态蒸馏的文案和内容质量规则
- `references/huashu-design.md` — 从 huashu-design 蒸馏的视觉和配图规则
- `references/wechat-html-format.md` — 公众号 HTML 格式规范
