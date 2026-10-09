# Journal Submission Adapter

一个面向 **Codex 等具备原生联网能力的 agent** 的投稿适配 skill。先研读目标期刊近期的同类全文，完成叙事与表达适配，复查内容，再按当前首投要求调整格式。

它不是自动改期刊名称的模板，也不是调用另一个 LLM 的批处理脚本。**选文、研读、科学判断和写作由当前 agent 完成**；附带脚本只处理已选全文的下载和 PDF 文本提取。

## 主要功能

1. **核查目标期刊**：确认准确刊名、文章类型、scope、官网要求和投稿入口，区分首投、返修与录用后要求。
2. **挑选近期相近研究**：通常研读 3–5 篇，优先近三个自然月，按主题、研究设计、原始数据贡献和证据深度选择；不足时明确扩大到半年或一年。
3. **保存并研读全文**：优先合法开放 PDF，可使用完整出版商 HTML 或已有下载 skill；阅读 Methods、Results、Discussion 和主要图注，不把摘要检索冒充全文研读。
4. **提炼写作规律**：逐篇记录问题定位、结果顺序、图件分工、摘要逻辑、句段节奏，并指出哪些写法适用、哪些依赖当前稿件没有的证据。
5. **适配整篇叙事**：优化标题、摘要、引言、结果结构、讨论和投稿信；允许调整故事讲述顺序，但不虚构实验、不把模型推断改写成因果证明。
6. **保护现有结果**：默认不重跑分析，保持数值、有效样本数、统计口径和数据来源。图件重排或需要新分析时，按用户授权范围处理。
7. **内容与附件同步复查**：检查正文、图像、图注、表格、补充文件的数字、名称、图号和引用是否一致，清理内部工作语气与占位内容。
8. **最后调整格式**：根据实时官网规则调整 Word 和引文格式；支持 Word MCP，已有 Zotero 活引文必须保留并通过其正确工作流处理。
9. **最小化投稿包**：只保留首投必需、适用的条件必需及支撑已报告结果的必要附件，不自动追加原始数据、审计报告或生产阶段材料。
10. **下载失败可交接**：给出准确标题、DOI、官方链接、失败原因和本地放置位置，由用户手动补充；其余可完成工作继续推进。

## 安装

真正的 skill 文件夹是：

```text
skills/journal-submission-adapter/
```

使用 Codex 自带的 `skill-installer`：

```text
请从 mingruiy270-debug/journal-submission-adapter-skill 安装
skills/journal-submission-adapter 到当前工作区的 skills 目录。
```

也可以将该文件夹完整复制到宿主会扫描的 `.agents/skills/` 或用户 skills 目录。不要把整个仓库当成一个 skill 复制，脚本和 references 必须随 skill 文件夹一起安装。安装后的可发现时间取决于宿主刷新方式；Codex 可在下一轮任务确认是否出现。

## 调用示例

```text
使用 $journal-submission-adapter。
目标期刊：Molecular Medicine；类型：Research article；阶段：首投。
稿件：/我的项目/Manuscript.docx。
图表和补充材料：/我的项目/附件/。
输出：/我的项目/投稿包/MM/。
优先近三个月的相近研究，下载并研读全文；不新增分析或实验。
先重整叙事，再复查，并用 Word MCP 适配格式，保留 Zotero 活引文。
投稿文件能少则少；缺失的必需事实请询问我。
```

其他刊物无需更换代码，也不需要维护一份静态期刊参数表。每次运行都由 agent 核查该刊当前要求。

## 环境与工具

| 能力 | 依赖 |
| --- | --- |
| 核心检索、研读、叙事适配 | agent 原生联网、网页阅读和文件访问 |
| 明确 URL 的全文下载 | Python 3.10+，默认标准库；可选 requests 传输，支持 HTTP/HTTPS 代理 |
| PDF 分页文本提取 | 可选 PyMuPDF，见 `requirements-reading.txt` |
| DOCX 操作 | 推荐 Word MCP；用户要求 MCP 或含 Zotero 活引文时必须使用 |
| 活引文新增/刷新/样式转换 | Word、Zotero、已连接的 Word MCP 及相应 Zotero skill |
| 文献元数据及机构授权下载 | 可选文献 MCP / 检索或下载 skill |

