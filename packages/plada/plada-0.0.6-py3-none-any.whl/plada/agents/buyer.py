import random

class Buyer:
    def __init__(self, strategy):
        self.purchased_data = []
        self.step_purchased_data = None
        self.asset = 100
        self.strategy = strategy
        self.utility = 1
    
    def purchase(self, G):
        # 購入データを選択
        node = self.strategy.select_data(G, self.purchased_data)
        
        # 購入データがすでに購入済みの場合は何もしない
        if node in self.purchased_data:
            return None
        
        # 購入データが未購入の場合は購入
        self.step_purchased_data = node
        return node

    def end_step(self):
        # ステップ終了時に購入データを追加し、リセット
        if self.step_purchased_data is not None:
            self.purchased_data.append(self.step_purchased_data)
        self.step_purchased_data = None

class RandomStrategy:
    def select_data(self, G, _):
        return random.choice(list(G.nodes()))

class RelatedStrategy:
    def __init__(self, market, related_prob=0.8, random_prob=0.2):
        self.market = market
        self.related_prob = related_prob
        self.random_prob = random_prob
    
    def select_data(self, G, purchased_data):
        if not purchased_data:
            return random.choice(list(G.nodes()))
        
        # 0.8の確率で前回の購入履歴と繋がっているノードを選択
        if random.random() < self.related_prob:
            last_purchased_data = purchased_data[-1]
            neighbors = list(G.neighbors(last_purchased_data))
            
            if neighbors:
                probabilities = self.calc_probabilities(G, neighbors)
                return random.choices(neighbors, weights=[probabilities[node] for node in neighbors])[0]
            else:
                return random.choice(list(G.nodes()))
        else:
            # 0.2の確率でランダムにノードを選択
            return random.choice(list(G.nodes()))
    
    def calc_probabilities(self, G, target_nodes):
        total_purchase_count = sum(self.market.datasets[node].purchase_count for node in target_nodes)
        if total_purchase_count == 0:
            return {node: 1 / len(target_nodes) for node in target_nodes}
        probabilities = {node: (self.market.datasets[node].purchase_count + 1) / (total_purchase_count + len(target_nodes)) for node in target_nodes}
        
        # 確率を正規化
        total_prob = sum(probabilities.values())
        return {node: prob / total_prob for node, prob in probabilities.items()}

class RankingStrategy:
    def __init__(self, market):
        self.market = market
    
    def select_data(self, G, _):
        # ノードごとの購入確率を計算
        probabilities = self.calc_probabilities(G)
        
        # 確率に基づいてノードを選択
        weights = [probabilities[node] for node in list(G.nodes())]
        return random.choices(list(G.nodes()), weights=weights, k=1)[0]
    
    def calc_probabilities(self, G):
        total_purchase_count = sum(self.market.datasets[node].purchase_count for node in G.nodes())
        if total_purchase_count == 0:
            return {node: 1 / len(G.nodes()) for node in G.nodes()}
        probabilities = {node: (self.market.datasets[node].purchase_count + 1) / (total_purchase_count + len(G.nodes())) for node in G.nodes()}
        
        # 確率を正規化
        total_prob = sum(probabilities.values())
        return {node: prob / total_prob for node, prob in probabilities.items()}


def create_buyer(strategy_type, market):
        if strategy_type == "random":
            strategy = RandomStrategy()
        elif strategy_type == "related":
            strategy = RelatedStrategy(market)
        elif strategy_type == "ranking":
            strategy = RankingStrategy(market)
        else:
            raise ValueError(f"Unknown strategy: {strategy_type}")
        return Buyer(strategy)
