import re

def parse_partner_reply(text):

    # Markdown hatao
    text = text.replace("**", "")

    data = {
        "trader_id": "",
        "country": "",
        "deposit": 0.0,
        "deposit_count": 0,
        "link_id": ""
    }

    m = re.search(r"Trader\s*#\s*(\d+)", text)
    if m:
        data["trader_id"] = m.group(1)

    m = re.search(r"Country:\s*(.+)", text)
    if m:
        data["country"] = m.group(1).strip()

    m = re.search(r"Link\s*Id:\s*(\d+)", text)
    if m:
        data["link_id"] = m.group(1)

    m = re.search(r"Deposits\s*Count:\s*(\d+)", text)
    if m:
        data["deposit_count"] = int(m.group(1))

    m = re.search(r"Deposits\s*Sum:\s*\$\s*([\d.]+)", text)
    if m:
        data["deposit"] = float(m.group(1))

    return data