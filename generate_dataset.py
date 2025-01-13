import utils
import graph_algo
import random
import utils
import networkx as nx
import shutil


def generate_cycle_question(task):
    """
    生成一个合法的环问题
    :param task: 任务字典
    :return: 修改后的 query 字符串
    """
    query = task['query']

    # 提取节点数量和边
    node_num = graph_algo.extract_node_num(query)
    edges = task['edges']

    # 生成节点范围描述
    node_range_desc = f"The nodes are numbered from 0 to {node_num - 1}"
    
    # 生成边描述（只使用前两个元素 u 和 v）
    edges_desc = "(" + ") (".join([f"{u}, {v}" for u, v, _ in edges]) + ")"
    
    # 组合成完整的 query 字符串
    new_query = (
        f"Determine whether or not there is a cycle in an undirected graph. "
        f"In an undirected graph, (i,j) means that node i and node j are connected with an undirected edge. "
        f"Given a graph, you need to output Yes or No, indicating whether there is a cycle in the graph. "
        f"Q: {node_range_desc}, and the edges are: {edges_desc}. Is there a cycle in this graph?"
    )

    return new_query


def generate_connectivity_question(task, dataset_type, used_pairs=None):
    """
    随机生成一个合法的连通性问题，并替换 query 的最后一句
    确保选取的两个节点是连通的，并且问题不重复
    对于无向图，(i,j) 和 (j,i) 被视为同一个节点对
    :param task: 任务字典
    :param dataset_type: 数据集类型，1 为 dataset1，2 为 dataset2
    :param used_pairs: 已经使用过的节点对集合，默认为 None
    :return: 修改后的 query 字符串和更新后的 used_pairs 集合
             如果所有可能的节点对都已使用，则返回 None
    """
    query = task['query']
    if used_pairs is None:
        used_pairs = set()  # 初始化已使用的节点对集合

    # 提取节点数量
    node_num = graph_algo.extract_node_num(query)

    # 计算所有可能的节点对（无向图，确保 (i,j) 和 (j,i) 被视为同一个节点对）
    all_pairs = set()
    for x in range(node_num):
        for y in range(x + 1, node_num):  # 避免重复，只生成 (i,j) 其中 i < j
            all_pairs.add((x, y))

    # 如果所有节点对都已使用，则返回 None
    if used_pairs.issuperset(all_pairs):
        return None, used_pairs

    # 随机选择一个未使用的节点对
    available_pairs = all_pairs - used_pairs
    x, y = random.choice(list(available_pairs))

    # 将新节点对添加到已使用集合
    used_pairs.add((x, y))

    # 生成新的问题
    question = f"Is there a path between node {x} and node {y}?"

    if(dataset_type == 1):
        # 找到最后一个句号的位置
        last_period_index = query.rfind('.')

        # 如果找到句号，则替换其后的内容
        if last_period_index != -1:
            # 截取最后一个句号之前的内容
            prefix = query[:last_period_index + 1]
            # 组合成新的 query
            new_query = f"{prefix} {question}"
        else:
            raise ValueError("最后一行不是问题")
    elif(dataset_type == 2):
        # 生成节点范围描述
        node_range_desc = f"The nodes are numbered from 0 to {node_num - 1}"
        
        # 生成边描述（只使用前两个元素 u 和 v）
        edges_desc = "(" + ") (".join([f"{u}, {v}" for u, v, _ in task['edges']]) + ")"
        
        # 组合成完整的 query 字符串
        new_query = (
            f"Determine whether two nodes are connected in an undirected graph. "
            f"In an undirected graph, (i,j) means that node i and node j are connected with an undirected edge. "
            f"Given a graph and a pair of nodes, you need to output Yes or No, indicating whether the node i and node j are connected. "
            f"Q: {node_range_desc}, and the edges are: {edges_desc}. {question}"
        )

    return new_query, used_pairs

def generate_bipartite_question(task):
    """
    生成一个合法的二分图问题
    :param task: 任务字典
    :return: 修改后的 query 字符串
    """
    query = task['query']

    # 提取节点数量和边
    node_num = graph_algo.extract_node_num(query)  
    edges = task['edges']

    # 生成节点范围描述
    node_range_desc = f"The nodes are numbered from 0 to {node_num - 1}"
    
    # 生成边描述（只使用前两个元素 u 和 v）
    edges_desc = "(" + ") (".join([f"{u}->{v}" for u, v, _ in edges]) + ")"
    
    # 组合成完整的 query 字符串
    new_query = (
        f"Determine whether or not a graph is bipartite. "
        f"In a directed graph, (i->j) means that node i and node j are connected with a directed edge from node i to node j. "
        f"Given a graph, you need to output Yes or No, indicating whether the graph is bipartite. "
        f"Q: {node_range_desc}, and the edges are: {edges_desc}. Is this graph bipartite?"
    )

    return new_query

