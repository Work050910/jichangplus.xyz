import os, sys, json, shutil, re
from datetime import datetime

DOMAIN = "https://jichangplus.xyz"
SITE_TITLE = "JichangPlus 机场加｜机场使用技巧与进阶管理教程"
BRAND = "JichangPlus 机场加"
TG_CHANNEL = "https://t.me/+96hrQEFzuPQ5NjQ1"

with open("data/site-seo-profile.json", "r", encoding="utf-8") as f:
  profile = json.load(f)

with open("data/providers.json", "r", encoding="utf-8") as f:
  providers = json.load(f)

with open("data/faq.json", "r", encoding="utf-8") as f:
  faqs = json.load(f)

if os.path.exists("public"):
  shutil.rmtree("public")
os.makedirs("public/css", exist_ok=True)
os.makedirs("public/js", exist_ok=True)
os.makedirs("public/images", exist_ok=True)

shutil.copy("static/css/cleanwhite.css", "public/css/cleanwhite.css")
shutil.copy("static/js/main.js", "public/js/main.js")
shutil.copy("static/favicon.svg", "public/favicon.svg")
if os.path.exists("static/favicon.png"):
  shutil.copy("static/favicon.png", "public/favicon.png")
if os.path.exists("static/images"):
  for item in os.listdir("static/images"):
    s = os.path.join("static/images", item)
    d = os.path.join("public/images", item)
    if os.path.isfile(s):
      shutil.copy(s, d)

all_urls = []
search_index = []

def wrap_html(title, desc, canonical, h1, body_content, breadcrumbs=None, json_ld=None):
  bc_html = ""
  if breadcrumbs:
    bc_items = "".join([f"<li><a href=\"{u}\">{t}</a></li>" if u else f"<li>{t}</li>" for t, u in breadcrumbs])
    bc_html = f"<div class=\"breadcrumbs-bar\"><div class=\"container\"><ul class=\"breadcrumbs-list\">{bc_items}</ul></div></div>"

  schema_script = ""
  if json_ld:
    schema_script = f"<script type=\"application/ld+json\">\n{json.dumps(json_ld, ensure_ascii=False, indent=2)}\n</script>"

  return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <link rel="canonical" href="{canonical}">
  <meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:site_name" content="{BRAND}">
  <meta property="og:type" content="article">
  <meta property="og:locale" content="zh_CN">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="icon" type="image/png" sizes="32x32" href="/favicon.png">
  <link rel="icon" type="image/svg+xml" href="/favicon.svg">
  <link rel="apple-touch-icon" sizes="192x192" href="/images/icon-192.png">
  <link rel="alternate" type="application/rss+xml" title="{BRAND} RSS" href="/rss.xml">
  <link rel="stylesheet" href="/css/cleanwhite.css?v=20260929v2">
  <script defer src="/js/main.js?v=20260929v2"></script>
  {schema_script}
</head>
<body>
  <header class="site-header">
    <div class="container">
      <div class="header-top">
        <div class="site-brand">
          <a href="/" class="brand-link" style="display:inline-flex; align-items:center; gap:8px;">
            <img src="/favicon.png" alt="JichangPlus Logo" width="28" height="28" style="border-radius:6px; box-shadow:0 1px 3px rgba(0,0,0,0.1);">
            {BRAND}
          </a>
          <span class="site-tagline">机场使用技巧与进阶管理教程</span>
        </div>
        <div class="header-actions">
          <div class="header-search">
            <input type="search" id="site-search-input" class="search-input" placeholder="搜索文章/技巧..." autocomplete="off">
            <div id="search-results" class="search-dropdown"></div>
          </div>
          <a href="/service/" class="header-cta-btn">机场服务说明</a>
          <button class="menu-toggle" aria-expanded="false" aria-label="切换主导航菜单">☰ 菜单</button>
        </div>
      </div>
      <nav class="main-nav" aria-label="全站主导航">
        <ul class="nav-list">
          <li><a href="/" class="nav-link">首页</a></li>
          <li><a href="/recommend/" class="nav-link">机场推荐</a></li>
          <li><a href="/service/" class="nav-link">机场服务说明</a></li>
          <li><a href="/client-tips/" class="nav-link">客户端技巧</a></li>
          <li><a href="/faq/" class="nav-link">常见问题</a></li>
          <li><a href="/about/" class="nav-link">关于本站</a></li>
        </ul>
      </nav>
    </div>
  </header>

  {bc_html}

  <main id="main-content">
    {body_content}
  </main>

  <footer class="site-footer">
    <div class="container">
      <div class="footer-top">
        <div class="footer-brand-col">
          <div class="footer-col-title">{BRAND} (jichangplus.xyz)</div>
          <p class="footer-brand-desc">
            本站专注当前年份性价比机场推荐、便宜机场与稳定机场选择，系统覆盖 Clash 机场推荐、机场节点管理、机场订阅与多设备使用进阶教程。持续追踪高展现专线机场、流量规划与使用习惯，为注重效率与安全的用户提供可靠参考。
          </p>
          <p class="footer-compliance-text">
            本站所有技术分享仅限网络正常交流与优化参考，请遵守所在国家和地区法律法规。服务数据包含最后核验时间，具体套餐与价格以各服务商当前结算页为准。官方交流频道：<a href="{TG_CHANNEL}" target="_blank" rel="noopener nofollow">Telegram 频道</a>。
          </p>
        </div>
        <div class="footer-nav-col">
          <div class="footer-col-title">进阶专题</div>
          <ul class="footer-links">
            <li><a href="/recommend/">精选机场推荐</a></li>
            <li><a href="/service/">机场服务说明</a></li>
            <li><a href="/client-tips/">客户端进阶技巧</a></li>
            <li><a href="/faq/">常见问题解答</a></li>
          </ul>
        </div>
        <div class="footer-legal-col">
          <div class="footer-col-title">关于与合规</div>
          <ul class="footer-links">
            <li><a href="/about/">关于 JichangPlus</a></li>
            <li><a href="/contact/">联系我们与纠错</a></li>
            <li><a href="/editorial-policy/">编辑原则</a></li>
            <li><a href="/methodology/">评测与核验方法</a></li>
            <li><a href="/affiliate-disclosure/">邀请与合作披露</a></li>
            <li><a href="/privacy/">隐私政策</a></li>
            <li><a href="/disclaimer/">免责声明</a></li>
            <li><a href="/sitemap.xml">站点地图 (Sitemap)</a></li>
          </ul>
        </div>
      </div>
      <div class="footer-bottom">
        <div>© 2026 {BRAND} (jichangplus.xyz). 保留所有权利。交流频道：<a href="{TG_CHANNEL}" target="_blank" rel="noopener nofollow">TG频道</a></div>
        <div>技术框架：Hugo Extended + Clean White 纯静态白底长文架构</div>
      </div>
    </div>
  </footer>
