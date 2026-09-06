from typing import Annotated

from fastapi import FastAPI, HTTPException, Path

from app.servicos.monitoramento import (
    analisar_memoria_ram,
    classificar_utilizacao_cpu,
)


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
        title="Utilização da CPU",
        description="Percentual atual de utilização da CPU.",
        examples=[75.0],
    ),
]


MemoriaTotalMB = Annotated[
    int,
    Path(
        gt=0,
        title="Memória total",
        description="Quantidade total de memória RAM em MB.",
        examples=[1024],
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
    "/saude",
    summary="Verificar saúde da API",
    response_description="Estado atual da API",
)
def verificar_saude() -> dict[str, str]:
    return {
        "status": "online",
    }


@app.get(
    "/cpu/{utilizacao_cpu}",
    summary="Classificar utilização da CPU",
    response_description="Classificação atual da utilização da CPU",
)
def verificar_cpu(
    utilizacao_cpu: PercentualCPU,
) -> dict[str, float | str]:
    classificacao = classificar_utilizacao_cpu(
        utilizacao_cpu,
    )

    resposta: dict[str, float | str] = {
        "utilizacao_cpu": utilizacao_cpu,
        "classificacao": classificacao,
    }

    return resposta


@app.get(
    "/memoria/{memoria_total_mb}/{memoria_usada_mb}",
    summary="Analisar utilização da memória RAM",
    response_description="Informações sobre a utilização da memória RAM",
)
def verificar_memoria_ram(
    memoria_total_mb: MemoriaTotalMB,
    memoria_usada_mb: MemoriaUsadaMB,
) -> dict[str, int | float | str]:
    try:
        resposta = analisar_memoria_ram(
            memoria_total_mb,
            memoria_usada_mb,
        )

        return resposta

    except ValueError as erro:
        raise HTTPException(
            status_code=400,
            detail=str(erro),
        ) from erro