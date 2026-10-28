"""API FastAPI : /health, /predict."""

from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse

from api import model
from api.schemas import HealthResponse, PredictRequest, PredictResponse


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Charge le modèle au démarrage. Refuse de démarrer s'il manque."""
    model.charger_modele()  # lève FileNotFoundError si le modèle est absent
    yield


app = FastAPI(title="Sentiment API", lifespan=lifespan)


@app.get("/", include_in_schema=False)
def racine():
    return RedirectResponse(url="/docs")


@app.get("/health", response_model=HealthResponse)
def health():
    return HealthResponse(status="OK", model="tfidf-logreg (TP2, models/sentiment.joblib)")


@app.post("/predict", response_model=PredictResponse)
def predict_route(req: PredictRequest):
    try:
        return model.predict(req.text)
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=500, detail="Erreur interne de l'API") from None



if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)