</body>
</html>"""

def write_page(rel_path, html_str):
  full_path = os.path.join("public", rel_path)
  os.makedirs(os.path.dirname(full_path), exist_ok=True)
  with open(full_path, "w", encoding="utf-8") as f:
    f.write(html_str)
  if rel_path.endswith("index.html"): 
    u = DOMAIN + "/" + rel_path[:-10]
    if u.endswith("//"): u = u[:-1]
    all_urls.append(u)

def format_inline_md(text):
  def repl_link(m):
    t, u = m.group(1), m.group(2)
    if u.startswith("http") and "jichangplus.xyz" not in u and "localhost" not in u:
      return f'<a href="{u}" target="_blank" rel="sponsored nofollow noopener" style="color:#2563eb; font-weight:600;">{t}</a>'
    return f'<a href="{u}">{t}</a>'
  res = re.sub(r"\[([^\]]+)\]\(([^\)]+)\)", repl_link, text)
  res = re.sub(r"\*\*([^\*]+)\*\*", r"<strong>\1</strong>", res)
  return res

def slugify_heading(h_text):
  clean = re.sub(r"[^\w\u4e00-\u9fff]+", "-", h_text).strip("-").lower()
  return clean if clean else "sec"

def md_to_html(md_text, return_headings=False):
  lines = md_text.strip().split("\n")
  html_lines = []
  in_ul = False
  in_ol = False
  headings = []
  h_counter = 0
  
  for line in lines:
    line_s = line.strip()
    if not line_s:
      if in_ul: html_lines.append("</ul>"); in_ul = False
      if in_ol: html_lines.append("</ol>"); in_ol = False
      continue
    
    if line_s.startswith("### "):
      if in_ul: html_lines.append("</ul>"); in_ul = False
      if in_ol: html_lines.append("</ol>"); in_ol = False
      raw_h = line_s[4:].strip()
      h_counter += 1
      hid = f"airport-{slugify_heading(raw_h)}" if re.match(r"^\d+\.", raw_h) else f"h3-{h_counter}-{slugify_heading(raw_h)}"
      headings.append((3, raw_h, hid))
      html_lines.append(f'<h3 id="{hid}">{format_inline_md(raw_h)}</h3>')
    elif line_s.startswith("## "):
      if in_ul: html_lines.append("</ul>"); in_ul = False
      if in_ol: html_lines.append("</ol>"); in_ol = False
      raw_h = line_s[3:].strip()
      h_counter += 1
      hid = f"sec-{h_counter}-{slugify_heading(raw_h)}"
      headings.append((2, raw_h, hid))
      html_lines.append(f'<h2 id="{hid}">{format_inline_md(raw_h)}</h2>')
    elif line_s.startswith("- "):
      if not in_ul:
        if in_ol: html_lines.append("</ol>"); in_ol = False
        html_lines.append("<ul>"); in_ul = True
      item_text = line_s[2:]
      html_lines.append(f"<li>{format_inline_md(item_text)}</li>")
    elif re.match(r"^\d+\.\s", line_s):
      if not in_ol:
        if in_ul: html_lines.append("</ul>"); in_ul = False
        html_lines.append("<ol>"); in_ol = True
      item_text = re.sub(r"^\d+\.\s*", "", line_s)
      html_lines.append(f"<li>{format_inline_md(item_text)}</li>")
    elif line_s.startswith("<div") or line_s.startswith("</div") or line_s.startswith("<h4") or line_s.startswith("<a") or line_s.startswith("<p"):
      if in_ul: html_lines.append("</ul>"); in_ul = False
      if in_ol: html_lines.append("</ol>"); in_ol = False
      html_lines.append(line_s)
    else:
      if in_ul: html_lines.append("</ul>"); in_ul = False
      if in_ol: html_lines.append("</ol>"); in_ol = False
      html_lines.append(f"<p>{format_inline_md(line_s)}</p>")

  if in_ul: html_lines.append("</ul>")
  if in_ol: html_lines.append("</ol>")
  
  if return_headings:
    return "\n".join(html_lines), headings
  return "\n".join(html_lines)

def build_right_sidebar(headings, sec_dir="", page_type=""):
  if not headings:
    return ""
  
  airport_items = [h for h in headings if h[0] == 3 and re.match(r"^\d+\.", h[1])]
  if len(airport_items) >= 4:
    sidebar_title = "✈️ 机场导航目录"
    badge_text = f"{len(airport_items)} 家"
  else:
    sidebar_title = "📑 本文目录导航"
    badge_text = f"{len(headings)} 节"
  
  items_html = ""
  for level, text, hid in headings:
    clean_text = re.sub(r"\*\*([^\*]+)\*\*", r"\1", text)
    level_class = "toc-level-2" if level == 2 else "toc-level-3"
    items_html += f'<li class="sidebar-nav-item {level_class}"><a href="#{hid}" class="sidebar-nav-link" data-target="{hid}" title="{clean_text}">{clean_text}</a></li>\n'
    
  return f"""<aside class="article-sidebar-right" aria-label="文章侧边栏导航">
    <div class="sidebar-sticky-box">
      <div class="sidebar-toc-header">
        <span>{sidebar_title}</span>
        <span class="sidebar-badge">{badge_text}</span>
      </div>
      <nav class="sidebar-toc-nav">
        <ul class="sidebar-nav-list">
          {items_html}
        </ul>
      </nav>
      <div class="sidebar-quick-top">
        <a href="#main-content" class="sidebar-back-top">⬆️ 返回顶部</a>
      </div>
    </div>
  </aside>"""

# Helper: Prominent 4-provider highlight box for articles
def render_prominent_four_box():
  return f"""<div class="featured-providers-box">
  <div class="featured-providers-title">🏆 核心推荐服务：按需选择 4 个主推方案</div>
  <div class="featured-providers-subtitle">本站严格区分以下 4 家核心服务的定位差异，请根据日常场景与设备预算选择</div>
  <div class="featured-four-grid">
    <div class="featured-item p1">
      <div class="featured-item-header">
        <span class="featured-badge">首要推荐 #1</span>
        <div class="featured-name">全球云 (Quanqiu)</div>
      </div>
      <div class="featured-price">20 元/月 起</div>
      <div class="featured-positioning">多地区专线 · 团队主力首选</div>
      <div class="featured-desc">涵盖丰富国家出口，智能分流及稳定低延迟专线，适合跨境商务、多端协作与生产环境。</div>
      <div style="margin-bottom: 12px; font-size: 0.8rem; background: #eff6ff; padding: 4px 8px; border-radius: 4px;">
        优惠码: <strong>qq88</strong>（8折优惠）
      </div>
      <a href="https://hueue09.gcvipaff.com/#/?code=z8U9aaa4" target="_blank" rel="sponsored nofollow noopener" class="btn-reg-prominent">👉 官网注册 / 查看当前套餐</a>
      <a href="/providers/quanqiu-cloud/" class="featured-link-sub">查阅独立测评报告</a>
    </div>

    <div class="featured-item p2">
      <div class="featured-item-header">
        <span class="featured-badge">第二推荐 #2</span>
        <div class="featured-name">飞猫云 (Flycat)</div>
      </div>
      <div class="featured-price">折合 7 元/月 (84元/年)</div>
      <div class="featured-positioning">高性价比 · 轻量备用神器</div>
      <div class="featured-desc">IEPL 专线保障，小流量年付极具价格优势，自研客户端与多设备家庭分享非常省心。</div>
      <div style="margin-bottom: 12px; font-size: 0.8rem; background: #f0fdf4; padding: 4px 8px; border-radius: 4px;">
        优惠码: <strong>flycat888</strong>（季付及以上8折）
      </div>
      <a href="https://quanqiu.flycatvipaff.cc/#/?code=7ZOeVmNS" target="_blank" rel="sponsored nofollow noopener" class="btn-reg-prominent">👉 官网注册 / 查看当前套餐</a>
      <a href="/providers/flycat-cloud/" class="featured-link-sub">查阅独立测评报告</a>
    </div>

    <div class="featured-item p3">
      <div class="featured-item-header">
        <span class="featured-badge">第三推荐 #3</span>
        <div class="featured-name">暮光加速 (Twilight)</div>
      </div>
      <div class="featured-price">20 元/月 起</div>
      <div class="featured-positioning">晚高峰多媒体 · 高速大流量</div>
      <div class="featured-desc">充足晚高峰带宽冗余，流媒体与多任务下载专线优化，适合对高清影音体验要求高的用户。</div>
      <div style="margin-bottom: 12px; font-size: 0.8rem; background: #faf5ff; padding: 4px 8px; border-radius: 4px;">
        优惠码: <strong>mm88</strong>（8折优惠）
      </div>
      <a href="https://quanqi12.twilightaff.com/#/?code=beAVqNPf" target="_blank" rel="sponsored nofollow noopener" class="btn-reg-prominent">👉 官网注册 / 查看当前套餐</a>
      <a href="/providers/twilight/" class="featured-link-sub">查阅独立测评报告</a>
    </div>

    <div class="featured-item p4">
      <div class="featured-item-header">
        <span class="featured-badge">第四推荐 #4</span>
        <div class="featured-name">微风网络 (BreezeNet)</div>
      </div>
      <div class="featured-price">18 元/月 · 100GB</div>
      <div class="featured-positioning">轻量年付 · 预算敏感型</div>
      <div class="featured-desc">自研客户端与第三方订阅无缝导入，价格亲民，适合低频出差与轻度日常浏览。</div>
      <div style="margin-bottom: 12px; font-size: 0.8rem; background: #fff7ed; padding: 4px 8px; border-radius: 4px;">
        优惠码: <strong>wf88</strong> (专属优惠)
      </div>
      <a href="https://edp01.breezenetaff.com/#/?code=vxDUI8kY" target="_blank" rel="sponsored nofollow noopener" class="btn-reg-prominent">👉 官网注册 / 查看当前套餐</a>
      <a href="/providers/breezenet/" class="featured-link-sub">查阅独立测评报告</a>
    </div>
  </div>
