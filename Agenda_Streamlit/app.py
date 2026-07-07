from __future__ import annotations

import json
import uuid
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path

import streamlit as st

# =====================================================
# CONFIGURAÇÃO
# =====================================================

st.set_page_config(
    page_title="SmartAgenda",
    page_icon="📅",
    layout="wide"
)
def carregar_css():

    css = Path("styles/style.css")

    if css.exists():

        st.markdown(

            f"<style>{css.read_text(encoding='utf-8')}</style>",

            unsafe_allow_html=True

        )


carregar_css()

DATA_FILE = Path("agenda.json")


# =====================================================
# MODELO
# =====================================================

@dataclass
class Evento:
    id: str
    titulo: str
    descricao: str
    categoria: str
    prioridade: str
    data: str
    hora: str
    recorrencia: str
    concluido: bool = False


# =====================================================
# PERSISTÊNCIA
# =====================================================

def carregar_eventos() -> list[Evento]:

    if not DATA_FILE.exists():
        salvar_eventos([])
        return []

    try:

        with open(
            DATA_FILE,
            "r",
            encoding="utf-8"
        ) as arquivo:

            dados = json.load(arquivo)

        return [
            Evento(**item)
            for item in dados
        ]

    except Exception:

        return []


def salvar_eventos(
    eventos: list[Evento]
) -> None:

    with open(
        DATA_FILE,
        "w",
        encoding="utf-8"
    ) as arquivo:

        json.dump(
            [
                asdict(evento)
                for evento in eventos
            ],
            arquivo,
            indent=4,
            ensure_ascii=False
        )


# =====================================================
# ESTADO
# =====================================================

if "eventos" not in st.session_state:

    st.session_state.eventos = (
        carregar_eventos()
    )


# =====================================================
# FUNÇÕES
# =====================================================

def adicionar_evento(
    titulo: str,
    descricao: str,
    categoria: str,
    prioridade: str,
    data,
    hora,
    recorrencia: str
):

    evento = Evento(

        id=str(uuid.uuid4()),

        titulo=titulo,

        descricao=descricao,

        categoria=categoria,

        prioridade=prioridade,

        data=data.strftime(
            "%d/%m/%Y"
        ),

        hora=hora.strftime(
            "%H:%M"
        ),

        recorrencia=recorrencia,

        concluido=False

    )

    st.session_state.eventos.append(
        evento
    )

    salvar_eventos(
        st.session_state.eventos
    )


def dias_restantes(
    data_evento: str
):

    hoje = datetime.now().date()

    evento = datetime.strptime(
        data_evento,
        "%d/%m/%Y"
    ).date()

    return (
        evento - hoje
    ).days


# =====================================================
# DASHBOARD
# =====================================================

def dashboard():

    st.title("📅 SmartAgenda")

    total = len(
        st.session_state.eventos
    )

    concluidos = sum(
        e.concluido
        for e in st.session_state.eventos
    )

    pendentes = (
        total - concluidos
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Eventos",
        total
    )

    col2.metric(
        "Pendentes",
        pendentes
    )

    col3.metric(
        "Concluídos",
        concluidos
    )

    futuros = [

        evento

        for evento in st.session_state.eventos

        if dias_restantes(
            evento.data
        ) >= 0

    ]

    if futuros:

        futuros.sort(

            key=lambda e:

            datetime.strptime(

                e.data,

                "%d/%m/%Y"

            )

        )

        proximo = futuros[0]

        st.info(

            f"Próximo compromisso: "
            f"{proximo.titulo} "
            f"(faltam "
            f"{dias_restantes(proximo.data)} dias)"

        )


# =====================================================
# SIDEBAR
# =====================================================

pagina = st.sidebar.radio(

    "Navegação",

    [

        "Dashboard",

        "Novo Evento",

        "Eventos"

    ]

)


# =====================================================
# DASHBOARD
# =====================================================

if pagina == "Dashboard":

    dashboard()


# =====================================================
# NOVO EVENTO
# =====================================================

