import streamlit as st
from openai import OpenAI
from io import BytesIO
from docx import Document

# Configuração inicial
st.set_page_config(page_title="Agente IA para Professores", layout="wide")

# Obtém a chave da API OpenAI dos secrets
api_key = st.secrets["OPENAI_API_KEY"]

# Configuração do cliente OpenAI
client = OpenAI(api_key=api_key)

def gerar_questoes(ano, componente, assunto, dificuldade, numero_questoes, tipo):
    """Função para gerar questões usando a OpenAI"""
    tipo_texto = "dissertativas" if tipo == "Dissertativas" else "objetivas"
    prompt = f"""
    Crie um conjunto de {numero_questoes} questões {tipo_texto} sobre o seguinte assunto:
    - Ano/Série: {ano}
    - Componente Curricular: {componente}
    - Assunto: {assunto}
    - Dificuldade: {dificuldade}

    Certifique-se de que as questões sejam claras e adequadas ao nível de ensino informado.
    """
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "Você é um assistente especializado na criação de questões educacionais."},
                 {"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

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

def gerar_assunto_contextualizado(ano, componente, assunto, interesse):
    """Função para gerar um assunto contextualizado usando a OpenAI"""
    prompt = f"""
    Crie um conteúdo contextualizado com as seguintes informações:
    - Ano/Série: {ano}
    - Componente Curricular: {componente}
    - Assunto: {assunto}
    - Tema de Interesse: {interesse}
    """
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "Você é um assistente especializado em contextualização educacional."},
                 {"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

def corrigir_questoes(respostas_aluno, gabarito, tipo):
    """Função para corrigir questões usando a OpenAI"""
    tipo_texto = "dissertativas" if tipo == "Dissertativas" else "objetivas"
    prompt = f"""
    Corrija as seguintes questões {tipo_texto} respondidas por um aluno. Baseie-se no gabarito fornecido e forneça uma análise detalhada de cada resposta:

    Respostas do Aluno:
    {respostas_aluno}

    Gabarito:
    {gabarito}

    Para cada questão, avalie:
    1. Se a resposta está correta ou não.
    2. Para questões incorretas, explique o erro e forneça a resposta correta.
    3. Para questões dissertativas, avalie a qualidade da resposta e sugira melhorias.
    """
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "Você é um assistente especializado em correção de questões educacionais."},
                 {"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

def gerar_docx(conteudo, titulo):
    """Função para gerar um arquivo DOCX a partir do conteúdo fornecido"""
    doc = Document()
    doc.add_heading(titulo, level=1)
    doc.add_paragraph(conteudo)

    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

# Barra lateral
st.sidebar.title("Agente IA para Professores")
st.sidebar.markdown("Escolha um módulo:")
modulo = st.sidebar.selectbox("Módulos", ["Plano de Aula", "Assunto Contextualizado", "Questões", "Correção de Questões"])

# Tela principal
st.title("Agente IA para Professores")
st.markdown("Automatize tarefas e otimize seu planejamento educacional.")

if modulo == "Plano de Aula":
    st.header("Plano de Aula")

    # Layout com barra lateral e tela maior
    with st.sidebar:
        ano = st.selectbox("Ano / Série", ["Selecione uma opção", "1º Ano", "2º Ano", "3º Ano", "6º Ano EF"])
        componente = st.selectbox("Componente Curricular", ["Selecione uma opção", "Matemática", "Português", "Ciências", "Arte"])
        capitulo = st.selectbox("Capítulo", ["Selecione uma opção", "Introdução", "Desenvolvimento", "Conclusão"])
        modulo = st.selectbox("Módulo", ["Selecione uma opção", "Teórico", "Prático"])
        duracao = st.number_input("Duração da aula (min)", min_value=10, max_value=180, value=50)
        metodologia = st.selectbox("Metodologia", ["Selecione uma opção", "Expositiva", "Interativa", "Dinâmica"])
        caracteristicas = st.text_area("Características da Turma (opcional)", placeholder="Exemplo: Turma distraída, gosta de conversar durante a aula.")

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

                    # Botão para download
                    buffer = gerar_docx(plano_aula, "Plano de Aula")
                    st.download_button("Baixar Plano de Aula", data=buffer, file_name="plano_de_aula.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
                except Exception as e:
                    st.error(f"Erro ao gerar plano de aula: {e}")

elif modulo == "Assunto Contextualizado":
    st.header("Assunto Contextualizado")

    # Formulário de entrada
    with st.form("contexto_form"):
        col1, col2 = st.columns(2)

        with col1:
            ano = st.selectbox("Ano / Série", ["Selecione uma opção", "1º Ano", "2º Ano", "3º Ano", "6º Ano EF"])
            componente = st.selectbox("Componente Curricular", ["Selecione uma opção", "Matemática", "Português", "Ciências", "Arte"])
            assunto = st.text_input("Assunto", placeholder="Exemplo: Aceleração")

        with col2:
            interesse = st.text_input("Tema de Interesse (opcional)", placeholder="Exemplo: Fórmula 1")

        gerar = st.form_submit_button("Gerar Assunto Contextualizado")

    if gerar:
        if ano == "Selecione uma opção" or componente == "Selecione uma opção" or not assunto:
            st.error("Por favor, preencha todos os campos obrigatórios!")
        else:
            with st.spinner("Gerando assunto contextualizado..."):
                try:
                    contexto = gerar_assunto_contextualizado(ano, componente, assunto, interesse)
                    st.success("Assunto contextualizado gerado com sucesso!")
                    st.markdown(contexto)

                    # Botão para download
                    buffer = gerar_docx(contexto, "Assunto Contextualizado")
                    st.download_button("Baixar Assunto Contextualizado", data=buffer, file_name="assunto_contextualizado.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
                except Exception as e:
                    st.error(f"Erro ao gerar assunto contextualizado: {e}")

elif modulo == "Questões":
    st.header("Questões")

    # Formulário de entrada
    with st.form("questoes_form"):
        col1, col2 = st.columns(2)

        with col1:
            ano = st.selectbox("Ano / Série", ["Selecione uma opção", "1º Ano", "2º Ano", "3º Ano", "6º Ano EF"])
            componente = st.selectbox("Componente Curricular", ["Selecione uma opção", "Matemática", "Português", "Ciências", "Arte"])
            assunto = st.text_input("Assunto", placeholder="Exemplo: Frações")
            numero_questoes = st.number_input("Número de Questões", min_value=1, max_value=20, value=5)

        with col2:
            dificuldade = st.selectbox("Dificuldade", ["Selecione uma opção", "Fácil", "Médio", "Difícil"])
            tipo = st.selectbox("Tipo de Questões", ["Selecione uma opção", "Objetivas", "Dissertativas"])

        gerar = st.form_submit_button("Gerar Questões")

        if gerar:
            if (
                ano == "Selecione uma opção"
                or componente == "Selecione uma opção"
                or not assunto
                or dificuldade == "Selecione uma opção"
                or tipo == "Selecione uma opção"
            ):
                st.error("Por favor, preencha todos os campos obrigatórios!")
            else:
                with st.spinner("Gerando questões..."):
                    try:
                        questoes = gerar_questoes(
                            ano=ano,
                            componente=componente,
                            assunto=assunto,
                            dificuldade=dificuldade,
                            numero_questoes=int(numero_questoes),
                            tipo=tipo,
                        )
                        st.success("Questões geradas com sucesso!")
                        st.markdown(questoes)

                        # Botão para download
                        buffer = gerar_docx(questoes, "Questões")
                        st.download_button("Baixar Questões", data=buffer, file_name="questoes.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
                    except Exception as e:
                        st.error(f"Erro ao gerar questões: {e}")

elif modulo == "Correção de Questões":
    st.header("Correção de Questões")

    # Formulário de entrada
    with st.form("correcao_form"):
        col1, col2 = st.columns(2)

        with col1:
            tipo = st.selectbox("Tipo de Questões", ["Selecione uma opção", "Objetivas", "Dissertativas"])
            respostas_aluno = st.text_area("Respostas do Aluno", placeholder="Insira as respostas do aluno aqui...")

        with col2:
            gabarito = st.text_area("Gabarito", placeholder="Insira o gabarito correspondente aqui...")

        corrigir = st.form_submit_button("Corrigir Questões")

    if corrigir:
        if tipo == "Selecione uma opção" or not respostas_aluno or not gabarito:
            st.error("Por favor, preencha todos os campos obrigatórios!")
        else:
            with st.spinner("Corrigindo questões..."):
                try:
                    correcao = corrigir_questoes(respostas_aluno, gabarito, tipo)
                    st.success("Correção concluída com sucesso!")
                    st.markdown(correcao)

                    # Botão para download
                    buffer = gerar_docx(correcao, "Correção de Questões")
                    st.download_button("Baixar Correção", data=buffer, file_name="correcao_questoes.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
                except Exception as e:
                    st.error(f"Erro ao corrigir questões: {e}")
