"""Gera um relatório HTML para uma semana de entradas do funil.

Sem --referencia, usa a semana atual. Quando informada, usa a semana que
contém a data de referência.
"""

import argparse
import logging
import math
import os
from datetime import date, datetime, timedelta
from html import escape
from pathlib import Path
import re
import sys
import tempfile
import unicodedata

import pandas as pd


RAIZ = Path(__file__).resolve().parent.parent
COLUNAS_ESSENCIAIS = {
    "id_proposta", "data_entrada", "canal_origem", "tipo_imovel",
    "valor_imovel", "valor_solicitado", "etapa_max_funil", "status_final",
}
COLUNAS_OPCIONAIS = {
    "cidade", "uf", "prazo_meses", "score_credito", "idade_cliente",
    "renda_mensal_declarada", "flag_cliente_recorrente", "consultor_id",
    "tempo_analise_dias", "data_assinatura_contrato", "taxa_juros_aa",
}
CANAIS = {
    "correspondente": "Correspondente", "organico": "Orgânico",
    "midia paga": "Mídia paga", "indicacao": "Indicação", "parceria": "Parceria",
}
STATUS = {
    "contratada": "Contratada", "desistiu": "Desistiu",
    "sem retorno": "Sem retorno", "reprovada credito": "Reprovada crédito",
    "problema garantia": "Problema garantia",
    "documentacao pendente": "Documentação pendente",
}


class DadosInvalidos(ValueError):
    """Entrada incompleta ou ambígua: a execução deve parar sem criar relatório."""


def chave(texto):
    texto = " ".join(str(texto).split()).casefold()
    texto = unicodedata.normalize("NFKD", texto)
    return "".join(c for c in texto if not unicodedata.combining(c))


def moeda(numero):
    return "R$ " + f"{numero:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def percentual(numero):
    return "—" if pd.isna(numero) else f"{numero * 100:.1f}%".replace(".", ",")


def caminho(argumento):
    destino = Path(argumento).expanduser()
    return destino if destino.is_absolute() else RAIZ / destino


def carregar_csv(arquivo, log):
    if not arquivo.is_file():
        raise DadosInvalidos(f"Arquivo não encontrado: {arquivo}")
    with arquivo.open("r", encoding="utf-8-sig", newline="") as f:
        cabecalho = f.readline()
    separador = ";" if cabecalho.count(";") > cabecalho.count(",") else ","
    log.info("Lendo %s com separador %r", arquivo, separador)
    bruto = pd.read_csv(
        arquivo, sep=separador, encoding="utf-8-sig", dtype=str,
        keep_default_na=False, on_bad_lines="error",
    )
    bruto.columns = bruto.columns.str.strip()
    if bruto.columns.duplicated().any():
        raise DadosInvalidos("Há nomes de colunas repetidos no CSV")
    ausentes = sorted(COLUNAS_ESSENCIAIS - set(bruto.columns))
    if ausentes:
        raise DadosInvalidos(f"Colunas essenciais ausentes: {', '.join(ausentes)}")
    opcionais_ausentes = sorted(COLUNAS_OPCIONAIS - set(bruto.columns))
    if opcionais_ausentes:
        log.warning("Colunas opcionais ausentes: %s", ", ".join(opcionais_ausentes))
    extras = sorted(set(bruto.columns) - COLUNAS_ESSENCIAIS - COLUNAS_OPCIONAIS)
    if extras:
        log.info("Colunas adicionais preservadas, não necessárias no relatório: %s", ", ".join(extras))
    if bruto.empty:
        raise DadosInvalidos("O CSV contém cabeçalho, mas nenhuma proposta")
    log.info("CSV carregado: %s linhas e %s colunas", len(bruto), len(bruto.columns))
    return bruto, separador, opcionais_ausentes


