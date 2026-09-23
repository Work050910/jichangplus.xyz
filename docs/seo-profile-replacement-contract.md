# SEO 配置层替换契约 (SEO Profile Replacement Contract)

## 1. 单一数据源与定位
本项目将全站核心关键词、导航定义、Hero 关键词簇、页脚品牌词及内容规划收敛于 `data/site-seo-profile.json`（镜像于 `docs/site-seo-profile.json`）。

## 2. 替换接口与输入参数
后续通过另一条万能替换提示词整体更换站点 SEO 配置时，接口必须提供以下结构化字段：
- `primaryKeywords`: 新的核心关键词列表（3~6 个）
- `secondaryKeywords`: 新的辅助关键词列表（10~20 个）
- `longTailKeywords`: 新的长尾关键词列表（15~30 个）
- `heroKeywords`: 新的首页首屏关键词列表（8~12 个）
- `footerKeywords`: 新的页脚关键词说明词表（5~8 个）
- `navigationItems`: 新的自定义导航（含 label, url, primaryKeyword, articleSeeds, articleCount）
- `protectedBrandTerms`: 需保留的品牌、服务商及邀请链接数据
- `inactiveKeywords`: 旧关键词退役归档池

## 3. 标准替换执行流程
1. **读取旧配置**: 读取当前 `site-seo-profile.json` 与全量 URL 映射清单。
2. **规范化与聚类**: 对新关键词清洗、去重，建立全新搜索意图集群。
3. **意图冲突检测**: 检查新关键词与导航是否存在同义重复或 URL 冲突。
4. **全站自动同步**: 更新配置层后，驱动模板与内容生成器，同步刷新 Hero、页脚、Header、meta、栏目落地页与内链。
5. **301 映射重定向**: 对发生变更且已有权重的旧 URL 建立到最匹配新 URL 的 301 规则，禁止全站跳首页或产生 404。
6. **保留商业资产**: 严格保留未被要求修改的服务商数据、固定前四名、邀请码、优惠券及合规披露。
7. **历史残留扫描**: 扫描代码库，确认旧活动关键词不再违规滞留在活动页面。
8. **重新构建与验证**: 执行 `python3 scripts/build.py` 与 `python3 scripts/validate.py` 确保 45+ 项质量指标全部达标。
