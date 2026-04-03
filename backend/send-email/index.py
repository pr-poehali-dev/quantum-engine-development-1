import json
import os
import smtplib
import psycopg2
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime


def save_lead(name, phone, company, message):
    """Сохраняет заявку в таблицу leads и возвращает id."""
    conn = psycopg2.connect(os.environ["DATABASE_URL"])
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO leads (name, phone, company, message) VALUES (%s, %s, %s, %s) RETURNING id",
        (name, phone, company or None, message or None)
    )
    lead_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return lead_id


def send_email(lead_id, name, phone, company, message):
    """Отправляет уведомление на почту о новой заявке."""
    smtp_host = os.environ.get("SMTP_HOST")
    smtp_user = os.environ.get("SMTP_USER")
    smtp_password = os.environ.get("SMTP_PASSWORD")
    from_email = os.environ.get("SMTP_FROM_EMAIL")
    to_email = os.environ.get("SMTP_TO_EMAIL")

    if not all([smtp_host, smtp_user, smtp_password, from_email, to_email]):
        return

    now = datetime.now().strftime("%d.%m.%Y %H:%M")
    company_row = f'<tr style="border-bottom:1px solid #eee"><td style="padding:12px 0;color:#666;font-size:13px;text-transform:uppercase;letter-spacing:1px;width:140px">Компания</td><td style="padding:12px 0;color:#1a1a1a;font-size:15px">{company}</td></tr>' if company else ""
    message_row = f'<tr><td style="padding:12px 0;color:#666;font-size:13px;text-transform:uppercase;letter-spacing:1px;vertical-align:top">Сообщение</td><td style="padding:12px 0;color:#1a1a1a;font-size:15px;line-height:1.6">{message.replace(chr(10), "<br>")}</td></tr>' if message else ""

    html = f"""<div style="font-family:Arial,sans-serif;max-width:600px;margin:0 auto;padding:20px;background:#f9f9f9">
  <div style="background:#1a1a1a;padding:24px;margin-bottom:24px">
    <h1 style="color:#fff;margin:0;font-size:24px;letter-spacing:2px">АВТОВОРОТА</h1>
    <p style="color:#999;margin:4px 0 0;font-size:12px;text-transform:uppercase">Новая заявка #{lead_id} с сайта</p>
  </div>
  <div style="background:#fff;padding:24px;border-left:4px solid #1a1a1a">
    <table style="width:100%;border-collapse:collapse">
      <tr style="border-bottom:1px solid #eee"><td style="padding:12px 0;color:#666;font-size:13px;text-transform:uppercase;letter-spacing:1px;width:140px">Имя</td><td style="padding:12px 0;color:#1a1a1a;font-size:15px;font-weight:bold">{name}</td></tr>
      <tr style="border-bottom:1px solid #eee"><td style="padding:12px 0;color:#666;font-size:13px;text-transform:uppercase;letter-spacing:1px">Телефон</td><td style="padding:12px 0;color:#1a1a1a;font-size:15px;font-weight:bold"><a href="tel:{phone}" style="color:#1a1a1a;text-decoration:none">{phone}</a></td></tr>
      {company_row}{message_row}
    </table>
  </div>
  <p style="color:#999;font-size:12px;margin-top:16px;text-align:center">Заявка поступила {now}</p>
</div>"""

    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"Новая заявка #{lead_id} от {name}" + (f" ({company})" if company else "")
    msg["From"] = f"АвтоВорота <{from_email}>"
    msg["To"] = to_email
    msg.attach(MIMEText(f"Заявка #{lead_id}\nИмя: {name}\nТелефон: {phone}" + (f"\nКомпания: {company}" if company else "") + (f"\nСообщение: {message}" if message else ""), "plain", "utf-8"))
    msg.attach(MIMEText(html, "html", "utf-8"))

    with smtplib.SMTP_SSL(smtp_host, 465) as server:
        server.login(smtp_user, smtp_password)
        server.sendmail(from_email, to_email, msg.as_string())


def handler(event, context):
    """Принимает заявку с сайта, сохраняет в БД и отправляет email-уведомление."""
    cors = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type",
    }

    if event.get("httpMethod") == "OPTIONS":
        return {"statusCode": 204, "headers": cors, "body": ""}

    if event.get("httpMethod") != "POST":
        return {"statusCode": 405, "headers": {"Content-Type": "application/json", **cors}, "body": json.dumps({"error": "Method not allowed"})}

    try:
        body = json.loads(event.get("body") or "{}")
    except Exception:
        return {"statusCode": 400, "headers": {"Content-Type": "application/json", **cors}, "body": json.dumps({"error": "Invalid JSON"})}

    name = (body.get("name") or "").strip()
    phone = (body.get("phone") or "").strip()
    company = (body.get("company") or "").strip()
    message = (body.get("message") or "").strip()

    if not name or not phone:
        return {"statusCode": 400, "headers": {"Content-Type": "application/json", **cors}, "body": json.dumps({"error": "Имя и телефон обязательны"})}

    try:
        lead_id = save_lead(name, phone, company, message)
        print(f"Lead saved: id={lead_id}, name={name}, phone={phone}")
    except Exception as e:
        print(f"DB error: {e}")
        return {"statusCode": 500, "headers": {"Content-Type": "application/json", **cors}, "body": json.dumps({"error": "Ошибка сохранения заявки"})}

    try:
        send_email(lead_id, name, phone, company, message)
        print(f"Email sent for lead #{lead_id}")
    except Exception as e:
        print(f"Email error (lead saved): {e}")

    return {"statusCode": 200, "headers": {"Content-Type": "application/json", **cors}, "body": json.dumps({"success": True, "id": lead_id})}
