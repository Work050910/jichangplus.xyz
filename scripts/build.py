import os, sys, json, shutil, re
from datetime import datetime

DOMAIN = "https://jichangplus.xyz"
SITE_TITLE = "JichangPlus 机场加｜机场使用技巧与进阶管理教程"
BRAND = "JichangPlus 机场加"

with open("data/site-seo-profile.json", "r", encoding="utf-8") as f:
  profile = json.load(f)

with open("data/providers.json", "r", encoding="utf-8") as f:
  providers = json.load(f)

with open("data/faq.json", "r", encoding="utf-8") as f:
  faqs = json.load(f)

if os.path.exists("public"): shutil.rmtree("public")
os.makedirs("public/css", exist_ok=True)
os.makedirs("public/js", exist_ok=True)
os.makedirs("public/images", exist_ok=True)

shutil.copy("static/css/cleanwhite.css", "public/css/cleanwhite.css")
shutil.copy("static/js/main.js", "public/js/main.js")
shutil.copy("static/favicon.svg", "public/favicon.svg")

all_urls = []

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
  <link rel="icon" type="image/svg+xml" href="/favicon.svg">
  <link rel="alternate" type="application/rss+xml" title="{BRAND} RSS" href="/rss.xml">
  <link rel="stylesheet" href="/css/cleanwhite.css">
  <script defer src="/js/main.js"></script>
  {schema_script}
</head>
<body>
  <header class="site-header">
    <div class="container">
      <div class="header-top">
        <div class="site-brand">
          <a href="/" class="brand-link">{BRAND}</a>
          <span class="site-tagline">机场使用技巧与进阶管理教程</span>
        </div>
        <div class="header-actions">
          <a href="/service/" class="header-cta-btn">查看服务说明</a>
          <button class="menu-toggle" aria-expanded="false" aria-label="切换主导航菜单">☰ 菜单</button>
        </div>
      </div>
      <nav class="main-nav" aria-label="全站主导航">
        <ul class="nav-list">
          <li><a href="/" class="nav-link">首页</a></li>
          <li><a href="/series/" class="nav-link">系列导读</a></li>
          <li><a href="/subscription-management/" class="nav-link">订阅管理</a></li>
          <li><a href="/multi-device/" class="nav-link">多设备使用</a></li>
          <li><a href="/traffic-nodes/" class="nav-link">流量与节点</a></li>
          <li><a href="/client-tips/" class="nav-link">客户端技巧</a></li>
          <li><a href="/safe-use/" class="nav-link">安全习惯</a></li>
          <li><a href="/service/" class="nav-link">服务说明</a></li>
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
            本站专注 JichangPlus 机场加进阶教程，系统覆盖订阅与流量管理、多设备使用技巧、客户端使用经验与系列文章，提供带核验日期的服务说明与免责声明，助你建立条理清晰的日常使用习惯。
          </p>
          <p class="footer-compliance-text">
            本站所有技术分享仅限网络正常交流与优化参考，请遵守所在国家和地区法律法规。服务数据包含最后核验时间，具体套餐与价格以各服务商当前结算页为准。
          </p>
        </div>
        <div class="footer-nav-col">
          <div class="footer-col-title">进阶专题</div>
          <ul class="footer-links">
            <li><a href="/subscription-management/">订阅日常管理</a></li>
            <li><a href="/multi-device/">多设备协同使用</a></li>
            <li><a href="/traffic-nodes/">流量规划与节点</a></li>
            <li><a href="/client-tips/">客户端进阶技巧</a></li>
            <li><a href="/safe-use/">安全使用常识</a></li>
            <li><a href="/service/">自营与精选服务</a></li>
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
        <div>© 2026 {BRAND} (jichangplus.xyz). 保留所有权利。</div>
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


