import streamlit as st
from openai import OpenAI

# Configuração inicial
st.set_page_config(page_title="Agente IA para Professores", layout="wide")

# Obtém a chave da API OpenAI dos secrets
api_key = st.secrets["OPENAI_API_KEY"]

# Configuração do cliente OpenAI
client = OpenAI(api_key=api_key)

def gerar_plano_aula(ano, componente, capitulo, modulo, duracao, metodologia, caracteristicas):
    """Função para gerar plano de aula usando a OpenAI"""
    prompt = f"""
    Crie um plano de aula com as seguintes características:
    - Ano/Série: {ano}
    - Componente Curricular: {componente}
    - Capítulo: {capitulo}
    - Módulo: {modulo}
    - Duração: {duracao} minutos
    - Metodologia: {metodologia}
    - Características da Turma: {caracteristicas}
    """
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "Você é um assistente especializado em planejamento educacional."},
                 {"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# Barra lateral
st.sidebar.title("Agente IA para Professores")
st.sidebar.markdown("Escolha um módulo:")
modulo = st.sidebar.selectbox("Módulos", ["Plano de Aula", "Assunto Contextualizado", "Questões (Em breve)", "Questões Adaptadas (Em breve)"])

# Tela principal
st.title("Agente IA para Professores")
st.markdown("Automatize tarefas e otimize seu planejamento educacional.")

if modulo == "Plano de Aula":
    st.header("Plano de Aula")

    # Layout com barra lateral e tela maior
    with st.sidebar:
        ano = st.selectbox("Ano / Série", ["Selecione uma opção", "1º Ano", "2º Ano", "3º Ano", "6º Ano EF"])
        componente = st.selectbox("Componente Curricular", ["Selecione uma opção", "Matemática", "Português", "Ciências", "Arte"])
        capitulo = st.selectbox("Capítulo", ["Selecione uma opção", "Introdução", "Desenvolvimento", "Conclusão", "Capítulo 2 - Arte"])
        modulo = st.selectbox("Módulo", ["Selecione uma opção", "Teórico", "Prático", "Módulo 4 - O que você..."])
        duracao = st.number_input("Duração da aula (min)", min_value=10, max_value=180, value=50)
        metodologia = st.selectbox("Metodologia", ["Selecione uma opção", "Expositiva", "Interativa", "Dinâmica", "Aula expositiva"])
        caracteristicas = st.text_area("Características da Turma (opcional)",
                                      placeholder="Exemplo: Turma distraída, gosta de conversar durante a aula.")

    # Botão para gerar plano de aula
    gerar = st.sidebar.button("Gerar Plano de Aula")

    if gerar:
        if ano == "Selecione uma opção" or componente == "Selecione uma opção" or capitulo == "Selecione uma opção" or modulo == "Selecione uma opção" or metodologia == "Selecione uma opção":
            st.error("Por favor, preencha todos os campos obrigatórios!")
        else:
            with st.spinner("Gerando plano de aula..."):
                try:
                    plano_aula = gerar_plano_aula(ano, componente, capitulo, modulo, duracao, metodologia, caracteristicas)
                    st.success("Plano de aula gerado com sucesso!")
                    st.markdown(plano_aula)
                except Exception as e:
                    st.error(f"Erro ao gerar plano de aula: {e}")

elif modulo == "Assunto Contextualizado":
    st.header("Assunto Contextualizado")
    st.markdown("Este módulo estará disponível em breve.")
else:
    st.header(f"{modulo}")
    st.markdown("Este módulo estará disponível em breve.")
