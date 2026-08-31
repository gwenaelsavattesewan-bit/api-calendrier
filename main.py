import calendar
from datetime import date, datetime
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import holidays
from vacances_scolaires_france import SchoolHolidayDates  # <--- Import de la bibliothèque

app = FastAPI(title="Mon API Calendrier")

# On instancie le gestionnaire de vacances scolaires
school_holidays = SchoolHolidayDates()

def calculer_infos_date(date_cible: date):
    jours_semaine = [
        "lundi",
        "mardi",
        "mercredi",
        "jeudi",
        "vendredi",
        "samedi",
        "dimanche",
    ]
    nom_jour = jours_semaine[date_cible.weekday()]
    annee_iso, semaine_iso, jour_iso = date_cible.isocalendar()
    quantieme = date_cible.timetuple().tm_yday
    est_bissextile = calendar.isleap(date_cible.year)
    jours_total = 366 if est_bissextile else 365

    # Jours fériés
    feries_france = holidays.France(years=date_cible.year)
    est_ferie = date_cible in feries_france
    nom_ferie = feries_france.get(date_cible)

    # --- NOUVEAU : Vacances scolaires par zone ---
    vacances_a = school_holidays.is_holiday_for_zone(date_cible, "A")
    vacances_b = school_holidays.is_holiday_for_zone(date_cible, "B")
    vacances_c = school_holidays.is_holiday_for_zone(date_cible, "C")

    return {
        "date": date_cible.isoformat(),
        "jour": nom_jour,
        "mois": date_cible.month,
        "semaine": semaine_iso,
        "quantieme": quantieme,
        "jours_dans_annee": jours_total,
        "est_ferie": est_ferie,
        "nom_ferie": nom_ferie,
        "vacances_scolaires": {
            "zone_a": vacances_a,
            "zone_b": vacances_b,
            "zone_c": vacances_c,
        },
    }


# ==========================================
# ENDPOINTS
# ==========================================


@app.get("/api/date")
def obtenir_date_du_jour():
    aujourd_hui = date.today()
    return calculer_infos_date(aujourd_hui)


@app.get("/api/date/{date_texte}")
def obtenir_date_precise(date_texte: str):
    try:
        date_convertie = datetime.strptime(date_texte, "%Y-%m-%d").date()
        return calculer_infos_date(date_convertie)
    except ValueError:
        return JSONResponse(
            status_code=400,
            content={
                "error": True,
                "message": "Date invalide. Utilisez le format AAAA-MM-JJ.",
            },
        )