def generate_topology_sort_question(task):
    """
    生成一个合法的拓扑排序问题
    :param task: 任务字典
    :return: 修改后的 query 字符串
    """
    query = task['query']

    # 提取节点数量和边
    node_num = graph_algo.extract_node_num(query)  
    edges = task['edges']

    # 生成节点范围描述
    node_range_desc = f"The nodes are numbered from 0 to {node_num - 1}"
    
    # 生成边描述（只使用前两个元素 u 和 v）
    edges_desc = "(" + ") (".join([f"{u}->{v}" for u, v, _ in edges]) + ")"
    
    # 组合成完整的 query 字符串
    new_query = (
        f"Find one of the topology sorting paths of the given graph. "
        f"In a directed graph, (i->j) means that node i and node j are connected with a directed edge from node i to node j. "
        f"Given a graph, you need to output one of the topology sorting paths of the graph. "
        f"Q: {node_range_desc}, and the edges are: {edges_desc}. Give one topology sorting path of this graph."
    )

    return new_query

def generate_shortest_path_question(task, dataset_type, used_pairs=None):
    """
    随机生成一个合法的最短路径问题，并替换 query 的最后一句
    优先使用连通的节点对，如果所有连通节点对都已使用，则允许使用不连通节点对
    对于无向图，(i,j) 和 (j,i) 被视为同一个节点对
    :param query: 原始 query 字符串
    :param dataset_type: 数据集类型，1 为 dataset1，2 为 dataset2
    :param used_pairs: 已经使用过的节点对集合，默认为 None
    :return: 修改后的 query 字符串和更新后的 used_pairs 集合
             如果所有可能的节点对都已使用，则返回 None
    """
    query = task['query']

    if used_pairs is None:
        used_pairs = set()  # 初始化已使用的节点对集合

    # 提取节点数量和边
    if dataset_type == 1:
        edges = graph_algo.extract_edges_c(query)  
    elif dataset_type == 2:
        edges = task['edges']
    node_num = graph_algo.extract_node_num(query)
        

    # 创建 networkx 图
    G = nx.Graph()
    G.add_nodes_from(range(0, node_num))  # 添加所有节点
    G.add_weighted_edges_from(edges)  # 添加带权边

    # 计算所有可能的节点对（无向图，确保 (i,j) 和 (j,i) 被视为同一个节点对）
    all_pairs = set()
    for x in range(node_num):
        for y in range(x + 1, node_num):  # 避免重复，只生成 (i,j) 其中 i < j
            all_pairs.add((x, y))

    # 计算所有可能的连通节点对
    all_connected_pairs = set()
    for x, y in all_pairs:
        if nx.has_path(G, x, y):
            all_connected_pairs.add((x, y))

    # 如果所有节点对都已使用，则返回 None
    if used_pairs.issuperset(all_pairs):
        return None, used_pairs

    # 优先使用未使用的连通节点对
    available_connected_pairs = all_connected_pairs - used_pairs
    if available_connected_pairs:
        x, y = random.choice(list(available_connected_pairs))
    else:
        # 如果没有未使用的连通节点对，则使用未使用的不连通节点对
        available_disconnected_pairs = all_pairs - used_pairs - all_connected_pairs
        if not available_disconnected_pairs:
            return None, used_pairs  # 如果没有未使用的节点对，返回 None
        x, y = random.choice(list(available_disconnected_pairs))

    # 将新节点对添加到已使用集合
    used_pairs.add((x, y))

    # 生成新的问题
    question = f"Give the weight of the shortest path from node {x} to node {y}."

    if dataset_type == 1:
        # 找到最后一个句号的位置
        last_period_index = query.rfind('.')
        if last_period_index == -1:
            raise ValueError("没有句号")

        # 在最后一个句号之前的部分字符串中，找到倒数第二个句号的位置
        second_last_period_index = query.rfind('.', 0, last_period_index)

        # 如果找到句号，则替换其后的内容
        if second_last_period_index != -1:
            # 截取最后一个句号之前的内容
            prefix = query[:second_last_period_index + 1]
            # 组合成新的 query
            new_query = f"{prefix} {question}"
        else:
            raise ValueError("最后一行不是问题")
    elif dataset_type == 2:
        # 生成节点范围描述
        node_range_desc = f"The nodes are numbered from 0 to {node_num - 1}"
        
        # 生成边描述（只使用前两个元素 u 和 v）
        edges_desc = "(" + ") (".join([f"{u},{v},{w}" for u, v, w in edges]) + ")"
        
        # 组合成完整的 query 字符串
        new_query = (
            f"Find the shortest path between two nodes in an undirected graph. "
            f"In an undirected graph, (i,j,k) means that node i and node j are connected with an undirected edge with weight k. "
            f"Given a graph and a pair of nodes, you need to output the weight of the shortest path between the two nodes. "
            f"Q: {node_range_desc}, and the edges are: {edges_desc}. {question}"
        )

    return new_query, used_pairs

