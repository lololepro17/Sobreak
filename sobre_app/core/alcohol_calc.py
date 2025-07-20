from .utils import heure_to_minutes, cl_to_grammes

def widmark(conso, poids, sexe, a_jeun):
    # conso : dict {type, volume, heure}
    # poids : en kg
    # sexe : 'Homme' ou 'Femme'
    # a_jeun : 'Oui' ou 'Non'
    r = 0.7 if sexe == 'Homme' else 0.6
    coef_jeun = 1.1 if a_jeun == 'Oui' else 1.0
    grammes = cl_to_grammes(conso['type'], float(conso['volume']))
    alcool = (grammes / (poids * r)) * coef_jeun
    return alcool

def courbe_alcoolemie(consommations, poids, sexe, a_jeun, heure_debut, taux_elimination=0.15):
    # consommations : liste de dicts {type, volume, heure}
    # heure_debut : heure de la première conso (en minutes depuis minuit)
    # Retourne une liste de tuples (minute, taux)
    points = []
    taux = 0
    timeline = {}
    for c in consommations:
        t = heure_to_minutes(c['heure'])
        a = widmark(c, poids, sexe, a_jeun)
        timeline.setdefault(t, 0)
        timeline[t] += a
    # On simule minute par minute
    minute = min(timeline.keys())
    max_minute = max(timeline.keys()) + 12*60  # 12h max
    taux = 0
    pic = 0
    pic_time = minute
    while minute <= max_minute and taux > 0 or minute == min(timeline.keys()):
        if minute in timeline:
            taux += timeline[minute]
        if taux > pic:
            pic = taux
            pic_time = minute
        points.append((minute, max(taux, 0)))
        taux -= taux_elimination / 60  # 0.15g/h => par minute
        if taux < 0:
            taux = 0
        minute += 1
    return points, pic, pic_time

def temps_retour_zero(points):
    # points : liste (minute, taux)
    for minute, taux in points:
        if taux <= 0:
            return minute
    return points[-1][0]  # dernier minute si jamais à 0