elif pagina == "Novo Evento":

    st.title(
        "➕ Novo Evento"
    )

    with st.form(
        "novo_evento"
    ):

        titulo = st.text_input(
            "Título"
        )

        descricao = st.text_area(
            "Descrição"
        )

        categoria = st.selectbox(

            "Categoria",

            [

                "Estudos",

                "Trabalho",

                "Saúde",

                "Família",

                "Financeiro",

                "Outros"

            ]

        )

        prioridade = st.selectbox(

            "Prioridade",

            [

                "Alta",

                "Média",

                "Baixa"

            ]

        )

        data = st.date_input(
            "Data"
        )

        hora = st.time_input(
            "Hora"
        )

        recorrencia = st.selectbox(

            "Recorrência",

            [

                "Nenhuma",

                "Diária",

                "Semanal",

                "Mensal",

                "Anual"

            ]

        )

        salvar = (
            st.form_submit_button(
                "Salvar"
            )
        )

        if salvar:

            adicionar_evento(

                titulo,

                descricao,

                categoria,

                prioridade,

                data,

                hora,

                recorrencia

            )

            st.success(
                "Evento salvo!"
            )
# =====================================================
# EVENTOS
# =====================================================

elif pagina == "Eventos":

    st.title("📋 Eventos")

    if not st.session_state.eventos:

        st.info("Nenhum evento cadastrado.")

    else:

        pesquisar = st.text_input(
            "🔎 Pesquisar"
        ).lower()

        categoria_filtro = st.selectbox(

            "Categoria",

            [

                "Todas",

                "Estudos",

                "Trabalho",

                "Saúde",

                "Família",

                "Financeiro",

                "Outros"

            ]

        )

        prioridade_filtro = st.selectbox(

            "Prioridade",

            [

                "Todas",

                "Alta",

                "Média",

                "Baixa"

            ]

        )

        eventos = sorted(

            st.session_state.eventos,

            key=lambda e: datetime.strptime(

                e.data,

                "%d/%m/%Y"

            )

        )

        for evento in eventos:

            if pesquisar:

                texto = (

                    evento.titulo

                    + evento.descricao

                    + evento.categoria

                ).lower()

                if pesquisar not in texto:

                    continue

            if (

                categoria_filtro != "Todas"

                and evento.categoria != categoria_filtro

            ):

                continue

            if (

                prioridade_filtro != "Todas"

                and evento.prioridade != prioridade_filtro

            ):

                continue

            dias = dias_restantes(

                evento.data

            )

            with st.expander(

                f"📅 {evento.titulo}"

            ):

                st.write(

                    f"**Descrição:** {evento.descricao}"

                )

                st.write(

                    f"**Categoria:** {evento.categoria}"

                )

                st.write(

                    f"**Prioridade:** {evento.prioridade}"

                )

                st.write(

                    f"**Data:** {evento.data}"

                )

                st.write(

                    f"**Hora:** {evento.hora}"

                )

                st.write(

                    f"**Recorrência:** {evento.recorrencia}"

                )

                if evento.concluido:

                    st.success(

                        "✅ Concluído"

                    )

                else:

                    st.warning(

                        "⌛ Pendente"

                    )

                if dias > 0:

                    st.info(

                        f"Faltam {dias} dias."

                    )

                elif dias == 0:

                    st.success(

                        "É hoje!"

                    )

                else:

                    st.error(

                        f"Atrasado há {-dias} dias."

                    )

                col1, col2 = st.columns(2)

                if col1.button(

                    "✅ Concluir",

                    key=f"c{evento.id}"

                ):

                    evento.concluido = True

                    salvar_eventos(

                        st.session_state.eventos

                    )

                    st.rerun()

                if col2.button(

                    "🗑 Excluir",

                    key=f"d{evento.id}"

                ):

                    st.session_state.eventos.remove(

                        evento

                    )

                    salvar_eventos(

                        st.session_state.eventos

                    )

                    st.rerun()


# =====================================================
# RODAPÉ
# =====================================================

st.divider()

st.caption(

    "SmartAgenda • versão 2.0"

)
