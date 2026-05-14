import streamlit as st
from google import genai

api_key = st.secrets.GeminiAPI.api_key
prompt_settings = st.secrets.AppSettings.chatbot_setting
client = genai.Client(api_key=api_key)

# st.session_stateを使いメッセージのやりとりを保存
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# チャットボットとやりとりする関数
def communicate():

    messages = st.session_state["messages"]

    # ユーザーメッセージ追加
    user_message = {
        "role": "user",
        "content": st.session_state["user_input"]
    }

    messages.append(user_message)

    # Geminiへ渡すプロンプト作成
    prompt = prompt_settings

    for msg in messages:
        prompt += f"{msg['role']}: {msg['content']}\n"

    # Geminiへ送信
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config ={"temperature": 1.5}
    )

    # AIメッセージ追加
    bot_message = {
        "role": "assistant",
        "content": response.text
    }

    messages.append(bot_message)

    # 入力欄を空にする
    st.session_state["user_input"] = ""


# UI
st.title("My AI Assistant")
st.write("Gemini API を使ったチャットボットです。")

user_input = st.text_input(
    "メッセージを入力してください。",
    key="user_input",
    on_change=communicate
)

# 会話履歴表示
chat_container = st.container(height=400)

with chat_container:

    if st.session_state["messages"]:

        messages = st.session_state["messages"]

        for message in messages:

            # ユーザー吹き出し
            if message["role"] == "user":
                with st.chat_message("user"):
                    st.write(message["content"])

            # AI吹き出し
            elif message["role"] == "assistant":
                with st.chat_message("assistant"):
                    st.write(message["content"])
