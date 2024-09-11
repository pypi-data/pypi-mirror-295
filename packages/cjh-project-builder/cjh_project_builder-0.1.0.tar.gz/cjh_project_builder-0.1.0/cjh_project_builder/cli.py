import os
import click

# 디렉토리 구조와 각 디렉토리에서 생성할 파일명 설정
DIRECTORY_STRUCTURE = {
    "domain": ["{module}_entity.py"],
    "endpoint": ["{module}.py"],
    "facades": ["{module}_facade.py"],
    "model/request": ["{module}_request.py"],
    "model/response": ["{module}_response.py"],
    "repository": ["{module}_repository.py"],
    "services": ["{module}_service.py"],
    "usecase": ["{module}_usecase.py"],
}

# 루트 디렉토리에서 공통적으로 생성할 파일들
ROOT_FILES = ["__init__.py", "routes.py", "container.py"]

# 파일 내용 템플릿 설정
TEMPLATES = {
    "endpoint": """# coding=utf-8
from fastapi import APIRouter

router = APIRouter()

@router.get()
async def get_{module}(): ...

@router.post()
async def post_{module}(): ...

@router.put()
async def put_{module}(): ...

@router.delete()
async def delete_{module}(): ...
""",
    "domain": """# coding=utf-8
from dataclasses import asdict, dataclass

@dataclass
class {Module}Entity:
    ...

    @classmethod
    def from_dict(cls, d):
        return cls(**d)

    def to_dict(self):
        return asdict(self)
""",
    "facades": """# coding=utf-8

class {Module}Facade:
    ...
""",
    "model/request": """# coding=utf-8
from pydantic import BaseModel

class Request{Module}Model(BaseModel):
    ...
""",
    "model/response": """# coding=utf-8
from pydantic import BaseModel

class Response{Module}Model(BaseModel):
    ...
""",
    "repository": """# coding=utf-8

class {Module}Repository:
    ...
""",
    "services": """# coding=utf-8

class {Module}Service:
    ...
""",
    "usecase": """# coding=utf-8

class {Module}Usecase:
    ...
""",
}

# __init__.py 템플릿 생성 (일반적인 경우)
INIT_TEMPLATE = """# coding=utf-8
from app.{module}.{folder}.{file_name} import {class_name}

__all__ = ["{class_name}"]
"""

# model 폴더의 request/response에 맞춘 __init__.py 템플릿 생성
MODEL_INIT_TEMPLATE = """# coding=utf-8
from app.{module}.model.{subfolder}.{file_name} import {class_name}

__all__ = ["{class_name}"]
"""

# model 디렉토리의 __init__.py 템플릿
MODEL_ROOT_INIT_TEMPLATE = """# coding=utf-8
from app.{module}.model.request.{request_file_name} import {request_class_name}
from app.{module}.model.response.{response_file_name} import {response_class_name}

__all__ = ["{request_class_name}", "{response_class_name}"]
"""


def generate_class_name(file_name):
    """
    파일 이름에서 클래스 이름을 생성하는 함수.
    파일 이름에서 '_'를 기준으로 나눈 뒤, 각 단어의 첫 글자를 대문자로 만들어서 결합.
    """
    return "".join([word.capitalize() for word in file_name.replace(".py", "").split("_")])


@click.command()
@click.argument("module_name")
def create_structure(module_name):
    """
    모듈명을 받아서 해당 이름의 파일들을 포함한 디렉토리 구조를 생성하는 CLI 도구
    """
    base_dir = os.path.join("src", "app", module_name)

    # 루트 디렉토리에서 필요한 파일 생성
    os.makedirs(base_dir, exist_ok=True)
    for root_file in ROOT_FILES:
        root_file_path = os.path.join(base_dir, root_file)
        with open(root_file_path, "w") as f:
            f.write("# coding=utf-8\n")
        print(f"Created root file: {root_file_path}")

    # 디렉토리 구조 생성
    model_request_file = ""
    model_response_file = ""
    model_request_class = ""
    model_response_class = ""

    for folder, files in DIRECTORY_STRUCTURE.items():
        folder_path = os.path.join(base_dir, folder)
        os.makedirs(folder_path, exist_ok=True)
        print(f"Created folder: {folder_path}")

        # 각 폴더에 대한 클래스/모듈 이름 설정
        folder_key = folder if folder in TEMPLATES else folder.split("/")[0]

        # 기본 파일들 생성 및 __init__.py 생성
        init_content = []
        for file_template in files:
            file_name = file_template.format(module=module_name)
            class_name = ""

            # request와 response는 따로 처리
            if "request" in file_name:
                class_name = f"Request{module_name.capitalize()}Model"
            elif "response" in file_name:
                class_name = f"Response{module_name.capitalize()}Model"
            else:
                # 일반적인 클래스 이름 생성
                class_name = generate_class_name(file_name)

            init_content.append((folder, file_name, class_name))

            file_path = os.path.join(folder_path, file_name)
            content = TEMPLATES.get(folder_key, "# coding=utf-8\n").format(
                module=module_name, Module=module_name.capitalize()
            )

            with open(file_path, "w") as f:
                f.write(content)
            print(f"Created file: {file_path} with content")

            # model/request 및 model/response 파일 이름 및 클래스명 저장
            if "model/request" in folder:
                model_request_file = file_name.replace(".py", "")
                model_request_class = class_name
            if "model/response" in folder:
                model_response_file = file_name.replace(".py", "")
                model_response_class = class_name

        # __init__.py 파일 내용 생성 (endpoint는 제외)
        init_file_path = os.path.join(folder_path, "__init__.py")

        if "endpoint" in folder:  # endpoint는 빈 파일 생성
            with open(init_file_path, "w") as f:
                f.write("# coding=utf-8\n")
            print(f"Created empty __init__.py in {folder}")
        else:
            if "model" in folder:  # model/request, model/response는 다른 경로로 설정
                subfolder = folder.split("/")[-1]
                init_imports = "\n".join(
                    [
                        MODEL_INIT_TEMPLATE.format(
                            module=module_name,
                            subfolder=subfolder,
                            file_name=info[1].replace(".py", ""),
                            class_name=info[2],
                        )
                        for info in init_content
                    ]
                )
            else:  # 일반적인 __init__.py
                init_imports = "\n".join(
                    [
                        INIT_TEMPLATE.format(
                            module=module_name, folder=folder, file_name=info[1].replace(".py", ""), class_name=info[2]
                        )
                        for info in init_content
                    ]
                )

            with open(init_file_path, "w") as f:
                f.write(init_imports)
            print(f"Created __init__.py in {folder_path} with imports")

    # model 폴더의 __init__.py 생성
    model_init_path = os.path.join(base_dir, "model", "__init__.py")
    os.makedirs(os.path.join(base_dir, "model"), exist_ok=True)
    with open(model_init_path, "w") as f:
        model_init_content = MODEL_ROOT_INIT_TEMPLATE.format(
            module=module_name,
            request_file_name=model_request_file,
            request_class_name=model_request_class,
            response_file_name=model_response_file,
            response_class_name=model_response_class,
        )
        f.write(model_init_content)
    print(f"Created __init__.py in model folder with request and response imports")

    print(f"\nModule '{module_name}' structure created successfully!")


# entry point
@click.group()
def cli():
    pass


cli.add_command(create_structure)

if __name__ == "__main__":
    cli()
