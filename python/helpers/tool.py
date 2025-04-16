from abc import abstractmethod
from dataclasses import dataclass

from agent import Agent
from python.helpers.print_style import PrintStyle


@dataclass
class Response:
    message:str
    break_loop: bool

class Tool:

    def __init__(self, agent: Agent, name: str, args: dict[str,str], message: str, **kwargs) -> None:
        self.agent = agent
        self.name = name
        self.args = args
        self.message = message

    @abstractmethod
    async def execute(self,**kwargs) -> Response:
        pass

    async def before_execution(self, **kwargs):
        PrintStyle(font_color="#1B4F72", padding=True, background_color="white", bold=True).print(f"{self.agent.agent_name}: Using tool '{self.name}'")
        self.log = self.get_log_object()
        if self.args and isinstance(self.args, dict):
            for key, value in self.args.items():
                PrintStyle(font_color="#85C1E9", bold=True).stream(self.nice_key(key)+": ")
                PrintStyle(font_color="#85C1E9", padding=isinstance(value,str) and "\n" in value).stream(value)
                PrintStyle().print()

    async def after_execution(self, response: Response, **kwargs):
        text = response.message.strip()
        self.agent.hist_add_tool_result(self.name, text)
        PrintStyle(font_color="#1B4F72", background_color="white", padding=True, bold=True).print(f"{self.agent.agent_name}: Response from tool '{self.name}'")
        PrintStyle(font_color="#85C1E9").print(response.message)
        self.log.update(content=response.message)

    def get_log_object(self):
        return self.agent.context.log.log(type="tool", heading=f"{self.agent.agent_name}: Using tool '{self.name}'", content="", kvps=self.args)

    def nice_key(self, key:str):
        words = key.split('_')
        words = [words[0].capitalize()] + [word.lower() for word in words[1:]]
        result = ' '.join(words)
        return result
