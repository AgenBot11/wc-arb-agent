# 注册清单 — 发布前必做

## 必须注册（赚钱相关）

| # | 平台 | 链接 | 用途 | 耗时 |
|---|------|------|------|------|
| 1 | **Stake Affiliate** | https://stake.com/affiliate | USDT 盘 + 返利 | 1-3 天审核 |
| 2 | **Cloudbet Affiliate** | https://www.cloudbet.com/affiliates | USDT 盘 + 返利 | 1-2 天 |
| 3 | **BC.Game Affiliate** | https://bc.game/affiliate | 第三平台 + 返利 | 较快 |

申请时附上 GitHub 仓库链接：`https://github.com/AgenBot11/wc-arb-agent`

## 必须注册（功能相关）— 每人用自己的 Key（BYOK）

> **禁止共用 API Key。** 额度按账号计算，共用几天就耗尽。详见 [API_KEYS.md](./API_KEYS.md)

| # | 平台 | 链接 | 用途 | 费用 |
|---|------|------|------|------|
| 4 | **The-Odds-API** | https://the-odds-api.com/#get-access | `scan --live` 实时赔率 | 免费 ~500 credits/月 **每账号** |
| 5 | **API-Football**（可选） | https://dashboard.api-football.com/register | `fixtures` + 事件 | 免费 ~100 次/天 **每账号** |

**备选：** 不注册 API 也可用 [BROWSER_AGENT.md](./BROWSER_AGENT.md) 让 Agent 浏览器抓 Stake/Cloudbet 盘口。

## 必须注册（推广相关）

| # | 平台 | 链接 | 用途 |
|---|------|------|------|
| 6 | **X (Twitter)** | https://x.com | 发帖推广 |
| 7 | **GitHub** | 已完成 | 代码托管 |

## 可选（进阶）

| # | 平台 | 用途 |
|---|------|------|
| 8 | xAI Plugin Marketplace PR | 官方 Grok 曝光 |
| 9 | Stake + Cloudbet 投注账户 | 自己测试 7U |

---

## 配置步骤

```bash
python cli.py setup          # 生成 config.yaml
# 编辑 config.yaml，填入所有 key 和 ref_code
python cli.py status         # 检查是否配齐
python cli.py affiliate      # 查看推广链接
python cli.py scan --all     # 演示+实盘扫描
```

---

## 推广链接要不要加密？

**不要加密，也不要写进 GitHub 源码。**

| 方案 | 推荐？ | 原因 |
|------|--------|------|
| 写在源码里 | ❌ | Fork 的人用你的码，你赚不到 |
| AES 加密放源码 | ❌ | 密钥也在代码里，等于没加密 |
| **config.yaml（gitignore）** | ✅ | 你的码只有你有 |
| **环境变量 WC_ARB_*_REF** | ✅ | CI/服务器部署用 |
| 远程 config URL | ✅ 进阶 | 只有你控制的链接 |

推荐码本质是**公开追踪 ID**，不是密码。  
防的是别人**复制你的仓库用你的码**，不是防用户看到。

正确做法：

```
config.example.yaml  → 占位符 YOUR_STAKE_CODE（提交 Git）
config.yaml          → 真实码（.gitignore，永不提交）
affiliate.py         → 只从 config 读取，源码无真实链接
```