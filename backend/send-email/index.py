import json
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime


def handler(request):
    # Handle CORS preflight
    if request.method == "OPTIONS":
        return {
            "statusCode": 204,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "POST, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type",
            },
            "body": "",
        }

    if request.method != "POST":
        return {
            "statusCode": 405,
            "headers": {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"},
            "body": json.dumps({"error": "Method not allowed"}),
        }

    try:
        body = request.json()
    except Exception:
        return {
            "statusCode": 400,
            "headers": {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"},
            "body": json.dumps({"error": "Invalid JSON"}),
        }

    name = body.get("name", "").strip()
    phone = body.get("phone", "").strip()
    company = body.get("company", "").strip()
    message = body.get("message", "").strip()

    if not name or not phone:
        return {
            "statusCode": 400,
            "headers": {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"},
            "body": json.dumps({"error": "Имя и телефон обязательны"}),
        }

    smtp_host = os.environ.get("SMTP_HOST")
    smtp_user = os.environ.get("SMTP_USER")
    smtp_password = os.environ.get("SMTP_PASSWORD")
    from_email = os.environ.get("SMTP_FROM_EMAIL")
    to_email = os.environ.get("SMTP_TO_EMAIL")

    if not all([smtp_host, smtp_user, smtp_password, from_email, to_email]):
        print("Missing SMTP configuration")
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"},
            "body": json.dumps({"error": "Ошибка конфигурации сервера"}),
        }

    now = datetime.now().strftime("%d.%m.%Y %H:%M")

    company_row = f"""
          <tr style="border-bottom: 1px solid #eee;">
            <td style="padding: 12px 0; color: #666; font-size: 13px; text-transform: uppercase; letter-spacing: 1px; width: 140px;">Компания</td>
            <td style="padding: 12px 0; color: #1a1a1a; font-size: 15px;">{company}</td>
          </tr>""" if company else ""

    message_row = f"""
          <tr>
            <td style="padding: 12px 0; color: #666; font-size: 13px; text-transform: uppercase; letter-spacing: 1px; vertical-align: top;">Сообщение</td>
            <td style="padding: 12px 0; color: #1a1a1a; font-size: 15px; line-height: 1.6;">{message.replace(chr(10), '<br>')}</td>
          </tr>""" if message else ""

    html_content = f"""
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; background: #f9f9f9;">
      <div style="background: #1a1a1a; padding: 24px; margin-bottom: 24px;">
        <h1 style="color: #ffffff; margin: 0; font-size: 24px; letter-spacing: 2px;">АВТОВОРОТА</h1>
        <p style="color: #999; margin: 4px 0 0; font-size: 12px; text-transform: uppercase; letter-spacing: 1px;">Новая заявка с сайта</p>
      </div>
      <div style="background: #ffffff; padding: 24px; border-left: 4px solid #1a1a1a;">
        <table style="width: 100%; border-collapse: collapse;">
          <tr style="border-bottom: 1px solid #eee;">
            <td style="padding: 12px 0; color: #666; font-size: 13px; text-transform: uppercase; letter-spacing: 1px; width: 140px;">Имя</td>
            <td style="padding: 12px 0; color: #1a1a1a; font-size: 15px; font-weight: bold;">{name}</td>
          </tr>
          <tr style="border-bottom: 1px solid #eee;">
            <td style="padding: 12px 0; color: #666; font-size: 13px; text-transform: uppercase; letter-spacing: 1px;">Телефон</td>
            <td style="padding: 12px 0; color: #1a1a1a; font-size: 15px; font-weight: bold;"><a href="tel:{phone}" style="color: #1a1a1a; text-decoration: none;">{phone}</a></td>
          </tr>
          {company_row}
          {message_row}
        </table>
      </div>
      <p style="color: #999; font-size: 12px; margin-top: 16px; text-align: center;">
        Заявка поступила {now}
      </p>
    </div>
    """

    text_content = f"Новая заявка:\nИмя: {name}\nТелефон: {phone}"
    if company:
        text_content += f"\nКомпания: {company}"
    if message:
        text_content += f"\nСообщение: {message}"

    subject = f"Новая заявка от {name}"
    if company:
        subject += f" ({company})"

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = f"АвтоВорота <{from_email}>"
    msg["To"] = to_email

    msg.attach(MIMEText(text_content, "plain", "utf-8"))
    msg.attach(MIMEText(html_content, "html", "utf-8"))

    try:
        with smtplib.SMTP_SSL(smtp_host, 465) as server:
            server.login(smtp_user, smtp_password)
            server.sendmail(from_email, to_email, msg.as_string())

        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"},
            "body": json.dumps({"success": True, "message": "Заявка успешно отправлена"}),
        }
    except Exception as e:
        print(f"Email send error: {e}")
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"},
            "body": json.dumps({"error": "Ошибка отправки письма"}),
        }
