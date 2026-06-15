# Affiliate Playbook — 卖铲子赚钱手册

## 核心逻辑

```
免费开源工具 → 用户 Star/Fork → 需要平台账户 → 点你的推荐链接注册 → 你拿佣金
```

博彩 affiliate 佣金通常：**$50–200 / 有效注册用户**，远高于自己拿 7U 套利。

---

## Step 1: 申请推荐码（今天做）

| 平台 | 申请入口 | 备注 |
|------|----------|------|
| Stake | stake.com → Affiliates | 需要流量证明，可用 GitHub 仓库链接 |
| Cloudbet | cloudbet.com/affiliates | 审核较快 |
| BC.Game | bc.game/affiliate | 门槛较低 |

拿到 code 后填入 `config.yaml`，更新 README 里的链接。

---

## Step 2: GitHub 发布清单

- [ ] 创建仓库 `wc-arb-agent`（Public）
- [ ] 添加 Topics: `arbitrage`, `sports-betting`, `world-cup`, `playwright`, `crypto`, `stake`, `usdt`
- [ ] README 顶部放 GIF 演示 `python cli.py scan`
- [ ] Pin 仓库到你的 GitHub 主页
- [ ] 发 v0.1.0 Release

---

## Step 3: X (Twitter) 发帖策略

### 首发帖（英文，全球流量）

```
We just open-sourced WC Arb Agent 🏆⚽

→ Cross-platform sports arbitrage for World Cup 2026
→ Asian handicap middle detection
→ AI live commentary signals
→ Playwright auto-bet scaffold
→ Works with Stake, Cloudbet, BC.Game (USDT)

Free on GitHub. Star if useful ⭐

[GitHub link]

#WorldCup2026 #SportsBetting #Arbitrage #Crypto #OpenSource
```

### 跟进帖（24h 后）

```
Most arbitrage bots only work on FanDuel/DraftKings.

WC Arb Agent is built for crypto sportsbooks:
• USDT deposits (TRC-20)
• Asian handicap middles
• 7U bankroll? Our scanner shows exact stakes.

Demo: python cli.py scan --bankroll 7

[GitHub link]
```

### 中文帖（华语圈）

```
世界杯套利工具开源了 ⚽

✅ 多平台赔率对比（Stake/Cloudbet）
✅ 亚盘中间盘自动计算
✅ AI 读文字直播给信号
✅ 7U 小本金也能玩

完全免费，GitHub 自取 👇
[链接]

#世界杯2026 #套利 #USDT #加密货币
```

### 发帖节奏

| 时间 | 内容 |
|------|------|
| Day 1 | 开源发布公告 |
| Day 2 | 演示 middle 计算结果截图 |
| Day 3 | "Spain 0-0 Cape Verde — why draws matter" 教程帖 |
| 每场大赛后 | 赛后复盘 + "our scanner would have..." |
| 每周 | 更新 Roadmap 勾选进度 |

---

## Step 4: 其他引流渠道

| 渠道 | 做法 |
|------|------|
| Reddit r/sportsbook | 发教程帖，遵守版规，不硬广 |
| Reddit r/cryptocurrency | 强调 USDT + 开源 |
| Hacker News | Show HN: WC Arb Agent |
| Dev.to / Medium | 技术文章：《Building a sports arbitrage scanner with Playwright》 |
| Telegram 博彩群 | 发工具链接 + 中盘演示 |
| Product Hunt | 世界杯期间上线 |

---

## Step 5: 收入追踪

| 指标 | 目标（第1月） |
|------|---------------|
| GitHub Stars | 200+ |
| Affiliate 注册 | 10+ |
| 预估收入 | $500–2000 |

追踪方式：各平台 affiliate dashboard。

---

## 合规注意

1. README 免责声明必须有
2. 不在禁赌地区主动推广
3. 不用"稳赚""无风险"等措辞 — 用 "educational tool"
4. 开源 MIT，不承担用户损失
5. 推荐链接旁标注 `#ad` 或 `affiliate link`