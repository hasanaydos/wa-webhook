from fastapi import FastAPI, Request
import httpx
import json
import re

app = FastAPI()

@app.get("/")
def home():
    return {"status": "ok"}

@app.post("/")
async def challenge_root(request: Request):
    raw = await request.body()
    raw_str = raw.decode("utf-8")

    # ✅ Monday challenge doğrulaması
    try:
        data = json.loads(raw_str)
        if "challenge" in data:
            return {"challenge": data["challenge"]}
    except:
        data = {}

    # 🔍 Veriyi yakalamaya çalış
    pulse_name = None
    value = None

    try:
        if "pulseName" in data:
            pulse_name = data["pulseName"]
        if "columnValues" in data and "metin" in data["columnValues"]:
            value = data["columnValues"]["metin"].get("value", "")
    except:
        pass

    # ❓ Eğer düzgün JSON değilse regex ile al
    if not pulse_name:
        match = re.search(r'"pulseName"\s*:\s*"([^"]+)"', raw_str)
        if match:
            pulse_name = match.group(1)

    if not value:
        match = re.search(r'"value"\s*:\s*"([^"]+)"', raw_str)
        if match:
            value = match.group(1)

    # 📨 Mesajı hazırla
    if not pulse_name and not value:
        message = "Veri alınamadı."
    else:
        message = f"Yeni Lead geldi:\n📞 {pulse_name}\n🏢 {value}"

    # ✅ Gönderilecek numaralar
    numbers = [
        "905427901559",
        "905314970408"
    ]

    wa_webhook_url = "https://api.watoolbox.com/webhooks/9D2LHF0S4"

    async with httpx.AsyncClient() as client:
        for phone in numbers:
            wa_payload = {
                "action": "send-message",
                "type": "text",
                "content": message,
                "phone": phone
            }
            await client.post(wa_webhook_url, json=wa_payload)

    return {"status": "Mesajlar gönderildi"}
