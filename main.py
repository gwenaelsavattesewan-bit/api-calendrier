from datetime import date

from fastapi import FastAPI

app = FastAPI(title="API Calendrier")


@app.get("/api/v1/date")
def get_date():
    aujourd_hui = date.today()

    return {
        "date": aujourd_hui.isoformat(),
        "mois": aujourd_hui.month,
        "semaine": aujourd_hui.isocalendar().week,
        "quantieme": aujourd_hui.timetuple().tm_yday
    }