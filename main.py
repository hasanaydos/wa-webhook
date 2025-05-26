from fastapi import FastAPI, Request
import httpx
import json

app = FastAPI()

@app.get("/")
def home():
    return {"status": "ok"}

@app.post("/")
async def challenge_root(request: Request):
    data = await request.json()
     # ✅ Monday challenge doğrulamasını kontrol et
    if "challenge" in data:
        return {"challenge": data["challenge"]}

    # Monday.com'dan gelen örnek veri: name ve phone varsayımı
    #name = data.get("name", "Bilinmiyor")
    #phone = data.get("phone", None)

    # Gönderilecek mesaj içeriği
    #message = f"📩 Yeni başvuru:\nAd: {name}\nTelefon: {phone}"

    # Verinin tamamını mesaj olarak gönder
    message = json.dumps(data, indent=2, ensure_ascii=False)

    # WA Toolbox Webhook ayarları
    wa_webhook_url = "https://api.watoolbox.com/webhooks/9D2LHF0S4"
    wa_payload = {
        "action": "send-message",
        "type": "text",
        "content": message,
        "phone": "905427901559"
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(wa_webhook_url, json=wa_payload)

    return {"status": "Mesaj gönderildi"}
