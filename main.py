import streamlit as st
from openai_functions import gerar_plano_aula, gerar_assunto_contextualizado, gerar_questoes
from file_processing import processar_arquivos, gerar_docx
from utils import redirecionar_com_query_params

# Configuração inicial do Streamlit
import streamlit as st

st.set_page_config(page_title="Assistente de IA para Professores", layout="wide")

# Listas globais
ANOS_SERIES = [
    "Selecione uma opção",
    "EF - 1º Ano", "EF - 2º Ano", "EF - 3º Ano", "EF - 4º Ano", "EF - 5º Ano",
    "EF - 6º Ano", "EF - 7º Ano", "EF - 8º Ano", "EF - 9º Ano",
    "EM - 1º Ano", "EM - 2º Ano", "EM - 3º Ano"
]

COMPONENTES_CURRICULARES = [
    "Selecione uma opção",
    "Matemática", "Português", "Ciências", "História", "Geografia", "Arte",
    "Educação Física", "Inglês", "Biologia", "Física", "Química", "Sociologia",
    "Filosofia", "Redação", "Literatura"
]

# Barra lateral para upload de arquivo
st.sidebar.title("Assistente de IA para Professores")
uploaded_file = st.sidebar.file_uploader(
    "Envie um arquivo para servir de contexto",
    type=["docx", "txt", "pdf", "csv", "xlsx"]
)
if uploaded_file:
    contexto_texto = processar_arquivos(uploaded_file)
    if contexto_texto:
        st.session_state["uploaded_file_content"] = contexto_texto
        st.sidebar.success("Arquivo processado com sucesso!")

# Inicializa estados gerais se ainda não existirem
if "texto_gerado_plano" not in st.session_state:
    st.session_state["texto_gerado_plano"] = None
    st.session_state["texto_editado_plano"] = None
    st.session_state["modo_edicao_plano"] = False

if "conteudo_gerado_assunto" not in st.session_state:
    st.session_state["conteudo_gerado_assunto"] = None
    st.session_state["conteudo_editado_assunto"] = None
    st.session_state["modo_edicao_assunto"] = False

if "questoes_geradas" not in st.session_state:
    st.session_state["questoes_geradas"] = None
    st.session_state["questoes_editadas"] = None
    st.session_state["modo_edicao_questoes"] = False

# Cria as abas para cada módulo
tabs = st.tabs(["Plano de Aula", "Assunto Contextualizado", "Questões", "Correção de Questões"])