</div>"""

# --- 1. HOMEPAGE ---
hero_text = (
  "当前年份最新性价比机场推荐、便宜机场与稳定机场选择指南。JichangPlus 机场加系统涵盖 Clash 机场推荐、机场节点管理、"
  "机场订阅管理与多设备使用系列教程。持续注入专线机场测速、多端协同与安全使用技巧，深入探讨机场订阅多久更新一次、"
  "机场流量怎么合理分配与多台设备如何管理机场订阅，帮助建立清晰有条理的高速网络工具使用规范与避坑清单。"
)

top4_cards = ""
for p in providers[:4]:
  top4_cards += f"""<div class="provider-card primary-rank rank-{p['rank']}">
    <div class="provider-card-header">
      <span class="provider-rank-badge">推荐 #{p['rank']}</span>
      <h3 class="provider-name">{p['name']}</h3>
    </div>
    <div class="provider-price-row" style="display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 12px;">
      <div class="provider-price" style="font-size: 1.25rem; font-weight: 800; color: #e11d48; white-space: nowrap;">{p['priceFrom']}</div>
      <div class="provider-traffic" style="font-size: 0.84rem; color: #64748b; white-space: nowrap;">流量基准：{p['trafficFrom']}</div>
    </div>
    <div class="provider-summary">{p['summary']}</div>
    <div class="provider-coupon-box">
      <span>优惠码: <strong class="coupon-code">{p['coupon']}</strong></span>
      <button class="coupon-copy-btn" data-coupon="{p['coupon']}">复制</button>
    </div>
    <div class="provider-actions" style="display: flex; flex-direction: row; gap: 8px; align-items: center; width: 100%; margin-top: 14px;">
      <a href="/providers/{p['slug']}/" class="btn-detail" title="查看 {p['name']} 独立测评" style="flex: 1 1 50%; display: inline-flex; align-items: center; justify-content: center; text-align: center; padding: 8px 4px; background: #f8fafc; color: #334155; border: 1px solid #cbd5e1; font-size: 0.85rem; font-weight: 600; border-radius: 6px; text-decoration: none; white-space: nowrap;">查看测评</a>
      <a href="{p['inviteURL']}" target="_blank" rel="sponsored nofollow noopener" class="btn-reg-prominent" title="前往 {p['name']} 官网注册" style="flex: 1 1 50%; display: inline-flex; align-items: center; justify-content: center; text-align: center; padding: 8px 4px; background: #ffffff !important; color: #000000 !important; border: 1px solid #cbd5e1 !important; font-size: 0.85rem; font-weight: 700; border-radius: 6px; text-decoration: none; white-space: nowrap; box-shadow: 0 1px 2px rgba(0,0,0,0.06);">官网注册</a>
    </div>
    <div class="provider-meta-footer">核验时间：{p['lastChecked']}</div>
  </div>"""

table_rows = ""
for p in providers[:12]:
  table_rows += f"""<tr>
    <td><strong>#{p['rank']} {p['name']}</strong></td>
    <td>{p['priceFrom']}</td>
    <td>{p['trafficFrom']}</td>
    <td>{p['coupon']}</td>
    <td>{p['suitableFor']}</td>
    <td>{p['lastChecked']}</td>
    <td>
      <a href="/providers/{p['slug']}/">测评</a> | 
      <a href="{p['inviteURL']}" target="_blank" rel="sponsored nofollow noopener" style="font-weight:700; color:#2563eb;">官网注册</a>
    </td>
  </tr>"""

home_body = f"""<section class="hero-section">
  <div class="container">
    <span class="hero-badge">当前年份性价比机场推荐 · Clash 机场测评 · 节点测速与选择</span>
    <h1 class="hero-title">JichangPlus 机场加：让订阅、设备和日常使用更有条理</h1>
    <p class="hero-description">{hero_text}</p>
    <div class="hero-actions">
      <a href="/recommend/" class="btn-primary">查看当前精选机场推荐榜</a>
      <a href="/service/" class="btn-secondary">机场服务说明</a>
      <a href="/faq/" class="btn-secondary">查阅 100 常见问题解答</a>
    </div>
    <div class="hero-disclosure">披露说明：本站包含赞助邀请链接 (sponsored nofollow noopener)，所有排序与推荐依据真实核验记录与使用场景，价格以各结算页为准。</div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="section-header">
      <h2 class="section-title">核心推荐榜单：按使用场景匹配可靠方案</h2>
      <p class="section-desc">本站严格区分并固定前四名主推服务，涵盖多地区专线、7元月付小流量备用、晚高峰流媒体及自研轻量端。</p>
    </div>
    <div class="cards-grid">
      {top4_cards}
    </div>
  </div>
