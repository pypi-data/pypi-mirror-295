#module1.py
def calculate_bonds(valor_face=1000, taxa_cupom=0.08, vencimento=10, maturidade=0.1, capitalizacao=2):
    
    periodos_semestrais = vencimento * capitalizacao

    # Taxas semestrais equivalentes, já que os valores estão anualizados
    taxa_cupom_semestral = (1 + taxa_cupom) ** (1 / capitalizacao) - 1
    maturidade_semestral = (1 + maturidade) ** (1 / capitalizacao) - 1

    # Pagamento semestral de cupom
    pagamento_semestral_cupom = valor_face * taxa_cupom_semestral

    preco_titulo = 0

    # Calcular o valor presente dos cupons
    for t in range(1, periodos_semestrais + 1):
        preco_titulo += pagamento_semestral_cupom / (1 + maturidade_semestral) ** t

    # Adicionar o valor presente do valor de face
    preco_titulo += valor_face / (1 + maturidade_semestral) ** periodos_semestrais

    return preco_titulo
