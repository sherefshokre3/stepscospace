from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse
from twilio.twiml.messaging_response import MessagingResponse

app = FastAPI()

@app.get("/")
def root():
    return {"status": "ShekoBot online", "webhook": "/webhook"}

@app.get("/webhook")
def redirect_to_post():
    return RedirectResponse(url="/webhook")

@app.post("/webhook")
async def webhook(request: Request):
    try:
        # نحاول نقرأ الرسالة سواء JSON أو form
        data = await request.form()
    except Exception:
        data = await request.json()

    text = data.get("Body", "").strip()
    resp = MessagingResponse()

    if text.startswith("/سعر مساهمة"):
        reply = "تمام، الشركة مساهمة السعر 25000 شامل كل مصاريف التأسيس (عقد + سجل + ضريبة + نشر + قيمة مضافة + توكين + غرفة + استعلامات). المدة 10–15 يوم في الهيئة + 15 للبطاقة الضريبية. المكتب الافتراضي مش داخل في السعر."
    elif text.startswith("/سعر مسئولية") or text.startswith("/سعر شخص"):
        reply = "شركة مسئولية محدودة أو شخص واحد السعر حسب رأس المال (من 2750 لحد 25000). يشمل العقد والسجل والبطاقة الضريبية. المدة 7–10 أيام عمل. المكتب 2900 في نصر أو 3900 في التجمع/روكسي."
    elif text.startswith("/سعر تضامن") or text.startswith("/سعر توصية"):
        reply = "تضامن أو توصية بسيطة السعر من 3500 لحد 16000 حسب رأس المال. يشمل عقد الشركاء والسجل والبطاقة. المدة 7–10 أيام عمل. المكتب الافتراضي بيتضاف."
    elif text.startswith("/سعر فردي"):
        reply = "منشأة فردية السعر من 2600 إلى 8000 حسب رأس المال. يشمل عقد التأسيس والسجل والبطاقة الضريبية. المدة 5–7 أيام عمل."
    elif text.startswith("/مكتب"):
        reply = "المكتب الافتراضي: نصر 2900 سنويًا – روكسي/تجمع 3900."
    elif text.startswith("/إضافة"):
        reply = "الإضافات: قيمة مضافة 1500 – توكين 2500 – صحيفة نشر 1000 – غرفة صناعية 3500."
    else:
        reply = "تمام، استخدم أمر زي /سعر أو /مكتب أو /إضافة للاستعلام."

    resp.message(reply)
    return str(resp)
