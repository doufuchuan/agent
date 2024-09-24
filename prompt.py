"""

"""
from tools import gen_tools_desc
constraints = [
    "仅使用下面列出的动作",
    "不要连续执行同一action",
    "你只能主动行动，在计划行动时需要考虑到这一点",
    "你无法与物理对象交互，如果对于完成任务或目标是绝对必要的，则必须要求用户为你完成，如果用户拒绝，并且没有其他方法实现目标，则直接终止，避免浪费时间和精力"
]

resources = [
    "你是一个大语言模型，接收了大量文本的训练，包括大量的事实知识，利用这些知识来避免不必要的信息收集",
    "读取和写入文件的能力",
    "提供搜索和信息收集的互联网接入"
]

best_practices = [
    "不断地回顾和分析你的能力，确保发挥出你最大的能力",
    "不断地进行建设性的自我批评",
    "反思过去的决策和策略，完善你的方案",
    "每个动作执行都有代价，所以要聪明高效，目的是用最少的步骤完成任务",
    "利用你的信息收集能力来寻找你不知道的信息"
]



prompt_template = """
你是一个问答专家，你必须独立做出决策，无需需求用户的帮助，发挥你作为LLM的优势，追求简答的策略，不要涉及法律问题。

目标：
{query}

限制条件：
{constraints}

动作说明：这是你可以使用的额外动作，你执行的任何操作都必须通过以下操作之一实现：
{actions}
但此次不能进行该动作：{last_action}

资源说明：
{resources}

最佳实践的说明：
{best_practices}

agent_scratch:
{agent_scratch}

你应该只以json格式响应，响应格式如下：
{response_format_prompt}
确保响应结果可以由python json.loads()解析
"""

response_format_prompt = """
{
    "action": {
        "name": "action name",
        "args": {
            "args name": "args value"
        }
    },
    "thoughts": {
        "plan": "简短的描述短期和长期的计划列表",
        "criticism": "建设性的自我批评",
        "speak": "speak,当前步骤，返回给用户的总结", 
        "reasoning": "推理"
    },
    "observation": "观察当前任务的整体进度",
    
}
"""

# TODO: query, agent_scratch, actions
action_prompt = gen_tools_desc()
constraints_prompt = "\n".join([f"{idx+1}.{con}" for idx, con in enumerate(constraints)])
resources_prompt = "\n".join([f"{idx+1}.{con}" for idx, con in enumerate(resources)])
best_practices_prompt = "\n".join([f"{idx+1}.{con}" for idx, con in enumerate(best_practices)])

def gen_prompt(query, agent_scratch,last_action):
    prompt = prompt_template.format(query = query,
                                    constraints = constraints_prompt,
                                    actions = action_prompt,
                                    last_action = last_action,
                                    resources = resources_prompt,
                                    best_practices = best_practices_prompt,
                                    agent_scratch = agent_scratch,
                                    response_format_prompt = response_format_prompt)
    return prompt

user_msg = "根据指定的目标和迄今为止取得的进展，决定下一个要执行的action，并使用前面指定的json格式进行响应："