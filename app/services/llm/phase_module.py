import gensim.downloader
import numpy as np
import pandas as pd
from pandas import DataFrame
import torch
from transformers import BitsAndBytesConfig
from langchain_community.llms.huggingface_pipeline import HuggingFacePipeline

from app.utils.docsim import DocSim


def metadata_processing(data: dict) -> DataFrame:
    '''
    Receive dict format metadata and return in dataframe format.
    '''

    metadata = pd.DataFrame(data)
    metadata.to_csv('metadata_df.csv')

    return metadata


def get_user_query() -> str:
    '''Receive user query.
    '''

    user_query = input("Enter your request: ")

    return user_query


def load_model() -> HuggingFacePipeline:
    '''
    llm 모델을 불러오는 함수.
    '''

    llama_2 = "meta-llama/Llama-2-7b-chat-hf"

    # Load the model with quantization
    llm = HuggingFacePipeline.from_model_id(
        model_id=llama_2,
        task="text-generation",
        model_kwargs={
            "quantization_config": BitsAndBytesConfig(
                load_in_4bit=True,  # 4bit로 quantization
                bnb_4bit_compute_dtype=torch.float16
            )
        },
        pipeline_kwargs={
            "max_new_tokens": 1024,
            "do_sample": True,
            "temperature": 0.01,
            "top_p": 0.9,
            "repetition_penalty": 1.15  # 반복을 통제
        }
    )

    return llm


def keyword_extraction(text: str) -> list:
    '''
    Extract keywords from the llm response in str format.
    '''

    key_list = []

    for i in range(10):
        start = f'{i+1}. '
        if i < 9:
            end = f'{i+2}. '
            keyword = text[text.find(start)+len(start):text.rfind(end)-1]
        else:
            end = '\n\n'
            keyword = text[text.find(start)+len(start):text.rfind(end)]
        key_list.append(keyword)

    return key_list


def metadata_search(keywords: list, metadata: DataFrame) -> list:
    '''
    Search relevant metadata matching the keywords.

    Use DocSim function
    '''

    metadata = pd.read_csv('metadata_df.csv', index_col=0)

    model_50 = gensim.downloader.load('glove-wiki-gigaword-50')

    query = ' '.join(keywords)

    ds_50 = DocSim(model_50)

    sim_score_50 = ds_50.calculate_similarity(
        query, [x for x in metadata['title']])

    selected_metadata = []

    for i in sim_score_50:
        selected_metadata.append(i['Data'])

    return selected_metadata  # return 3 targets with similarity score in higest order


def print_search_result(result: list, metadata: DataFrame) -> dict:
    '''
    Print metadata search outcome in desired format.
    '''

    result_dict = {result[0]: metadata.loc[metadata['title'] == result[0], 'owner'].values[0],
                   result[1]: metadata.loc[metadata['title'] == result[1], 'owner'].values[0],
                   result[2]: metadata.loc[metadata['title'] == result[2], 'owner'].values[0]}

    print(f'''The following is the most likely results that may contain the data you need.
          1. {result[0]} by {result_dict[result[0]]}
          2. {result[1]} by {result_dict[result[1]]}
          3. {result[2]} by {result_dict[result[2]]}
          ''')

    return result_dict


def user_selection(phase1_result: dict) -> list:
    '''
    Extract the selected data.

    Return the title and the owner of the data
    '''

    while True:
        selection = input(
            '''Please select the data you want to generate the issue with DataSquare LLM! (Select number): ''')
        try:
            number = int(selection)
            title = list(phase1_result)[number-1]
            owner = phase1_result[title]
            result = [title, owner]
            break

        except:
            print('Please type in the number only. (eg. 1 or 2)')

    return result


def extract_answer(response: str) -> dict:
    '''
    Extract items from the llm response.
    '''

    response_final = response[response.find(
        '### Response:')+len('### Response:'):]

    to_ = response_final[response_final.find(
        '\nTo:')+len('\nTo:'):response_final.rfind('\nFrom:')].strip('\n')

    from_ = response_final[response_final.find(
        '\nFrom:')+len('\nFrom:'):response_final.rfind('\nSubject:')].strip('\n')

    subject_ = response_final[response_final.find(
        '\nSubject:')+len('\nSubject:'):response_final.rfind('\nRequest Detail:')].strip('\n')

    request_detail_ = response_final[response_final.find('\nRequest Detail:')+len(
        '\nRequest Detail:'):response_final.rfind('\nData Usage Purpose:')].strip('\n')

    usage_purposes_ = response_final[response_final.find('\nData Usage Purpose: ')+len(
        '\nData Usage Purpose:'):response_final.rfind('\nData File Format:')].strip('\n')

    file_format_ = response_final[response_final.find('\nData File Format:')+len(
        '\nData File Format:'):response_final.rfind('\nData Period:')].strip('\n')

    data_preiod_ = response_final[response_final.find('\nData Period:')+len(
        '\nData Period:'):response_final.rfind('\nData Example:')].strip('\n')

    data_example_ = response_final[response_final.find(
        '\nData Example:')+len('\nData Example:'):].strip('\n')

    extracted_response = {'to': to_, 'from': from_, 'subject': subject_, 'request_detail': request_detail_, 'usage_purposes': usage_purposes_,
                          'data format': file_format_, 'data period': data_preiod_, 'data example': data_example_, 'full response': response_final}

    return extracted_response
