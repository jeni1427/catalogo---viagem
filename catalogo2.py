import streamlit as st
from PIL import Image
import requests
import gspread
from google.oauth2.service_account import Credentials

st.set_page_config(
    page_title="Catálogo de Viagens",
    page_icon="logo3.png",
    layout="wide"
)

imagem_topo = Image.open("logo3.png")
st.image(imagem_topo, width="stretch")

senha_admin = "1326"


def conectar_planilha():
    escopos = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

    credenciais = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=escopos
    )

    cliente = gspread.authorize(credenciais)

    planilha = cliente.open_by_key(
        st.secrets["GOOGLE_SHEET_ID"]
    )

    return planilha.sheet1


def carregar_imagens():
    aba = conectar_planilha()
    return aba.get_all_records()


def salvar_imagem_na_planilha(url, delete_url, nome):
    aba = conectar_planilha()
    aba.append_row([url, delete_url, nome])


def remover_imagem_da_planilha(numero_da_linha):
    aba = conectar_planilha()
    aba.delete_rows(numero_da_linha)


def enviar_para_imgbb(arquivo):
    url = "https://api.imgbb.com/1/upload"

    payload = {
        "key": st.secrets["IMGBB_API_KEY"]
    }

    files = {
        "image": arquivo.getvalue()
    }

    resposta = requests.post(
        url,
        data=payload,
        files=files
    )

    resultado = resposta.json()

    if not resultado.get("success"):
        st.error("Erro ao enviar imagem para o ImgBB.")
        st.write(resultado)
        return None

    return {
        "url": resultado["data"]["url"],
        "delete_url": resultado["data"].get("delete_url", ""),
        "nome": arquivo.name
    }


with st.sidebar:
    st.subheader("Área administrativa")

    senha = st.text_input(
        "Senha do administrador",
        type="password"
    )

    admin_logado = senha == senha_admin


if "imagem_aberta" not in st.session_state:
    st.session_state.imagem_aberta = None

if "nome_aberto" not in st.session_state:
    st.session_state.nome_aberto = None


if admin_logado:
    st.subheader("Adicionar novo folder")

    arquivos_enviados = st.file_uploader(
        "Escolha os folders",
        type=["jpg", "jpeg", "png", "webp"],
        accept_multiple_files=True
    )

    if arquivos_enviados:
        for arquivo in arquivos_enviados:
            dados_imagem = enviar_para_imgbb(arquivo)

            if dados_imagem:
                salvar_imagem_na_planilha(
                    dados_imagem["url"],
                    dados_imagem["delete_url"],
                    dados_imagem["nome"]
                )

        st.success("Folders adicionados com sucesso!")
        st.rerun()


imagens = carregar_imagens()

if not imagens:
    st.info("Nenhum folder cadastrado ainda.")


colunas = st.columns(3)

for i, imagem in enumerate(imagens):
    url_imagem = imagem["url"]
    nome_imagem = imagem.get("nome", f"Imagem {i + 1}")

    linha_planilha = i + 2

    with colunas[i % 3]:
        st.image(url_imagem, width="stretch")

        if st.button("Abrir", key=f"abrir_{i}"):
            st.session_state.imagem_aberta = url_imagem
            st.session_state.nome_aberto = nome_imagem

        if st.session_state.imagem_aberta == url_imagem:
            st.markdown("""
                <a href="#folder-ampliado">
                <button style="
                background-color:blue;
                color:white;
                border:none;
                padding:10px 20px;
                border-radius:10px;
                cursor:pointer;
                font-size:16px;
                ">
                Ir para imagem ampliada
                </button>
                </a>
            """, unsafe_allow_html=True)

        if admin_logado:
            if st.button("Remover", key=f"remover_{i}"):
                remover_imagem_da_planilha(linha_planilha)

                if st.session_state.imagem_aberta == url_imagem:
                    st.session_state.imagem_aberta = None
                    st.session_state.nome_aberto = None

                st.success("Imagem removida do site!")
                st.rerun()


if st.session_state.imagem_aberta:
    st.divider()

    st.markdown(
        '<div id="folder-ampliado"></div>',
        unsafe_allow_html=True
    )

    st.markdown("""
    <h1 style='
    color:black;
    padding:20px;
    border-radius:20px;
    text-align:center;
    font-size:50px;
    box-shadow:0px 0px 20px rgba(0,0,0,0.3);
    '>
    Foto Ampliada
    </h1>
    """, unsafe_allow_html=True)

    st.image(
        st.session_state.imagem_aberta,
        width="stretch"
    )