from datetime import datetime

def format_date(d: str):
    if d is None or len(d.strip()) == 0:
        return ""

    try:
        parse = datetime.strptime(d.strip(), "%d de %B, %Y às %H:%M")
        return datetime.strftime(parse, "%Y-%m-%d %H:%M:%S")
    except Exception:
        pass