</section>

<section class="section" style="background: #fafafa;">
  <div class="container">
    <div class="section-header">
      <h2 class="section-title">性价比机场与主推服务特性快速对比表</h2>
      <p class="section-desc">前四名固定排在表格前四行，提供带核验日期的参考价格、优惠码与官网直达入口。</p>
    </div>
    <div class="table-responsive">
      <table class="data-table">
        <thead>
          <tr>
            <th>服务商</th>
            <th>参考起步价</th>
            <th>流量基准</th>
            <th>优惠码</th>
            <th>适用场景</th>
            <th>核验时间</th>
            <th>操作入口</th>
          </tr>
        </thead>
        <tbody>
          {table_rows}
        </tbody>
      </table>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="section-header">
      <h2 class="section-title">按需选择：不同场景下的进阶配置策略</h2>
      <p class="section-desc">结合预算、设备规模与网络需求，建立精准的订阅与节点规划。</p>
    </div>
    <div class="cards-grid">
      <div class="article-card">
        <h3 class="article-card-title"><a href="/recommend/">机场推荐精选指南</a></h3>
        <p class="article-card-summary">10 篇高点击率深度长文，全网 27 家主流机场全维度横向评测，含线路、价格与官网直达。</p>
      </div>
      <div class="article-card">
        <h3 class="article-card-title"><a href="/service/">机场服务说明</a></h3>
        <p class="article-card-summary">全网精选 23 家服务详细说明、节点配置、流媒体与 AI 解锁能力及官网直达通道。</p>
      </div>
      <div class="article-card">
        <h3 class="article-card-title"><a href="/client-tips/">客户端进阶技巧</a></h3>
        <p class="article-card-summary">16 篇规则进阶，深入 Clash Mixin 覆写、sing-box 独立出站与 TUN 模式调优。</p>
      </div>
    </div>
  </div>
</section>

<section class="section" style="background: #fafafa;">
  <div class="container">
    <div class="section-header">
      <h2 class="section-title">常见问题中心精选 (FAQ) - 全部已展开</h2>
      <p class="section-desc">精选日常高频提问，涵盖 9 大主题配额与 100 项长尾解答。</p>
    </div>
    <div class="faq-accordion">
      <details class="faq-item" open>
        <summary class="faq-question">【新手指南】新手如何根据日常需求挑选合适的机场套餐？</summary>
        <div class="faq-answer">
          <p>【建议】月付试用，勿直接长付。适用条件：常规日常网络维护与稳定进阶配置场景。操作要点：①首先检查当前订阅是否正常同步，并确认客户端核心版本；②进入系统设置核对DNS防泄漏状态与分流规则，排除本地网络干扰；③根据实际流量消耗与设备并发合理配置，避免多端挤占冲突。详细配置步骤与进阶技巧请参考本站【系列长文指南】。</p>
        </div>
      </details>
      <details class="faq-item" open>
        <summary class="faq-question">【Clash进阶】Clash 规则模式与全局模式有什么本质区别？</summary>
        <div class="faq-answer">
          <p>【建议】日常推荐规则分流，特定调试时使用全局。适用条件：常规日常网络维护与稳定进阶配置场景。操作要点：①首先检查当前订阅是否正常同步，并确认客户端核心版本；②进入系统设置核对DNS防泄漏状态与分流规则，排除本地网络干扰；③根据实际流量消耗与设备并发合理配置，避免多端挤占冲突。详细配置步骤与进阶技巧请参考本站【系列长文指南】。</p>
        </div>
      </details>
      <details class="faq-item" open>
        <summary class="faq-question">【流量管理】机场节点的倍率到底是什么意思？如何计算扣费？</summary>
        <div class="faq-answer">
          <p>【建议】实际扣除流量等于实际使用量乘以此倍率数值。适用条件：常规日常网络维护与稳定进阶配置场景。操作要点：①首先检查当前订阅是否正常同步，并确认客户端核心版本；②进入系统设置核对DNS防泄漏状态与分流规则，排除本地网络干扰；③根据实际流量消耗与设备并发合理配置，避免多端挤占冲突。详细配置步骤与进阶技巧请参考本站【系列长文指南】。</p>
        </div>
      </details>
    </div>
    <div style="text-align: center; margin-top: 30px;">
      <a href="/faq/" class="btn-primary">浏览全部 100 个已展开常见问题</a>
    </div>
  </div>
