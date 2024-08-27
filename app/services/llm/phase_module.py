import torch
import gensim.downloader
import pandas as pd
from pandas import DataFrame
from transformers import BitsAndBytesConfig
from langchain_core.prompts import PromptTemplate
from langchain_community.llms.huggingface_pipeline import HuggingFacePipeline

from app.utils import prompts
from app.utils.docsim import DocSim


class LLMPhase:
    def __init__(
        self,
        data: dict,
        query: str,
        model_id: str = "meta-llama/Llama-2-7b-chat-hf"  # Temporary model
    ):
        self.data = data
        self.query = query
        self.model_id = model_id

        self.llm = self._load_model()
        self.metadata = self._metadata_processing(data)

        self.prompt1 = PromptTemplate.from_template(prompts.phase1)
        self.prompt2 = PromptTemplate.from_template(prompts.phase2)

        self.phase1 = self.prompt1 | self.llm
        self.phase2 = self.prompt2 | self.llm

    def _load_model(self) -> HuggingFacePipeline:
        '''
        llm 모델을 불러오는 함수.
        '''

        # Load the model with quantization
        llm = HuggingFacePipeline.from_model_id(
            model_id=self.model_id,
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
            },
        )

        return llm

    def _metadata_processing(self, data: dict) -> DataFrame:
        '''
        Receive dict format metadata and return in dataframe format.
        '''

        metadata = pd.DataFrame(data)
        metadata.to_csv('metadata_df.csv')

        return metadata

    def _keyword_extraction(self, text: str) -> list:
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

    def _metadata_search(self, keywords: list, metadata: DataFrame) -> list:
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

    def _extract_answer(self, response: str) -> dict:
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

    def _run_phase1(self):
        # phase 1: extract keywords from the user query & search the relevant metadata
        phase1_output = self.phase1.invoke({"user_query": self.query})

        keywords = self._keyword_extraction(phase1_output)
        most_relevant = self._metadata_search(keywords, self.metadata)

        return most_relevant

    def _run_phase2(self, most_relevant: list):
        # phase 2: select the most relevant metadata and generate issue
        final_data_title = most_relevant[0]
        final_data_owner = self.metadata.loc[self.metadata['title']
                                             == final_data_title, 'owner'].values[0]

        output_phase2 = self.phase2.invoke(
            {'user_query': self.query, 'dataset_1': f"{final_data_title} owned by {final_data_owner}"})

        result_dict = self._extract_answer(output_phase2)

        return result_dict

    def run_phases(self):
        most_relevant = self._run_phase1()
        return self._run_phase2(most_relevant)

    ### Codes below are (maybe) for future use ###

    # def _print_search_result(self, result: list, metadata: DataFrame) -> dict:
    #     '''
    #     Print metadata search outcome in desired format.
    #     '''

    #     result_dict = {result[0]: metadata.loc[metadata['title'] == result[0], 'owner'].values[0],
    #                    result[1]: metadata.loc[metadata['title'] == result[1], 'owner'].values[0],
    #                    result[2]: metadata.loc[metadata['title'] == result[2], 'owner'].values[0]}

    #     print(f'''The following is the most likely results that may contain the data you need.
    #             1. {result[0]} by {result_dict[result[0]]}
    #             2. {result[1]} by {result_dict[result[1]]}
    #             3. {result[2]} by {result_dict[result[2]]}
    #             ''')

    #     return result_dict

    # def _user_selection(self, phase1_result: dict) -> list:
    #     '''
    #     Extract the selected data.

    #     Return the title and the owner of the data
    #     '''

    #     while True:
    #         selection = input(
    #             '''Please select the data you want to generate the issue with DataSquare LLM! (Select number): ''')
    #         try:
    #             number = int(selection)
    #             title = list(phase1_result)[number-1]
    #             owner = phase1_result[title]
    #             result = [title, owner]
    #             break

    #         except:
    #             print('Please type in the number only. (eg. 1 or 2)')

    #     return result

    # def _get_user_query(self) -> str:
    #     '''Receive user query.
    #     '''

    #     user_query = input("Enter your request: ")

    #     return user_query
