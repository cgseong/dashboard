import os
import re
import pandas as pd

def analyze_agent_repo(repo_path):
    summary = {
        'promptLen': 0,
        'toolCount': 0,
        'logicScore': 0,
        'hasEvals': False
    }
    
    # 1. 구조적 검사 (평가셋 폴더 여부)
    for root, dirs, _ in os.walk(repo_path):
        if any(keyword in root.lower() for keyword in ['evals', 'test_cases', 'ragas', 'benchmarks']):
            summary['hasEvals'] = True
            break

    # 2. 파일 내용 분석
    for root, _, files in os.walk(repo_path):
        # 제외할 폴더 (라이브러리 등)
        if any(x in root for x in ['venv', '.git', '__pycache__', 'node_modules']):
            continue

        for file in files:
            file_path = os.path.join(root, file)
            ext = os.path.splitext(file)[1].lower()
            
            if ext in ('.py', '.js', '.ts', '.yaml', '.json', '.txt'):
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        code = f.read()
                        
                        # 프롬프트 길이 측정 개선 (텍스트 파일은 전체 길이, 코드는 멀티라인 분석)
                        if ext in ('.txt', '.yaml'):
                            summary['promptLen'] = max(summary['promptLen'], len(code))
                        else:
                            prompts = re.findall(r'["\']{3}(.*?)["\']{3}', code, re.DOTALL)
                            if prompts:
                                summary['promptLen'] = max([len(p) for p in prompts] + [summary['promptLen']])
                        
                        # 도구 활용 및 로직 점수 (중복 최소화를 위해 단어 경계 \b 활용)
                        summary['toolCount'] += len(re.findall(r'@tool|define_tool|tools\s*=\s*\[', code))
                        summary['logicScore'] += len(re.findall(r'\b(StateGraph|ConditionalEdge|ReAct|AgentExecutor|node)\b', code, re.I))
                        
                except Exception as e:
                    print(f"⚠️ 파일 읽기 오류 ({file}): {e}")
                    continue
    return summary

def update_dashboard_data():
    try:
        df = pd.read_csv("teams.csv")
    except FileNotFoundError:
        print("❌ teams.csv 파일을 찾을 수 없습니다.")
        return

    # 기술 지표 컬럼이 없으면 초기화
    for col in ['promptLen', 'toolCount', 'logicScore', 'hasEvals']:
        if col not in df.columns:
            df[col] = 0 if col != 'hasEvals' else False

    for index, row in df.iterrows():
        # 폴더 이름이 팀명과 정확히 일치하는지 확인
        repo_local_path = f"./submissions/{row['name']}"
        if os.path.exists(repo_local_path):
            print(f"🔍 분석 중: {row['name']}...")
            tech_data = analyze_agent_repo(repo_local_path)
            
            df.at[index, 'promptLen'] = tech_data['promptLen']
            df.at[index, 'toolCount'] = tech_data['toolCount']
            df.at[index, 'logicScore'] = tech_data['logicScore']
            df.at[index, 'hasEvals'] = tech_data['hasEvals']
        else:
            print(f"⏩ 폴더 없음 (건너뜀): {row['name']}")

    df.to_csv("teams.csv", index=False, encoding='utf-8-sig')
    print("✅ 분석 완료 및 teams.csv 업데이트 성공!")

if __name__ == "__main__":
    update_dashboard_data()