</section>
"""

home_schema = {
  "@context": "https://schema.org",
  "@type": "WebSite",
  "name": BRAND,
  "url": DOMAIN,
  "description": profile["siteTopic"]
}

write_page("index.html", wrap_html(SITE_TITLE, profile["siteTopic"], DOMAIN + "/", "JichangPlus 机场加：让订阅、设备和日常使用更有条理", home_body, json_ld=home_schema))

# --- 2. SECTION LANDING PAGES & EXPANDED ARTICLES ---
sections = [
  ("recommend", "机场推荐", "机场推荐与精选评测", 10),
  ("service", "机场服务说明", "机场服务说明与选型指南", 23),
  ("client-tips", "客户端技巧", "客户端使用技巧", 16)
]

prominent_box_html = render_prominent_four_box()

other_slugs_list = [
  'u1s1', 'jilian-cloud', 'guangnian-ti', 'guangsu-cloud', 'weitu-cloud',
  'yuzhou-cloud', 'sujie', 'sogo-cloud', 'kuaili', 'ermao-cloud',
  'yifan-cloud', 'edgenova', 'kexin-cloud', 'wavenet', 'laddercloud',
  'lingdong-cloud', 'yinxingren', 'flyv', 'wuyou-link', 'civet-net',
  'flashleap', 'firefly-net', 'kuajie-cloud'
]
other_provs = []
for oslg in other_slugs_list:
  op = next((p for p in providers if p['slug'] == oslg), None)
  if op: other_provs.append(op)

for sec_dir, sec_name, sec_kw, count in sections:
  nav_item = next(item for item in profile["navigationItems"] if sec_dir in item["url"])
  seeds = nav_item["articleSeeds"]
  
  cards_html = ""
  for s_idx, title in enumerate(seeds, 1):
    art_slug = f"{sec_dir}-part-{s_idx:02d}"
    art_file_peek = f"content/{sec_dir}/{art_slug}.md"
    card_words = "约 1500 字"
    card_summary = f"围绕【{sec_kw}】与性价比机场选择展开的步骤化深度长文，提供落地实操与防踩坑指南。"
    extra_action_html = ""
    
    if sec_dir == "recommend" and s_idx == 1:
      card_words = "约 6800 字（全网27家大盘点）"
      card_summary = "本专栏核心支柱长文：全网 27 家主流机场全维度横向评测档案，涵盖价格、专线节点、适用场景、解锁 AI 与流媒体能力及官网注册直达。"
    elif sec_dir == "service":
      p_obj = other_provs[s_idx - 1] if s_idx <= len(other_provs) else None
      p_name = p_obj["name"] if p_obj else title
      p_price = p_obj.get("priceFrom", "20 元/月") if p_obj else "详见官网"
      p_traffic = p_obj.get("trafficFrom", "100GB/月") if p_obj else ""
      p_coupon = p_obj.get("coupon", "暂无优惠码") if p_obj else "暂无"
      p_invite = p_obj["inviteURL"] if p_obj else "#"
      card_words = f"起步：{p_price}"
      card_summary = f"【{p_name}】详细服务说明与配置评测：入门价格 {p_price} · {p_traffic}，优惠码【{p_coupon}】。支持常用 AI 与海外 4K 流媒体解锁，包含节点覆盖与客户端配置实操。"
      extra_action_html = f'''<div style="margin-top: 14px; display: flex; gap: 10px; align-items: center;">
        <a href="{p_invite}" target="_blank" rel="sponsored nofollow noopener" class="btn-primary btn-reg-prominent" style="padding: 6px 14px; font-size: 13px; text-decoration: none; border-radius: 4px;">👉 官网注册</a>
        <a href="/{sec_dir}/{art_slug}/" class="btn-secondary" style="padding: 6px 14px; font-size: 13px; text-decoration: none; border-radius: 4px;">服务说明</a>
      </div>'''
    elif os.path.exists(art_file_peek):
      with open(art_file_peek, "r", encoding="utf-8") as f_peek:
        c_peek = f_peek.read()
      cn_p = len([c for c in c_peek if "一" <= c <= "鿿"])
      card_words = f"约 {cn_p} 字"
      m_desc = re.search(r'description:\s*["\']?([^"\']+)["\']?', c_peek)
      if m_desc:
        card_summary = m_desc.group(1).strip()

    badge_text = f"精选服务 {s_idx:02d}" if sec_dir == "service" else f"第 {s_idx} 篇"
    card_id_attr = f' id="airport-card-{s_idx:02d}"' if sec_dir == "service" else ""
    cards_html += f"""<div class="article-card"{card_id_attr}>
      <span class="article-card-badge">{badge_text}</span>
      <h3 class="article-card-title"><a href="/{sec_dir}/{art_slug}/">{title}</a></h3>
      <p class="article-card-summary">{card_summary}</p>
      <div class="article-card-meta">
        <span>更新：2026-09-28</span>
        <span>{card_words}</span>
      </div>
      {extra_action_html}
    </div>"""

  extra_box = prominent_box_html if sec_dir == "recommend" else ""
  if sec_dir == "service":
    sec_h1 = "机场服务说明"
    sec_lead = "收录全网主流精选 23 家机场服务详细说明、节点配置、流媒体与AI解锁能力、套餐资费及官方直达注册通道，助你全面掌握各服务商核心特性与适用场景。"

    service_sidebar_items = ""
    for s_idx, title in enumerate(seeds, 1):
      p_obj = other_provs[s_idx - 1] if s_idx <= len(other_provs) else None
      p_name = p_obj["name"] if p_obj else f"服务 {s_idx:02d}"
      service_sidebar_items += f'<li class="sidebar-nav-item"><a href="#airport-card-{s_idx:02d}" class="sidebar-nav-link" title="{s_idx:02d}. {p_name}">{s_idx:02d}. {p_name}</a></li>\n'
    
    service_sidebar_html = f"""<aside class="article-sidebar-right" aria-label="机场服务导航">
      <div class="sidebar-sticky-box">
        <div class="sidebar-toc-header">
          <span>✈️ 机场导航目录</span>
          <span class="sidebar-badge">{len(seeds)} 家</span>
        </div>
        <nav class="sidebar-toc-nav">
          <ul class="sidebar-nav-list">
            {service_sidebar_items}
          </ul>
        </nav>
        <div class="sidebar-quick-top">
          <a href="#main-content" class="sidebar-back-top">⬆️ 返回顶部</a>
        </div>
      </div>
    </aside>"""

    sec_content = f"""<section class="section">
      <div class="container">
        <div class="section-header">
          <h1 class="section-title">{sec_h1}</h1>
          <p class="section-desc">{sec_lead}</p>
        </div>
        <div class="article-layout" style="margin-top: 24px; padding: 0;">
          <div class="article-content-main">
            <div class="cards-grid">
              {cards_html}
            </div>
          </div>
          {service_sidebar_html}
        </div>
      </div>
    </section>"""
  elif sec_dir == "recommend":
    sec_h1 = f"{sec_name}精选指南与横向评测"
    sec_lead = f"本专栏系统收录 {len(seeds)} 篇高点击率深度长文，围绕性价比机场推荐、便宜机场、稳定专线、Clash 机场及多设备协同，提供落地实操与防踩坑选型指南。"
    sec_content = f"""<section class="section">
      <div class="container">
        <div class="section-header">
          <h1 class="section-title">{sec_h1}</h1>
          <p class="section-desc">{sec_lead}</p>
        </div>
        {extra_box}
        <div class="cards-grid" style="margin-top: 24px;">
          {cards_html}
        </div>
      </div>
    </section>"""
  else:
    sec_h1 = f"{sec_name}进阶系列教程"
    sec_lead = f"本专栏收录 {len(seeds)} 篇深度进阶长文，围绕“{sec_kw}”核心意图，系统建立条理分明的日常网络使用与管理体系。"
    sec_content = f"""<section class="section">
      <div class="container">
        <div class="section-header">
          <h1 class="section-title">{sec_h1}</h1>
          <p class="section-desc">{sec_lead}</p>
        </div>
        <div class="cards-grid" style="margin-top: 24px;">
          {cards_html}
        </div>
      </div>
    </section>"""

  sec_bc = [("首页", "/"), (sec_name, "")]
  write_page(f"{sec_dir}/index.html", wrap_html(f"{sec_name}｜{BRAND}", f"JichangPlus 机场加{sec_name}专栏，系统收录 {count} 篇进阶深度长文。", f"{DOMAIN}/{sec_dir}/", sec_h1, sec_content, breadcrumbs=sec_bc))

  for s_idx, title in enumerate(seeds, 1):
    art_slug = f"{sec_dir}-part-{s_idx:02d}"
    art_file = f"content/{sec_dir}/{art_slug}.md"
    with open(art_file, "r", encoding="utf-8") as f:
      raw = f.read()
    
    parts = re.split(r"^---\s*$", raw, maxsplit=2, flags=re.MULTILINE)
    content_raw = parts[2] if len(parts) > 2 else raw
    content_lines = [l for l in content_raw.split("\n") if not l.startswith("# ")]
    body_cn = len([c for c in content_raw if "一" <= c <= "鿿"])
    
    meta = {}
    if len(parts) > 2:
      for m_line in parts[1].strip().split("\n"):
        if ":" in m_line:
          mk, mv = m_line.split(":", 1)
          meta[mk.strip()] = mv.strip().strip('"').strip("'")
    
    art_desc = meta.get("description", f"深入探讨{title}，提供条理分明的专业进阶配置与选型指南。")
    art_kw = meta.get("primaryKeyword", title)
    art_tags = meta.get("tags", "")

    full_content_text = "\n".join(content_lines)
    rendered_body, article_headings = md_to_html(full_content_text, return_headings=True)
    right_sidebar_html = build_right_sidebar(article_headings, sec_dir=sec_dir)
    
    # Add to client search index
    search_index.append({
      "title": title,
      "desc": art_desc,
      "url": f"/{sec_dir}/{art_slug}/",
      "keywords": f"{art_kw} {sec_name} {title} {art_tags}"
    })

    art_page_html = f"""<article class="article-page">
      <div class="article-layout">
        <div class="article-content-main">
          <header class="article-header">
            <div class="article-category">{sec_name}专栏 · 深度指南</div>
            <h1 class="article-title">{title}</h1>
            <div class="article-meta">
              <span>作者：JichangPlus 编辑团队</span>
              <span>更新时间：2026-09-28</span>
              <span>字数：约 {body_cn} 字</span>
            </div>
          </header>

          <div class="series-box">
            <div class="series-box-title">所属专栏：{sec_name}（第 {s_idx} / {len(seeds)} 篇）</div>
            <div>本专栏汇总全网精选主流机场服务详细说明、节点配置、流媒体与AI解锁能力、套餐资费及官方直达注册通道。交流频道：<a href="{TG_CHANNEL}" target="_blank" rel="noopener nofollow">Telegram 频道</a>。</div>
          </div>

          <div class="article-body">
            {rendered_body}
            {prominent_box_html}
          </div>

          <div class="post-nav">
            <div class="post-nav-item">
              <div class="post-nav-label">所属专栏</div>
              <div class="post-nav-title"><a href="/{sec_dir}/">返回【{sec_name}】专栏目录</a></div>
            </div>
            <div class="post-nav-item" style="text-align: right;">
              <div class="post-nav-label">常见问题</div>
              <div class="post-nav-title"><a href="/faq/">查阅【常见问题】解答中心</a></div>
            </div>
          </div>
        </div>
        {right_sidebar_html}
      </div>
    </article>"""

    art_bc = [("首页", "/"), (sec_name, f"/{sec_dir}/"), (title, "")]
    art_ld = {
      "@context": "https://schema.org",
      "@type": "Article",
      "headline": title,
      "datePublished": "2026-09-23",
      "dateModified": "2026-09-23",
      "author": {"@type": "Organization", "name": BRAND},
      "publisher": {"@type": "Organization", "name": BRAND}
    }
    write_page(f"{sec_dir}/{art_slug}/index.html", wrap_html(f"{title}｜{BRAND}", art_desc, f"{DOMAIN}/{sec_dir}/{art_slug}/", title, art_page_html, breadcrumbs=art_bc, json_ld=art_ld))

# --- 3. PROVIDER REVIEW PAGES ---
prov_cards_all = ""
for p in providers:
  name = p["name"]
  slug = p["slug"]
  rank = p["rank"]
  price = p["priceFrom"]
  traffic = p["trafficFrom"]
  coupon = p["coupon"]
  invite = p["inviteURL"]
  last_checked = p["lastChecked"]
  
  with open(f"content/providers/{slug}.md", "r", encoding="utf-8") as f:
    raw = f.read()
  parts = re.split(r"^---\s*$", raw, maxsplit=2, flags=re.MULTILINE)
  content_raw = parts[2] if len(parts) > 2 else raw
  content_lines = [l for l in content_raw.split("\n") if not l.startswith("# ")]

  meta = {}
  if len(parts) > 2:
    for m_line in parts[1].strip().split("\n"):
      if ":" in m_line:
        mk, mv = m_line.split(":", 1)
        meta[mk.strip()] = mv.strip().strip('"').strip("'")
  
  prov_desc = meta.get("description", f"{name}怎么样？本篇详尽评测{name}的参考价格、套餐梯度、节点线路分布及购买前注意事项。")
  full_prov_content = "\n".join(content_lines)
  rendered_body, prov_headings = md_to_html(full_prov_content, return_headings=True)
  prov_sidebar_html = build_right_sidebar(prov_headings, page_type="provider")
  
  search_index.append({
    "title": f"{name}机场测评：价格、套餐、节点与适合人群",
    "desc": prov_desc,
    "url": f"/providers/{slug}/",
    "keywords": f"{name} {name}机场测评 {name}优惠码 {name}官网 {name}套餐"
  })

  prov_h1 = f"{name}机场测评：价格、套餐、节点与适合人群"
  prov_page_html = f"""<article class="article-page">
    <div class="article-layout">
      <div class="article-content-main">
        <header class="article-header">
          <div class="article-category">服务商测评库 · 推荐排名 #{rank}</div>
          <h1 class="article-title">{prov_h1}</h1>
          <div class="article-meta">
            <span>参考价格：{price}</span>
            <span>基准流量：{traffic}</span>
            <span>核验时间：{last_checked}</span>
            <span>官方频道：<a href="{TG_CHANNEL}" target="_blank" rel="noopener nofollow">Telegram 频道</a></span>
          </div>
        </header>

        <div class="article-body">
          {rendered_body}
          <div style="background:#eff6ff; border:2px solid #93c5fd; border-radius:10px; padding:24px; margin:36px 0; text-align:center;">
            <h3 style="margin-bottom:8px; font-weight:800; color:#1e40af;">前往 {name} 官方网站核验与注册</h3>
            <p style="font-size:0.9rem; color:#475569; margin-bottom:18px;">优惠码：<strong style="color:#2563eb;">{coupon}</strong> ｜ 核验日期：{last_checked} ｜ 请以当前结算页数据为准</p>
            <a href="{invite}" target="_blank" rel="sponsored nofollow noopener" class="btn-reg-prominent" style="max-width:320px; margin:0 auto; font-size:1.05rem;">👉 官网注册 / 查看当前套餐</a>
          </div>
          {prominent_box_html}
        </div>

        <div class="post-nav">
          <div class="post-nav-item">
            <div class="post-nav-label">服务总览</div>
            <div class="post-nav-title"><a href="/providers/">返回【服务资料库】目录</a></div>
          </div>
          <div class="post-nav-item" style="text-align: right;">
            <div class="post-nav-label">服务说明</div>
            <div class="post-nav-title"><a href="/service/">查看【机场服务说明】</a></div>
          </div>
        </div>
      </div>
      {prov_sidebar_html}
    </div>
  </article>"""

  prov_bc = [("首页", "/"), ("服务测评", "/providers/"), (name, "")]
  prov_ld = {
    "@context": "https://schema.org",
    "@type": "Article",
    "headline": prov_h1,
    "datePublished": "2026-09-23",
    "dateModified": "2026-09-23",
    "author": {"@type": "Organization", "name": BRAND}
  }
  write_page(f"providers/{slug}/index.html", wrap_html(f"{name}机场测评｜{BRAND}", prov_desc, f"{DOMAIN}/providers/{slug}/", prov_h1, prov_page_html, breadcrumbs=prov_bc, json_ld=prov_ld))

  prov_cards_all += f"""<div class="provider-card">
    <div class="provider-card-header">
      <span class="provider-rank-badge">排名 #{rank}</span>
      <h3 class="provider-name">{name}</h3>
    </div>
    <div class="provider-price-row" style="display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 12px;">
      <div class="provider-price" style="font-size: 1.25rem; font-weight: 800; color: #e11d48; white-space: nowrap;">{price}</div>
      <div class="provider-traffic" style="font-size: 0.84rem; color: #64748b; white-space: nowrap;">流量基准：{traffic}</div>
    </div>
    <div class="provider-summary">{p['summary']}</div>
    <div class="provider-coupon-box">
      <span>优惠码: <strong class="coupon-code">{coupon}</strong></span>
      <button class="coupon-copy-btn" data-coupon="{coupon}">复制</button>
    </div>
    <div class="provider-actions" style="display: flex; flex-direction: row; gap: 8px; align-items: center; width: 100%; margin-top: 14px;">
      <a href="/providers/{slug}/" class="btn-detail" style="flex: 1 1 50%; display: inline-flex; align-items: center; justify-content: center; text-align: center; padding: 8px 4px; background: #f8fafc; color: #334155; border: 1px solid #cbd5e1; font-size: 0.85rem; font-weight: 600; border-radius: 6px; text-decoration: none; white-space: nowrap;">查看测评</a>
      <a href="{invite}" target="_blank" rel="sponsored nofollow noopener" class="btn-reg-prominent" style="flex: 1 1 50%; display: inline-flex; align-items: center; justify-content: center; text-align: center; padding: 8px 4px; background: #ffffff !important; color: #000000 !important; border: 1px solid #cbd5e1 !important; font-size: 0.85rem; font-weight: 700; border-radius: 6px; text-decoration: none; white-space: nowrap; box-shadow: 0 1px 2px rgba(0,0,0,0.06);">官网注册</a>
    </div>
  </div>"""

providers_index_html = f"""<section class="section">
  <div class="container">
    <div class="section-header">
      <h1 class="section-title">服务资料库与测评总览</h1>
      <p class="section-desc">本库收录 {len(providers)} 个独立服务商的测评资料与核验记录，前四名为本站主推核心服务。</p>
    </div>
    <div class="cards-grid">
      {prov_cards_all}
    </div>
  </div>
