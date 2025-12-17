from dotenv import load_dotenv

load_dotenv()

import os
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

# =========================
# 環境変数の読み込み
# =========================
load_dotenv()

if "OPENAI_API_KEY" not in os.environ:
    st.error("OPENAI_API_KEY が設定されていません。.env を確認してください。")
    st.stop()

# =========================
# LLM呼び出し関数
# =========================
def ask_llm(input_text: str, expert_type: str) -> str:
    """
    入力テキストと専門家タイプを受け取り、
    LLMの回答を返す
    """

    if expert_type == "A":
        system_prompt = (
            "あなたはIT・ソフトウェア開発の専門家です。"
            "技術的に正確で、初心者にも分かりやすく説明してください。"
        )
    else:
        system_prompt = (
            "あなたはビジネス戦略の専門家です。"
            "実務に役立つ視点で、簡潔かつ論理的に説明してください。"
        )

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.5
    )

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=input_text)
    ]

    response = llm.invoke(messages)

    return response.content


# =========================
# Streamlit UI
# =========================
st.title("専門家切り替え型 LLM Webアプリ")

st.markdown("""
### アプリ概要
入力したテキストに対して、
選択した専門家として振る舞う LLM が回答します。

### 操作方法
1. 専門家を選択
2. テキストを入力
3. 送信ボタンをクリック
""")

expert_type = st.radio(
    "専門家の種類を選択してください",
    ["A", "B"],
    format_func=lambda x: "A：IT・ソフトウェア開発の専門家"
    if x == "A"
    else "B：ビジネス戦略の専門家"
)

input_text = st.text_area(
    "入力テキスト",
    height=150
)

if st.button("送信"):
    if not input_text.strip():
        st.warning("入力テキストを入力してください。")
    else:
        with st.spinner("回答を生成しています..."):
            answer = ask_llm(input_text, expert_type)

        st.subheader("回答結果")
        st.write(answer)
