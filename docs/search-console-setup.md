# Google Search Console & Bing Webmaster 接入说明

## 1. 站点验证
- 在 `config.toml` 或构建脚本中配置 `google-site-verification` 与 `msvalidate.01` Meta 标签。
- 部署至线上后通过 HTML 标签或 DNS TXT 记录完成所有权验证。

## 2. 提交 Sitemap
- 站点地图文件规范地址为：`https://jichangplus.xyz/sitemap.xml`
- 在 Google Search Console 与 Bing Webmaster 后台分别提交该 URL。
