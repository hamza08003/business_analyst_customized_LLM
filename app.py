import streamlit as st
import pandas as pd
from services.pdf_processor import process_pdf
from services.website_processor import process_website
from services.vectorizer import create_embeddings_and_vector_store
from utils.pdf_displayer import displayPDF
from utils.questions import porters_five_forces, systemic_thinking, cynefin_framework
from services.query_model import query_gemini_model
from utils.report_generator import generate_pdf_report
import time


# Initialize session state for storing results from the analysis
if 'results' not in st.session_state:
    st.session_state['results'] = None

if 'startup_name' not in st.session_state:
    st.session_state['startup_name'] = None


# Streamlit UI
st.set_page_config(page_title="Document & Website Analyzer", page_icon=":mag:", layout="centered")

st.title("🔍 Automated Business Analyst")
st.markdown("<p style='text-align: center; font-size: 18px; font-weight: bold; font-style: italic; font-family: Arial, sans-serif;'>🚀 Uncover insights from your documents and web pages effortlessly</p>", unsafe_allow_html=True)
# st.markdown("All you need to do is upload a PDF file and input a website link of the Business. Then, hit the 'Analyze' button to generate insightful results")


with st.container():
    st.markdown('<div class="input-container">', unsafe_allow_html=True)
    pdf_file = st.file_uploader("Upload PDF", type=["pdf"], key="pdf_uploader")
    website_url = st.text_input("Website URL", key="website_input")
    startup_name = st.text_input("Startup Name", key="startup_name")
    st.markdown('</div>', unsafe_allow_html=True)



if st.button("Analyze", use_container_width=True):

    if pdf_file is None or not website_url or not startup_name:
        st.error("Please upload a PDF, input a website URL, and provide the startup name.")

    else:
        st.info("Hang tight, this might take a while...")
        time.sleep(1.5)

        with st.status("Gathering Data...", expanded=True) as status:

            st.write("Reading PDF...")
            pdf_chunks = process_pdf(pdf_file)
            
            st.write("Fetching website data...")
            website_chunks = process_website(website_url)

            combined_chunks = pdf_chunks + website_chunks

            st.write("Creating embeddings and vector store...")
            _, vector_store = create_embeddings_and_vector_store(combined_chunks)

            status.update(label="Data Processing Completed!", state="complete", expanded=False)

        with st.status("Analyzing Business...", expanded=True) as status:

            all_questions = {
                "Porter's Five Forces": porters_five_forces,
                "Systemic Thinking": systemic_thinking,
                "Cynefin Framework": cynefin_framework
            }

            progress_bar = st.progress(10, text="Porter's Five Forces Analysis...")

            results = []

            for idx, (analysis_type, questions) in enumerate(all_questions.items()):
                for question_text, question_prompt in questions.items():
                    context = " ".join([doc.page_content for doc in vector_store.similarity_search(query=question_prompt)])
                    # Check if the question is a rating question
                    if "Rating" in question_text:
                        # Modify the prompt for rating questions
                        response = query_gemini_model(f"Given the context: {context}, answer the following question \n\n {question_prompt}")
                    else:
                        # Use separate prompt for other questions
                        response = query_gemini_model(f"Given the context: {context}, answer the following question short to the point (no more than 300 words):\n\n {question_prompt}")

                    results.append((analysis_type, question_text, response))

                if analysis_type == "Porter's Five Forces":
                    progress_bar.progress(35, text="Systemic Thinking Analysis...")
                elif analysis_type == "Systemic Thinking":
                    progress_bar.progress(70, text="Cynefin Framework Analysis...")
                elif analysis_type == "Cynefin Framework":
                    progress_bar.progress(100, text="Querying Complete...")

            status.update(label="Analysis Complete!", state="complete", expanded=False)


        # Generate conclusion based on all results
        all_responses = " ".join([response for _, _, response in results])
        conclusion_prompt = f"Based on the following analysis results, provide a short to the point conclusion for this startup:\n\n{all_responses}"
        conclusion = query_gemini_model(conclusion_prompt)
        results.append(("Conclusion", "Conclusion", conclusion))

        # Store results in session state
        st.session_state['results'] = results

        # Store analysis results in a DataFrame
        df_results = pd.DataFrame(results, columns=["Analysis type", "Question", "Answer"])
        df_results = df_results.sort_values(by="Analysis type")

        # Display analysis results in an organized table format
        for analysis_type in df_results['Analysis type'].unique():
            with st.expander(f"{analysis_type} Analysis"):
                analysis_data = df_results[df_results['Analysis type'] == analysis_type].drop(columns=['Analysis type', 'Question'])
                st.table(analysis_data)

        
# PDF generation and download
if st.session_state['results']:
    # if st.button("Download Report", use_container_width=True):
        report_data_bytes = generate_pdf_report(st.session_state['results'], st.session_state['startup_name'])
        displayPDF(report_data_bytes)
        # st.download_button("Download PDF", data=report_data, file_name=f"{st.session_state['startup_name']}_Report.pdf", mime="application/pdf", use_container_width=True)


# Button to Restart the app
if st.button('Restart Over', use_container_width=True):
    st.session_state['results'] = None
    st.experimental_rerun()
