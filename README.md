# 图上下文数据集任务

## 数据集1

| 同类 `task` | 同个图 | 不同的问题 |
| ----------- | ------ | ---------- |

要求

只抽取 `connectivity`,`shortest`, `flow` 问题，因为这几个问题可修改：修改源点和终点

1. - 根据结点数不同，分为不同难度
     `easy: [5,35]; middle: (35,65], hard: (65,100]` ,
     即`easy: [5,36); middle: [36,66), hard: [66,101)` 
   - 图的数量尽量抽取 100 个，若难度范围内没有 100 个图，则全部抽取
   
   - 建立主键 `"graph"`，和键 `"complexity"`
   
2. 为每个问题生成同类别问题 ==16== 个

3. 每个问题使用自己的算法计算出正确答案，保证答案正确性

4. 答案格式使用 `###` 作为前缀符
   eg：`### Yes` 或 `### No`

> [example]
>
> 数据集的 `json` 格式：
>
> ```json
> {
>     "query":{},
>     "answer":{},
>     "task":{},		
>     "graph":{},  
>     "complexity":{},
>     "#task": "connectivity, shortest, flow",
>     "#graph": "图主键 graph<num>",
>     "#complexity": "easy, middle, hard"
> }
> ```
>



对应文件夹 `dataset1`



## 数据集2

| 不同类 `task` | 同个图 | 不同的问题 |
| ------------- | ------ | ---------- |

要求

1. ==100== 个图，全部抽取 `flow` 类任务的图
   建立主键 `"graph"`
   首先做有向图任务，再把指向去掉做无向图任务。（subgraph, triangle 暂时不做）
2. 为每个图生成 ==7== 个不同类别问题各 ==1== 个
   - 每个不可修改问题扩充成 ==9== 个问题，随机删除一条边不重复。（包括最初的一个图，删 8 次）
     我们近似地把删除一条边后的图看做和原图相同，故而 `"graph"` 的值不变
   - 每个可修改问题扩充成 ==9== 个问题，同数据集一进行问题随机化。 
3. 每个问题使用自己的算法计算出正确答案，保证答案正确性
4. 答案格式使用 `###` 作为前缀符
   eg：`### Yes` 或 `### No`

> [example]
>
> 数据集的 `json` 格式：
>
> ```json
> {
>     "query":{},
>     "answer":{},
>     "task":{},
>     "graph":{},
>     "edges": [
>         "[u, v, w]",
>     ],
>     "#edges": "[u, v, w] 表示从节点 u 到节点 v 的一条有向边，权重为 w"
> }
> ```
> 如果是不可修改的问题会加入 `removed_edge` 字段
>
> `"removed_edge": [u,v,w]`
> 值为 `null` 代表没有删除边，是原图的边集



| cycle  | connect | bipartite | topology                             |
| ------ | ------- | --------- | ------------------------------------ |
| Yes/No | Yes/No  | Yes/No    | topology sorting path<br />eg. [ , ] |

| shortest                               | triangle                                                     | flow                                              | hamilton | subgraph |
| -------------------------------------- | ------------------------------------------------------------ | ------------------------------------------------- | -------- | -------- |
| weight of the shortest path<br />(num) | maximum sum of the weights of three interconnected nodes<br />(num) | the maximum flow between the two nodes<br />(num) | Yes/No   | Yes/No   |



对应文件夹 `dataset2`



## 附录

### cycle 问题

- [x] 

无向图

> [example]
>
> Determine whether or not there is a cycle in an undirected graph. In an undirected graph, (i,j) means that node i and node j are connected with an undirected edge. Given a graph, you need to output Yes or No, indicating whether there is a cycle in the graph. Q: The nodes are numbered from 0 to 9, and the edges are: (0, 9) (0, 6) (0, 1) (0, 5) (0, 7) (1, 9) (1, 7) (1, 4) (1, 2) (2, 7) (2, 3) (2, 8) (2, 5) (2, 9) (3, 6) (3, 9) (3, 8) (4, 8) (4, 6) (6, 8) (6, 9). Is there a cycle in this graph?



answer：

1. `### Yes`
2. `### No`





### connectivity 问题

- [x] 

无向图