def generate_max_flow_question(query, used_pairs=None):
    """
    随机生成一个合法的最大流问题，并替换 query 的最后一句
    优先使用连通的节点对，如果所有连通节点对都已使用，则允许使用不连通节点对
    对于有向图，(i,j) 和 (j,i) 被视为不同的节点对
    :param query: 原始 query 字符串
    :param used_pairs: 已经使用过的节点对集合，默认为 None
    :return: 修改后的 query 字符串和更新后的 used_pairs 集合
             如果所有可能的节点对都已使用，则返回 None
    """
    if used_pairs is None:
        used_pairs = set()  # 初始化已使用的节点对集合

    # 提取节点数量和边
    node_num = graph_algo.extract_node_num(query)
    edges = graph_algo.extract_edges_d(query)  

    # 创建 networkx 有向图
    G = nx.DiGraph()
    G.add_nodes_from(range(0, node_num))  # 添加所有节点
    G.add_weighted_edges_from(edges)  # 添加带权边

    # 计算所有可能的节点对（有向图，(i,j) 和 (j,i) 被视为不同的节点对）
    all_pairs = set()
    for x in range(node_num):
        for y in range(node_num):
            if x != y:
                all_pairs.add((x, y))

    # 计算所有可能的连通节点对
    all_connected_pairs = set()
    for x, y in all_pairs:
        if nx.has_path(G, x, y):  # 检查是否存在从 x 到 y 的路径
            all_connected_pairs.add((x, y))

    # 如果所有节点对都已使用，则返回 None
    if used_pairs.issuperset(all_pairs):
        return None, used_pairs

    # 优先使用未使用的连通节点对
    available_connected_pairs = all_connected_pairs - used_pairs
    if available_connected_pairs:
        source, target = random.choice(list(available_connected_pairs))
    else:
        # 如果没有未使用的连通节点对，则使用未使用的不连通节点对
        available_disconnected_pairs = all_pairs - used_pairs - all_connected_pairs
        if not available_disconnected_pairs:
            return None, used_pairs  # 如果没有未使用的节点对，返回 None
        source, target = random.choice(list(available_disconnected_pairs))

    # 将新节点对添加到已使用集合
    used_pairs.add((source, target))

    # 生成新的问题
    question = f"What is the maximum flow from node {source} to node {target}?"

    # 找到最后一个句号的位置
    last_period_index = query.rfind('.')

    # 如果找到句号，则替换其后的内容
    if last_period_index != -1:
        # 截取最后一个句号之前的内容
        prefix = query[:last_period_index + 1]
        # 组合成新的 query
        new_query = f"{prefix} {question}"
    else:
        raise ValueError("最后一行不是问题")

    return new_query, used_pairs

def generate_hamiltonian_path_question(task):
    """
    生成一个合法的哈密顿路径问题
    :param task: 任务字典
    :return: 修改后的 query 字符串
    """
    query = task['query']

    # 提取节点数量和边
    node_num = graph_algo.extract_node_num(query) 
    edges = task['edges']

    # 生成节点范围描述
    node_range_desc = f"The nodes are numbered from 0 to {node_num - 1}"
    
    # 生成边描述（只使用前两个元素 u 和 v）
    edges_desc = "(" + ") (".join([f"{u}, {v}" for u, v, _ in edges]) + ")"
    
    # 组合成完整的 query 字符串
    new_query = (
        f"Determine whether or not there is a Hamiltonian path in an undirected graph. "
        f"In an undirected graph, (i,j) means that node i and node j are connected with an undirected edge. "
        f"Given a graph, you need to output Yes or No, indicating whether there is a Hamiltonian path in the graph. "
        f"Q: {node_range_desc}, and the edges are: {edges_desc}. Is there a Hamiltonian path in this graph?"
    )

    return new_query