</section>"""
write_page("providers/index.html", wrap_html(f"服务资料库与测评总览｜{BRAND}", "汇总收录 27 个独立网络连接服务的测评资料与参考信息。", f"{DOMAIN}/providers/", "服务资料库与测评总览", providers_index_html, breadcrumbs=[("首页", "/"), ("服务测评", "")]))

# --- 4. ALL FAQS EXPANDED BY DEFAULT (100 FAQs across 5 pages) ---
PAGE_SIZE = 20
total_faq_pages = (len(faqs) + PAGE_SIZE - 1) // PAGE_SIZE

for pno in range(1, total_faq_pages + 1):
  start_idx = (pno - 1) * PAGE_SIZE
  page_faqs = faqs[start_idx:start_idx + PAGE_SIZE]
  
  # Note: OPEN attribute on all details elements so ALL FAQs are expanded by default!
  faq_items_html = ""
  for item in page_faqs:
    faq_items_html += f"""<details class="faq-item" id="{item['slug']}" open>
      <summary class="faq-question">【{item['category']}】{item['question']}</summary>
      <div class="faq-answer">
        <p>{item['answer']}</p>
        <p style="margin-top: 10px; font-size: 0.85rem;"><a href="{item['internalLink']}">👉 阅读相关进阶指南</a> ｜ <a href="{TG_CHANNEL}" target="_blank" rel="noopener nofollow">加入 TG 交流群讨论</a></p>
      </div>
    </details>"""

  pag_links = ""
  for i in range(1, total_faq_pages + 1):
    u = "/faq/" if i == 1 else f"/faq/page/{i}/"
    act = "active" if i == pno else ""
    pag_links += f"<a href=\"{u}\" class=\"page-link {act}\">{i}</a> "

  faq_page_content = f"""<section class="section">
    <div class="container">
      <div class="section-header">
        <h1 class="section-title">常见问题中心 (FAQ) - 第 {pno} 页 (已全部展开)</h1>
        <p class="section-desc">本中心共收录 100 个高频进阶疑问解答，全部问题与答案默认完整展开呈现，涵盖 9 大主题配额。</p>
      </div>

      <div class="faq-accordion">
        {faq_items_html}
      </div>

      <div class="pagination">
        {pag_links}
      </div>
    </div>
  </section>"""

  rel_faq_path = "faq/index.html" if pno == 1 else f"faq/page/{pno}/index.html"
  canonical_faq = f"{DOMAIN}/faq/" if pno == 1 else f"{DOMAIN}/faq/page/{pno}/"
  faq_bc = [("首页", "/"), ("常见问题", "/faq/")] if pno > 1 else [("首页", "/"), ("常见问题", "")]
  write_page(rel_faq_path, wrap_html(f"常见问题中心 (第 {pno} 页)｜{BRAND}", "JichangPlus 机场加常见问题解答中心，提供 100 个高频进阶疑问的标准解答与指南内链。", canonical_faq, f"常见问题中心 (FAQ) - 第 {pno} 页 (已全部展开)", faq_page_content, breadcrumbs=faq_bc))

# --- 5. LEGAL PAGES ---
legal_slugs = ["about", "contact", "editorial-policy", "methodology", "corrections", "affiliate-disclosure", "privacy", "terms", "disclaimer"]
for lslug in legal_slugs:
  with open(f"content/{lslug}/_index.md", "r", encoding="utf-8") as f:
    raw = f.read()
  parts = raw.split("---")
  content_lines = [l for l in (parts[2] if len(parts) > 2 else raw).split("\n") if not l.startswith("# ")]
  rendered_legal = md_to_html("\n".join(content_lines))
  
  meta_title = "关于我们"
  if lslug == "about": meta_title = "关于 JichangPlus 机场加"
  elif lslug == "contact": meta_title = "联系我们"
  elif lslug == "editorial-policy": meta_title = "编辑原则"
  elif lslug == "methodology": meta_title = "评测与核验方法"
  elif lslug == "corrections": meta_title = "纠错与更新政策"
  elif lslug == "affiliate-disclosure": meta_title = "邀请链接与合作披露"
  elif lslug == "privacy": meta_title = "隐私政策"
  elif lslug == "terms": meta_title = "服务条款"
  elif lslug == "disclaimer": meta_title = "免责声明"
  
  page_html = f"""<section class="section">
    <div class="container article-container">
      <h1 class="section-title">{meta_title}</h1>
      <div class="article-body">
        {rendered_legal}
      </div>
    </div>
  </section>"""
  write_page(f"{lslug}/index.html", wrap_html(f"{meta_title}｜{BRAND}", f"JichangPlus 机场加{meta_title}说明页面。", f"{DOMAIN}/{lslug}/", meta_title, page_html, breadcrumbs=[("首页", "/"), (meta_title, "")]))

# --- 6. 404 PAGE ---
page_404 = wrap_html(f"404 页面未找到｜{BRAND}", "很抱歉，您访问的页面不存在或已被移除。", f"{DOMAIN}/404.html", "404 - 页面未找到", """<section class="section">
  <div class="container article-container" style="text-align: center; padding: 60px 0;">
    <h1 class="section-title">404 - 页面未找到</h1>
    <p class="section-desc" style="margin-bottom: 24px;">您所寻找的文章或专栏可能已更新或迁移路径。</p>
    <a href="/" class="btn-primary">返回首页</a>
    <a href="/service/" class="btn-secondary" style="margin-left: 10px;">查看机场服务说明</a>
  </div>
