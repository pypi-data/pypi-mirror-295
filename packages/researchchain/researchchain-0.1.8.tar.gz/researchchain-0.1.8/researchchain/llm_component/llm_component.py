# %%
import json
from llmlinks.function import LLMFunction
from llmlinks.llm_client import LLMClient


class LLMComponent:
    def __init__(self, json_file_path=None, json_data=None):
        if json_file_path:
            with open(json_file_path, 'r') as file:
                self.json_data = json.load(file)
        elif json_data:
            if isinstance(json_data, str):
                self.json_data = json.loads(json_data)
            elif isinstance(json_data, dict):
                self.json_data = json_data
        else:
            raise ValueError("Either json_file_path or json_data must be provided.")
        self.input = self.json_data.get('input')
        self.output = self.json_data.get('output')
        self.prompt_template = self.json_data.get('prompt')
        print("LLMComponent initialized")
        print(f"input: {self.input}")
        print(f"output: {self.output}")
        
    def __call__(self, llm_name, memory_):
        """LLMComponentの実行

        Args:
            memory_ (_type_): _description_

        Returns:
            _type_: _description_
        """
        llm = LLMClient(llm_name)
        
        # LLMを複数回実行する場合
        if isinstance(self.input[0], list):
            num_loop = len(self.input)
            for i in range(num_loop):
                prompt = self.prompt_template[i]
                func = LLMFunction(
                    llm, 
                    prompt,
                    self.input[i],
                    self.output[i],
                )
                
                kwargs = {key: memory_[key] for key in self.input[i]}
                response = func(**kwargs)
                print('--------------------')
                print(f"response:{response}")
                for key in self.output[i]:
                    if response[key]:
                        memory_[key] = response[key][0]
                    else:
                        print(f"Warning: No data returned for [{response[key]}]")
            
        # LLMを一回だけ実行する場合
        else:
            func = LLMFunction(
                llm, 
                self.prompt_template,
                self.input,
                self.output,
            )
            
            kwargs = {key: memory_[key] for key in self.input}
            response = func(**kwargs)
            for key in self.output:
                memory_[key] = response[key][0]
        return memory_


if __name__ == "__main__":
    """
    memory = {
        'source': 'Hello World!!',
        'language': 'japanese',
        'output': None
        }
        
    # 基本となる処理の実行
    llm_name = 'gpt-4o-2024-08-06'
    json_file_path = './llm_component_test_file/base.json'
    translate = LLMComponent(json_file_path=json_file_path)
    memory1 = translate(llm_name, memory.copy())
    print(memory1)
    
    # outputが二つある場合の実行
    llm_name = 'gpt-4o-2024-08-06'
    json_file_path = 'llm_component_test_file/two_outputs.json'
    translate2 = LLMComponent(json_file_path=json_file_path)
    memory2 = translate2(llm_name, memory.copy())
    print(memory2)
    
    # llmの実行が2回ある場合の実行
    llm_name = 'gpt-4o-2024-08-06'
    json_file_path = 'llm_component_test_file/two_runs.json'
    translate3 = LLMComponent(json_file_path=json_file_path)
    memory3 = translate3(llm_name, memory.copy())
    print(memory3)

    # jsonデータを直接渡す場合
    llm_name = 'gpt-4o-2024-08-06'
    json_data = {
        "input": ["source", "language"],
        "output": ["output"],
        "prompt": "<source_text>\n{source}\n</source_text>\n<target_language>\n{language}\n</target_language>\n<rule>\nsource_text タグで与えられた文章を target_language で指定された言語に翻訳して output タグを用いて出力せよ．\n</rule>"
    }
    translate4 = LLMComponent(json_data=json_data)
    memory4 = translate4(llm_name, memory.copy())
    print(memory4)
    """

    llm_name = 'gpt-4o-2024-08-06'
    memory = {
        "environment" : 
        """
        The following two experimental environments are available
        ・Fine tuning of the LLM and experiments with rewriting the Optimizer or loss function.
        ・Verification of the accuracy of prompt engineering.
        """,
        "objective" : 
        """
        Batch Size Grokking: Assessing the impact of the training batchsize on the grokking phenomenon. Modify the experiments to dynamically adjust the batch size during training, starting with a small batch size and gradually increasing it. This could potentially lead to faster generalization on the validation set.
        """
        ,
    }
    json_data = {
        "input" : [
            ["environment","objective"],
            ["environment","objective", "keywords_mid_thought_1"]
            ],
        "output" : [
            ["keywords_mid_thought_1", "keywords_1"],
            ["keywords_1"]
            ],
        "prompt" : [
            "You have to think of a 5 KEYWORDs regarding academic search. There is a ojbective and limitation that we can handle, so you have to first interpret what the objective really means in keyword search. Answer step by step what do we need when thinking keywords.== OBJECTIVE ==\n{objective}== LIMITATION ==\n{environment}",
            "You have to think of a 5 KEYWORDs in in JSON format. Read all the information and make a report in JSON formatt\n\n You have to write keyword ONLY.\n\n== REPORT EXAMPLE ==\n{report_example}== OBJECTIVE ==\n{objective}== LIMITATION ==\n{environment}== THOUGHT ==\n{keywords_mid_thought}"
            ]
    }
    keyworder1 = LLMComponent(json_data = json_data)

    # 実行
    memory = keyworder1(llm_name, memory)