def generate_dataset1():
    """
    抽取数据集任务 50 条
    生成 dataset1 的新任务 connectivity, flow, shortest
    """
    flag_sampled1 = True   # 是否已经采样过 dataset1
    if flag_sampled1 == False:
        utils.sample_dataset1()
    generate_size = 15  # 需要生成的新 query 数量
    sample_path = "sampled-dataset1"
    STR_sampled_ = "sampled_"
    task_list = ['connectivity', 'flow', 'shortest']
    # task_list = ['flow']
    dataset_path = 'dataset1'

    for task_name in task_list:
        sampled_file = f"{sample_path}/{STR_sampled_}{task_name}.json"  # 已采样的样本文件
        sampled_tasks = utils.load_data(sampled_file)

        # 用于存储新生成的任务
        new_tasks = []

        for task in sampled_tasks:
            # 生成 generate_size 个新 query
            new_tasks.append(task)
            used_pairs = None
            for _ in range(generate_size):
                # 复制原始任务，避免修改原始数据
                new_task = task.copy()

                # 替换 query
                # 生成新的问题
                if(task_name == 'connectivity'):
                    new_question, used_pairs = generate_connectivity_question(new_task['query'], 1, used_pairs)

                elif(task_name == 'flow'):
                    new_question, used_pairs = generate_max_flow_question(new_task['query'], 1, used_pairs)
                    
                elif(task_name == 'shortest'):
                    new_question, used_pairs = generate_shortest_path_question(new_task['query'], 1, used_pairs)
                    
                # 替换 query
                new_task["query"] = new_question

                # 将新任务添加到列表中
                new_tasks.append(new_task)

        # 保存新生成的任务到文件
        output_file = f"{dataset_path}/generated_{task_name}.json"
        utils.save_data(new_tasks, output_file)
        print(f"已生成 {len(new_tasks)} 个新任务，保存到 {output_file}")

        # 为生成的任务计算正确答案
        for task_name in task_list:
            utils.get_answer(dataset_path,task_name=task_name)

def generate_dataset2():
    """
    抽取 flow 数据集 100 条，作为图
    生成其他 8 类任务数据集 dataset2 
    """
    flag_sampled1 = True   # 是否已经采样过 dataset2
    if flag_sampled1 == False:
        utils.sample_dataset2()

    sample_path = "sampled-dataset2"
    STR_sampled_ = "sampled_"
    task_list = ['cycle', 'connectivity','bipartite', 'topology', 'shortest', 'flow', 'hamilton']
    # task_list = ['hamilton']
    dataset_path = 'dataset2'

    for task_name in task_list:

        sampled_file = f"{sample_path}/{STR_sampled_}flow.json"  # 已采样的样本文件
        sampled_tasks = utils.load_data(sampled_file)

        if task_name == 'flow':
            try:
                output_file = f"{dataset_path}/generated_flow.json"
                shutil.copy(sampled_file, output_file)
                print(f"已复制文件 {sampled_file} 到 {output_file}")
            except FileNotFoundError:
                print(f"文件 {sampled_file} 未找到，无法复制。")
            continue  # 跳过后续生成步骤，直接处理下一个任务

        # 用于存储新生成的任务
        new_tasks = []

        for task in sampled_tasks:
            # 复制原始任务，避免修改原始数据
            new_task = task.copy()

            # 替换 query
            # 生成新的问题
            if(task_name == 'cycle'):
                new_question = generate_cycle_question(new_task)

            elif(task_name == 'connectivity'):
                new_question, _ = generate_connectivity_question(new_task, 2)
            
            elif(task_name == 'bipartite'):
                new_question = generate_bipartite_question(new_task)
            
            elif(task_name == 'topology'):
                new_question = generate_topology_sort_question(new_task)

            elif(task_name == 'shortest'):
                new_question, _ = generate_shortest_path_question(new_task, 2)

            elif(task_name == 'hamilton'):
                new_question = generate_hamiltonian_path_question(new_task)
                
            # 替换 query
            new_task["query"] = new_question
            new_task["task"] = task_name

            # 将新任务添加到列表中
            new_tasks.append(new_task)

        # 保存新生成的任务到文件
        output_file = f"{dataset_path}/generated_{task_name}.json"
        utils.save_data(new_tasks, output_file)
        print(f"已生成 {len(new_tasks)} 个新任务，保存到 {output_file}")

    # 为生成的任务计算正确答案
    for task_name in task_list:
        if task_name == 'flow':
            continue
        utils.get_answer(dataset_path,task_name=task_name)