# Markdown to HTML converter
def md_to_html(md_text):
  lines = md_text.strip().split("\n")
  html_lines = []
  in_ul = False
  in_ol = False
  
  for line in lines:
    line_s = line.strip()
    if not line_s:
      if in_ul: html_lines.append("</ul>"); in_ul = False
      if in_ol: html_lines.append("</ol>"); in_ol = False
      continue
    
    if line_s.startswith("### "):
      if in_ul: html_lines.append("</ul>"); in_ul = False
      if in_ol: html_lines.append("</ol>"); in_ol = False
      html_lines.append(f"<h3>{line_s[4:]}</h3>")
    elif line_s.startswith("## "):
      if in_ul: html_lines.append("</ul>"); in_ul = False
      if in_ol: html_lines.append("</ol>"); in_ol = False
      html_lines.append(f"<h2>{line_s[3:]}</h2>")
    elif line_s.startswith("- "):
      if not in_ul:
        if in_ol: html_lines.append("</ol>"); in_ol = False
        html_lines.append("<ul>"); in_ul = True
      item_text = line_s[2:]
      item_text = re.sub(r"\[([^\]]+)\]\(([^\)]+)\)", r"<a href='\2'>\1</a>", item_text)
      item_text = re.sub(r"\*\*([^\*]+)\*\*", r"<strong>\1</strong>", item_text)
      html_lines.append(f"<li>{item_text}</li>")
    elif re.match(r"^\d+\.\s", line_s):
      if not in_ol:
        if in_ul: html_lines.append("</ul>"); in_ul = False
        html_lines.append("<ol>"); in_ol = True
      item_text = re.sub(r"^\d+\.\s*", "", line_s)
      item_text = re.sub(r"\[([^\]]+)\]\(([^\)]+)\)", r"<a href='\2'>\1</a>", item_text)
      item_text = re.sub(r"\*\*([^\*]+)\*\*", r"<strong>\1</strong>", item_text)
      html_lines.append(f"<li>{item_text}</li>")
    elif line_s.startswith("<div") or line_s.startswith("</div") or line_s.startswith("<h4") or line_s.startswith("<a") or line_s.startswith("<p"):
      if in_ul: html_lines.append("</ul>"); in_ul = False
      if in_ol: html_lines.append("</ol>"); in_ol = False
      html_lines.append(line_s)
    else:
      if in_ul: html_lines.append("</ul>"); in_ul = False
      if in_ol: html_lines.append("</ol>"); in_ol = False
      p_text = line_s
      p_text = re.sub(r"\[([^\]]+)\]\(([^\)]+)\)", r"<a href='\2'>\1</a>", p_text)
      p_text = re.sub(r"\*\*([^\*]+)\*\*", r"<strong>\1</strong>", p_text)
      html_lines.append(f"<p>{p_text}</p>")

  if in_ul: html_lines.append("</ul>")
  if in_ol: html_lines.append("</ol>")
  return "\n".join(html_lines)

# --- 1. HOMEPAGE ---
hero_text = (
  "面向已有基础的中文读者，JichangPlus 机场加系统提供机场使用技巧、订阅管理、流量管理与多设备使用系列教程。"
  "持续更新日常使用经验、设备协同配置与安全习惯，深入探讨机场订阅多久更新一次、机场流量怎么合理分配与多台设备如何管理机场订阅，"
  "帮助建立清晰有条理的日常网络工具使用规范。"
)

top4_cards = ""
for p in providers[:4]:
  top4_cards += f"""<div class="provider-card primary-rank">
    <div class="provider-card-header">
      <span class="provider-rank-badge">推荐 #{p['rank']}</span>
      <h3 class="provider-name">{p['name']}</h3>
    </div>
    <div class="provider-price">{p['priceFrom']}</div>
    <div class="provider-traffic">流量基准：{p['trafficFrom']}</div>
    <div class="provider-summary">{p['summary']}</div>
    <div class="provider-coupon-box">
      <span>优惠码: <strong class="coupon-code">{p['coupon']}</strong></span>
      <button class="coupon-copy-btn" data-coupon="{p['coupon']}">复制</button>
    </div>
    <div class="provider-actions">
      <a href="/providers/{p['slug']}/" class="btn-detail">查看 {p['name']} 机场测评</a>
      <a href="{p['inviteURL']}" target="_blank" rel="sponsored nofollow noopener" class="btn-cta">{p['ctaText']}</a>
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
      <a href="/providers/{p['slug']}/">测评详情</a> | 
      <a href="{p['inviteURL']}" target="_blank" rel="sponsored nofollow noopener">核对套餐</a>
    </td>
  </tr>"""

