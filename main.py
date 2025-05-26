from fastapi import FastAPI, Request
import httpx

app = FastAPI()

@app.get("/")
def home():
    return {"status": "ok"}

@app.post("/")
async def challenge_root(request: Request):
    data = await request.json()
    if "challenge" in data:
        return data["challenge"]
    return {"error": "Sadece challenge bekleniyordu"}


@app.post("/webhook")
async def receive_webhook(request: Request):
    data = await request.json()

     # Monday doğrulama isteği mi kontrol et
    if "challenge" in data:
        return data["challenge"]  # Monday bunu bekliyor

    # Monday.com'dan gelen örnek veri: name ve phone varsayımı
    name = data.get("name", "Bilinmiyor")
    phone = data.get("phone", None)

    if not phone:
        return {"error": "Telefon numarası bulunamadı."}

    # Gönderilecek mesaj içeriği
    message = f"📩 Yeni başvuru:\nAd: {name}\nTelefon: {phone}"

    # WA Toolbox Webhook ayarları
    wa_webhook_url = "https://api.watoolbox.com/webhooks/9D2LHF0S4"
    wa_payload = {
        "action": "send-message",
        "type": "text",
        "content": message,
        "phone": phone
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(wa_webhook_url, json=wa_payload)

    return {"status": "Mesaj gönderildi"}