def test_cycle():
    """
    测试 generate_cycle_question 函数
    """
    task = {
        "query": "Determine whether or not there is a cycle in an undirected graph. In an undirected graph, (i,j) means that node i and node j are connected with an undirected edge. Given a graph, you need to output Yes or No, indicating whether there is a cycle in the graph. Q: The nodes are numbered from 0 to 4, and the edges are: (0, 1) (1, 2) (2, 3) (3, 4). Is there a cycle in this graph?",
        "edges": [(0, 1, 1), (1, 2, 1), (2, 3, 1), (3, 4, 1)]
    }
    new_query = generate_cycle_question(task)
    print(new_query)

def test_connectivity():
    """
    测试 generate_connectivity_question 函数
    """
    task = {
        "query": "Determine whether two nodes are connected in an undirected graph. In an undirected graph, (i,j) means that node i and node j are connected with an undirected edge. Given a graph and a pair of nodes, you need to output Yes or No, indicating whether the node i and node j are connected. Q: The nodes are numbered from 0 to 4, and the edges are: (0, 1) (1, 2) (2, 3) (3, 4). Is there a path between node 0 and node 4?",
        "edges": [(0, 1, 1), (1, 2, 1), (2, 3, 1), (3, 4, 1)]
    }
    used_pairs = set()
    for _ in range(10):
        new_query, used_pairs = generate_connectivity_question(task, 2, used_pairs)
        print(new_query)
    print(f"used_pairs: {used_pairs}")

def test_bipartite():
    """
    测试 generate_bipartite_question 函数
    """
    task = {
        "query": "Determine whether or not a graph is bipartite. In a directed graph, (i->j) means that node i and node j are connected with a directed edge from node i to node j. Given a graph, you need to output Yes or No, indicating whether the graph is bipartite. Q: The nodes are numbered from 0 to 4, and the edges are: (0->1) (1->2) (2->3) (3->4). Is this graph bipartite?",
        "edges": [(0, 1, 1), (1, 2, 1), (2, 3, 1), (3, 4, 1)]
    }
    new_query = generate_bipartite_question(task)
    print(new_query)

def test_topology_sort():
    """
    测试 generate_topology_sort_question 函数
    """
    task = {
        "query": "Find one of the topology sorting paths of the given graph. In a directed graph, (i->j) means that node i and node j are connected with a directed edge from node i to node j. Given a graph, you need to output one of the topology sorting paths of the graph. Q: The nodes are numbered from 0 to 4, and the edges are: (0->1) (1->2) (2->3) (3->4). Give one topology sorting path of this graph.",
        "edges": [(0, 1, 1), (1, 2, 1), (2, 3, 1), (3, 4, 1)]
    }
    new_query = generate_topology_sort_question(task)
    print(new_query)

def test_shortest_path():
    """
    测试 generate_shortest_path_question 函数
    """
    task={
        "query": "Find the shortest path from node 0 to node 4. Q: The nodes are numbered from 0 to 4, and the edges are: (0, 1, 1) (1, 2, 1) (2, 3, 1) (3, 4, 1). Give the weight of the shortest path from node 0 to node 4.",
        "edges": [(0, 1, 1), (1, 2, 1), (2, 3, 1), (3, 4, 1)]
    }
    used_pairs = set()
    for _ in range(10):
        new_query, used_pairs = generate_shortest_path_question(task, 2, used_pairs)
        print(new_query)

def test_hamiltonian_path():
    """
    测试 generate_hamiltonian_path_question 函数
    """
    task = {
        "query": "Determine whether or not there is a Hamiltonian path in an undirected graph. In an undirected graph, (i,j) means that node i and node j are connected with an undirected edge. Given a graph, you need to output Yes or No, indicating whether there is a Hamiltonian path in the graph. Q: The nodes are numbered from 0 to 4, and the edges are: (0, 1) (1, 2) (2, 3) (3, 4). Is there a Hamiltonian path in this graph?",
        "edges": [(0, 1, 1), (1, 2, 1), (2, 3, 1), (3, 4, 1)]
    }
    new_query = generate_hamiltonian_path_question(task)
    print(new_query)

if __name__ == "__main__":
    # generate_dataset1()
    generate_dataset2()
    # test_cycle()
    # test_connectivity()
    # test_bipartite()
    # test_topology_sort()
    # test_shortest_path()
    # test_hamiltonian_path()
    # test_max_flow()