Word MCP、Zotero 和文献服务不是本仓库内置服务器。agent 应发现当前环境的实际工具，不能把“安装了包”当成“已成功连接”。Word MCP 缺失时，文献工作可以继续，需明确 Word 分支尚未完成。

## 可选文件工具

把 `assets/articles.example.json` 复制到**工作目录而非投稿上传目录**，由 agent 填写已经核实的选文信息及全文 URL：

```bash
python skills/journal-submission-adapter/scripts/acquire_fulltext.py --manifest /work/articles.json --out /work/papers --report /work/download_report.json
python skills/journal-submission-adapter/scripts/extract_pdf.py /work/papers/P01.pdf --out /work/readings/P01.txt
```

安装后的路径是实际 skill 目录下的 `scripts/`。下载脚本不会检索、破解访问限制或自动扩大下载范围；最多处理清单内 20 篇，正常任务通常只需 3–5 篇。它检查传输与文件类型，并不证明文章身份或内容已经读过。

遇到正常 HTTP 客户端兼容性问题时，可安装 `skills/journal-submission-adapter/requirements-network.txt`，显式选择 `--transport requests`。不会自动切换或循环重试，也不会绕过登录、验证码或付费墙。两种传输都保留大小上限、伪 PDF 拒绝和已有文件保护。大 PDF 可明确调整 `--max-mb`（最大 100），不扩大选文范围。

两个客户端均最多跟随五次普通重定向，逐跳验证地址并关闭中间响应，不自动读入重定向正文。Word MCP 接口缺少打开/关闭工具时，可用限定到目标文件的原生生命周期桥接；编辑、排版和保存仍走 MCP。重复搜索位置不能被当作完整搜索结果。

在线先发表页面即使标注 OA/full access，也可能只有摘要；需读取其 PDF 正文。期刊适配还会核对最新作者修改稿，以及目标期刊规定的准确摘要章节，不能沿用旧工作区或其他刊物模板。

退出码：下载 `0` 表示所有请求均保存成功，`2` 表示有人工补充或已有未检查文件，`1` 表示输入/执行错误。提取 `2` 表示存在低文本页，需检查页面或 OCR。已有文件不覆盖。

## 建议的任务输出

```text
目标期刊工作区/
  working/       官网要求、选文记录、阅读卡、适配说明和复查记录
  papers/        下载的比较论文，仅本地研读
  manuscript/    可编辑的派生主稿与投稿信
  upload/        实际首投文件，不放内部记录或比较论文
```

支持用户已有目录结构，不强制新建大量表格。期刊文件清单依实时要求生成，不预设所有期刊都必须上传湿实验原始数据、checklist 或单独图片。

## 测试

```bash
python -m unittest discover -s tests -v
```

标准库下载测试覆盖伪 PDF、HTML、拒绝访问、大小限制、已有文件保护、清单路径安全和查询参数不进入报告。安装 PyMuPDF 后还会测试实际 PDF 解析、页码定位、低文本页识别和本机 HTTP 下载至文本提取的端到端流程。可选依赖清单也放在 skill 内，单独安装 skill 后仍可使用。独立 agent 的行为测试方法见 [tests/behavioral_cases.md](tests/behavioral_cases.md)。

本 skill 不保证送审或录用，也不能通过语言调整解决真实科学矛盾。它会把“已完成适配”“必需信息尚缺”“科学口径仍未解决”分别报告。

当前 1.0.1 的验证范围见 [docs/validation.md](docs/validation.md)：29 项本机测试通过；真实稿件已完成一次 Cell & Bioscience 适配，下载并研读三篇近期全文，通过 Word MCP 修改派生稿与投稿信，保留全部 70 个引文字段和书目字段。未执行实际投稿，也未测试引文新增、重排或 Zotero Refresh。公开仓库不包含这次真实稿件或全文论文。

## 开源与参考

MIT 许可。公开仓库只含通用指令、工具、文档及虚拟测试材料，不包含作者稿件、下载论文或审稿访问凭据。

设计时参考了 [OpenAI skills](https://github.com/openai/skills)、[K-Dense Scientific Agent Skills](https://github.com/K-Dense-AI/scientific-agent-skills) 的相关公开项目，以及本地 Word/Zotero 与文献工具的接口经验。没有复制或打包这些项目的源码；来源与取舍见 [docs/design-sources.md](docs/design-sources.md)。
