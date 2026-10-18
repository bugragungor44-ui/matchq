from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from zoneinfo import ZoneInfo
from pathlib import Path

app = FastAPI(title="Match Q")
engine = create_engine("sqlite:///matchq.db", connect_args={"check_same_thread": False})
Base = declarative_base()
Session = sessionmaker(bind=engine)
TZ = ZoneInfo("Europe/Istanbul")

class Analysis(Base):
    __tablename__ = "analyses"
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime)
    category = Column(String)
    summary = Column(String)
    odds = Column(Float, nullable=True)

Base.metadata.create_all(engine)

def daily_job():
    # Gerçek maç/oran API'si bağlanmadan tahmin uydurulmaz.
    with Session() as db:
        db.add(Analysis(created_at=datetime.now(TZ).replace(tzinfo=None),
                        category="sistem", summary="Günlük görev çalıştı; canlı veri kaynağı bekleniyor."))
        db.commit()

scheduler = BackgroundScheduler(timezone=TZ)
scheduler.add_job(daily_job, "cron", hour=10, minute=0, id="daily_analysis", replace_existing=True)
scheduler.start()

@app.get("/")
def home():
    return FileResponse(Path(__file__).parent / "index.html")

@app.get("/api/status")
def status():
    with Session() as db:
        records = db.query(Analysis).order_by(Analysis.id.desc()).limit(10).all()
        return {"app":"Match Q","timezone":"Europe/Istanbul","daily_run":"10:00",
                "live_data_connected":False,
                "history":[{"time":str(x.created_at),"message":x.summary} for x in records]}

@app.get("/api/plans")
def plans():
    return [{"name":"Standart","monthly_try":100},{"name":"Premium","monthly_try":250},{"name":"VIP","monthly_try":400}]
import os
import requests

API_SPORTS_KEY = os.getenv("API_SPORTS_KEY")

@app.get("/api/football/live")
def get_live_football():
    if not API_SPORTS_KEY:
        return {"error": "API anahtarı bulunamadı"}

    url = "https://v3.football.api-sports.io/fixtures"

    headers = {
        "x-apisports-key": API_SPORTS_KEY
    }

    params = {
        "live": "all"
    }

    try:
        response = requests.get(
            url,
            headers=headers,
            params=params,
            timeout=15
        )
        response.raise_for_status()
        return response.json()

    except requests.RequestException as e:
        return {"error": str(e)}

@app.get("/{page_name}.html")
def html_page(page_name: str):
    allowed_pages = {
        "index",
        "mac-merkezi",
        "analiz",
        "tahminler",
        "kuponlar",
        "uyelik",
        "giris",
        "admin",
    }

    if page_name not in allowed_pages:
        raise HTTPException(status_code=404, detail="Sayfa bulunamadi")

    return FileResponse(
        Path(__file__).parent / f"{page_name}.html",
        media_type="text/html"
    )
