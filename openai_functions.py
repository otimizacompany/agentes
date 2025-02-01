import streamlit as st
from openai import OpenAI

def get_openai_client():
    # Pega a chave da API armazenada no st.secrets
    api_key = st.secrets["OPENAI_API_KEY"]
    return OpenAI(api_key=api_key)

def gerar_questoes(ano, componente, assunto, dificuldade, numero_questoes, tipo, contexto=None):
    """Função para gerar questões usando a OpenAI"""
    tipo_texto = "dissertativas" if tipo == "Dissertativas" else "objetivas"
    contexto_texto = f"Utilize o seguinte contexto: \n{contexto}\n\n" if contexto else ""

    prompt = f"""
    {contexto_texto}
    Crie um conjunto de {numero_questoes} questões {tipo_texto} sobre o seguinte assunto:
    - Ano/Série: {ano}
    - Componente Curricular: {componente}
    - Assunto: {assunto if assunto else "N/A"}
    - Dificuldade: {dificuldade}

    Certifique-se de que as questões sejam claras e adequadas ao nível de ensino informado.
    """
    client = get_openai_client()
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Você é um assistente especializado na criação de questões educacionais."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

def gerar_plano_aula(ano, componente, capitulo, modulo, duracao, metodologia, caracteristicas, assunto=None, contexto=None):
    """Função para gerar plano de aula usando a OpenAI"""
    contexto_texto = f"Utilize o seguinte contexto: \n{contexto}\n\n" if contexto else ""

    prompt = f"""
    {contexto_texto}
    Crie um plano de aula com as seguintes características:
    - Ano/Série: {ano}
    - Componente Curricular: {componente}
    - Capítulo do livro: {capitulo}
    - Módulo do capítulo: {modulo}
    - Assunto: {assunto}
    - Duração: {duracao} minutos
    - Metodologia: {metodologia}
    - Características da Turma: {caracteristicas if caracteristicas else "N/A"}
    """
    client = get_openai_client()
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Você é um assistente especializado em geração de planejamento educacional para os professores."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

def gerar_assunto_contextualizado(ano, componente, assunto, interesse, contexto=None):
    """Função para gerar um assunto contextualizado usando a OpenAI"""
    contexto_texto = f"Utilize o seguinte contexto: \n{contexto}\n\n" if contexto else ""

    prompt = f"""
    {contexto_texto}
    Crie um conteúdo contextualizado com as seguintes informações:
    - Ano/Série: {ano}
    - Componente Curricular: {componente}
    - Assunto: {assunto if assunto else "N/A"}
    - Tema de Interesse: {interesse if interesse else "N/A"}
    """
    client = get_openai_client()
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Você é um assistente especializado em gerar contextualização educacional."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

def corrigir_questoes(respostas_aluno, gabarito, tipo, contexto=None):
    """Função para corrigir questões usando a OpenAI"""
    tipo_texto = "dissertativas" if tipo == "Dissertativas" else "objetivas"
    contexto_texto = f"Utilize o seguinte contexto: \n{contexto}\n\n" if contexto else ""

    prompt = f"""
    {contexto_texto}
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
    client = get_openai_client()
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Você é um assistente especializado em correção de questões educacionais."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content
