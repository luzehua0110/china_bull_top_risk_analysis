print("Python脚本运行测试")
print("牛市顶部判断分析系统")

# 简单的风险评分示例
def calculate_risk_score():
    risk_factors = [
        {"name": "技术指标超买", "score": 8},
        {"name": "估值水平", "score": 7},
        {"name": "市场情绪", "score": 9},
        {"name": "资金流向", "score": 6},
        {"name": "政策环境", "score": 5}
    ]
    
    total_score = sum(factor["score"] for factor in risk_factors)
    avg_score = total_score / len(risk_factors)
    
    print(f"\n风险因素评分:")
    for factor in risk_factors:
        print(f"- {factor['name']}: {factor['score']}/10")
    
    print(f"\n平均风险评分: {avg_score:.1f}/10")
    
    if avg_score >= 8:
        print("风险等级: 极高 ⚠️")
    elif avg_score >= 6:
        print("风险等级: 高 ⚠️")
    elif avg_score >= 4:
        print("风险等级: 中等")
    else:
        print("风险等级: 低")

if __name__ == "__main__":
    calculate_risk_score()