---
title: "Clash 覆写配置（Mixin / Script）入门：自定义规则不再被订阅覆盖｜JichangPlus 机场加"
description: "详解 Clash Verge 与现代客户端中 Mixin 与 Script 扩展机制，教你优雅注入自定义规则与本地策略组，彻底告别订阅更新冲掉配置的烦恼。"
date: 2026-09-28
lastmod: 2026-09-28
author: "JichangPlus 编辑团队"
categories: ["客户端技巧"]
tags: ['Clash 覆写', 'Mixin', 'Yaml 扩展', '配置持久化', 'Clash Verge']
primaryKeyword: "Clash Mixin 覆写"
series: ["客户端技巧系列"]
seriesPart: 2
seriesTotal: 16
slug: "client-tips-part-02"
---

# Clash 覆写配置（Mixin / Script）入门：自定义规则不再被订阅覆盖

## 导读：订阅更新与自定义规则的冲突之痛

在使用 Clash 的进阶过程中，几乎所有读者都经历过这样的挫败：为了让某个特定公司内网走直连，或者为了给特定海外服务指定专用节点，辛辛苦苦手动编辑了下载下来的 `config.yaml` 配置文件。然而几天后，当点击客户端的“更新订阅”时，服务商下发的全新配置瞬间将所有手动修改覆盖抹除，一切又被打回原形。

难道每次更新订阅都要重新手动改一遍文件吗？当然不用！现代 Clash 客户端（如 Clash Verge Rev、Clash Nyanpasu）早已引入了极其强大的**配置覆写（Mixin / Script）**机制。本文将教你如何用最优雅的姿态管理自定义规则，实现“配置随心定制，订阅放心更新”。

## Mixin 与 Script 的底层运行机制

所谓的覆写（Mixin），本质上是一种在内存中动态执行的“后处理过滤器”。当客户端从服务商服务器拉取到最新的订阅配置后，并不会直接将其交由内核运行，而是先将原始配置与你编写的 Mixin 脚本进行合并：

```
[远端订阅原始配置] ──> [本地 Mixin 规则预处理] ──> [最终生效的完整配置] ──> [交给内核运行]
```

由于你的自定义代码保存在独立的本地覆写脚本中，无论远端订阅更新多少次，客户端在每次启动或更新时都会全自动将你的规则智能缝合进去，从而彻底终结了配置被冲掉的历史。

## 实战指南：在 Clash Verge Rev 中配置 Mixin

目前主流的现代客户端 Clash Verge Rev 支持两种覆写模式：简洁直观的 YAML 声明式覆写，以及功能无限强大的 JavaScript / TypeScript 编程式覆写。

### 模式一：声明式 YAML Mixin（适合基础规则注入）
如果你只是希望在现有规则的最顶部追加几条自己的域名规则，或者修改某些默认端口与 DNS 参数，使用 YAML 覆写最为省心：

```yaml
# 在规则最前面追加私有直连与代理规则
prepend-rules:
  - DOMAIN-SUFFIX,internal.company.com,DIRECT
  - DOMAIN-KEYWORD,my-private-api,PROMPT-PROXY
  - IP-CIDR,10.0.0.0/8,DIRECT

# 开启 TUN 模式核心开关
tun:
  enable: true
  stack: mixed
  dns-hijack:
    - any:53
```
在客户端配置面板中开启 Mixin 开关，上述声明的内容就会在每次更新时全自动合并至最终配置。

### 模式二：编程式 Script 扩展（适合高阶逻辑定制）
如果你需要根据节点名称动态批量创建自定义策略组，可以使用 JavaScript 脚本：
```javascript
function main(config) {
  // 遍历所有节点，挑选出所有香港和日本专线
  const hkNodes = config.proxies.filter(p => p.name.includes("香港")).map(p => p.name);
  
  // 注入一个专属于自己的极速策略组
  config["proxy-groups"].unshift({
    name: "🚀 专属低延迟组",
    type: "url-test",
    url: "http://www.gstatic.com/generate_204",
    interval: 300,
    proxies: hkNodes.length > 0 ? hkNodes : ["DIRECT"]
  });

  return config;
}
```

## 维护自定义覆写的三大黄金法则

- **规则位置要用 prepend（前置）**：Clash 规则是先匹配先执行，自定义规则一定要插入到规则列表的最前面（prepend），否则若被后面的通用白名单拦截将无法生效；
- **严格遵循 YAML 缩进规范**：YAML 语言对空格极其敏感，必须使用 2 个空格缩进，严禁使用 Tab 键制表符；
- **配置修改后及时检查日志**：保存 Mixin 后，在客户端的日志窗口观察是否有语法报错提示。若有报错，客户端通常会回退到原始配置，便于即时修复。

## 常见问题解答 (FAQ)

### 为什么在 Mixin 中添加了规则，但测试访问时依然不走指定策略？
首先检查规则拼写与类型是否正确（例如域名后缀必须用 `DOMAIN-SUFFIX` 而不能错拼为 `DOMAIN`）；其次，确认客户端的 Mixin 主开关是否处于激活状态；最后，关闭浏览器重新发起新连接，排除浏览器内部长连接缓存的干扰。

### 多个不同机场的订阅，可以共用同一套本地 Mixin 规则吗？
完全可以！这正是 Mixin 架构的最大魅力所在。你只需维护一份通用的本地 Mixin 脚本，它会自动对你导入的所有机场订阅生效，让你在切换不同服务商时依然享有完全一致的操作习惯与分流逻辑。