def numero_bruto(valor):
    texto = str(valor).strip().replace("R$", "").replace("\u00a0", "").replace(" ", "")
    if not texto:
        return math.nan
    if "," in texto and "." in texto:
        texto = texto.replace(".", "").replace(",", ".") if texto.rfind(",") > texto.rfind(".") else texto.replace(",", "")
    elif "," in texto:
        texto = texto.replace(",", ".")
    try:
        return float(texto)
    except ValueError:
        return math.nan


def exigir_valido(serie, nome, df, positivo=False):
    invalidos = serie.isna() | ~serie.map(math.isfinite)
    if positivo:
        invalidos |= serie <= 0
    if invalidos.any():
        ids = df.loc[invalidos, "id_proposta"].head(5).tolist()
        raise DadosInvalidos(f"{nome} inválido em {int(invalidos.sum())} propostas; exemplos: {ids}")


def tratar(bruto, log):
    dados = bruto.copy()
    dados["id_proposta"] = dados.id_proposta.str.strip()
    if dados.id_proposta.eq("").any() or dados.id_proposta.duplicated().any():
        raise DadosInvalidos("id_proposta vazio ou repetido; não é seguro contar propostas")

    datas_iso = pd.to_datetime(dados.data_entrada, format="%Y-%m-%d", errors="coerce")
    datas_br = pd.to_datetime(dados.data_entrada, format="%d/%m/%Y", errors="coerce")
    dados["entrada"] = datas_iso.fillna(datas_br)
    if dados.entrada.isna().any():
        ids = dados.loc[dados.entrada.isna(), "id_proposta"].head(5).tolist()
        raise DadosInvalidos(f"data_entrada em formato desconhecido; exemplos: {ids}")

    for coluna in ("valor_imovel", "valor_solicitado"):
        dados[coluna + "_num"] = dados[coluna].map(numero_bruto)
        exigir_valido(dados[coluna + "_num"], coluna, dados, positivo=True)

    etapa = pd.to_numeric(dados.etapa_max_funil, errors="coerce")
    exigir_valido(etapa, "etapa_max_funil", dados)
    if (etapa % 1 != 0).any():
        raise DadosInvalidos("etapa_max_funil contém valores não inteiros")
    dados["etapa"] = etapa.astype(int)
    dados["etapa_invalida"] = ~dados.etapa.between(1, 6)

    for origem, destino, mapa in (
        ("canal_origem", "canal", CANAIS), ("status_final", "status", STATUS)
    ):
        chaves = dados[origem].map(chave)
        desconhecidos = sorted(set(chaves) - set(mapa))
        if desconhecidos:
            raise DadosInvalidos(f"Novas categorias em {origem}: {desconhecidos}; revisar mapeamento")
        dados[destino] = chaves.map(mapa)

    dados["tipo_imovel_limpo"] = dados.tipo_imovel.str.strip()
    terreno = dados.tipo_imovel_limpo.map(chave).eq("terreno")
    qualidade = {
        "brutas": len(dados),
        "terrenos": int(terreno.sum()),
        "datas_br": int(datas_iso.isna().sum()),
        "valores_com_prefixo": int(dados.valor_imovel.str.contains("R$", regex=False).sum()),
        "canais_normalizados": int(dados.canal_origem.ne(dados.canal).sum()),
        "etapas_invalidas": int(dados.etapa_invalida.sum()),
    }
    if "idade_cliente" in dados:
        idades = pd.to_numeric(dados.idade_cliente, errors="coerce")
        qualidade["idades_menores_18"] = int((idades < 18).sum())
    if "data_assinatura_contrato" in dados:
        assinaturas = pd.to_datetime(dados.data_assinatura_contrato, format="%Y-%m-%d", errors="coerce")
        qualidade["assinaturas_anteriores"] = int((assinaturas < dados.entrada).sum())

    analise = dados.loc[~terreno].copy()
    analise["contratada"] = analise.status.eq("Contratada")
    analise["ltv_solicitado"] = analise.valor_solicitado_num / analise.valor_imovel_num
    qualidade["contratos_ltv_acima_60"] = int(
        (analise.contratada & (analise.ltv_solicitado > .60)).sum()
    )
    log.info("Tratamento: %s terrenos excluídos; %s propostas elegíveis", qualidade["terrenos"], len(analise))
    log.info("Qualidade: %s", qualidade)
    if qualidade["etapas_invalidas"]:
        log.warning("Há %s etapa(s) fora de 1 a 6; ficam no total e fora da tabela por etapa", qualidade["etapas_invalidas"])
    return analise, qualidade