home_body = f"""<section class="hero-section">
  <div class="container">
    <span class="hero-badge">当前年份中文机场进阶教程 · 订阅管理 · 多设备协同</span>
    <h1 class="hero-title">JichangPlus 机场加：让订阅、设备和日常使用更有条理</h1>
    <p class="hero-description">{hero_text}</p>
    <div class="hero-actions">
      <a href="/service/" class="btn-primary">查看设备适配与服务说明</a>
      <a href="/series/" class="btn-secondary">浏览全站系列学习地图</a>
      <a href="/faq/" class="btn-secondary">查阅 100 常见问题解答</a>
    </div>
    <div class="hero-disclosure">披露说明：本站可能包含赞助链接，所有推荐基于资料核验与场景契合度，价格以各结算页为准。</div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="section-header">
      <h2 class="section-title">核心推荐榜单：按使用场景匹配可靠方案</h2>
      <p class="section-desc">本站严格维护前四名主推顺序，结合多地区节点、小流量年付、晚高峰影音及轻量自研端多维评估。</p>
    </div>
    <div class="cards-grid">
      {top4_cards}
    </div>
  </div>
</section>

<section class="section" style="background: #fafafa;">
  <div class="container">
    <div class="section-header">
      <h2 class="section-title">服务特性快速对比表</h2>
      <p class="section-desc">前四名固定排在表格前四行，提供带核验日期的参考价格与套餐定位。</p>
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
            <th>操作</th>
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
        <h3 class="article-card-title"><a href="/subscription-management/">订阅日常管理</a></h3>
        <p class="article-card-summary">16 篇深度长文，涵盖订阅更新周期、失效清理、防泄露及多机场备用容灾架构。</p>
      </div>
      <div class="article-card">
        <h3 class="article-card-title"><a href="/multi-device/">多设备协同使用</a></h3>
        <p class="article-card-summary">14 篇进阶实战，解决 Windows、Mac、iPhone 与 Android 的规则同步与局域网共享。</p>
      </div>
      <div class="article-card">
        <h3 class="article-card-title"><a href="/traffic-nodes/">流量规划与节点</a></h3>
        <p class="article-card-summary">16 篇系统长文，看懂倍率计算、测速技巧、丢包抖动与地区出口匹配。</p>
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
      <h2 class="section-title">常见问题中心精选 (FAQ)</h2>
      <p class="section-desc">精选日常高频提问，涵盖 9 大主题配额与 100 项长尾解答。</p>
    </div>
    <div class="cards-grid">
      <div class="article-card">
        <h3 class="article-card-title"><a href="/faq/">新手如何根据日常需求挑选合适的机场套餐？</a></h3>
        <p class="article-card-summary">建议优先选择小额月付观察网络稳定性，切勿直接购买长周期大额年付套餐。</p>
      </div>
      <div class="article-card">
        <h3 class="article-card-title"><a href="/faq/">Clash 规则模式与全局模式有什么本质区别？</a></h3>
        <p class="article-card-summary">日常推荐规则分流模式，实现国内流量直连而海外请求平稳走代理节点。</p>
      </div>
      <div class="article-card">
        <h3 class="article-card-title"><a href="/faq/">机场节点的倍率到底是什么意思？如何计算扣费？</a></h3>
        <p class="article-card-summary">实际扣除的流量等于使用量乘以倍率，高倍率节点会成倍消耗可用配额。</p>
      </div>
      <div class="article-card">
        <h3 class="article-card-title"><a href="/faq/">多台设备同时使用同一个订阅链接会有冲突吗？</a></h3>
        <p class="article-card-summary">只要未超出服务商规定的并发在线设备上限，多台设备可以安全稳定同时在线。</p>
      </div>
    </div>
    <div style="text-align: center; margin-top: 30px;">
      <a href="/faq/" class="btn-primary">浏览全部 100 个常见问题解答</a>
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

# --- 2. SECTION LANDING PAGES & ARTICLES ---
sections = [
  ("subscription-management", "订阅管理", "机场订阅管理", 16),
  ("multi-device", "多设备使用", "机场多设备使用", 14),
  ("traffic-nodes", "流量与节点", "机场流量管理", 16),
  ("client-tips", "客户端技巧", "客户端使用技巧", 16),
  ("safe-use", "安全习惯", "机场安全使用", 10),
  ("service", "服务说明", "机场订阅服务", 6)
]

for sec_dir, sec_name, sec_kw, count in sections:
  nav_item = next(item for item in profile["navigationItems"] if sec_dir in item["url"])
  seeds = nav_item["articleSeeds"]
  
  cards_html = ""
  for s_idx, title in enumerate(seeds, 1):
    art_slug = f"{sec_dir}-part-{s_idx:02d}"
    cards_html += f"""<div class="article-card">
      <span class="article-card-badge">第 {s_idx} 篇</span>
      <h3 class="article-card-title"><a href="/{sec_dir}/{art_slug}/">{title}</a></h3>
      <p class="article-card-summary">围绕【{sec_kw}】展开的步骤化深度长文，提供可落地的实操建议与日常维护指引。</p>
      <div class="article-card-meta">
        <span>更新：2026-09-23</span>
        <span>字数：约 960 字</span>
      </div>
    </div>"""

  sec_content = f"""<section class="section">
    <div class="container">
      <div class="section-header">
        <h1 class="section-title">{sec_name}进阶系列教程</h1>
        <p class="section-desc">本专栏收录 {len(seeds)} 篇深度进阶长文，围绕“{sec_kw}”核心意图，系统建立条理分明的日常网络使用与管理体系。</p>
      </div>
      <div class="cards-grid">
        {cards_html}
      </div>
    </div>
  </section>"""

  sec_bc = [("首页", "/"), (sec_name, "")]
  write_page(f"{sec_dir}/index.html", wrap_html(f"{sec_name}｜{BRAND}", f"JichangPlus 机场加{sec_name}专栏，系统收录 {count} 篇进阶深度长文。", f"{DOMAIN}/{sec_dir}/", f"{sec_name}进阶系列教程", sec_content, breadcrumbs=sec_bc))

  for s_idx, title in enumerate(seeds, 1):
    art_slug = f"{sec_dir}-part-{s_idx:02d}"
    art_file = f"content/{sec_dir}/{art_slug}.md"
    with open(art_file, "r", encoding="utf-8") as f:
      raw = f.read()
    
    parts = raw.split("---")
    content_raw = parts[2] if len(parts) > 2 else raw
    content_lines = [l for l in content_raw.split("\n") if not l.startswith("# ")]
    rendered_body = md_to_html("\n".join(content_lines))
    
    art_page_html = f"""<article class="article-page">
      <div class="container article-container">
        <header class="article-header">
          <div class="article-category">{sec_name}</div>
          <h1 class="article-title">{title}</h1>
          <div class="article-meta">
            <span>作者：JichangPlus 编辑团队</span>
            <span>更新时间：2026-09-23</span>
            <span>字数：约 960 字</span>
          </div>
        </header>

        <div class="series-box">
          <div class="series-box-title">所属系列：{sec_name}系列（第 {s_idx} / {len(seeds)} 篇）</div>
          <div>本系列旨在系统建立网络工具日常管理与进阶技巧，建议按顺序阅读。</div>
        </div>

        <div class="toc-box">
          <div class="toc-title">目录导航</div>
          <ul>
            <li><a href="#section-1">导读与核心结论</a></li>
            <li><a href="#section-2">适用对象与开始前准备</a></li>
            <li><a href="#section-3">详细步骤与进阶配置指南</a></li>
            <li><a href="#section-4">推荐服务在当前场景下的适配建议</a></li>
            <li><a href="#section-5">常见误区与维护建议</a></li>
            <li><a href="#section-6">常见问题解答 (FAQ)</a></li>
          </ul>
        </div>

        <div class="article-body">
          {rendered_body}
        </div>

        <div class="in-article-cta">
          <h4>寻找经过核验的稳定网络方案？</h4>
          <p>按你的使用习惯了解适配订阅方案，避免盲目尝试与反复折腾。</p>
          <a href="/service/" class="btn-primary">查看设备适配与服务说明</a>
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
    write_page(f"{sec_dir}/{art_slug}/index.html", wrap_html(f"{title}｜{BRAND}", f"深入探讨{title}，提供清晰条理的进阶管理方法。", f"{DOMAIN}/{sec_dir}/{art_slug}/", title, art_page_html, breadcrumbs=art_bc, json_ld=art_ld))

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
  parts = raw.split("---")
  content_raw = parts[2] if len(parts) > 2 else raw
  content_lines = [l for l in content_raw.split("\n") if not l.startswith("# ")]
  rendered_body = md_to_html("\n".join(content_lines))
  
  prov_h1 = f"{name}机场测评：价格、套餐、节点与适合人群"
  prov_page_html = f"""<article class="article-page">
    <div class="container article-container">
      <header class="article-header">
        <div class="article-category">服务商测评库 · 推荐排名 #{rank}</div>
        <h1 class="article-title">{prov_h1}</h1>
        <div class="article-meta">
          <span>参考价格：{price}</span>
          <span>基准流量：{traffic}</span>
          <span>核验时间：{last_checked}</span>
        </div>
      </header>

      <div class="toc-box">
        <div class="toc-title">目录导航</div>
        <ul>
          <li><a href="#section-1">核心结论与服务定位</a></li>
          <li><a href="#section-2">当前参考价格与套餐体系</a></li>
          <li><a href="#section-3">线路节点与技术协议兼容</a></li>
          <li><a href="#section-4">适用人群与不适用场景分析</a></li>
          <li><a href="#section-5">购买前核验与避坑指南</a></li>
          <li><a href="#section-6">常见问题解答 (FAQ)</a></li>
        </ul>
      </div>

      <div class="article-body">
        {rendered_body}
      </div>

      <div class="post-nav">
        <div class="post-nav-item">
          <div class="post-nav-label">服务总览</div>
          <div class="post-nav-title"><a href="/providers/">返回【服务资料库】目录</a></div>
        </div>
        <div class="post-nav-item" style="text-align: right;">
          <div class="post-nav-label">服务说明</div>
          <div class="post-nav-title"><a href="/service/">查看【服务说明与适配指南】</a></div>
        </div>
      </div>
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
  write_page(f"providers/{slug}/index.html", wrap_html(f"{name}机场测评｜{BRAND}", f"{name}怎么样？本篇详尽评测{name}的价格、套餐、节点与注意事项。", f"{DOMAIN}/providers/{slug}/", prov_h1, prov_page_html, breadcrumbs=prov_bc, json_ld=prov_ld))

  prov_cards_all += f"""<div class="provider-card">
    <div class="provider-card-header">
      <span class="provider-rank-badge">排名 #{rank}</span>
      <h3 class="provider-name">{name}</h3>
    </div>
    <div class="provider-price">{price}</div>
    <div class="provider-traffic">流量基准：{traffic}</div>
    <div class="provider-summary">{p['summary']}</div>
    <div class="provider-coupon-box">
      <span>优惠码: <strong class="coupon-code">{coupon}</strong></span>
      <button class="coupon-copy-btn" data-coupon="{coupon}">复制</button>
    </div>
    <div class="provider-actions">
      <a href="/providers/{slug}/" class="btn-detail">查看测评</a>
      <a href="{invite}" target="_blank" rel="sponsored nofollow noopener" class="btn-cta">{p['ctaText']}</a>
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

