# 自主投注 — 安装完就能自己下注

用户只需 **3 步**（Grok Build + 本程序），之后可说一句话让 Agent 自动扫盘并下注。

## 流程总览

```
安装插件 → 登录 Stake/Cloudbet（各一次）→ 开启 autopilot → 说「执行套利」
```

| 步骤 | Grok MCP | 命令行 |
|------|----------|--------|
| 1 初始化 | `wc_arb_onboard` | `python cli.py onboard` |
| 2 登录 Stake | `wc_arb_login("stake")` | `python cli.py login --platform stake` |
| 3 登录 Cloudbet | `wc_arb_login("cloudbet")` | `python cli.py login --platform cloudbet` |
| 4 开启自动下注 | `wc_arb_autopilot_enable` | `python cli.py autopilot --enable` |
| 5 执行 | `wc_arb_autopilot` | `python cli.py autopilot` |

**一键全流程：** `wc_arb_go`（Grok 按顺序执行上述步骤）

## 登录说明

- 会弹出**有头浏览器**，你手动登录（含 2FA）
- 登录态保存在 `.sessions/`，**不用每次重登**
- 密码由浏览器处理，工具**不存储密码**

## 自动下注做什么

1. 扫描 surebet / middle（demo + 你的 The-Odds-API）
2. 只选 **Stake + Cloudbet** 两边都能下的机会
3. 按赔率从难到易依次下单（行业标准）
4. 截图保存在 `.sessions/bets/`
5. 写日志 JSON 便于核对

## 安全开关

```yaml
bot:
  auto_execute: false   # autopilot --enable 后变 true
  dry_run: true         # enable 时默认 false（真下注）
```

预览不下注：`python cli.py autopilot --preview`

## API Key

实时扫盘仍需 **你自己的** The-Odds-API Key（见 [API_KEYS.md](./API_KEYS.md)）。  
没 Key 时可用 `--source demo` 测通流程，但演示盘不会真金白银。

## 故障排查

| 状态 | 处理 |
|------|------|
| `need_login` | 跑 `login --platform stake/cloudbet` |
| `need_enable` | 跑 `autopilot --enable` |
| `no_opportunity` | 正常，稍后重试或 `scan` 查看 |
| `partial` | 看 `.sessions/bets/` 截图，可能 DOM 变更 |

## 免责声明

自动下注有风险（赔率变动、延迟、账户限制）。先用 `--preview` 和 7U 小资金测试。