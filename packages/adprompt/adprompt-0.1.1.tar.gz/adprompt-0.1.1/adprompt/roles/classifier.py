from typing import List

from openai import BaseModel
from openai.types.chat import ChatCompletion

from adprompt.chat import ChatResponse
from adprompt.role import BaseRole
from adprompt.utils.json_utils import load_json_result


class ClassDef(BaseModel):
    key: str
    desc: str


_ROLE_TMPL = """你将负责根据预先定义好的类别以及这个类别包含哪些内容的描述，分析用户的输入和哪个类别所包含的内容相关。
下面我会依次给出各个类别的名称以及对类别中包含哪些内容的描述。
{}

接下来我会提供给你一个用户的输入，你需要判断用户的输入是否和某个类别描述中包含的内容相关，如果相关则认为用户的输入属于该类别，你需要进一步评估用户输入和该类别的相关程度。
你需要用列表形式输出不超过{}个和用户输入最相关的类别，每个相关类别的分析结果用一个json格式数据表示，其中class字段的值为类别的标识，related为用户的输入和对应类别的相关程度（取值包括“非常相关”、“一般相关”、“不相关”）。
如果经过分析后不是十分确定用户的输入所属的类别，则输出一个空的json列表。
你需要严格按照json格式输出结果，不要输出其他无关内容。
"""


class Classifier(BaseRole):
    """
    根据类别描述进行文本分类
    """

    def __init__(self, classes: List[ClassDef], top_k: int = 3):
        self.classes = classes
        self.top_k = top_k

    def get_role_context(self) -> List[dict]:
        return [{
            "role": "system",
            "content": self._fill_tmpl(),
        }]

    def _fill_tmpl(self) -> str:
        lines = []
        for _i, c in enumerate(self.classes):
            lines.append(f'{_i + 1}. {c.key}：{c.desc}')
        return _ROLE_TMPL.format('\n'.join(lines), self.top_k)

    def post_process(self, completion: ChatCompletion) -> ChatResponse:
        content = self._get_response_content(completion)
        try:
            data = load_json_result(content)
        except Exception as e:
            return ChatResponse(
                content=content,
                completion=completion,
                error_message=f'Failed to load json result: {e}',
            )
        else:
            result = []
            if isinstance(data, list):
                for d in data:
                    class_key = d.get('class')
                    if class_key:
                        for i in self.classes:
                            if i.key == class_key:
                                result.append(d)
            return ChatResponse(
                result={'result': result},
                content=content,
                completion=completion,
            )
