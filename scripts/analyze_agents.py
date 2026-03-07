import os, re

def check_agent_tech(path):
    results = {"prompt_len": 0, "tools": 0, "logic": 0, "evals": False}
    
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(('.py', '.ts', '.yaml')):
                with open(os.path.join(root, file), 'r', errors='ignore') as f:
                    code = f.read()
                    # 프롬프트 길이 추출 (정규식)
                    prompts = re.findall(r'["\']{3}(.*?)["\']{3}', code, re.DOTALL)
                    results["prompt_len"] = max([len(p) for p in prompts] + [results["prompt_len"]])
                    
                    # 도구 및 로직 키워드 카운트
                    results["tools"] += len(re.findall(r'@tool|define_tool', code))
                    results["logic"] += len(re.findall(r'StateGraph|ConditionalEdge|ReAct', code))
                    
                    # 평가셋 흔적
                    if "ragas" in code.lower() or "test_cases" in code.lower():
                        results["evals"] = True
    return results

# 예시 실행
# print(check_agent_tech("./team_attention_repo"))
