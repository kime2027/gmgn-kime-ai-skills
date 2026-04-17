# gmgn-kime-ai-skills
基于GMGN官方Skills的小资金狙击器，由kime开发
# gmgn-kime-ai-skills —— GMGN官方Skills风格小资金狙击器

我是 Kime (@Kime_Crypto)，这次把机器人彻底改成GMGN Skills格式！  
既能本地一键跑自动抄聪明钱，又能直接被AI Agent调用

核心Skills（官方格式）：
- 自动抄聪明钱技能（Trenches实时跟单）
- 实时持仓可视化技能（余额跳动 + PNL%）
- Web一键配置技能（零改.env）
- 胜率 & 未实现PNL统计技能
- 安全审查 + anti-MEV技能
- Telegram即时通知技能

使用方法（超简单）：
1. `pip install -r requirements.txt`
2. `python main.py`
3. 浏览器打开 http://127.0.0.1:5000 → 第一次填API Key、私钥、钱包地址 → 保存自动启动
4. 以后直接看赛博Skills面板，技能卡片实时亮起！

纯开源、可审计、无恶意代码，欢迎AI Agent直接安装使用～  
交易有风险，自己review后再上！
