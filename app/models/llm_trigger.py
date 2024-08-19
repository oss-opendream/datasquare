from langchain import PromptTemplate
from llm_utils import (load_model, keyword_extraction, metadata_search, metadata_processing, get_user_query, extract_answer)

# Prompts
phase1_prompt = """From the given user query, extract 10 keywords that represent the data that user needs.

### User Query: {user_query}

### Response:
"""

phase2_prompt = """Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request.

### Instruction:
Fill out the 'Request Template' based on the following input with user request and relevant datasets. The 'Request Template' is sent from the user to the relevant datasets ower.

### Input:
User Request: {user_query}

Relevant Dataset: {dataset_1}

'Request Template'
To: (format: Dataset owner)
From: (format: User name, Team name)
Subject:
Request detail:
Data usage purpose:
Data file format (eg. .csv, .jpeg, .py, .json, etc.):
Data period: (format: YYYY-MM-DD)
Data example:

### Response:
"""
# 임시 metadata
data_= {'title':['Resource usage statistics for cloud infrastructure','Server load data during peak and off-peak hours over the last year','Customer complaint records Q1','Customer service logs Q1','Employee performance reviews 2023','Customer feedback from product launch surveys'], 'owner':['Computing Team','Resource Team','Customer Support Team','Customer Support Team','HR','Marketing Team'], 'columns':[[1,2,3,4,5],[2,4,6,1,9],['id','date','purchase','complaint','product'],['id','product','price','date','detail'],['employee id','salary','performance','grading','date'],['id','detail','date','feedback','customer_since','annual purchase']]}

# langchain 구현
def llm_trigger(data:dict):

    llm = load_model()
    metadata = metadata_processing(data)

    # chain 1 (유저 쿼리 받고 키워드 추출단계)
    prompt1 = PromptTemplate.from_template(phase1_prompt)
    prompt2 = PromptTemplate.from_template(phase2_prompt)
    query = "I’m Emily, a customer service operations manager. I am managing a project aimed at reducing customer complaints by 15% over the next quarter. To support this initiative, I need access to customer service data for Q1 to analyze complaint trends and identify key areas for service improvement."

    phase1 = prompt1 | llm | keyword_extraction | metadata_search
    output_phase1 = phase1.invoke({"user_query": query})

    # 1 번째 데이터만 추출
    final_data_title = output_phase1[0]
    final_data_owner = metadata.loc[metadata['title'] == final_data_title, 'owner'].values[0]

    # issue 생성
    phase2 = prompt2 | llm
    output_phase2 = phase2.invoke({'user_query':query, 'dataset_1':f"{final_data_title} owned by {final_data_owner}"})

    # 생성된 issue 답변 추출, dictionary 형태로 반환 (각 인자별 추출필요)
    result_dict = extract_answer(output_phase2)
    
    return result_dict

if __name__ =="__main__":
    llm_trigger(data_)