# --- 4. FAQ CENTER ---
PAGE_SIZE = 20
total_faq_pages = (len(faqs) + PAGE_SIZE - 1) // PAGE_SIZE

for pno in range(1, total_faq_pages + 1):
  start_idx = (pno - 1) * PAGE_SIZE
  page_faqs = faqs[start_idx:start_idx + PAGE_SIZE]
  
  faq_items_html = ""
  for item in page_faqs:
    faq_items_html += f"""<details class="faq-item" id="{item['slug']}" open>
      <summary class="faq-question">【{item['category']}】{item['question']}</summary>
      <div class="faq-answer">
        <p>{item['answer']}</p>
        <p style="margin-top: 8px; font-size: 0.85rem;"><a href="{item['internalLink']}">👉 阅读相关进阶指南</a></p>
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
        <h1 class="section-title">常见问题中心 (FAQ) - 第 {pno} 页</h1>
        <p class="section-desc">本中心共收录 100 个高频进阶疑问解答，涵盖 9 大主题配额，帮助排除网络日常使用与管理难题。</p>
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
  write_page(rel_faq_path, wrap_html(f"常见问题中心 (第 {pno} 页)｜{BRAND}", "JichangPlus 机场加常见问题解答中心，提供 100 个高频进阶疑问的标准解答与指南内链。", canonical_faq, f"常见问题中心 (FAQ) - 第 {pno} 页", faq_page_content, breadcrumbs=faq_bc))

# --- 5. SERIES & LEGAL PAGES ---
with open("content/series/_index.md", "r", encoding="utf-8") as f:
  raw = f.read()
parts = raw.split("---")
rendered_series = md_to_html(parts[2] if len(parts) > 2 else raw)
series_page_html = f"""<section class="section">
  <div class="container article-container">
    <h1 class="section-title">JichangPlus 机场加系列教程学习地图</h1>
    <div class="article-body">
      {rendered_series}
    </div>
  </div>
</section>"""
write_page("series/index.html", wrap_html(f"系列导读与学习地图｜{BRAND}", "JichangPlus 机场加系统系列教程导读，梳理从订阅管理到客户端调优的完整学习路径。", f"{DOMAIN}/series/", "JichangPlus 机场加系列教程学习地图", series_page_html, breadcrumbs=[("首页", "/"), ("系列导读", "")]))

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
    <a href="/series/" class="btn-secondary" style="margin-left: 10px;">查阅系列导读</a>
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

print(f"Build complete! Successfully generated {len(sitemap_urls)} static pages in public/")
