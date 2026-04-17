import time
import threading
import os
import sys
from flask import Flask, render_template, jsonify, request
from utils import gmgn_request
from config import *
import requests

app = Flask(__name__)
status = {
    "running": True,
    "daily_spent": 0.0,
    "recent_trades": [],
    "logs": [],
    "portfolio": {"sol_balance": 0, "total_value_sol": 0, "win_rate": 0, "unrealized_pnl_pct": 0, "tokens": []},
    "skills_unlocked": ["抄聪明钱", "持仓可视化", "胜率统计", "安全审查", "anti-MEV", "Web配置"]  # Skills展示用
}

def log(msg):
    timestamp = time.strftime('%H:%M:%S')
    status["logs"].append(f"[{timestamp}] {msg}")
    if len(status["logs"]) > 100: status["logs"].pop(0)
    print(msg)

def send_telegram(msg):
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat = os.getenv("TELEGRAM_CHAT_ID")
    if token and chat:
        requests.get(f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat}&text={msg}")

def is_configured():
    load_dotenv(override=True)
    return all(os.getenv(k) for k in ["GMGN_API_KEY", "GMGN_PRIVATE_KEY", "WALLET_ADDRESS"])

def get_wallet_holdings():
    data = gmgn_request("GET", "/v1/user/holdings", {"chain": "sol"})
    if data.get("code") == 0:
        d = data.get("data", {})
        status["portfolio"] = {
            "sol_balance": d.get("sol_balance", 0),
            "total_value_sol": d.get("total_value_sol", 0),
            "win_rate": d.get("win_rate", 75.0),
            "unrealized_pnl_pct": d.get("unrealized_pnl_pct", 0),
            "tokens": d.get("tokens", [])
        }
        log(f"📊 持仓刷新 | SOL: {status['portfolio']['sol_balance']:.4f} | 胜率: {status['portfolio']['win_rate']}%")

def sniper_loop():
    log("gmgn-kime-ai-skills 已启动！Skills模式全开...")
    send_telegram("gmgn-kime-ai-skills Skills版上线！开始自动抄聪明钱～")
    while status["running"]:
        if status["daily_spent"] >= DAILY_MAX_SOL:
            log("今日额度用完，休息中...")
            time.sleep(3600); continue
        try:
            tokens = get_trenches()
            for t in tokens:
                address = t.get("address")
                smart_count = t.get("smart_money_buy_count", 0)
                if COPY_SMART_MONEY and smart_count >= MIN_SMART_MONEY_BUYS:
                    safe, _ = check_security(address)
                    if safe:
                        log(f"🔥 聪明钱信号！{address[:8]}... x{smart_count}")
                        success = quote_and_buy(address, MAX_POSITION_SOL, f"抄聪明钱 x{smart_count}")
                        if success:
                            status["daily_spent"] += MAX_POSITION_SOL
            get_wallet_holdings()
            time.sleep(8)
        except Exception as e:
            log(f"循环出错: {e}")
            time.sleep(15)

@app.route("/")
def dashboard():
    configured = is_configured()
    return render_template("index.html", configured=configured, status=status)

@app.route("/save_config", methods=["POST"])
def save_config():
    pass  

@app.route("/api/status")
def api_status():
    get_wallet_holdings()
    return jsonify(status)

@app.route("/api/toggle", methods=["POST"])
def toggle():
    status["running"] = not status["running"]
    log(f"机器人已{'启动' if status['running'] else '暂停'}")
    return jsonify({"running": status["running"]})

if __name__ == "__main__":
    load_dotenv()
    if is_configured():
        sniper_thread = threading.Thread(target=sniper_loop, daemon=True)
        sniper_thread.start()
    else:
        log("⚠️ 首次启动，请在Web面板填写GMGN Skills配置")

    log(f"🌐 GMGN Skills kimeai面板启动 → http://127.0.0.1:{WEB_PORT}")
    app.run(host="127.0.0.1", port=WEB_PORT, debug=False)
