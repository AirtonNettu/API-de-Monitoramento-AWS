def classificar_utilizacao_cpu(utilizacao_cpu: float) -> str:
    if utilizacao_cpu >= 90:
        return "critico"
    elif utilizacao_cpu >= 70:
        return "alerta"
    else:
        return "normal"


def analisar_memoria_ram(
    memoria_total_mb: int,
    memoria_usada_mb: int,
) -> dict[str, int | float | str]:
    if memoria_total_mb <= 0:
        raise ValueError("A memória total deve ser maior que zero.")

    if memoria_usada_mb < 0:
        raise ValueError("A memória usada não pode ser negativa.")

    if memoria_usada_mb > memoria_total_mb:
        raise ValueError(
            "A memória usada não pode superar a memória total."
        )

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
        "memoria_total_mb": memoria_total_mb,
        "memoria_usada_mb": memoria_usada_mb,
        "memoria_livre_mb": memoria_livre_mb,
        "percentual_utilizado": percentual_utilizado,
        "classificacao": classificacao,
    }