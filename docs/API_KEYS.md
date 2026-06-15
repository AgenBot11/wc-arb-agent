# API Keys — 必须用户自己注册（BYOK）

## 为什么不能用别人的 Key？

The-Odds-API 和 API-Football 都是**按账号计费/限额**的：

| 服务 | 免费额度 | 耗尽后果 |
|------|----------|----------|
| [The-Odds-API](https://the-odds-api.com/#get-access) | ~500 credits/月 | 无法拉取实时赔率，`scan --live` 失效 |
| [API-Football](https://dashboard.api-football.com/register) | ~100 次/天 | 无法查赛程/事件 |

如果把维护者的 Key 写进开源仓库或 Grok 插件默认值：

1. **所有用户共用同一额度** → 几天内就会被扫光  
2. **Key 泄露** → 别人可以盗用你的配额  
3. **无法追责** → 谁用了多少请求无法区分  

因此本项目**从不提供、不内置、不共享**任何第三方 API Key。

---

## 正确做法（每个用户一份）

```bash
python cli.py setup    # 生成你自己的 config.yaml
```

在 **你自己的** `config.yaml` 填入 **你自己注册** 的 Key：

```yaml
the_odds_api:
  key: "你的_the_odds_api_key"

api_football:
  key: "你的_api_football_key"   # 可选
```

或用环境变量（适合服务器 / Grok 云端，不写入文件）：

```bash
export WC_ARB_THE_ODDS_API_KEY=你的key
export WC_ARB_API_FOOTBALL_KEY=你的key
```

---

## 注册链接（直接点）

| 服务 | 注册 |
|------|------|
| The-Odds-API | https://the-odds-api.com/#get-access |
| API-Football | https://dashboard.api-football.com/register |

API-Football **没有单独的「世界杯 API」**，注册后复制 Dashboard 里的 API Key 即可，工具自动按联赛筛选。

---

## 额度节省建议

- 默认 `scan` 会缓存赔率 **90 秒**，避免重复扣费  
- 不要开 `watch` 高频轮询（未来功能会默认限速）  
- 没有 Key 时仍可用 `python cli.py scan --demo` 演示逻辑  
- 需要平台真实盘口时，用 **浏览器 Agent** 接管（见 [BROWSER_AGENT.md](./BROWSER_AGENT.md)），不消耗 API 额度  

---

## 维护者 / Fork 作者

- `config.yaml` 已在 `.gitignore`，**禁止提交真实 Key**  
- `config.example.yaml` 只放占位符 `YOUR_*`  
- 文档和 SKILL 中提醒用户 BYOK，不要把个人 Key 发给他人或贴在 Issue 里