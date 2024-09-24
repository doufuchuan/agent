
# agent入口
"""
1. 加载环境变量
2. 工具引入
3. prompt模板
4. 模型初始化、调用
"""
import time
from tools import tools_map
from prompt import gen_prompt, user_msg
from model_provider import ModelProvider
from dotenv import load_dotenv
load_dotenv()
mp = ModelProvider()

def parse_thoughts(response):

    try:
        thoughts = response.get("thoughts")
        observation = response.get("observation")
        plan = thoughts.get("plan")
        reasoning = thoughts.get("reasoning")
        criticism = thoughts.get("criticism")
        prompt = f"plan: {plan}\n reasoning:{reasoning}\n criticism:{criticism}\n observation:{observation}"
        return prompt
    except Exception as err:
        print("parse thoughts err: {}".format(err))
        return "".format(err)
    

def agent_execute(query, max_request_time = 10):
    cur_request_time = 0
    chat_history = []  # 历史记忆 
    agent_scratch = ""
    last_action = ""
    flag = False
    while cur_request_time < max_request_time:
        cur_request_time += 1
        # 达到预期结果，则直接返回
        """
            prompt包含的功能：
                任务描述
                工具描述
                用户的输入user_msg
                assistant_msg
                限制
                给出更好实践的描述

        """
        #记录上次调用的工具，添加到prompt，避免连续执行同一操作
        prompt = gen_prompt(query, agent_scratch,last_action) 
        start_time = time.time()
        print("------{} 开始调用大模型-----".format(cur_request_time), flush=True)
        # call LLM
        """
        sys_prompt:
        user_msg, assistant, history
        """
        response = mp.chat(prompt, chat_history)

        end_time = time.time()
        print("------{} 调用大模型结束”耗时{}".format(cur_request_time, end_time - start_time), flush=True)

        if not response or not isinstance(response, dict):
            print("错误，重试....", response)
            continue

        """格式
        response: 
        {
            "action": {
                "name": "action_name",
                "args": {
                    "args_name": "args value"
                }
            },
            "thoughts": {
                "text": "thought",
                "plan": "plan",
                "criticism": "criticism",
                "speak": "speak,当前步骤返回给用户的总结", 
                "reasoning": " "
            }
        }
        """
        # print(response)
        action_info = response.get("action")
        action_name = action_info.get("name")
        action_args = action_info.get("args")
        print("当前action: ",action_name, action_args)
        
        thoughts = response.get("thoughts")
        plan = thoughts.get("plan")
        reasoning = thoughts.get("reasoning")
        criticism = thoughts.get("criticism")
        observation = thoughts.get("speak")
        print("observation:{}".format(observation))
        print("plan:{}".format(plan))
        print("reasoning:{}".format(reasoning))
        print("criticism:{}".format(criticism))

        if action_name == "finish":
            final_answer = action_args.get("answer")
            print("final_answer:", final_answer)
            break

        if action_name == "write_to_file":
            flag = True
        
        observation = response.get("observation")
        try:
            """
                action_name到函数的映射：map-> {action_name: func}
            """
            func = tools_map.get(action_name)
            call_func_result = func(**action_args)
            last_action = action_name
            print("调用结果："+call_func_result)
        except Exception as err:
            print("调用工具异常：",err)
            call_func_result = "{}".format(err)

        agent_scratch = agent_scratch + "\n: observation:{}\n execute action result: {}\n".format(observation, call_func_result)

        
        assistant_msg = parse_thoughts(response)
        chat_history.append([user_msg, assistant_msg])
    if cur_request_time == max_request_time:
        if flag:
            print("未找到最佳结果，但存在已有回答") # 找不到最好结果，就保持当前已经搜索到的
        else:
            print("任务失败")

    else:
        print("任务成功")
    

def main():
    # 支持用户多次交互
    max_request_time = 10
    while True:
        query = input("输入：")
        if query == "exit":
            return
        agent_execute(query, max_request_time = max_request_time)

    pass

if __name__ == "__main__":
    main()
