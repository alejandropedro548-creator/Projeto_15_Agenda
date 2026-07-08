from __future__ import annotations

import json
import uuid

from dataclasses import dataclass, asdict
from datetime import datetime, date, time
from pathlib import Path

import streamlit as st


# =====================================================
# CONFIGURAÇÃO
# =====================================================

st.set_page_config(
    page_title="SmartAgenda",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =====================================================
# CSS
# =====================================================

def carregar_css():

    arquivo_css = Path("styles/style.css")

    if arquivo_css.exists():

        st.markdown(
            f"""
            <style>
            {arquivo_css.read_text(
                encoding="utf-8"
            )}
            </style>
            """,
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

    cor: str = "#2563eb"

    icone: str = "📅"

    criado_em: str = ""

    atualizado_em: str = ""

    favorito: bool = False

    concluido: bool = False



# =====================================================
# BANCO DE DADOS JSON
# =====================================================


def salvar_eventos(
    eventos: list[Evento]
):

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



def carregar_eventos():

    if not DATA_FILE.exists():

        salvar_eventos([])

        return []


    try:

        with open(
            DATA_FILE,
            "r",
            encoding="utf-8"
        ) as arquivo:

            dados = json.load(
                arquivo
            )


        eventos = []


        for item in dados:


            evento = Evento(

                id=item.get(
                    "id",
                    str(uuid.uuid4())
                ),

                titulo=item.get(
                    "titulo",
                    ""
                ),

                descricao=item.get(
                    "descricao",
                    ""
                ),

                categoria=item.get(
                    "categoria",
                    "Outros"
                ),

                prioridade=item.get(
                    "prioridade",
                    "Média"
                ),

                data=item.get(
                    "data",
                    ""
                ),

                hora=item.get(
                    "hora",
                    ""
                ),

                recorrencia=item.get(
                    "recorrencia",
                    "Nenhuma"
                ),

                cor=item.get(
                    "cor",
                    "#2563eb"
                ),

                icone=item.get(
                    "icone",
                    "📅"
                ),

                criado_em=item.get(
                    "criado_em",
                    ""
                ),

                atualizado_em=item.get(
                    "atualizado_em",
                    ""
                ),

                favorito=item.get(
                    "favorito",
                    False
                ),

                concluido=item.get(
                    "concluido",
                    False
                )

            )


            eventos.append(
                evento
            )


        return eventos


    except Exception:

        return []



# =====================================================
# ESTADO DA APLICAÇÃO
# =====================================================


if "eventos" not in st.session_state:

    st.session_state.eventos = carregar_eventos()



if "pagina" not in st.session_state:

    st.session_state.pagina = "Dashboard"



# =====================================================
# FUNÇÕES PRINCIPAIS
# =====================================================


def adicionar_evento(

    titulo,

    descricao,

    categoria,

    prioridade,

    data_evento,

    hora_evento,

    recorrencia

):


    agora = datetime.now().strftime(
        "%d/%m/%Y %H:%M"
    )


    evento = Evento(

        id=str(
            uuid.uuid4()
        ),

        titulo=titulo,

        descricao=descricao,

        categoria=categoria,

        prioridade=prioridade,

        data=data_evento.strftime(
            "%d/%m/%Y"
        ),

        hora=hora_evento.strftime(
            "%H:%M"
        ),

        recorrencia=recorrencia,

        criado_em=agora,

        atualizado_em=agora

    )


    st.session_state.eventos.append(
        evento
    )


    salvar_eventos(
        st.session_state.eventos
    )



def dias_restantes(
    data_evento
):

    hoje = datetime.now().date()


    evento = datetime.strptime(

        data_evento,

        "%d/%m/%Y"

    ).date()


    return (
        evento - hoje
    ).days



def total_eventos():

    return len(
        st.session_state.eventos
    )



def total_concluidos():

    return sum(

        evento.concluido

        for evento in st.session_state.eventos

    )



def total_pendentes():

    return (

        total_eventos()

        -

        total_concluidos()

    )
# =====================================================
# COMPONENTES VISUAIS
# =====================================================


def navbar():

    st.markdown(
        """
        <div class="navbar">

            <div class="brand">

                <div class="brand-icon">
                    ⚡
                </div>


                <div>

                    <h2>
                    SmartAgenda
                    </h2>

                    <span>
                    Gestão inteligente da sua rotina
                    </span>

                </div>

            </div>


            <div class="status">

                <span>
                🚀 Sistema Online
                </span>

            </div>

        </div>
        """,

        unsafe_allow_html=True
    )



def hero():

    st.markdown(
        """

        <section class="hero">

            <div>

                <span class="badge">
                SMARTAGENDA 3.0
                </span>


                <h1>
                Organize sua vida
                com inteligência.
                </h1>


                <p>

                Controle compromissos,
                estudos, trabalho e objetivos
                em um único lugar.

                </p>

            </div>


            <div class="hero-symbol">

                ⚡

            </div>


        </section>

        """,

        unsafe_allow_html=True
    )



def card_estatistica(
    icone,
    titulo,
    valor
):

    st.markdown(

        f"""

        <div class="stat-card">


            <div class="stat-icon">

                {icone}

            </div>


            <div class="stat-title">

                {titulo}

            </div>


            <div class="stat-number">

                {valor}

            </div>


        </div>

        """,

        unsafe_allow_html=True

    )



def sidebar():

    st.sidebar.markdown(
        """

        <div class="side-logo">

        ⚡ SmartAgenda

        </div>


        <div class="side-description">

        Seu assistente pessoal
        de organização.

        </div>

        """,

        unsafe_allow_html=True
    )


    st.sidebar.divider()


    escolha = st.sidebar.radio(

        "MENU",

        [

            "Dashboard",

            "Novo Evento",

            "Eventos"

        ]

    )


    return escolha



# =====================================================
# DASHBOARD
# =====================================================


def mostrar_dashboard():


    navbar()


    hero()


    eventos = total_eventos()

    concluidos = total_concluidos()

    pendentes = total_pendentes()



    col1, col2, col3 = st.columns(3)



    with col1:

        card_estatistica(

            "📅",

            "Eventos",

            eventos

        )


    with col2:

        card_estatistica(

            "⌛",

            "Pendentes",

            pendentes

        )


    with col3:

        card_estatistica(

            "✅",

            "Concluídos",

            concluidos

        )



    st.markdown(
        "<br>",
        unsafe_allow_html=True
    )



    proximos = [

        evento

        for evento in st.session_state.eventos

        if dias_restantes(
            evento.data
        ) >= 0

    ]



    if proximos:


        proximos.sort(

            key=lambda evento:

            datetime.strptime(

                evento.data,

                "%d/%m/%Y"

            )

        )


        evento = proximos[0]


        st.markdown(

            f"""

            <div class="next-card">


                <h3>

                ⭐ Próximo compromisso

                </h3>


                <h2>

                {evento.icone}
                {evento.titulo}

                </h2>


                <p>

                📅 {evento.data}

                • 

                ⏰ {evento.hora}

                </p>


            </div>

            """,

            unsafe_allow_html=True

        )



# =====================================================
# EXECUÇÃO PRINCIPAL
# =====================================================


pagina = sidebar()



if pagina == "Dashboard":

    mostrar_dashboard()
# =====================================================
# NOVO EVENTO
# =====================================================


def mostrar_novo_evento():


    navbar()


    st.markdown(

        """

        <div class="page-title">

        <h1>
        ➕ Criar novo evento
        </h1>

        <p>
        Adicione um compromisso à sua rotina.
        </p>

        </div>

        """,

        unsafe_allow_html=True

    )



    with st.form(
        "novo_evento_form"
    ):


        titulo = st.text_input(
            "Título do evento"
        )


        descricao = st.text_area(
            "Descrição"
        )


        col1, col2 = st.columns(2)


        with col1:


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



        with col2:


            prioridade = st.selectbox(

                "Prioridade",

                [

                    "Alta",

                    "Média",

                    "Baixa"

                ]

            )



        col3, col4 = st.columns(2)



        with col3:


            data_evento = st.date_input(

                "Data",

                value=date.today()

            )



        with col4:


            hora_evento = st.time_input(

                "Hora",

                value=time(
                    12,
                    0
                )

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



        enviar = st.form_submit_button(

            "🚀 Criar evento"

        )



        if enviar:


            if not titulo.strip():


                st.error(

                    "Digite um título para o evento."

                )


            else:


                adicionar_evento(

                    titulo,

                    descricao,

                    categoria,

                    prioridade,

                    data_evento,

                    hora_evento,

                    recorrencia

                )


                st.success(

                    "Evento criado com sucesso!"

                )


                st.rerun()



# =====================================================
# PÁGINA EVENTOS
# =====================================================


def mostrar_eventos():


    navbar()


    st.markdown(

        """

        <div class="page-title">

        <h1>
        📋 Meus eventos
        </h1>

        <p>
        Visualize e gerencie seus compromissos.
        </p>

        </div>

        """,

        unsafe_allow_html=True

    )



    if not st.session_state.eventos:


        st.info(

            "Nenhum evento cadastrado ainda."

        )


        return



    pesquisa = st.text_input(

        "🔎 Pesquisar eventos"

    ).lower()



    for evento in st.session_state.eventos:


        texto = (

            evento.titulo

            +

            evento.descricao

            +

            evento.categoria

        ).lower()



        if pesquisa and pesquisa not in texto:

            continue



        dias = dias_restantes(

            evento.data

        )


        status = (

            "✅ Concluído"

            if evento.concluido

            else

            "⌛ Pendente"

        )



        st.markdown(

            f"""

            <div class="event-card">


                <div class="event-header">


                    <h2>

                    {evento.icone}

                    {evento.titulo}

                    </h2>


                    <span>

                    {status}

                    </span>


                </div>



                <p>

                {evento.descricao}

                </p>



                <div class="event-info">


                📂 {evento.categoria}


                <br>


                ⚡ {evento.prioridade}


                <br>


                📅 {evento.data}

                às {evento.hora}


                </div>


            </div>

            """,

            unsafe_allow_html=True

        )



        col1, col2 = st.columns(2)



        with col1:


            if st.button(

                "✅ Concluir",

                key=f"ok_{evento.id}"

            ):


                evento.concluido = True


                evento.atualizado_em = datetime.now().strftime(

                    "%d/%m/%Y %H:%M"

                )


                salvar_eventos(

                    st.session_state.eventos

                )


                st.rerun()



        with col2:


            if st.button(

                "🗑 Excluir",

                key=f"del_{evento.id}"

            ):


                st.session_state.eventos.remove(

                    evento

                )


                salvar_eventos(

                    st.session_state.eventos

                )


                st.rerun()



# =====================================================
# ROTAS
# =====================================================


if pagina == "Novo Evento":

    mostrar_novo_evento()



elif pagina == "Eventos":

    mostrar_eventos()