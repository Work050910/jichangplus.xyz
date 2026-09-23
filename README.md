# JichangPlus 机场加 (jichangplus.xyz)

JichangPlus 机场加是一个面向已有基础、希望持续提升使用体验的中文读者的纯静态白底长文系列教程站。技术栈基于 **Hugo Extended + Clean White** 设计规范，同时配备了零外部依赖的 Python 自动化构建与 45+ 项全量 SEO 验收引擎。

---

## 1. 核心定位与结构特征

- **规范域名**: `https://jichangplus.xyz`
- **品牌名称**: JichangPlus 机场加
- **设计风格**: Clean White 极简白底长文风格，无干扰阅读排版，针对中文长文阅读优化正文宽度、行距与字阶。
- **系列架构**: 涵盖 5 大系列（订阅管理、多设备使用、流量与节点、客户端技巧、安全习惯），共收录 78+ 篇深度长文（正文净中文字符严格控制在 800~1200 字之间）。
- **常见问题**: 100 个 AI 生成不重复长尾问答，严格匹配 9 大配额（18, 14, 10, 10, 8, 14, 10, 8, 8），提供 5 页独立可抓取分页卡片。
- **服务测评**: 27 个服务商独立规范测评落地页，严格维护前四名主推顺序（全球云 1, 飞猫云 2, 暮光加速 3, 微风网络 4）及原始邀请链接。
- **单一配置层**: 核心关键词、导航、Hero 与页脚定义均收敛于 `data/site-seo-profile.json`，支持后续整体批量替换。

---

## 2. 快速开始与本地运行

环境要求：`Python 3.8+`（环境自带，无需额外安装任何第三方库）或 `Hugo Extended`。

### 本地构建 (Build)
```bash
python3 scripts/build.py
```
*该命令将解析 `content/` 与 `data/`，在 `public/` 目录下生成包含所有 HTML、CSS、JS、Sitemap、Robots 与 RSS 的纯静态产物。*

### 本地预览 (Serve)
```bash
python3 scripts/serve.py 1313
```
*启动后在浏览器中访问 [http://localhost:1313](http://localhost:1313) 即可实时查阅完整网站。*

### 自动化质量与 SEO 验收 (Validate)
```bash
python3 scripts/validate.py
```
*执行 45+ 项质量指标测试，包括 H1 唯一性、Canonical 绝对地址、800~1200 字符数审计、主推顺序核验、100 FAQ 配额与参考发布者黑名单全量扫描拦截。*

---

## 3. 目录结构概览

```text
jichangplus.xyz/
├── config.toml                  # 标准 Hugo 配置文件
├── AGENTS.md                    # 代理与协作约定
├── README.md                    # 项目完整维护文档
├── data/
│   ├── site-seo-profile.json    # 单一 SEO 配置层（活动关键词、导航、配额）
│   ├── providers.json           # 27 个服务商结构化数据源
│   └── faq.json                 # 100 个长尾 FAQ 数据源
├── docs/                        # 运营文档、矩阵与合约
│   ├── site-seo-profile.json    # 配置层镜像
│   ├── seo-profile-replacement-contract.md  # 关键词替换契约
│   ├── reference-publisher-blocklist.md    # 内部隔离黑名单
│   ├── keyword-map.md           # 关键词聚类说明
│   ├── keyword-coverage.csv     # 关键词覆盖审计表
│   ├── cross-site-content-ledger.md        # 跨站防内耗账本
│   ├── navigation-content-matrix.md        # 导航文章矩阵
│   ├── faq-keywords-100.csv     # 100 FAQ 清单
│   ├── faq-content-matrix.md    # 100 FAQ 矩阵
│   ├── provider-review-matrix.md           # 27 服务测评矩阵
│   └── content-plan.md          # 长期内容规划
├── content/                     # Markdown 源内容（78+ 长文 + 27 测评 + 信任合规页）
├── layouts/                     # Hugo 模板与 Partial 组件
├── static/                      # CSS、JS、Favicon 原生静态资源
├── scripts/
│   ├── build.py                 # 零依赖静态生成器
│   ├── validate.py              # 45+ 项自动化验收脚本
│   └── serve.py                 # 本地轻量预览服务器
└── public/                      # 最终生产纯静态输出产物
```

---

## 4. 核心维护与替换操作指南

### 如何新增文章
1. 在 `content/{section}/` 下新建 Markdown 文件；
2. 填写 Frontmatter（`title`, `description`, `primaryKeyword`, `series`, `seriesPart` 等）；
3. 正文净中文字符保持在 800 至 1200 字之间；
4. 运行 `python3 scripts/build.py && python3 scripts/validate.py` 验证。

### 如何更新服务商价格与优惠码
1. 编辑 `data/providers.json` 对应条目的 `priceFrom`, `coupon`, `lastChecked` 字段；
2. 保持前四名对象不动；
3. 执行构建与验收脚本完成全站同步。

### 如何批量替换全站 SEO 关键词
参考 `docs/seo-profile-replacement-contract.md`：只需更新 `data/site-seo-profile.json`，再执行构建，Hero、页脚、Header、meta、栏目落地页将自动全量更新，无需手动逐个文件修改。

---

## 5. 部署说明

- **Cloudflare Pages / Vercel / GitHub Pages**:
  - 构建命令：`python3 scripts/build.py`
  - 发布目录：`public`
- **Nginx 部署**:
  - 直接将 `public/` 目录下全部内容同步到 Web 根目录即可。
