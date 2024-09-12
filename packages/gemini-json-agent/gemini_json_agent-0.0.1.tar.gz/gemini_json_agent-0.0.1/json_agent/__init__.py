from gemini_agents_toolkit import agent


PROMPT = ["""
You are an a library that is designed to be producing JSON files accorindg to the asks from the customers.

Possible input that can be:
* JSON file content that needs to be checked and do small correction of mistakes
* other data strucutres, like YAML, to be converted to the JSON

Outputs requirenments:
Your output STRICTLY should be JSON content, it will be saved to JSON file by customer. Therefore 
the output should NOT have any prefix/postfix. For example do not wrap your output in ```. 
Do not provide any explanation of what you did an why, just output the final version of the json
"""]


def create_agent(*, model_name="gemini-1.5-flash", debug=False, history_depth=1, on_message=None):
    return agent.create_agent_from_functions_list(
         model_name=model_name, 
         debug=debug, 
         system_instruction=PROMPT, 
         add_scheduling_functions=False,
         recreate_client_each_time=True,
         on_message=on_message)