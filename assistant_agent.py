
# Copyright (c) 2025 Beijing Volcano Engine Technology Co., Ltd. and/or its affiliates.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging

from veadk import Agent, Runner

from agentkit.apps import AgentkitSimpleApp
from veadk.prompts.agent_default_prompt import DEFAULT_DESCRIPTION, DEFAULT_INSTRUCTION
from veadk.tools.builtin_tools.web_search import web_search
from veadk.tools.builtin_tools.vesearch import vesearch
#from veadk.tools.builtin_tools.llm_shield import content_safety

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


app = AgentkitSimpleApp()

agent_name = "ywli_assistant"
description = "this is the assistant for ywli" 
system_prompt = "you are an assistant" 
endpoint = "https://ark.ap-southeast.bytepluses.com/api/v3/"


tools = [web_search]

# from veadk.tools.builtin_tools.web_search import web_search
# tools.append(web_search)


agent = Agent(
    name=agent_name,
    description=description,
    instruction=system_prompt,
    tools=tools,
    model_api_base = endpoint,
    #before_model_callback=content_safety.before_model_callback, 
    #after_model_callback=content_safety.after_model_callback,
    #before_tool_callback=content_safety.before_tool_callback,
    #after_tool_callback=content_safety.after_tool_callback,
    model_name="deepseek-v3-1-250821"
)
runner = Runner(agent=agent)


@app.entrypoint
async def run(payload: dict, headers: dict) -> str:
    prompt = payload["prompt"]
    user_id = headers["user_id"]
    session_id = headers["session_id"]

    logger.info(
        f"Running agent with prompt: {prompt}, user_id: {user_id}, session_id: {session_id}"
    )
    response = await runner.run(messages=prompt, user_id=user_id, session_id=session_id)

    logger.info(f"Run response: {response}")
    return response


@app.ping
def ping() -> str:
    return "pong!"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
