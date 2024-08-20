phase1 = '''From the given user query, extract 10 keywords that represent the data that user needs.

### User Query: {user_query}

### Response:
'''

phase2 = '''Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request.

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
'''