def semana_da_data(referencia):
    inicio = referencia - timedelta(days=referencia.weekday())
    return inicio, inicio + timedelta(days=6)


def resumo(df):
    total = len(df)
    contratos = int(df.contratada.sum())
    return {
        "propostas": total,
        "contratos": contratos,
        "conversao": contratos / total if total else math.nan,
        "solicitado": float(df.valor_solicitado_num.sum()),
        "nao_contratado": float(df.loc[~df.contratada, "valor_solicitado_num"].sum()),
    }


def linha_tabela(celulas, cabecalho=False):
    tag = "th" if cabecalho else "td"
    return "<tr>" + "".join(f"<{tag}>{escape(str(c))}</{tag}>" for c in celulas) + "</tr>"


def tabela(cabecalhos, linhas):
    return "<table><thead>" + linha_tabela(cabecalhos, True) + "</thead><tbody>" + (
        "".join(linha_tabela(linha) for linha in linhas) if linhas
        else linha_tabela(["Sem propostas no período"] + ["—"] * (len(cabecalhos) - 1))
    ) + "</tbody></table>"


def gerar_html(
    analise, qualidade, opcionais_ausentes, inicio, fim, referencia, arquivo,
    anterior_inicio, anterior_fim, rotulo_anterior,
):
    periodo = analise.loc[analise.entrada.dt.date.between(inicio, fim)].copy()
    periodo_anterior = analise.loc[
        analise.entrada.dt.date.between(anterior_inicio, anterior_fim)
    ]
    kpi, anterior, total = resumo(periodo), resumo(periodo_anterior), resumo(analise)

    canais = periodo.groupby("canal").agg(
        propostas=("id_proposta", "size"), contratos=("contratada", "sum"),
        valor=("valor_solicitado_num", "sum")
    ).sort_values("propostas", ascending=False)
    linhas_canais = [
        (nome, int(r.propostas), int(r.contratos), percentual(r.contratos / r.propostas), moeda(r.valor))
        for nome, r in canais.iterrows()
    ]

    sem_contrato = periodo.loc[~periodo.contratada]
    etapas = sem_contrato.loc[sem_contrato.etapa.between(1, 5)].groupby("etapa").agg(
        propostas=("id_proposta", "size"), valor=("valor_solicitado_num", "sum")
    ).reindex(range(1, 6), fill_value=0)
    linhas_etapas = [(int(etapa), int(r.propostas), moeda(r.valor)) for etapa, r in etapas.iterrows()]
    sem_etapa = int((~sem_contrato.etapa.between(1, 5)).sum())
    ultima_entrada = analise.entrada.max()
    ultima_entrada_texto = "nenhuma" if pd.isna(ultima_entrada) else ultima_entrada.strftime("%d/%m/%Y")

    status = periodo.groupby("status").agg(
        propostas=("id_proposta", "size"), valor=("valor_solicitado_num", "sum")
    ).sort_values("propostas", ascending=False)
    linhas_status = [(nome, int(r.propostas), moeda(r.valor)) for nome, r in status.iterrows()]

    alertas = []
    if periodo.empty:
        alertas.append(
            f"Nenhuma proposta elegível entrou nesse período. Última entrada elegível do arquivo: {ultima_entrada_texto}."
        )
    if pd.notna(ultima_entrada) and ultima_entrada.date() > referencia:
        alertas.append(
            "A data de referência é anterior a entradas presentes neste CSV. Este é um exemplo retrospectivo de coorte; "
            "os status podem ter mudado depois da referência e não reconstituem o relatório histórico daquela data."
        )
    if sem_etapa:
        alertas.append(f"{sem_etapa} proposta(s) não contratada(s) ficaram fora do quadro por etapa (etapa fora de 1–5).")
    if qualidade["etapas_invalidas"]:
        alertas.append(f"A base completa contém {qualidade['etapas_invalidas']} etapa(s) fora da faixa 1–6.")
    if opcionais_ausentes:
        alertas.append("Colunas opcionais ausentes: " + ", ".join(opcionais_ausentes) + ".")
    alertas_html = "".join(f"<li>{escape(a)}</li>" for a in alertas) if alertas else "<li>Sem alertas adicionais para este recorte.</li>"

    def cartao(titulo, valor, detalhe=""):
        return f'<div class="card"><span>{escape(titulo)}</span><strong>{escape(str(valor))}</strong><small>{escape(detalhe)}</small></div>'

    cards = "".join([
        cartao("Propostas recebidas", kpi["propostas"], f"{rotulo_anterior}: {anterior['propostas']}"),
        cartao("Contratadas no status atual", kpi["contratos"]),
        cartao("Conversão observada", percentual(kpi["conversao"])),
        cartao("Crédito solicitado", moeda(kpi["solicitado"]), f"{rotulo_anterior}: {moeda(anterior['solicitado'])}"),
        cartao("Solicitado não contratado", moeda(kpi["nao_contratado"]), "exposição bruta; não é receita perdida"),
    ])

    html = f"""<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Funil de crédito | {inicio:%d/%m/%Y} a {fim:%d/%m/%Y}</title>
<style>
body{{font:16px/1.5 system-ui,Arial,sans-serif;color:#173046;background:#f4f7fa;margin:0}}
main{{max-width:1080px;margin:32px auto;padding:0 20px 40px}}
h1{{font-size:1.9rem;margin-bottom:4px}}h2{{margin-top:32px;font-size:1.25rem}}
.muted,small{{color:#566b7a}}.cards{{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:12px;margin:24px 0}}
.card{{background:#fff;border:1px solid #dbe4eb;border-radius:10px;padding:16px;display:flex;flex-direction:column;gap:6px}}
.card strong{{font-size:1.5rem;color:#155b76}}.card small{{font-size:.82rem}}
table{{width:100%;border-collapse:collapse;background:#fff}}th,td{{padding:10px 12px;text-align:left;border-bottom:1px solid #e2e9ef}}
th{{background:#e8f1f6}}.table-wrap{{overflow-x:auto;border-radius:8px;border:1px solid #dbe4eb}}
.note{{background:#eaf4f7;border-left:4px solid #27738a;padding:12px 16px;border-radius:4px}}
footer{{margin-top:32px;color:#566b7a;font-size:.9rem}}
</style></head><body><main>
<h1>Relatório do funil de crédito</h1>
<p class="muted">Entradas de {inicio:%d/%m/%Y} a {fim:%d/%m/%Y} · Referência {referencia:%d/%m/%Y} · Gerado em {datetime.now().astimezone():%d/%m/%Y %H:%M}</p>
<div class="cards">{cards}</div>
<p class="note"><strong>Leitura correta:</strong> o período agrupa propostas pela data de entrada. Contratação e status são os valores presentes no CSV recebido nesta execução, sem histórico de quando cada status mudou. Coortes recentes podem ter tido menos tempo para contratar.</p>
<h2>Por canal de origem</h2><div class="table-wrap">{tabela(['Canal','Propostas','Contratadas','Conversão observada','Crédito solicitado'], linhas_canais)}</div>
<h2>Não contratadas por etapa máxima</h2><div class="table-wrap">{tabela(['Etapa máxima','Propostas','Crédito solicitado não contratado'], linhas_etapas)}</div>
<p class="muted">Cada proposta não contratada aparece uma vez na sua etapa máxima. O valor pedido não é lucro, desembolso ou perda recuperável.</p>
<h2>Desfecho registrado no CSV</h2><div class="table-wrap">{tabela(['Status','Propostas','Crédito solicitado'], linhas_status)}</div>
<h2>Qualidade e contexto</h2><ul>{alertas_html}</ul>
<p>Base de entrada: {qualidade['brutas']} registros; {qualidade['terrenos']} terrenos excluídos; {total['propostas']} propostas na base analítica. Conversão observada no arquivo completo: {percentual(total['conversao'])}.</p>
<p class="muted">Última entrada elegível registrada: {ultima_entrada_texto}. Fonte: {escape(arquivo.name)} (dados sintéticos do desafio Bari). Ver logs para detalhes do tratamento: {qualidade['datas_br']} datas brasileiras, {qualidade['valores_com_prefixo']} valores de imóvel com R$, {qualidade['canais_normalizados']} rótulos de canal padronizados. A unidade de <code>taxa_juros_aa</code> é ambígua e não entra no relatório; {qualidade['contratos_ltv_acima_60']} contratos têm LTV solicitado acima de 60%, o que pede reconciliação com o valor aprovado.</p>
<footer>Relatório para acompanhamento operacional. Os indicadores de conversão não medem desempenho causal dos canais.</footer>
</main></body></html>"""
    return html, kpi


