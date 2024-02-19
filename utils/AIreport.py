import streamlit as st
from openai import OpenAI
from copy import deepcopy

# Models: "gpt-4-0125-preview", "gpt-3.5-turbo-0125"
# Question to our report AI

content = f"""
    Je bent een deskundig adviseur in de gebouwde omgeving voor de stad Amsterdam. Je bent gevraagd een rapport te schrijven voor een dasboard waarin je verschillende scenario’s voor de circulaire economie vergelijkt.
    De scenario's verschillen in: hoeveelheid m2 die wordt gebruikt voor woningen, het soort gebouwen dat wordt gebruikt en de totale impact afhankelijk van het type gebouw dat wordt gebruikt.
    Schrijf een beknopt rapport van max 100 woorden waarin u de verschillende scenario's, de voor- en nadelen van elk scenario.
    Gebruik feitelijke cijfers uit de tabel bij het opbouwen van uw betoog. Geef geen eindconclusie, of inleidingmaar begin meteen met de analyse
    Dit zijn de scenariogegevens:
    """

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
session = st.session_state

def create_report_message(content) -> dict:
    role = "assistant"
    content += str(session.scenarios)
    message = {"role": role, "content": content}
    return message

def get_ai_report(message):
    report = client.chat.completions.create(
        model="gpt-4-0125-preview",
        messages=[message], 
        stream=True
    )
    return report

def produce_report(container):
    try:
        message = create_report_message(content)
        stream = get_ai_report(message)
                
        if 'ai_report_text' not in session:
            text_chunks = []
            for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    with container:
                        text_chunks.append(chunk.choices[0].delta.content)            
                        st.write(''.join(text_chunks))
            session['ai_report_text'] = ''.join(text_chunks)  # Store the text

    except Exception as e:
        print(e)