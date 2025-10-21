# 完全离线的牛市顶部分析工具
# 只使用Python标准库，无需网络连接和额外依赖

class OfflineBullMarketAnalyzer:
    def __init__(self):
        print("====== 中国股市牛市顶部风险分析工具 ======")
        print("本工具提供离线分析功能，帮助识别牛市可能见顶的信号")
    
    def calculate_rsi(self, prices, period=14):
        """计算RSI指标"""
        if len(prices) < period + 1:
            return None
            
        deltas = [prices[i] - prices[i-1] for i in range(1, len(prices))]
        gains = [max(0, delta) for delta in deltas]
        losses = [max(0, -delta) for delta in deltas]
        
        # 简单移动平均
        avg_gain = sum(gains[-period:]) / period
        avg_loss = sum(losses[-period:]) / period
        
        if avg_loss == 0:
            return 100
        
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def detect_divergence(self, prices, indicators):
        """检测顶背离"""
        if len(prices) < 2 or len(indicators) < 2:
            return False
            
        # 简化版背离检测：价格创新高但指标未创新高
        price_higher = prices[-1] > prices[-2]
        indicator_higher = indicators[-1] > indicators[-2]
        
        return price_higher and not indicator_higher
    
    def analyze_risk_factors(self):
        """分析各项风险因素"""
        print("\n请根据当前市场情况，为以下指标评分（1-10分）:")
        
        # 风险因素评分表
        risk_factors = [
            {"name": "指数涨幅（近6个月）", "weight": 0.15},
            {"name": "市盈率水平", "weight": 0.15},
            {"name": "市净率水平", "weight": 0.10},
            {"name": "融资余额增速", "weight": 0.15},
            {"name": "新增投资者数量增长", "weight": 0.10},
            {"name": "媒体报道热度", "weight": 0.10},
            {"name": "机构持仓变化", "weight": 0.10},
            {"name": "技术指标超买程度", "weight": 0.15}
        ]
        
        # 模拟评分（实际应用中应该让用户输入）
        scores = [7, 6, 5, 8, 7, 6, 4, 7]  # 示例评分
        
        total_score = 0
        for i, factor in enumerate(risk_factors):
            factor_score = scores[i]
            weighted_score = factor_score * factor["weight"] * 10  # 转换为0-100分制
            total_score += weighted_score
            print(f"{factor['name']}: {factor_score}/10分 (权重: {factor['weight']}, 加权分: {weighted_score:.1f})")
        
        return min(100, total_score)
    
    def get_historical_comparison(self):
        """历史牛市顶部特征对比"""
        print("\n==== 历史牛市顶部特征对比 ====")
        
        features = [
            {"name": "上涨幅度", "2007": "500%+", "2015": "150%+", "current": "请根据实际情况判断"},
            {"name": "市盈率峰值", "2007": "70+", "2015": "50+", "current": "请根据实际情况判断"},
            {"name": "市净率峰值", "2007": "7+", "2015": "5+", "current": "请根据实际情况判断"},
            {"name": "市场情绪", "2007": "全民炒股", "2015": "杠杆牛", "current": "请根据实际情况判断"},
            {"name": "政策转向", "2007": "加息、提准", "2015": "去杠杆", "current": "请根据实际情况判断"},
            {"name": "成交量特征", "2007": "天量天价", "2015": "杠杆推动", "current": "请根据实际情况判断"}
        ]
        
        for feature in features:
            print(f"{feature['name']}: 2007年-{feature['2007']}, 2015年-{feature['2015']}, 当前-{feature['current']}")
    
    def run_analysis(self):
        """运行完整分析"""
        # 技术指标演示
        print("\n==== 技术指标演示 ====")
        
        # 模拟价格数据
        prices = [3200, 3250, 3300, 3350, 3400, 3450, 3500, 3550, 3600, 3650, 
                 3700, 3750, 3800, 3850, 3900, 3950, 4000, 4050, 4100, 4150, 
                 4200, 4250, 4300, 4350, 4400]
        
        # 计算RSI
        rsi = self.calculate_rsi(prices)
        print(f"当前RSI值: {rsi:.2f}")
        if rsi > 80:
            print("RSI状态: 严重超买 ⚠️")
        elif rsi > 70:
            print("RSI状态: 超买 ⚠️")
        elif rsi < 30:
            print("RSI状态: 超卖")
        elif rsi < 20:
            print("RSI状态: 严重超卖")
        else:
            print("RSI状态: 正常")
        
        # 模拟指标数据
        indicators = [50, 55, 60, 65, 70, 75, 78, 80, 79, 78, 
                     77, 76, 75, 74, 73, 72, 71, 70, 69, 68, 
                     67, 66, 65, 64, 63]
        
        # 检测背离
        divergence = self.detect_divergence(prices, indicators)
        print(f"是否存在顶背离: {'是 ⚠️' if divergence else '否'}")
        
        # 风险因素分析
        print("\n==== 综合风险因素分析 ====")
        risk_score = self.analyze_risk_factors()
        
        # 风险评级
        print(f"\n综合风险评分: {risk_score:.1f}/100分")
        
        if risk_score >= 80:
            print("风险等级: 极高 ⚠️⚠️⚠️")
            print("结论: 强烈的牛市顶部信号，市场可能即将见顶")
        elif risk_score >= 60:
            print("风险等级: 高 ⚠️⚠️")
            print("结论: 明显的牛市顶部特征，需高度警惕")
        elif risk_score >= 40:
            print("风险等级: 中等 ⚠️")
            print("结论: 存在一定的顶部风险，建议谨慎操作")
        elif risk_score >= 20:
            print("风险等级: 低")
            print("结论: 风险信号较弱，市场仍有上升空间")
        else:
            print("风险等级: 极低")
            print("结论: 未发现明显顶部信号")
        
        # 历史对比
        self.get_historical_comparison()
        
        # 投资建议
        print("\n==== 投资建议 ====")
        if risk_score >= 80:
            print("🔴 操作建议:")
            print("  1. 立即大幅减仓，控制仓位在20%以下")
            print("  2. 全部卖出高估值、概念炒作类股票")
            print("  3. 避免任何形式的追高和杠杆操作")
            print("  4. 可考虑小仓位做空对冲风险")
        elif risk_score >= 60:
            print("🟠 操作建议:")
            print("  1. 大幅减仓至30-40%仓位")
            print("  2. 减持高估值板块，保留低估值防御性板块")
            print("  3. 设置严格止损，防范大幅回调风险")
            print("  4. 耐心等待更好的入场机会")
        elif risk_score >= 40:
            print("🟡 操作建议:")
            print("  1. 适度减仓至50-60%仓位")
            print("  2. 调整持仓结构，增加防御性资产比例")
            print("  3. 密切关注市场变化和政策动向")
            print("  4. 逢高减持，逢低少量吸纳优质股票")
        else:
            print("🟢 操作建议:")
            print("  1. 可保持较高仓位，但不建议满仓")
            print("  2. 重点关注业绩增长确定性强的优质公司")
            print("  3. 定期回顾风险指标变化")
            print("  4. 分批操作，避免一次性大额交易")
        
        print("\n📊 关键监控指标:")
        print("  1. RSI指标是否持续在超买区域")
        print("  2. 成交量是否出现明显萎缩")
        print("  3. 融资余额变化趋势")
        print("  4. 政策态度是否转向")
        print("  5. 外资流向变化")
        
        print("\n⚠️ 风险提示: 本工具仅供参考，不构成任何投资建议。")
        print("市场有风险，投资需谨慎。请根据自身风险承受能力做出决策。")

# 主函数
def main():
    analyzer = OfflineBullMarketAnalyzer()
    analyzer.run_analysis()

if __name__ == "__main__":
    main()