</section>""")
write_page("404.html", page_404)

# --- 7. SITEMAP.XML ---
now_str = datetime.now().strftime("%Y-%m-%d")
sitemap_urls = sorted(list(set(all_urls)))
sitemap_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
""" + "".join([f"""  <url>
    <loc>{u}</loc>
    <lastmod>{now_str}</lastmod>
    <changefreq>{"daily" if u == DOMAIN + "/" else "weekly"}</changefreq>
    <priority>{"1.0" if u == DOMAIN + "/" else "0.8"}</priority>
  </url>\n""" for u in sitemap_urls]) + "</urlset>"

with open("public/sitemap.xml", "w", encoding="utf-8") as f:
  f.write(sitemap_xml)

# --- 8. ROBOTS.TXT ---
robots_txt = f"""User-agent: *
Allow: /

Sitemap: {DOMAIN}/sitemap.xml
"""
with open("public/robots.txt", "w", encoding="utf-8") as f:
  f.write(robots_txt)

# --- 9. RSS.XML ---
rss_items = ""
for sec_dir, sec_name, sec_kw, count in sections:
  nav_item = next(item for item in profile["navigationItems"] if sec_dir in item["url"])
  for s_idx, title in enumerate(nav_item["articleSeeds"][:3], 1):
    art_slug = f"{sec_dir}-part-{s_idx:02d}"
    rss_items += f"""    <item>
      <title>{title}</title>
      <link>{DOMAIN}/{sec_dir}/{art_slug}/</link>
      <description>{title} - JichangPlus 机场加进阶深度长文指南。</description>
      <pubDate>Wed, 23 Sep 2026 12:00:00 +0800</pubDate>
      <guid>{DOMAIN}/{sec_dir}/{art_slug}/</guid>
    </item>\n"""

rss_xml = f"""<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0">
  <channel>
    <title>{BRAND}</title>
    <link>{DOMAIN}</link>
    <description>{profile['siteTopic']}</description>
    <language>zh-CN</language>
    <lastBuildDate>Wed, 23 Sep 2026 12:00:00 +0800</lastBuildDate>
{rss_items}  </channel>
</rss>"""

with open("public/rss.xml", "w", encoding="utf-8") as f:
  f.write(rss_xml)

# --- 10. SEARCH-INDEX.JSON (For instant article search) ---
with open("public/search-index.json", "w", encoding="utf-8") as f:
  json.dump(search_index, f, ensure_ascii=False)

print(f"Build complete! Successfully generated {len(sitemap_urls)} static pages & search index in public/")
