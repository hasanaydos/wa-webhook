from fastapi import FastAPI, Request
import httpx

app = FastAPI()

@app.get("/")
def home():
    return {"status": "ok"}

@app.post("/webhook")
async def receive_webhook(request: Request):
    data = await request.json()

    # Monday webhook'tan gelen örnek veri:
    name = data.get("name", "Bilinmiyor")
    phone = data.get("phone", "Yok")

    # WA Toolbox için mesaj
    message = f"📩 Yeni başvuru:\nAd: {name}\nTelefon: {phone}"

    wa_api_url = "https://api.watoolbox.com/send"
    wa_payload = {
        "group_id": "WHATSAPP_GRUP_ID",   # Buraya senin grup ID’in
        "text": message,
        "token": "WA_TOOLBOX_TOKEN"       # Buraya senin özel token’ın
    }

    async with httpx.AsyncClient() as client:
        await client.post(wa_api_url, json=wa_payload)

    return {"message": "Gönderildi"}
