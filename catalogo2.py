import streamlit as st
from PIL import Image
import os
import streamlit.components.v1 as components

st.set_page_config(page_title="Catálogo de Viagens", page_icon="logo2.jpeg",layout="wide")

imagem_topo = Image.open("logo2.jpeg")

st.markdown("""
<head>
<meta property="og:title" content="Catálogo de Viagens" />
<meta property="og:description" content="Conheça os pacotes da JmJ turismo" />
<meta property="og:image" content="https://catalogo---viagem-jhtaq6fqzglkqin4xexqbm.streamlit.app/" />
</head>
""", unsafe_allow_html=True)

st.image(imagem_topo, width="stretch")

pasta = "folders"
os.makedirs(pasta, exist_ok=True)

senha_admin = "1326"  # troque por uma senha sua

with st.sidebar:
    st.subheader("Área administrativa")

    senha = st.text_input(
        "Senha do administrador",
        type="password"
    )

    admin_logado = senha == senha_admin

if admin_logado:
    st.subheader("Adicionar novo folder")

    arquivos_enviados = st.file_uploader(
        "Escolha os folders",
        type=["jpg", "jpeg", "png", "webp"],
        accept_multiple_files=True
    )

    if arquivos_enviados:
        for arquivo in arquivos_enviados:
            caminho = os.path.join(pasta, arquivo.name)

            with open(caminho, "wb") as f:
                f.write(arquivo.getbuffer())

        st.success("Folders adicionados com sucesso!")        

arquivos = os.listdir(pasta)

imagens = [
    arquivo for arquivo in arquivos
    if arquivo.lower().endswith((".jpg", ".jpeg", ".png", ".webp"))
]

if "imagem_aberta" not in st.session_state:
    st.session_state.imagem_aberta = None

if "arquivo_aberto" not in st.session_state:
    st.session_state.arquivo_aberto = None

colunas = st.columns(3)

for i, arquivo in enumerate(imagens):
    caminho = os.path.join(pasta, arquivo)

    with colunas[i % 3]:
        imagem = Image.open(caminho)

        st.image(imagem, width="stretch")

        if st.button(
            "Abrir",
            key=f"abrir_{arquivo}"
        ):

            st.session_state.imagem_aberta = caminho
            st.session_state.arquivo_aberto = arquivo

        # botão para ir até imagem grande
        if st.session_state.arquivo_aberto == arquivo:

            if st.session_state.arquivo_aberto == arquivo:

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
                     """, unsafe_allow_html=True
                     )

        if admin_logado:
            nova_imagem = st.file_uploader(
                f"Atualizar {arquivo}",
                type=["jpg", "jpeg", "png", "webp"],
                key=f"upload_{arquivo}"
            )

            if nova_imagem:
                with open(caminho, "wb") as f:
                    f.write(nova_imagem.getbuffer())

                st.success("Imagem atualizada!")
                st.rerun()

            if st.button("Remover", key=f"remover_{arquivo}"):
                os.remove(caminho)

                if st.session_state.imagem_aberta == caminho:
                    st.session_state.imagem_aberta = None

                st.success("Imagem removida!")
                st.rerun()

if st.session_state.imagem_aberta:

    st.divider()

    st.markdown(
        '<div id="folder-ampliado"></div>',
        unsafe_allow_html=True
    )

    st.markdown(
    """
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
    """,
    unsafe_allow_html=True
)

    imagem_grande = Image.open(
        st.session_state.imagem_aberta
    )

    st.image(
        imagem_grande,
        width="stretch"
    )
    