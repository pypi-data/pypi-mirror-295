import json

class Saver:
    def __init__(self, file_path="result_notebook.json"):
        self.file_path = file_path
        self.results = {}
    
    def save(self, iteration, step, data_info, var_info, agent_info):
        if iteration not in self.results:
            self.results[iteration] = {}
        self.results[iteration][step] = {
            "data_info": data_info,
            "var_info": var_info,
            "agent_info": agent_info
        }
    
    def write_results(self):
        with open(self.file_path, 'w') as file:
            json.dump(self.results, file, indent=4)

