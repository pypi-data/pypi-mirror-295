class Market:
    def __init__(self, G) -> None:
        self.G = G
        self.datasets = {}
        self.initialize_market()
    
    # 市場の各ノードをDataとして初期化
    def initialize_market(self):
        for node in self.G.nodes():
            variables = [int(var) for var in self.G.nodes[node]['variables'].split(',')]
            self.datasets[node] = Data(node, variables)
    
    # 市場全体でデータ価格の更新
    def update_data_prices(self):
        for data_id, data in self.datasets.items():
            data.update_price()
    
    # 市場全体でデータの購入回数を更新
    def update_data_purchase_count(self, buyers):
        for data_id, data in self.datasets.items():
            data.update_purchase_count(buyers)

class Data:
    def __init__(self, data_id, variables) -> None:
        self.data_id = data_id
        self.price = 0
        self.variables = {var_id: Variable(var_id, 10) for var_id in variables}
        self.purchase_count = 0 # このデータが合計で何回購入されたか
    
    # データの購入回数の更新
    def update_purchase_count(self, buyers):
        self.purchase_count = sum(
            1 for buyer in buyers if buyer.step_purchased_data == self.data_id
        )
    
    # データ価格の更新
    def update_price(self):
        self.price = sum(var.get_price() for var in self.variables.values())

class Variable:
    def __init__(self, var_id, price=10) -> None:
        self.var_id = var_id
        self.price = price
    
    def set_price(self, price):
        self.price = price
    
    def get_price(self):
        return self.price