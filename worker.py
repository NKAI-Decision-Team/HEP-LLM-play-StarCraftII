from sc2_rl_agent.starcraftenv_test.env.starcraft_env import StarCraftEnvSelector
from sc2_rl_agent.starcraftenv_test.utils.action_info import ActionDescriptions
from sc2_rl_agent.starcraftenv_test.prompt.prompt import *
from sc2_rl_agent.starcraftenv_test.agent.chatgpt_agent import ChatGPTAgent
from sc2_rl_agent.starcraftenv_test.agent.glm4_agent import Glm4Agent

def agent_test(agent, env, args=None):
    """
    通用的代理测试函数
    """
    # 如果args中包含特定于代理的设置或参数，可以在这里使用
    if args is not None:
        process_id = args.process_id
        # 如果需要，可以在这里使用process_id

    observation, _ = env.reset()  # 获取初始观察
    done = False

    while not done:
        action = agent.action(observation)
        observation, reward, done, result, info = env.step(action)

        if done:
            break


def chatgpt_worker(input_args):
    """
    为多进程定义的工作函数
    """
    # 使用args中的设置创建环境
    args = input_args

    selector = StarCraftEnvSelector(args)
    env = selector.create_env()

    action_description = ActionDescriptions(env.player_race)
    action_dict = action_description.action_descriptions

    sc2prompt = StarCraftII_HEP(race=args.player_race, K="5", action_dict=action_dict)
    system_prompt, example_input_prompt, example_output_prompt = sc2prompt.generate_prompts()
    example_input_prompt.format(K_1=4)
    example_prompt = [example_input_prompt, example_output_prompt]

    # 创建并测试chatgpt agent
    gpt_agent = ChatGPTAgent(model_name=args.LLM_model_name, api_key=args.LLM_api_key,
                             api_base=args.LLM_api_base, system_prompt=system_prompt,
                             temperature=args.LLM_temperature, example_prompt=example_prompt,
                             args=args, action_description=action_description,last_k=1)
    agent_test(gpt_agent, env, args=args)


def glm4_worker(input_args):
    """
    为多进程定义的工作函数
    """
    # 使用args中的设置创建环境
    args = input_args

    selector = StarCraftEnvSelector(args)
    env = selector.create_env()

    action_description = ActionDescriptions(env.player_race)
    action_dict = action_description.action_descriptions

    # 假设这些参数和设置对于random agent仍然有用
    sc2prompt = StarCraftIIPrompt_HEP(race=args.player_race, K="5", action_dict=action_dict)


    system_prompt, example_input_prompt, example_output_prompt = sc2prompt.generate_prompts()
    example_input_prompt.format(K_1=4)
    example_prompt = [example_input_prompt, example_output_prompt]

    # 创建并测试random agent
    glm4_agent = Glm4Agent(model_name=args.LLM_model_name, api_key=args.LLM_api_key,
                             api_base=args.LLM_api_base, system_prompt=system_prompt,
                             temperature=args.LLM_temperature, example_prompt=example_prompt,
                             args=args, action_description=action_description,last_k=1)
    agent_test(glm4_agent, env, args=args)