def gravar_atomico(destino, texto):
    destino.parent.mkdir(parents=True, exist_ok=True)
    temporario = None
    try:
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=destino.parent, suffix=".tmp", delete=False) as f:
            temporario = Path(f.name)
            f.write(texto)
        os.replace(temporario, destino)
    finally:
        if temporario is not None:
            temporario.unlink(missing_ok=True)


def argumentos():
    parser = argparse.ArgumentParser(description="Gera relatório HTML semanal do funil")
    parser.add_argument("--csv", default="data/raw/propostas_credito.csv", help="CSV de entrada (relativo à raiz do projeto)")
    parser.add_argument("--referencia", type=date.fromisoformat, metavar="AAAA-MM-DD",
                        help="Usa a semana de segunda a domingo que contém esta data; sem informar, usa a semana atual")
    parser.add_argument("--saida", help="Caminho do HTML (padrão: outputs/relatorios/relatorio_DATA.html)")
    parser.add_argument("--log", default="logs/execucao.log", help="Arquivo de log")
    return parser.parse_args()


def main():
    args = argumentos()
    log_path = caminho(args.log)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s",
        handlers=[logging.FileHandler(log_path, encoding="utf-8"), logging.StreamHandler(sys.stderr)],
    )
    log = logging.getLogger("funil")
    arquivo = caminho(args.csv)
    try:
        bruto, separador, opcionais_ausentes = carregar_csv(arquivo, log)
        analise, qualidade = tratar(bruto, log)
        if args.referencia is None:
            referencia = date.today()
            inicio, fim = semana_da_data(referencia)
            log.info("Sem referência informada; usando a semana atual")
        else:
            inicio, fim = semana_da_data(args.referencia)
            referencia = args.referencia
        anterior_inicio = inicio - timedelta(days=7)
        anterior_fim = inicio - timedelta(days=1)
        rotulo_anterior = "semana anterior"
        destino = caminho(args.saida) if args.saida else RAIZ / "outputs" / "relatorios" / f"relatorio_{inicio.isoformat()}.html"
        log.info("Início da execução; período de %s a %s", inicio, fim)
        html, kpi = gerar_html(
            analise, qualidade, opcionais_ausentes, inicio, fim, referencia, arquivo,
            anterior_inicio, anterior_fim, rotulo_anterior,
        )
        gravar_atomico(destino, html)
    except Exception as exc:
        log.exception("Relatório não gerado: %s", exc)
        print(f"ERRO: {exc}\nDetalhes em: {log_path}", file=sys.stderr)
        return 1
    log.info("Relatório gerado: %s | propostas no período: %s | separador: %s", destino, kpi["propostas"], separador)
    print(f"Relatório pronto: {destino}")
    print(f"Período: {inicio:%d/%m/%Y} a {fim:%d/%m/%Y} | propostas: {kpi['propostas']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
