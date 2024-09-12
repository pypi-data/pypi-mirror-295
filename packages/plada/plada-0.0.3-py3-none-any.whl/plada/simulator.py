from tqdm import tqdm

def run_single_step(buyers, market) -> None:
    """
    1ステップのシミュレーションを実行する関数
    """
    for buyer in buyers:
        buyer.purchase(market.G)

def end_step(buyers):
    for buyer in buyers:
        buyer.end_step()

def run_sim(buyers, market, numSteps) -> dict:
    saver = {}
    
    for step in range(numSteps):
        # データ価格の更新
        market.update_data_prices()
        
        # 全ての買い手について1ステップのシミュレーションを実行
        run_single_step(buyers, market)
        
        # ステップ終了時の結果を保存
        saver[f"step_{step}"] = {
            "data_info": get_data_info(market, buyers),
            "var_info": get_var_info(market),
            "agent_info": get_agent_info(buyers)
        }
        
        end_step(buyers)
    
    return saver

def get_data_info(market, buyers) -> list:
    data_info = []
    
    for data in market.G.nodes():
        num_purchased = sum(
            1 for buyer in buyers if data == buyer.step_purchased_data
        )
        data_info.append({
            "data_id": data,
            "price": market.datasets[data].price,
            "num_purchased": num_purchased
        })
    
    return data_info

def get_var_info(market) -> list:
    var_info = []
    combined_dict = {}
    
    for data in market.G.nodes():
        variables_dict = market.datasets[data].variables
        combined_dict.update(variables_dict)
    
    sorted_var_dict = {key: combined_dict[key] for key in sorted(combined_dict)}
    
    for var_id, variable in sorted_var_dict.items():
        var_info.append({
            "var_id": variable.var_id,
            "price": variable.price
        })
    return var_info

def get_agent_info(buyers) -> list:
    agent_info = []
    
    for i, buyer in enumerate(buyers):
        agent_info.append({
            "agent_id": i,
            "step_purchased_data": buyer.step_purchased_data,  # ステップごとのデータ
            "asset": buyer.asset,  # 資産
            "utility": buyer.utility,  # 効用
        })
    
    return agent_info

