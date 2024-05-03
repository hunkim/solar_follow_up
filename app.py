# from https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps

import streamlit as st
from langchain_upstage import ChatUpstage as Chat
from langchain_upstage import GroundednessCheck

from langchain_core.output_parsers import StrOutputParser
from langchain_upstage import UpstageLayoutAnalysisLoader
from langchain_core.prompts import PromptTemplate

import tempfile, os, json

from vote import thumbs_up, thumbs_down, get_agents, set_agents
from agents import default_agents

import streamlit_google_oauth as oauth


llm = Chat()
groundedness_check = GroundednessCheck()

agent_results = {}

if "agents" not in st.session_state:
    st.session_state.agents = default_agents


def get_agent_response(agent, context):
    comon_instruction = "Please reply in the language of the context."
    prompt_str = (
        agent["instruction"] + "\n" + comon_instruction + "\n\n---\nCONTEXT: {context}"
    )

    for addition_context in agent.get("additional_context", []):
        prompt_str += "\n\n---\n" + addition_context + ": {" + addition_context + "}"

    prompt_template = PromptTemplate.from_template(prompt_str)

    chain = prompt_template | llm | StrOutputParser()

    return chain.stream(
        {
            "context": context,
            **agent_results,
        }
    )


def GC_response(agent, context, response):
    instruction = agent["instruction"]
    additional_context = agent.get("additional_context", [])
    for addition_context in additional_context:
        if addition_context in agent_results:
            context += "\n\n" + agent_results[addition_context]

    gc_result = groundedness_check.run(
        {
            "context": f"Context:{context}\n\nInstruction{instruction}",
            "answer": response,
        }
    )

    return gc_result.lower() == "grounded"


def run_follow_up():
    for agent in st.session_state.agents:
        with st.status(f"Running {agent['name']} agent ...", expanded=True):
            place = st.empty()
            place_info = st.empty()
            for i in range(3):
                response = place.write_stream(get_agent_response(agent, context))
                place_info.info(f"Checking the response. Trial {i+1} ...")
                if GC_response(agent, context, response):
                    place_info.success("Agent response is good!")
                    break

            # store the agent response
            agent_results[agent["name"]] = response


if __name__ == "__main__":
    st.title("Follow Up")
    st.write("This app is designed to help you follow up on your documents.")

    client_id = st.secrets["GOOGLE_CLIENT_ID"]
    client_secret = st.secrets["GOOGLE_CLIENT_SECRET"]
    redirect_uri = st.secrets["GOOGLE_REDIRECT_URI"]

    login_info = oauth.login(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        app_name="Login to configure agent",
        logout_button_text="Logout",
    )
    if login_info:
        user_id, user_email = login_info
        with st.expander(f"Configure the agent for {user_email}"):
            st.session_state.agents = get_agents(user_email)
            if not st.session_state.agents:
                st.session_state.agents = default_agents

            agent_text = st.text_area(
                "Add your agent in the JSON format: {name, instruction, additional_context}",
                value=json.dumps(st.session_state.agents, indent=2),
                height=500,
            )

            col1, col2, col3 = st.columns([1, 1, 5])
            with col1:
                if st.button("Save"):
                    try:
                        my_agents = json.loads(agent_text)
                        set_agents(user_email, json.loads(agent_text))
                    except:
                        st.error("Invalid JSON format!")
            with col2:
                if st.button("Reset"):
                    st.session_state.agents = default_agents
                    set_agents(user_email, default_agents)

    with st.sidebar:
        st.header(f"Add your conext such as text email or screenshots!")

        context = st.text_area("Paste your context here", height=120)
        uploaded_file = st.file_uploader(
            "Otional: Choose your pdf or image file", type=["png", "jpeg", "jpg", "pdf"]
        )
        button = st.button("Follow Up")

    if button and (context or uploaded_file):
        if uploaded_file and not uploaded_file.name:
            with st.status("Processing the data ..."):
                with tempfile.TemporaryDirectory() as temp_dir:
                    file_path = os.path.join(temp_dir, uploaded_file.name)

                    with open(file_path, "wb") as f:
                        f.write(uploaded_file.getvalue())

                    st.write("Indexing your document...")
                    layzer = UpstageLayoutAnalysisLoader(file_path, split="page")
                    # For improved memory efficiency, consider using the lazy_load method to load documents page by page.
                    docs = layzer.load()  # or layzer.lazy_load()

                    for doc in docs:
                        context += "\n\n" + str(doc)

        run_follow_up()

        col1, col2, col3, col4 = st.columns([8, 1, 1, 8])
        with col1:
            pass
        with col2:
            if st.button(":thumbsup:"):
                thumbs_up()
                st.success("Thank you for your feedback!")
        with col3:
            if st.button(":thumbsdown:"):
                thumbs_down()
                st.error("We will improve the service based on your feedback!")
        with col4:
            pass
