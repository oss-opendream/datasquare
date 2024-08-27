from app.services.llm.phase_module import LLMPhase


def llm_trigger(data: dict, query: str) -> dict:
    '''
    Triggers langchain.
    '''

    phase = LLMPhase(data, query)

    try:
        result_dict = phase.run_phases()
    except Exception:
        result_dict = {}

    return result_dict