### Aba 1: Plano de Aula
with tabs[0]:
    st.header("Plano de Aula")
    # Se ainda não foi gerado conteúdo, exibe o formulário para gerar
    if st.session_state.get("texto_gerado_plano") is None:
        with st.form("plano_aula_form"):
            col1, col2 = st.columns(2)
            with col1:
                ano = st.selectbox("Ano / Série", ANOS_SERIES)
                componente = st.selectbox("Componente Curricular", COMPONENTES_CURRICULARES)
                assunto = st.text_input("Assunto", placeholder="Exemplo: Introdução à língua portuguesa")
            with col2:
                duracao = st.number_input("Duração da aula (min)", min_value=10, max_value=180, value=50)
                metodologia = st.selectbox("Metodologia", ["Selecione uma opção", "Expositiva", "Interativa", "Dinâmica"])
            st.markdown("### Características da Turma (opcional)")
            col1, col2 = st.columns([1, 2])
            with col1:
                caracteristicas_padrao = [
                    "Turma distraída",
                    "Gosta de conversar durante a aula",
                    "Prefere atividades práticas",
                    "Praticam Bullying",
                ]
                if "caracteristicas_selecionadas" not in st.session_state:
                    st.session_state["caracteristicas_selecionadas"] = []
                for opcao in caracteristicas_padrao:
                    if st.checkbox(opcao, key=f"check_{opcao}"):
                        if opcao not in st.session_state["caracteristicas_selecionadas"]:
                            st.session_state["caracteristicas_selecionadas"].append(opcao)
                    else:
                        if opcao in st.session_state["caracteristicas_selecionadas"]:
                            st.session_state["caracteristicas_selecionadas"].remove(opcao)
            with col2:
                caracteristicas_personalizadas = st.text_area(
                    "Adicione outras características (opcional)",
                    placeholder="Exemplo: Turma com interesse em tecnologia.",
                    height=100
                )
            caracteristicas = (
                ", ".join(st.session_state["caracteristicas_selecionadas"]) +
                (", " + caracteristicas_personalizadas if caracteristicas_personalizadas.strip() else "")
            )
            gerar = st.form_submit_button("Gerar Plano de Aula ✅")
        if gerar:
            if ano == "Selecione uma opção" or componente == "Selecione uma opção" or metodologia == "Selecione uma opção":
                st.error("Por favor, preencha todos os campos obrigatórios!")
            else:
                with st.spinner("Gerando plano de aula..."):
                    try:
                        plano_aula = gerar_plano_aula(
                            ano=ano,
                            componente=componente,
                            capitulo=None,
                            modulo=None,
                            duracao=duracao,
                            metodologia=metodologia,
                            caracteristicas=caracteristicas,
                            assunto=assunto,
                            contexto=st.session_state.get("uploaded_file_content", None)
                        )
                        st.session_state["texto_gerado_plano"] = plano_aula
                        st.session_state["texto_editado_plano"] = plano_aula
                        st.session_state["modo_edicao_plano"] = False
                        st.success("Plano de aula gerado com sucesso! ✅")
                    except Exception as e:
                        st.error(f"Erro ao gerar plano de aula: {e}")
    # Exibição ou edição do conteúdo gerado
    if st.session_state.get("texto_gerado_plano") is not None:
        if not st.session_state.get("modo_edicao_plano", False):
            col_editar, col_gap1, col_download, col_gap2, col_novo = st.columns([1, 0.05, 1, 0.05, 1])
            with col_editar:
                st.button("✏️ Editar", key="editar_plano", on_click=lambda: st.session_state.update({"modo_edicao_plano": True}))
            with col_download:
                buffer = gerar_docx(st.session_state["texto_gerado_plano"], "Plano de Aula")
                st.download_button(
                    label="📥 Baixar Plano",
                    data=buffer,
                    file_name="plano_de_aula.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    key="download_plano"
                )
            with col_novo:
                st.button("🆕 Novo Plano de Aula", key="novo_plano", on_click=lambda: st.session_state.update({
                    "texto_gerado_plano": None,
                    "texto_editado_plano": None,
                    "modo_edicao_plano": False
                }))
            st.markdown("### Plano de Aula Gerado ✅")
            st.markdown(st.session_state["texto_gerado_plano"], unsafe_allow_html=True)
        else:
            st.markdown("### Editor do Plano de Aula")
            st.session_state["texto_editado_plano"] = st.text_area(
                "Edite o Plano de Aula",
                value=st.session_state["texto_editado_plano"],
                height=400,
                key="textarea_plano"
            )
            col_salvar, col_cancelar = st.columns(2)
            with col_salvar:
                st.button("💾 Salvar Edição", key="salvar_plano", on_click=lambda: st.session_state.update({
                    "texto_gerado_plano": st.session_state["texto_editado_plano"],
                    "modo_edicao_plano": False
                }))
            with col_cancelar:
                st.button("Cancelar", key="cancelar_plano", on_click=lambda: st.session_state.update({"modo_edicao_plano": False}))

### Aba 2: Assunto Contextualizado
with tabs[1]:
    st.header("Assunto Contextualizado")
    if st.session_state.get("conteudo_gerado_assunto") is None:
        with st.form("contexto_form"):
            col1, col2 = st.columns(2)
            with col1:
                ano = st.selectbox("Ano / Série", ANOS_SERIES)
                componente = st.selectbox("Componente Curricular", COMPONENTES_CURRICULARES)
                assunto = st.text_input("Assunto (opcional)", placeholder="Exemplo: Aceleração")
            with col2:
                interesse = st.text_input("Tema de Interesse (opcional)", placeholder="Exemplo: Fórmula 1")
            contexto = st.session_state.get("uploaded_file_content", None)
            gerar = st.form_submit_button("Gerar Assunto Contextualizado ✅")
        if gerar:
            if ano == "Selecione uma opção" or componente == "Selecione uma opção":
                st.error("Por favor, preencha todos os campos obrigatórios!")
            else:
                with st.spinner("Gerando assunto contextualizado..."):
                    try:
                        conteudo = gerar_assunto_contextualizado(ano, componente, assunto, interesse, contexto)
                        st.session_state["conteudo_gerado_assunto"] = conteudo
                        st.session_state["conteudo_editado_assunto"] = conteudo
                        st.session_state["modo_edicao_assunto"] = False
                        st.success("Assunto contextualizado gerado com sucesso! ✅")
                    except Exception as e:
                        st.error(f"Erro ao gerar assunto contextualizado: {e}")
    if st.session_state.get("conteudo_gerado_assunto") is not None:
        if not st.session_state.get("modo_edicao_assunto", False):
            col1, col2, col3 = st.columns([1, 1, 1])
            with col1:
                st.button("✏️ Editar Assunto", key="editar_assunto", on_click=lambda: st.session_state.update({"modo_edicao_assunto": True}))
            with col2:
                buffer = gerar_docx(st.session_state["conteudo_gerado_assunto"], "Assunto Contextualizado")
                st.download_button(
                    label="📥 Baixar Assunto",
                    data=buffer,
                    file_name="assunto_contextualizado.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    key="download_assunto"
                )
            with col3:
                st.button("🆕 Novo Assunto", key="novo_assunto", on_click=lambda: st.session_state.update({
                    "conteudo_gerado_assunto": None,
                    "conteudo_editado_assunto": None,
                    "modo_edicao_assunto": False
                }))
            st.markdown("### Assunto Contextualizado Gerado ✅")
            st.markdown(st.session_state["conteudo_gerado_assunto"], unsafe_allow_html=True)
        else:
            st.markdown("### Editor do Assunto Contextualizado")
            st.session_state["conteudo_editado_assunto"] = st.text_area(
                "Edite o Assunto Contextualizado",
                value=st.session_state["conteudo_editado_assunto"],
                height=400,
                key="textarea_assunto"
            )
            col1, col2 = st.columns(2)
            with col1:
                st.button("💾 Salvar Edição", key="salvar_assunto", on_click=lambda: st.session_state.update({
                    "conteudo_gerado_assunto": st.session_state["conteudo_editado_assunto"],
                    "modo_edicao_assunto": False
                }))
            with col2:
                st.button("Cancelar", key="cancelar_assunto", on_click=lambda: st.session_state.update({"modo_edicao_assunto": False}))