> [example]
>
> Determine whether two nodes are connected in an undirected graph. In an undirected graph, (i,j) means that node i and node j are connected with an undirected edge. Given a graph and a pair of nodes, you need to output Yes or No, indicating whether the node i and node j are connected. Q: The nodes are numbered from 0 to 19, and the edges are: (0, 11) (0, 16) (0, 7) (0, 5) (0, 12) (0, 15) (0, 17) (0, 19) (0, 4) (1, 2) (1, 13) (1, 12) (1, 15) (1, 5) (1, 19) (1, 18) (1, 10) (1, 8) (2, 8) (2, 6) (2, 4) (2, 15) (2, 11) (2, 5) (2, 10) (2, 7) (2, 12) (2, 13) (3, 10) (3, 18) (3, 16) (3, 12) (3, 19) (3, 14) (3, 5) (3, 17) (3, 11) (3, 4) (4, 12) (4, 10) (4, 8) (4, 17) (4, 11) (4, 13) (4, 5) (4, 7) (4, 19) (4, 6) (4, 16) (5, 16) (5, 7) (5, 12) (5, 15) (5, 10) (5, 13) (5, 11) (6, 12) (6, 10) (6, 18) (6, 16) (6, 9) (6, 14) (6, 19) (6, 13) (7, 12) (7, 14) (7, 16) (7, 15) (7, 8) (7, 13) (8, 13) (8, 18) (8, 11) (8, 14) (8, 19) (8, 15) (9, 18) (9, 10) (9, 13) (9, 17) (9, 15) (9, 11) (10, 19) (10, 14) (10, 15) (10, 13) (10, 12) (11, 14) (11, 18) (11, 12) (11, 17) (11, 13) (12, 19) (12, 15) (12, 16) (13, 15) (13, 14) (14, 15) (15, 18) (15, 17) (15, 19) (16, 18) (17, 19) (17, 18) (18, 19). Is there a path between node 6 and node 9?

- 可修改问题



answer：

1. `### Yes`
2. `### No`



### bipartite 问题

- [x] 

有向图

> [example]
>
> Determine whether or not a graph is bipartite. In a directed graph, (i->j) means that node i and node j are connected with an directed edge from node i to node j. Given a graph, you need to output Yes or No, indicating whether the graph is bipartite. Q: The nodes are numbered from 0 to 1, and the edges are: (0->1). Is this graph bipartite?



answer：

1. `### Yes`
2. `### No`

### topology 问题

- [x] 

有向图

> [example]
>
> Find one of the topology sorting paths of the given graph. In a directed graph, (i->j) means that node i and node j are connected with a directed edge from node i to node j. Given a graph, you need to output one of the topology sorting paths of the graph. Q: The nodes are numbered from 0 to 16, and the edges are: (0->10) (0->1) (0->7) (0->16) (0->4) (0->3) (0->2) (0->15) (0->6) (0->13) (0->8) (0->11) (1->16) (1->4) (1->7) (1->14) (1->6) (1->5) (1->2) (1->11) (1->12) (1->15) (1->10) (1->9) (1->13) (2->15) (2->9) (2->3) (2->12) (2->14) (2->11) (2->4) (2->8) (2->6) (2->10) (2->16) (3->15) (3->14) (3->13) (3->4) (3->8) (3->9) (3->7) (3->16) (3->6) (3->12) (4->14) (4->16) (4->10) (4->9) (4->5) (4->6) (4->12) (4->11) (5->8) (5->7) (5->9) (5->14) (5->12) (5->11) (5->13) (5->6) (6->12) (6->8) (6->9) (6->13) (6->15) (6->14) (6->16) (6->11) (6->10) (7->10) (7->15) (7->12) (7->16) (7->11) (7->8) (8->14) (8->11) (8->13) (8->12) (8->15) (8->9) (8->10) (9->13) (9->12) (9->15) (10->16) (10->15) (10->13) (10->11) (11->16) (11->15) (11->14) (11->12) (12->15) (12->13) (12->16) (12->14) (13->14) (13->15) (14->15) (14->16) (15->16). Give one topology sorting path of this graph.



answer  eg:

`### [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16] `



### shortest 问题

- [x] 

无向图

