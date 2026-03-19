[JimLiu/baoyu-skills](https://github.com/JimLiu/baoyu-skills)
# Baoyu Skills 技能列表

| # | 技能 | 描述 |
|---|---|---|
| [] | baoyu-article-illustrator | 分析文章结构，识别需要插图的位置，使用 Type × Style 二维方法生成插图。用于"为文章配图"、"添加图片"、"生成文章图片"等场景。 |
| [] | baoyu-comic | 知识漫画创建器，支持多种画风和基调。创建原创教育漫画，详细面板布局和顺序图像生成。用于创建"知识漫画"、"教育漫画"、"传记漫画"、"教程漫画"或"Logicomix 风格漫画"。 |
| [] | baoyu-compress-image | 将图片压缩为 WebP（默认）或 PNG，自动选择工具。用于"压缩图片"、"优化图片"、"转换为webp"或减少图片文件大小。 |
| [] | baoyu-cover-image | 生成文章封面图，支持 5 个维度（类型、配色、渲染、文字、情绪）、10 种配色和 7 种渲染风格。支持电影感 (2.35:1)、宽屏 (16:9) 和方形 (1:1) 比例。用于"生成封面图"、"创建文章封面"或"制作封面"。 |
| [] | baoyu-danger-gemini-web | 通过逆向工程 Gemini Web API 生成图像和文本。支持文本生成、图像生成、参考图像视觉输入和多轮对话。用于需要 Gemini 图像/文本生成后端或视觉 AI 功能的场景。需用户同意。 |
| [] | baoyu-danger-x-to-markdown | 将 X (Twitter) 推文和文章转换为 Markdown，带 YAML 前置内容。使用逆向工程 API，需用户同意。用于"X 转 markdown"、"推文转 markdown"、"保存推文"或提供 x.com/twitter.com URL 进行转换。 |
| ✅ | baoyu-format-markdown | 格式化纯文本或 Markdown 文件，添加前置内容、标题、摘要、标题、加粗、列表和代码块。用于"格式化 markdown"、"美化文章"、"添加格式"或改进文章布局。输出到 {filename}-formatted.md。 |
| [] | baoyu-image-gen | 支持 OpenAI、Google、OpenRouter、DashScope（阿里通义万象）、Jimeng（即梦）、Seedream（豆包）和 Replicate 等 API 的 AI 图像生成工具。支持文本到图像、参考图像、长宽比、批量生成。用于用户请求生成、创建或绘制图像的任何场景。 |
| [] | baoyu-infographic | 生成专业信息图，支持 21 种布局类型和 20 种视觉风格。分析内容，推荐布局×风格组合，生成出版级信息图。用于创建"信息图"、"可视化摘要"、"可视化"或"高密度信息大图"。 |
| ✅ | baoyu-markdown-to-html | 将 Markdown 转换为带样式的 HTML，支持微信兼容主题（default、grace、simple、modern）。支持代码高亮、数学公式、PlantUML、脚注、提示框、信息图，以及可选的外链底部引用。用于"markdown 转 html"、"转换 md 为 html"、"md转html"、"微信外链转底部引用"或需要从 Markdown 输出带样式的 HTML。 |
| [] | baoyu-post-to-wechat | 通过 API 或 Chrome CDP 发布内容到微信公众号。支持文章发布（HTML、Markdown 或纯文本输入）和图文发布（多图，最多 9 张）。Markdown 文章工作流默认将外链转为底部引用。用于"发布公众号"、"post to wechat"、"微信公众号"或"贴图/图文/文章"。 |
| [] | baoyu-post-to-weibo | 发布内容到微博。支持带文字、图片、视频的常规帖子，以及通过 Chrome CDP 的头条文章（Markdown 输入）。使用真实 Chrome 浏览器绕过反机器人检测。用于"发布微博"、"发微博"、"post to Weibo"、"分享到微博"或"微博头条文章"。 |
| [] | baoyu-post-to-x | 发布内容和文章到 X (Twitter)。支持带图片/视频的常规帖子、引用推文和 X Articles（长篇 Markdown）。使用真实 Chrome 和 CDP 绕过反自动化检测。用于"post to X"、"tweet"、"publish to Twitter"或"share on X"。 |
| [] | baoyu-slide-deck | 从内容生成专业幻灯片图像。创建带样式说明的大纲，然后生成单张幻灯片图像。支持 16 种预设风格（blueprint、chalkboard、corporate、minimal、sketch-notes 等）和自定义维度。用于"创建幻灯片"、"制作演示文稿"、"generate deck"、"slide deck"或"PPT"。 |
| ✅ | baoyu-translate | 在语言间翻译文章和文档，提供三种模式——快速（直接翻译）、普通（分析后翻译）、精细（分析、翻译、审查、润色）。通过 EXTEND.md 支持自定义术语表和术语一致性。用于"translate"、"翻译"、"精翻"、"translate article"、"translate to Chinese/English"、"改成中文"、"改成英文"或任何文档翻译需求。 |
| ✅ | baoyu-url-to-markdown | 通过 Chrome CDP 获取任意 URL 并转换为 Markdown。保存渲染后的 HTML 快照和 Markdown，使用升级版 Defuddle 流程（更好的 Web 组件处理和 YouTube 字幕提取），必要时自动回退到旧版 HTML-to-Markdown 流程。支持自动捕获和等待用户信号两种模式。用于将网页保存为 Markdown。 |
| [] | baoyu-xhs-images | 生成小红书信息图系列，支持 11 种视觉风格（cute、fresh、warm、bold、minimal、retro、pop、notion、chalkboard、study-notes、screen-print）和 8 种布局。将内容分解为 1-10 张卡通风格图像，优化小红书互动。用于"小红书图片"、"XHS images"、"RedNote infographics"、"小红书种草"或为中国平台制作社交媒体信息图。 |
