# Agent 浏览器接管 — 不耗 API 额度的备选方案

当 The-Odds-API 额度紧张，或需要 **Stake / Cloudbet 真实盘口**（API 里没有 crypto 盘）时，用 **Agent 浏览器接管** 更合适。

## 适用场景

| 场景 | 推荐方式 |
|------|----------|
| 批量扫赔率、算套利 | The-Odds-API（自备 Key） |
| Stake/Cloudbet 真实页面赔率 | 浏览器 Agent |
| 登录态保存、一次登录长期用 | Playwright session |
| 辅助下单（人工确认） | 浏览器 Agent + `dry_run` |

## 支持的接管方式

本项目提供 **Playbook（步骤剧本）**，可交给以下任一 Agent 执行：

| Agent / 工具 | 说明 |
|--------------|------|
| **Grok Build** | 调用 MCP `wc_arb_browser_playbook`，按步骤操作用户浏览器 |
| **Playwright**（内置） | `python cli.py browser scrape --platform stake --url ...` |
| **browser-use**（可选） | `pip install browser-use`，见下方 |
| **Computer Use / 其他 MCP 浏览器** | 读取 playbook JSON，映射到 click/type/navigate |

## 快速开始

### 1. 获取剧本（Grok / 任意 Agent）

```bash
python cli.py browser playbook stake_scrape_odds
python cli.py browser list
```

MCP：`wc_arb_browser_playbook(scenario="stake_scrape_odds")`

### 2. Playwright 本地抓取

```bash
playwright install chromium
python cli.py browser scrape --platform stake --url "https://stake.com/sports/..."
```

首次需登录：用 **有头模式** 手动登录一次，会话保存在 `.sessions/`。

```bash
python cli.py browser login --platform stake
```

### 3. 可选：browser-use

```bash
pip install browser-use
python cli.py browser agent --scenario cloudbet_scrape_odds --url "https://..."
```

需要本机 LLM API Key（OpenAI 等），由 browser-use 自主导航页面。

## 预置剧本

| ID | 用途 |
|----|------|
| `stake_login` | 打开 Stake，保存登录态 |
| `stake_scrape_odds` | 读取比赛页 1x2 / 亚盘赔率 |
| `cloudbet_login` | Cloudbet 登录态 |
| `cloudbet_scrape_odds` | Cloudbet 比赛赔率 |
| `compare_platforms` | 双平台对照套利（开两个标签） |
| `assisted_bet` | 填好注单，**不自动提交**，等人确认 |

## 安全默认值

```yaml
bot:
  auto_execute: false
  dry_run: true
```

`assisted_bet` 剧本**永远不会自动点 Confirm**；Agent 只填金额和选项，用户自己点下注。

## Grok 操作员指令

1. 用户缺 API Key → 建议 `scan --demo` + 浏览器剧本抓真实盘  
2. 调用 `wc_arb_browser_playbook` 拿到步骤  
3. 用 Grok 浏览器 / Computer Use 逐步执行  
4. 把读到的赔率文本回传 `wc_arb_agent` 或本地计算  

## 文件位置

```
agent/browser_playbooks.py   # 剧本定义
executor/browser_agent.py    # Playwright / browser-use 执行器
.sessions/                   # 登录态（gitignore）
```