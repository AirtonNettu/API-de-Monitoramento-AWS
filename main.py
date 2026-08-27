from fastapi import FastAPI

app = FastAPI()

def classificar_utilizacao_cpu(utilizacao_cpu: float) -> str:
    if utilizacao_cpu >= 90:
        return "critico"
    elif utilizacao_cpu >= 70:
        return "alerta"
    else:
        return "normal"

@app.get("/saude")
def verificar_saude():
    return {"status": "online"}

@app.get("/cpu/{utilizacao_cpu}")
def verificar_cpu(utilizacao_cpu: float):
    classificacao = classificar_utilizacao_cpu(utilizacao_cpu)

    return {
        "utilizacao_cpu": utilizacao_cpu,
        "classificacao": classificacao,
    }