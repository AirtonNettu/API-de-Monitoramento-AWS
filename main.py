from typing import Annotated

from fastapi import FastAPI, HTTPException, Path



app = FastAPI(
    title="API de Monitoramento AWS",
    description="API REST para monitoramento de recursos computacionais.",
    version="0.1.0",
)


PercentualCPU = Annotated[
    float,
    Path(
        ge=0,
        le=100,
        title="Ultilização de CPU",
        description="Percentual atual de utilização de CPU",
        examples=[75.0],
    ),
]

def classificar_utilizacao_cpu(utilizacao_cpu: float) -> str:
    if utilizacao_cpu >= 90:
        return "critico"
    elif utilizacao_cpu >= 70:
        return "alerta"
    else:
        return "normal"


@app.get("/saude", summary="Verificar saúde da API")
def verificar_saude() -> dict[str, str]:
    return {"status": "online"}


@app.get(
    "/cpu/{utilizacao_cpu}",
    summary="Classificar utilização da CPU",
    response_description="Classificação atual da utilização da CPU"
)


def verificar_cpu(
    utilizacao_cpu: PercentualCPU,
) -> dict[str, float | str]:
    classificacao = classificar_utilizacao_cpu(utilizacao_cpu)

    resposta: dict[str, float | str] = {
        "utilizacao_cpu": utilizacao_cpu,
        "classificacao": classificacao,
    }

    return resposta


def analisar_memoria_ram(
        memoria_total_mb: int,
        memoria_usada_mb: int,
) -> dict[str, int | float | str]:
    if memoria_total_mb <= 0:
        raise ValueError("A memória total deve ser maior que zero.")
    if memoria_usada_mb < 0:
        raise ValueError("A memória usada não pode ser negativa.")
    if memoria_usada_mb > memoria_total_mb:
        raise ValueError("A memória usada não pode superar a memória total.")

    memoria_livre_mb = memoria_total_mb - memoria_usada_mb

    percentual_utilizado = round(
        memoria_usada_mb / memoria_total_mb * 100, 
        2,
    )


    if percentual_utilizado >= 90:
        classificacao = "critico"
    elif percentual_utilizado >= 70:
        classificacao = "alerta"
    else:
        classificacao = "normal"

    return {
        "memoria_total_mb":memoria_total_mb,
        "memoria_usada_mb":memoria_usada_mb,
        "memoria_livre_mb": memoria_livre_mb,
        "percentual_utilizado": percentual_utilizado,
        "classificacao": classificacao,
    }

MemoriaTotalMB = Annotated[
    int,
    Path(
        gt=0,
        title="Memória total",
        description="Quantidade total de memória RAM em MB.",
        example=[1024],
    ),
]

MemoriaUsadaMB = Annotated[
    int,
    Path(
        ge=0,
        title="Memória utilizada",
        description="Quantidade de memória RAM utilizada em MB.",
        examples=[768],
    ),
]

@app.get(
    "/memoria/{memoria_total_mb}/{memoria_usada_mb}",
    summary="Analisar utilização da memória RAM",
    response_description="Informações sobre o utilização da Memória RAM",
)

def verificar_memoria_ram(
    memoria_total_mb: MemoriaTotalMB,
    memoria_usada_mb: MemoriaUsadaMB,
) -> dict[str, int | float| str]:
    try:
        resposta = analisar_memoria_ram(
            memoria_total_mb,
            memoria_usada_mb,
        )

        return resposta

    except ValueError as erro:
        raise HTTPException(
            status_code=400,
            details=str(erro),
        ) from erro