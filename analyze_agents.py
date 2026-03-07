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
    
    # 분석 로직 (앞서 설명한 정규식 기반 스캔)
    for root, dirs, files in os.walk(repo_path):
        for file in files:
            if file.endswith(('.py', '.js', '.ts', '.yaml', '.json')):
                try:
                    with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                        code = f.read()
                        # 프롬프트 길이
                        prompts = re.findall(r'["\']{3}(.*?)["\']{3}', code, re.DOTALL)
                        summary['promptLen'] = max([len(p) for p in prompts] + [summary['promptLen']])
                        # 도구 및 로직 점수
                        summary['toolCount'] += len(re.findall(r'@tool|define_tool|tools=\[', code))
                        summary['logicScore'] += len(re.findall(r'StateGraph|ConditionalEdge|ReAct|agent', code, re.I))
                        if re.search(r'evals/|ragas|test_cases', root.lower()):
                            summary['hasEvals'] = True
                except: continue
    return summary

# 메인 실행부
def update_dashboard_data():
    # 1. 기존 기본 정보(팀명, ID 등)가 담긴 CSV 읽기
    df = pd.read_csv("teams.csv")

    # 2. 각 팀 폴더를 돌며 기술 지표 스캔
    for index, row in df.iterrows():
        repo_local_path = f"./submissions/{row['name']}" # 팀 폴더 경로
        if os.path.exists(repo_local_path):
            tech_data = analyze_agent_repo(repo_local_path)
            # 데이터 업데이트
            df.at[index, 'promptLen'] = tech_data['promptLen']
            df.at[index, 'toolCount'] = tech_data['toolCount']
            df.at[index, 'logicScore'] = tech_data['logicScore']
            df.at[index, 'hasEvals'] = tech_data['hasEvals']

    # 3. 업데이트된 내용을 다시 CSV로 저장 (대시보드가 이 파일을 읽음)
    df.to_csv("teams.csv", index=False, encoding='utf-8-sig')
    print("✅ 기술 지표 분석 및 teams.csv 업데이트 완료!")

if __name__ == "__main__":
    update_dashboard_data()
