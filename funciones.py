import re

def es_patente_valida(patente):
    if re.match(r"[A-Z]{2}+\d{3}+[A-Z]{2}", patente):
        return True
    elif re.match(r"[A-Z]{3}+\d{3}", patente):
        return True
    else:
        return False