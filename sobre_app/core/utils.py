def heure_to_minutes(hhmm):
    # '22:30' -> 1350
    h, m = map(int, hhmm.split(':'))
    return h * 60 + m

def format_duree(minutes):
    # 80 -> 'dans 1h 20min'
    h = minutes // 60
    m = minutes % 60
    if h > 0:
        return f"dans {h}h {m}min" if m > 0 else f"dans {h}h"
    else:
        return f"dans {m}min"

# Valeurs moyennes d'alcool pur par type (en g/cl)
ALCOOL_GRAMMES_PAR_CL = {
    'Bière': 0.4,      # 25cl à 5% = 10g
    'Vin': 0.8,        # 12cl à 12% = 9.6g
    'Spiritueux': 0.32 # 4cl à 40% = 12.8g
}

def cl_to_grammes(type_alcool, volume_cl):
    coef = ALCOOL_GRAMMES_PAR_CL.get(type_alcool, 0.8)
    return coef * volume_cl
