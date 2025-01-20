import streamlit as st
from openai import OpenAI
import pandas as pd

# Obtém a chave da API OpenAI dos secrets
api_key = st.secrets["OPENAI_API_KEY"]

# Configuração do cliente OpenAI
client = OpenAI(api_key=api_key)

# Título da aplicação
st.title("🤖💬 Chatbot GPT Interativo com Client")

# Inicializar o histórico de mensagens na sessão
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {
            "role": "system",
            "content": (
                "Você é um assistente altamente qualificado em marketing digital, especializado em criar "
                "copywriting persuasivo e envolvente, além de roteiros criativos e estratégicos para reels no Instagram. "
                "Seu objetivo é ajudar usuários a alcançar engajamento máximo e conversões significativas, entregando "
                "respostas claras, criativas e alinhadas às melhores práticas do mercado. Você também pode sugerir "
                "técnicas modernas de marketing e storytelling para ampliar a eficácia dos conteúdos produzidos."
            )
        }
    ]

# Upload de arquivos
uploaded_file = st.file_uploader("Envie um arquivo (TXT, CSV)", type=["txt", "csv"])
if uploaded_file:
    file_type = uploaded_file.type

    if file_type == "text/plain":
        file_content = uploaded_file.read().decode("utf-8")
        st.success(f"Arquivo de texto '{uploaded_file.name}' processado com sucesso!")
        st.session_state["messages"].append(
            {"role": "user", "content": f"Recebi o seguinte texto do arquivo '{uploaded_file.name}':\n{file_content}"}
        )

    elif file_type == "text/csv":
        df = pd.read_csv(uploaded_file)
        st.dataframe(df)
        st.success(f"Arquivo CSV '{uploaded_file.name}' carregado com sucesso!")
        st.session_state["messages"].append(
            {
                "role": "user",
                "content": f"Recebi um arquivo CSV chamado '{uploaded_file.name}' com as seguintes colunas: {', '.join(df.columns)}"
            }
        )

# Exibir o histórico de mensagens
for message in st.session_state["messages"]:
    if message["role"] == "user":
        with st.chat_message("user"):
            st.markdown(message["content"])
    elif message["role"] == "assistant":
        with st.chat_message("assistant"):
            st.markdown(message["content"])

# Campo de entrada para o usuário
if user_input := st.chat_input("Digite sua mensagem:"):
    st.session_state["messages"].append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        try:
            # Chamada à API OpenAI
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=st.session_state["messages"]
            )
            # Corrigir o acesso ao conteúdo da resposta
            full_response = response.choices[0].message.content
            message_placeholder.markdown(full_response)
            st.session_state["messages"].append({"role": "assistant", "content": full_response})
        except Exception as e:
            message_placeholder.markdown(f"**Erro:** {e}")
