# Kime Sniper Skill - GMGN OpenAPI 自动抄聪明钱

**Skill ID**: kime-sniper  
**Author**: Kime (@Kime_Crypto)  
**Version**: 1.0  
**Description**: 专为小资金玩家打造的GMGN Skills版狙击机器人，自动检测Trenches聪明钱信号并跟单

**Capabilities**:
- 实时Trenches扫描 + 聪明钱跟单
- 安全审查（蜜罐、LP锁、dev持仓）
- 持仓可视化 + 胜率/PNL实时刷新
- Web一键配置API（无需改.env）
- anti-MEV + 严格仓位风控（0.05 SOL/笔）
- Telegram通知

**Usage**:
- AI Agent可直接调用：`invoke kime-sniper start`
- 本地运行：`python main.py` 打开 http://127.0.0.1:5000

**Required Credentials**:
- Query: GMGN_API_KEY
- Trading: GMGN_PRIVATE_KEY + WALLET_ADDRESS

**GitHub**: https://github.com/你的用户名/gmgn-kime-ai-skills
