from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
import json
import requests
from datetime import datetime
import pandas as pd
from fpdf import FPDF

app = FastAPI(title="Consulta DirectData")

# Configura templates e arquivos estáticos
BASE_DIR = os.path.dirname(__file__)
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")

HISTORY_PATH = os.path.join(BASE_DIR, "data", "history.json")


def load_history():
    if os.path.exists(HISTORY_PATH):
        with open(HISTORY_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_history(history):
    os.makedirs(os.path.dirname(HISTORY_PATH), exist_ok=True)
    with open(HISTORY_PATH, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)


def call_directd(chave: str):
    """Consulta a API do DirectData. Se a chave de API não estiver
    configurada, retorna dados de demonstração."""
    api_key = os.getenv("DIRECTD_API_KEY")
    base_url = os.getenv("DIRECTD_BASE_URL", "https://app.directd.com.br/api")
    if api_key:
        params = {"chave": chave, "token": api_key}
        try:
            r = requests.get(f"{base_url}/buscar", params=params, timeout=30)
            r.raise_for_status()
            return r.json()
        except Exception as exc:  # pragma: no cover
            return {"erro": str(exc)}

    # Dados fictícios para demonstração
    return {
        "nome": "João da Silva",
        "documento": chave,
        "endereco": "Rua Exemplo, 123",
        "renda": 5000,
        "societario": ["Empresa A", "Empresa B"],
        "empregos": ["Emprego A", "Emprego B"],
        "processos": 2,
        "score": 750,
        "risco": "Baixo",
        "regiao": "SP",
    }


@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/api/busca")
async def busca(chave: str):
    data = call_directd(chave)
    history = load_history()
    entry = {"chave": chave, "data": data, "data_hora": datetime.utcnow().isoformat()}
    history.append(entry)
    save_history(history)
    return data


@app.get("/api/historico")
async def historico():
    return load_history()


@app.get("/api/export/pdf")
async def export_pdf(chave: str):
    data = call_directd(chave)
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for k, v in data.items():
        pdf.multi_cell(0, 10, txt=f"{k}: {v}")
    file_path = f"/tmp/{chave}.pdf"
    pdf.output(file_path)
    return FileResponse(file_path, media_type="application/pdf", filename=f"{chave}.pdf")


@app.get("/api/export/excel")
async def export_excel(chave: str):
    data = call_directd(chave)
    df = pd.DataFrame(list(data.items()), columns=["Campo", "Valor"])
    file_path = f"/tmp/{chave}.xlsx"
    df.to_excel(file_path, index=False)
    return FileResponse(
        file_path,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        filename=f"{chave}.xlsx",
    )

