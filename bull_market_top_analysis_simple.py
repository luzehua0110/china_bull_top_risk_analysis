import csv
import json
from datetime import datetime, timedelta
import math
import urllib.request
import re

class SimpleBullMarketAnalyzer:
    def __init__(self):
        self.data = []
        self.ticker = None
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    def fetch_stock_data_from_sina(self, code='sh000001'):
        """从新浪财经获取股票数据"""
        try:
            self.ticker = code
            url = f'http://hq.sinajs.cn/list={code}'
            req = urllib.request.Request(url, headers=self.headers)
            with urllib.request.urlopen(req) as response:
                content = response.read().decode('gb2312')
                
                # 解析实时数据
                pattern = r'var hq_str_' + code + r'="([^"]+)"'
                match = re.search(pattern, content)
                if match:
                    data_str = match.group(1)
                    data_list = data_str.split(',')
                    
                    # 上证指数数据格式
                    if code.startswith('sh'):
                        date = data_list[30]
                        time = data_list[31]
                        open_price = float(data_list[1])
                        close_price = float(data_list[2])
                        current_price = float(data_list[3])
                        high_price = float(data_list[4])
                        low_price = float(data_list[5])
                        volume = float(data_list[8])
                        
                        print(f"成功获取{code}的实时数据:")
                        print(f"日期: {date} {time}")
                        print(f"开盘: {open_price}")
                        print(f"收盘: {close_price}")
                        print(f"当前: {current_price}")
                        print(f"最高: {high_price}")
                        print(f"最低: {low_price}")
                        print(f"成交量: {volume}")
                        
                        # 添加到数据列表
                        self.data.append({
                            'date': date,
                            'open': open_price,
                            'high': high_price,
                            'low': low_price,
                            'close': current_price,
                            'volume': volume
                        })
                    return True
                else:
                    print("无法解析数据")
                    return False
        except Exception as e:
            print(f"获取数据失败: {e}")
            return False
    
    def calculate_simple_metrics(self, recent_prices, recent_volumes):
        """计算简单的技术指标"""
        metrics = {}
        
        # 计算价格变化率
        if len(recent_prices) > 1:
            price_change_rate = (recent_prices[-1] - recent_prices[0]) / recent_prices[0] * 100
            metrics['price_change_rate'] = price_change_rate
        
        # 计算波动率
        if len(recent_prices) > 1:
            mean_price = sum(recent_prices) / len(recent_prices)
            variance = sum((p - mean_price) ** 2 for p in recent_prices) / len(recent_prices)
            volatility = math.sqrt(variance) / mean_price * 100
            metrics['volatility'] = volatility
        
        # 计算成交量变化
        if len(recent_volumes) > 1:
            volume_change = (recent_volumes[-1] - recent_volumes[0]) / recent_volumes[0] * 100
            metrics['volume_change'] = volume_change
        
        return metrics
    
    def estimate_valuation_metrics(self, market_type='sh'):
        """估算估值指标"""
        # 这里使用历史平均水平作为参考
        if market_type == 'sh':
            # 上证指数历史估值参考
            current_pe = 15.0  # 示例值，实际应用中应该从数据源获取
            current_pb = 1.6   # 示例值，实际应用中应该从数据源获取
            historical_pe_avg = 14.5
            historical_pb_avg = 1.5
            
            pe_percentile = min(100, max(0, (current_pe / historical_pe_avg) * 100))
            pb_percentile = min(100, max(0, (current_pb / historical_pb_avg) * 100))
            
            return {
                'estimated_pe': current_pe,
                'estimated_pb': current_pb,
                'pe_percentile': pe_percentile,
                'pb_percentile': pb_percentile
            }
        return None
    
    def risk_assessment(self):
        """简化的风险评估"""
        # 模拟最近30天的价格和成交量数据（实际应用中应从数据源获取）
        # 这里使用示例数据进行演示
        recent_prices = [3200, 3250, 3300, 3350, 3400, 3450, 3500, 3550, 3600, 3650, 
                        3700, 3750, 3800, 3850, 3900, 3950, 4000, 4050, 4100, 4150, 
                        4200, 4250, 4300, 4350, 4400, 4450, 4500, 4520, 4540, 4560]
        recent_volumes = [2000, 2200, 2400, 2600, 2800, 3000, 3200, 3400, 3600, 3800, 
                         4000, 4200, 4400, 4600, 4800, 5000, 5200, 5400, 5600, 5800, 
                         6000, 5800, 5600, 5400, 5200, 5000, 4800, 4600, 4400, 4200]
        
        metrics = self.calculate_simple_metrics(recent_prices, recent_volumes)
        valuation = self.estimate_valuation_metrics()
        
        risk_score = 0
        risk_factors = []
        
        # 价格变化率检查
        if 'price_change_rate' in metrics and metrics['price_change_rate'] > 40:
            risk_score += 25
            risk_factors.append(f"近期涨幅过大: {metrics['price_change_rate']:.1f}%")
        
        # 成交量变化检查（量价背离）
        if 'price_change_rate' in metrics and 'volume_change' in metrics:
            if metrics['price_change_rate'] > 10 and metrics['volume_change'] < 0:
                risk_score += 20
                risk_factors.append(f"量价背离: 价格上涨{metrics['price_change_rate']:.1f}%，成交量下降{abs(metrics['volume_change']):.1f}%")
        
        # 估值检查
        if valuation:
            if valuation['pe_percentile'] > 90:
                risk_score += 25
                risk_factors.append(f"市盈率处于历史高位: {valuation['pe_percentile']:.1f}%")
            if valuation['pb_percentile'] > 90:
                risk_score += 25
                risk_factors.append(f"市净率处于历史高位: {valuation['pb_percentile']:.1f}%")
        
        # 波动率检查
        if 'volatility' in metrics and metrics['volatility'] > 5:
            risk_score += 15
            risk_factors.append(f"市场波动率过高: {metrics['volatility']:.1f}%")
        
        # 风险等级判断
        risk_level = ""
        risk_description = ""
        
        if risk_score >= 80:
            risk_level = "极高"
            risk_description = "强烈的牛市顶部信号，建议立即减仓"
        elif risk_score >= 60:
            risk_level = "高"
            risk_description = "明显的牛市顶部特征，建议大幅减仓"
        elif risk_score >= 40:
            risk_level = "中高"
            risk_description = "存在牛市顶部风险，建议适度减仓"
        elif risk_score >= 20:
            risk_level = "中"
            risk_description = "需要关注的风险信号，建议谨慎操作"
        else:
            risk_level = "低"
            risk_description = "风险信号较少，可继续持有"
        
        assessment = {
            'risk_score': min(100, risk_score),
            'risk_level': risk_level,
            'risk_description': risk_description,
            'risk_factors': risk_factors
        }
        
        return assessment
    
    def get_market_sentiment(self):
        """获取市场情绪指标（简化版）"""
        # 这里使用模拟数据，实际应用中应该从新闻、社交媒体等获取
        sentiment_indicators = [
            {"name": "融资余额增速", "value": 15.2, "threshold": 10, "risk": True},
            {"name": "新增投资者数量", "value": 22.5, "threshold": 20, "risk": True},
            {"name": "券商看多比例", "value": 85, "threshold": 80, "risk": True},
            {"name": "媒体报道热度", "value": 78, "threshold": 75, "risk": True},
            {"name": "北向资金净流入", "value": 5.2, "threshold": 0, "risk": False}
        ]
        
        risk_sentiment_count = sum(1 for indicator in sentiment_indicators if indicator["risk"])
        total_indicators = len(sentiment_indicators)
        
        sentiment_level = ""
        if risk_sentiment_count >= 4:
            sentiment_level = "极度乐观（风险信号）"
        elif risk_sentiment_count >= 3:
            sentiment_level = "明显乐观"
        elif risk_sentiment_count >= 2:
            sentiment_level = "中性偏乐观"
        else:
            sentiment_level = "相对理性"
        
        return {
            'sentiment_level': sentiment_level,
            'risk_sentiment_count': risk_sentiment_count,
            'total_indicators': total_indicators,
            'indicators': sentiment_indicators
        }
    
    def run_analysis(self):
        """运行完整分析"""
        print("开始牛市顶部风险分析...")
        
        # 获取市场数据
        self.fetch_stock_data_from_sina()
        
        # 风险评估
        print("\n===== 顶部风险评估 =====")
        assessment = self.risk_assessment()
        print(f"风险评分: {assessment['risk_score']}")
        print(f"风险等级: {assessment['risk_level']}")
        print(f"风险描述: {assessment['risk_description']}")
        print("风险因素:")
        for factor in assessment['risk_factors']:
            print(f"  - {factor}")
        
        # 市场情绪分析
        print("\n===== 市场情绪分析 =====")
        sentiment = self.get_market_sentiment()
        print(f"市场情绪: {sentiment['sentiment_level']}")
        print(f"风险情绪指标: {sentiment['risk_sentiment_count']}/{sentiment['total_indicators']}")
        print("具体指标:")
        for indicator in sentiment['indicators']:
            status = "⚠️ 风险信号" if indicator["risk"] else "✅ 正常"
            print(f"  - {indicator['name']}: {indicator['value']} (阈值: {indicator['threshold']}) {status}")
        
        # 历史对比
        print("\n===== 历史牛市顶部特征对比 =====")
        historical_features = [
            {"feature": "上涨幅度", "current": "较高", "2007年顶部": "极高", "2015年顶部": "极高", "warning": True},
            {"feature": "估值水平", "current": "中等偏高", "2007年顶部": "极高", "2015年顶部": "极高", "warning": True},
            {"feature": "市场情绪", "current": "乐观", "2007年顶部": "极度乐观", "2015年顶部": "极度乐观", "warning": True},
            {"feature": "政策环境", "current": "中性", "2007年顶部": "收紧", "2015年顶部": "收紧", "warning": False},
            {"feature": "经济周期", "current": "复苏", "2007年顶部": "过热", "2015年顶部": "放缓", "warning": False}
        ]
        
        print("特征对比:")
        for feature in historical_features:
            status = "⚠️" if feature["warning"] else "✅"
            print(f"  {status} {feature['feature']}: 当前-{feature['current']}, 2007年-{feature['2007年顶部']}, 2015年-{feature['2015年顶部']}")
        
        # 综合建议
        print("\n===== 综合建议 =====")
        warning_count = sum(1 for feature in historical_features if feature["warning"])
        
        if assessment['risk_level'] in ["极高", "高"] or warning_count >= 4:
            print("🔴 强烈建议：")
            print("  1. 立即大幅减仓，控制仓位在30%以下")
            print("  2. 高估值股票优先减仓")
            print("  3. 避免追高和使用杠杆")
        elif assessment['risk_level'] == "中高" or warning_count >= 3:
            print("🟠 建议：")
            print("  1. 适度减仓，控制仓位在50%以下")
            print("  2. 降低投资组合风险，增加防御性资产")
            print("  3. 设置严格止损")
        elif assessment['risk_level'] == "中":
            print("🟡 谨慎建议：")
            print("  1. 保持中性仓位，观望为主")
            print("  2. 关注政策变化和市场情绪转变")
            print("  3. 分批操作，避免一次性大额交易")
        else:
            print("🟢 积极建议：")
            print("  1. 可继续持有核心资产")
            print("  2. 关注业绩增长确定的优质公司")
            print("  3. 保持适度仓位，做好风险管理")
        
        print("\n⚠️ 风险提示：本分析仅供参考，不构成投资建议。市场有风险，投资需谨慎。")

# 主函数
def main():
    analyzer = SimpleBullMarketAnalyzer()
    analyzer.run_analysis()

if __name__ == "__main__":
    main()