### Aba 3: Questões
with tabs[2]:
    st.header("Questões")
    if st.session_state.get("questoes_geradas") is None:
        with st.form("questoes_form"):
            col1, col2 = st.columns(2)
            with col1:
                ano = st.selectbox("Ano / Série", ANOS_SERIES)
                componente = st.selectbox("Componente Curricular", COMPONENTES_CURRICULARES)
                assunto = st.text_input("Assunto (opcional)", placeholder="Exemplo: Frações")
                numero_questoes = st.number_input("Número de Questões", min_value=1, max_value=20, value=5)
            with col2:
                dificuldade = st.selectbox("Dificuldade", ["Selecione uma opção", "Fácil", "Médio", "Difícil"])
                tipo = st.selectbox("Tipo de Questões", ["Selecione uma opção", "Objetivas", "Dissertativas"])
            contexto = st.session_state.get("uploaded_file_content", None)
            gerar = st.form_submit_button("Gerar Questões ✅")
        if gerar:
            if ano == "Selecione uma opção" or componente == "Selecione uma opção" or dificuldade == "Selecione uma opção" or tipo == "Selecione uma opção":
                st.error("Por favor, preencha todos os campos obrigatórios!")
            else:
                with st.spinner("Gerando questões..."):
                    try:
                        questoes = gerar_questoes(ano, componente, assunto, dificuldade, numero_questoes, tipo, contexto)
                        st.session_state["questoes_geradas"] = questoes
                        st.session_state["questoes_editadas"] = questoes
                        st.session_state["modo_edicao_questoes"] = False
                        st.success("Questões geradas com sucesso!")
                    except Exception as e:
                        st.error(f"Erro ao gerar questões: {e}")
    if st.session_state.get("questoes_geradas") is not None:
        if not st.session_state.get("modo_edicao_questoes", False):
            st.markdown("###")
            col_editar, col_download, col_novo = st.columns([1, 1, 1])
            with col_editar:
                st.button("✏️ Editar Questões", key="editar_questoes", on_click=lambda: st.session_state.update({"modo_edicao_questoes": True}))
            with col_download:
                buffer = gerar_docx(st.session_state["questoes_geradas"], "Questões")
                st.download_button(
                    label="📥 Baixar Questões",
                    data=buffer,
                    file_name="questoes.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    key="download_questoes"
                )
            with col_novo:
                st.button("🆕 Novas Questões", key="novo_questoes", on_click=lambda: st.session_state.update({
                    "questoes_geradas": None,
                    "questoes_editadas": None,
                    "modo_edicao_questoes": False
                }))
            st.markdown("### Questões Geradas ✅")
            st.markdown(st.session_state["questoes_geradas"], unsafe_allow_html=True)
        else:
            st.markdown("### Editor de Questões")
            st.session_state["questoes_editadas"] = st.text_area(
                "Edite as Questões Geradas",
                value=st.session_state["questoes_editadas"],
                height=400,
                key="textarea_questoes"
            )
            col1, col2 = st.columns(2)
            with col1:
                st.button("💾 Salvar Edição", key="salvar_questoes", on_click=lambda: st.session_state.update({
                    "questoes_geradas": st.session_state["questoes_editadas"],
                    "modo_edicao_questoes": False
                }))
            with col2:
                st.button("Cancelar", key="cancelar_questoes", on_click=lambda: st.session_state.update({"modo_edicao_questoes": False}))

### Aba 4: Correção de Questões
with tabs[3]:
    st.header("Correção de Questões")
    st.info("🚧 Este módulo estará disponível em breve! Fique ligado.")
