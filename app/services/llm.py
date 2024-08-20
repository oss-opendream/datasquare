from langchain_core.prompts import PromptTemplate

from app.utils.llm import *
from app.utils import prompts


def llm_trigger(data: dict, query: str) -> dict:
    '''
    Triggers langchain.
    '''

    llm = load_model()
    metadata = metadata_processing(data)

    # phase 1: extract keywords from the user query & search the relevant metadata
    phase1_prompt = prompts.phase1
    phase2_prompt = prompts.phase2

    prompt1 = PromptTemplate.from_template(phase1_prompt)
    prompt2 = PromptTemplate.from_template(phase2_prompt)

    phase1 = prompt1 | llm
    output_phase1 = phase1.invoke({"user_query": query})

    keywords = keyword_extraction(output_phase1)
    most_relevant = metadata_search(keywords, metadata)

    # phase 2: select the most relevant metadata and generate issue
    final_data_title = most_relevant[0]
    final_data_owner = metadata.loc[metadata['title']
                                    == final_data_title, 'owner'].values[0]

    phase2 = prompt2 | llm
    output_phase2 = phase2.invoke(
        {'user_query': query, 'dataset_1': f"{final_data_title} owned by {final_data_owner}"})

    result_dict = extract_answer(output_phase2)

    return result_dict
