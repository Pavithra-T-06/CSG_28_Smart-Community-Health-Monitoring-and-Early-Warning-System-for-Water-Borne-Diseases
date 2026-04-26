import requests
import smtplib
from email.mime.text import MIMEText

# ---------------- CONFIG ----------------
BOT_TOKEN = "8770727550:AAGjaDQcR1a9UvPM4086LZBv2a-gCKrIjFg"
CHAT_IDS = ["5047255761"]

SENDER_EMAIL = "pavithrat0441@gmail.com"
SENDER_PASSWORD = "piru hmmp nexv mnxl"
RECEIVER_EMAILS = ["aravindachar2004@gmail.com"]

# ---------------- TELEGRAM ----------------
def send_telegram(message):
    if not BOT_TOKEN or "YOUR" in BOT_TOKEN:
        print("⚠ Telegram not configured")
        return

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    for chat_id in CHAT_IDS:
        try:
            res = requests.get(url, params={"chat_id": chat_id, "text": message})
            print("Telegram:", res.json())
        except Exception as e:
            print("Telegram error:", e)

# ---------------- EMAIL ----------------
def send_email(subject, body):
    if not SENDER_EMAIL or "your_" in SENDER_EMAIL:
        print("⚠ Email not configured")
        return

    try:
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = SENDER_EMAIL
        msg["To"] = ", ".join(RECEIVER_EMAILS)

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAILS, msg.as_string())
        server.quit()

        print("Email sent")

    except Exception as e:
        print("Email error:", e)

# ---------------- SCIENTIFIC SEVERITY ----------------
def calculate_severity(ph, turbidity, tds, coliform):
    # pH deviation
    ph_score = 0
    if ph < 6.5:
        ph_score = min((6.5 - ph) / 3, 1)
    elif ph > 8.5:
        ph_score = min((ph - 8.5) / 3, 1)

    # TDS (>500 unsafe)
    tds_score = min(max((tds - 500) / 1000, 0), 1)

    # Turbidity (>5 unsafe)
    turb_score = min(max((turbidity - 5) / 20, 0), 1)

    # Coliform (any presence bad)
    coliform_score = min(coliform / 50, 1)

    severity = (
        0.35 * coliform_score +
        0.25 * ph_score +
        0.20 * turb_score +
        0.20 * tds_score
    )

    return round(severity * 100, 2)

# ---------------- MAIN ALERT ----------------
def check_and_alert(community, risk, data):
    ph, turbidity, tds, coliform, rainfall, temperature = data

    issues = []
    actions = []

    # ---------------- ISSUES ----------------
    if coliform > 0:
        issues.append("Bacterial contamination")

    if ph < 6.5 or ph > 8.5:
        issues.append("Unsafe pH")

    if turbidity > 5:
        issues.append("High turbidity")

    if tds > 500:
        issues.append("High TDS")

    # ---------------- ACTIONS ----------------
    if risk.lower() == "high":
        actions = [
            "Do NOT consume water.",
            "Boil or treat immediately."
        ]
    elif risk.lower() == "medium":
        actions = ["Boil or filter before use."]
    else:
        actions = ["Safe for consumption."]

    issues_text = ", ".join(issues) if issues else "No major issues detected"

    # ---------------- SEVERITY ----------------
    severity = calculate_severity(ph, turbidity, tds, coliform)

    if severity >= 80:
        severity_label = "CRITICAL"
    elif severity >= 60:
        severity_label = "HIGH"
    elif severity >= 30:
        severity_label = "MODERATE"
    else:
        severity_label = "LOW"

    # ---------------- MESSAGE ----------------
    message = f"""
🚨 {risk.upper()} RISK ALERT

📍 Community: {community}

⚠ Issues:
{issues_text}

📊 Readings:
- pH: {ph:.2f}
- TDS: {tds:.2f}
- Turbidity: {turbidity:.2f}
- Coliform: {coliform:.2f}

🔥 Severity Score: {severity} ({severity_label})

💧 Action:
""" + "\n".join(actions)

    # ---------------- SEND ----------------
    send_telegram(message)
    send_email(f"{risk} Risk Alert - {community}", message)

def send_health_alert(community, cases):
    message = f"""
🚨 HEALTH ALERT

Community: {community}
Cases: {cases}

Possible outbreak detected. Immediate attention required.
"""

    send_telegram(message)
    send_email("Health Alert", message)