> [example]
> 
> Find the shortest path between two nodes in an undirected graph. In an undirected graph, (i,j,k) means that node i and node j are connected with an undirected edge with weight k. Given a graph and a pair of nodes, you need to output the shortest path between the two nodes. Q: The nodes are numbered from 0 to 37, and the edges are: (0,16,4) (0,23,3) (0,32,10) (0,27,5) (0,12,2) (0,24,9) (0,36,7) (1,13,3) (1,5,1) (1,31,4) (1,28,1) (1,2,9) (1,22,5) (1,24,1) (1,7,10) (1,6,1) (2,25,4) (2,13,4) (2,34,2) (2,5,7) (2,18,10) (2,19,8) (2,27,1) (3,35,9) (3,13,2) (3,32,1) (3,28,6) (3,17,8) (3,37,3) (4,16,5) (4,35,4) (5,31,8) (5,34,4) (5,15,5) (5,10,2) (5,20,2) (5,26,2) (6,8,3) (6,32,7) (6,12,6) (6,9,5) (7,36,10) (7,23,8) (7,24,8) (7,16,1) (7,27,7) (7,8,7) (8,12,6) (8,33,7) (8,35,4) (8,31,7) (9,37,2) (9,27,10) (9,33,7) (10,23,10) (10,27,6) (10,20,10) (10,19,8) (10,21,7) (10,30,8) (10,26,8) (10,18,9) (10,37,1) (11,25,2) (11,34,10) (11,16,2) (11,26,3) (11,12,8) (11,27,9) (11,33,4) (12,36,6) (12,25,6) (12,24,6) (12,19,10) (12,35,4) (12,15,3) (13,37,1) (13,20,4) (14,30,8) (14,34,6) (14,29,4) (14,35,9) (14,26,3) (15,19,9) (15,28,4) (15,23,5) (15,37,4) (15,17,1) (15,18,2) (15,36,4) (16,17,4) (17,33,9) (17,22,7) (18,34,5) (18,25,9) (19,30,2) (19,31,6) (19,20,4) (20,34,8) (20,37,1) (20,29,9) (20,30,4) (20,21,5) (21,26,1) (21,34,7) (21,36,8) (21,28,10) (21,35,10) (21,33,9) (22,29,10) (22,33,2) (22,35,1) (23,35,1) (23,26,2) (24,35,6) (24,31,4) (24,36,5) (25,36,4) (26,31,7) (26,32,1) (26,33,8) (26,35,1) (27,34,10) (27,30,5) (28,37,5) (28,30,8) (28,31,5) (28,29,5) (29,33,10) (29,31,3) (30,34,6) (31,37,10) (31,33,2) (32,36,1) (34,37,10). Give the weight of the shortest path from node 7 to node 33.

- 可修改问题

answer:

1. `### <num>`
2. `### There is no path between nodes`



### triangle 问题

- [ ] 

无向图

> [example]
> 
> Find the maximum sum of the weights of three interconnected nodes. In an undirected graph, [i, k] means that node i has the weight k. (i,j) means that node i and node j are connected with an undirected edge. Given a graph, you need to output the maximum sum of the weights of three interconnected nodes. Q: The nodes are numbered from 0 to 12, weights of nodes are: [0, 9] [1, 3] [2, 6] [3, 3] [4, 6] [5, 4] [6, 7] [7, 9] [8, 4] [9, 1] [10, 7] [11, 2] [12, 9], and the edges are: (0, 10) (0, 9) (2, 6) (7, 9) (9, 10). What is the maximum sum of the weights of three nodes?

最后搞

answer:

1. `### <num>`
2. `### No triples satisfy the condition`



### flow 问题

- [x] 

有向图

> [example]
> 
> Find the maximum flow between two nodes in a directed graph. In a directed graph, (i->j,k) means that node i and node j are connected with an directed edge from node i to node j with weight k. Given a graph and a pair of nodes, you need to output the maximum flow between the two nodes. Q: The nodes are numbered from 0 to 7, and the edges are: (0->7,8) (0->4,1) (0->2,9) (0->6,1) (1->7,8) (1->3,10) (1->6,5) (1->5,1) (4->5,2) (5->6,6) (6->7,2). What is the maximum flow from node 4 to node 7?

- 可修改问题

answer:

1. `### <num>`，除了 ``### 0`
2. `### 0`，表示两点间不连通

### hamilton 问题

- [x] 

无向图

> [example]
> 
> Determine whether or not there is a Hamiltonian path in an undirected graph. In an undirected graph, (i,j) means that node i and node j are connected with an undirected edge. Given a graph, you need to output Yes or No, indicating whether there is a Hamiltonian path in the graph. Q: The nodes are numbered from 0 to 1, and the edges are: (0, 1). Is there a Hamiltonian path in this graph?

哈密顿图处理问题：只回答 `Yes/No`.

原数据集 answer 有的 Yes 生成后会带上哈密顿路径



answer：

1. `### Yes`
2. `### No`



### subgraph 问题

- [ ] 

有向图

> [example]
> 
> Determine if a smaller graph is present as an exact match within a larger graph. In a directed graph, (i->j) means that node i and node j are connected with a directed edge from node i to node j. Given a graph G and a subgraph G', you need to output Yes or No, indicating whether subgraph G' is present within the directed graph G. Q: The nodes of graph G are numbered from 0 to 6, and the edges are: (0->2) (0->4) (1->3) (2->5) (3->4) (4->5). The nodes of subgraph G' are numbered from a to d, and the edges are: (a->b) (a->d) (a->c) (b->d) (b->c) (c->d). Is subgraph G' present within graph G as a direct substructure?





answer：

1. `### Yes`
2. `### No`
