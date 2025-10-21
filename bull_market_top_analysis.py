import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import yfinance as yf
from scipy import stats

class BullMarketTopAnalyzer:
    def __init__(self):
        self.data = None
        self.ticker = None
    
    def fetch_stock_data(self, ticker, period='5y'):
        """获取股票数据"""
        try:
            self.ticker = ticker
            self.data = yf.download(ticker, period=period)
            print(f"成功获取{self.ticker}的数据，共{len(self.data)}条记录")
            return self.data
        except Exception as e:
            print(f"获取数据失败: {e}")
            return None
    
    def calculate_rsi(self, period=14):
        """计算相对强弱指标(RSI)"""
        if self.data is None:
            print("请先获取数据")
            return None
        
        delta = self.data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        
        self.data['RSI'] = rsi
        return rsi
    
    def calculate_macd(self, fast_period=12, slow_period=26, signal_period=9):
        """计算MACD指标"""
        if self.data is None:
            print("请先获取数据")
            return None
        
        exp1 = self.data['Close'].ewm(span=fast_period, adjust=False).mean()
        exp2 = self.data['Close'].ewm(span=slow_period, adjust=False).mean()
        macd = exp1 - exp2
        signal = macd.ewm(span=signal_period, adjust=False).mean()
        histogram = macd - signal
        
        self.data['MACD'] = macd
        self.data['MACD_Signal'] = signal
        self.data['MACD_Histogram'] = histogram
        return macd, signal, histogram
    
    def calculate_bollinger_bands(self, period=20, num_std=2):
        """计算布林带指标"""
        if self.data is None:
            print("请先获取数据")
            return None
        
        sma = self.data['Close'].rolling(window=period).mean()
        std = self.data['Close'].rolling(window=period).std()
        upper_band = sma + (std * num_std)
        lower_band = sma - (std * num_std)
        bandwidth = (upper_band - lower_band) / sma * 100
        
        self.data['BB_Upper'] = upper_band
        self.data['BB_Middle'] = sma
        self.data['BB_Lower'] = lower_band
        self.data['BB_Width'] = bandwidth
        return upper_band, sma, lower_band, bandwidth
    
    def calculate_moving_averages(self, short_period=50, long_period=200):
        """计算移动平均线"""
        if self.data is None:
            print("请先获取数据")
            return None
        
        self.data['MA50'] = self.data['Close'].rolling(window=short_period).mean()
        self.data['MA200'] = self.data['Close'].rolling(window=long_period).mean()
        self.data['MA50_MA200_Ratio'] = self.data['MA50'] / self.data['MA200']
        return self.data['MA50'], self.data['MA200']
    
    def detect_divergence(self, indicator='RSI', lookback=50):
        """检测价格与指标的背离现象"""
        if self.data is None or indicator not in self.data.columns:
            print(f"请先获取数据并计算{indicator}指标")
            return None
        
        divergences = []
        recent_highs = self.data['Close'].rolling(window=lookback).max()
        recent_indicator_highs = self.data[indicator].rolling(window=lookback).max()
        
        for i in range(len(self.data)):
            if i < lookback:
                continue
                
            # 检测顶背离：价格创新高但指标未创新高
            if self.data['Close'].iloc[i] == recent_highs.iloc[i] and \
               self.data[indicator].iloc[i] < recent_indicator_highs.iloc[i]:
                divergences.append((self.data.index[i], 'Bearish Divergence'))
        
        return divergences
    
    def volume_analysis(self):
        """成交量分析"""
        if self.data is None:
            print("请先获取数据")
            return None
        
        # 计算成交量移动平均
        self.data['Volume_MA20'] = self.data['Volume'].rolling(window=20).mean()
        self.data['Volume_Ratio'] = self.data['Volume'] / self.data['Volume_MA20']
        
        # 检测量价背离：价格创新高但成交量未创新高
        price_highs = self.data['Close'].rolling(window=20).max()
        volume_highs = self.data['Volume'].rolling(window=20).max()
        self.data['Price_High'] = self.data['Close'] == price_highs
        self.data['Volume_Price_Divergence'] = self.data['Price_High'] & (self.data['Volume'] < volume_highs)
        
        return self.data[['Volume_MA20', 'Volume_Ratio', 'Volume_Price_Divergence']]
    
    def calculate_valuation_metrics(self, pe_ratio=None, pb_ratio=None, dividend_yield=None):
        """计算估值指标"""
        # 这里可以添加实际的估值数据，例如从API获取PE、PB等数据
        # 暂时使用模拟数据进行演示
        metrics = {}
        
        if pe_ratio is not None:
            metrics['PE_Ratio'] = pe_ratio
            metrics['PE_Percentile'] = self._calculate_percentile(pe_ratio, [5, 10, 15, 20, 25, 30, 35, 40])
        
        if pb_ratio is not None:
            metrics['PB_Ratio'] = pb_ratio
            metrics['PB_Percentile'] = self._calculate_percentile(pb_ratio, [1, 2, 3, 4, 5, 6, 7, 8])
        
        if dividend_yield is not None:
            metrics['Dividend_Yield'] = dividend_yield
        
        return metrics
    
    def _calculate_percentile(self, value, history_values):
        """计算某个值在历史数据中的百分位"""
        sorted_values = sorted(history_values)
        percentile = sum(1 for x in sorted_values if x <= value) / len(sorted_values) * 100
        return percentile
    
    def trend_strength(self):
        """计算趋势强度"""
        if self.data is None:
            print("请先获取数据")
            return None
        
        # 使用线性回归斜率计算趋势强度
        x = np.arange(len(self.data))
        slope, _, r_value, _, _ = stats.linregress(x, self.data['Close'])
        
        # 年化斜率（假设每天的数据）
        annualized_slope = slope * 252
        r_squared = r_value ** 2
        
        trend_strength = {
            'Slope': slope,
            'Annualized_Slope': annualized_slope,
            'R_Squared': r_squared,
            'Trend_Strength_Score': min(100, max(0, r_squared * 100))
        }
        
        return trend_strength
    
    def top_risk_assessment(self, valuation_metrics=None):
        """综合风险评估"""
        if self.data is None:
            print("请先获取数据")
            return None
        
        # 确保必要的指标已计算
        if 'RSI' not in self.data.columns:
            self.calculate_rsi()
        if 'MACD' not in self.data.columns:
            self.calculate_macd()
        if 'MA50' not in self.data.columns:
            self.calculate_moving_averages()
        
        risk_score = 0
        risk_factors = []
        
        # RSI超买检查
        latest_rsi = self.data['RSI'].iloc[-1]
        if latest_rsi > 80:
            risk_score += 30
            risk_factors.append(f"RSI超买严重: {latest_rsi:.2f}")
        elif latest_rsi > 70:
            risk_score += 20
            risk_factors.append(f"RSI处于超买区域: {latest_rsi:.2f}")
        
        # MACD死亡交叉检查
        if self.data['MACD'].iloc[-1] < self.data['MACD_Signal'].iloc[-1] and \
           self.data['MACD'].iloc[-2] > self.data['MACD_Signal'].iloc[-2]:
            risk_score += 25
            risk_factors.append("MACD形成死亡交叉")
        
        # 均线系统检查
        if 'MA50' in self.data.columns and 'MA200' in self.data.columns:
            if self.data['MA50'].iloc[-1] < self.data['MA200'].iloc[-1] and \
               self.data['MA50'].iloc[-2] > self.data['MA200'].iloc[-2]:
                risk_score += 30
                risk_factors.append("均线形成死亡交叉")
            
            # 均线距离过大检查
            ma_ratio = self.data['MA50'].iloc[-1] / self.data['MA200'].iloc[-1]
            if ma_ratio > 1.2:
                risk_score += 15
                risk_factors.append(f"短期均线与长期均线距离过大: {ma_ratio:.2f}")
        
        # 量价背离检查
        vol_analysis = self.volume_analysis()
        if self.data['Volume_Price_Divergence'].iloc[-1]:
            risk_score += 20
            risk_factors.append("出现量价背离")
        
        # 估值指标检查
        if valuation_metrics:
            if 'PE_Percentile' in valuation_metrics and valuation_metrics['PE_Percentile'] > 90:
                risk_score += 25
                risk_factors.append(f"PE处于历史高位: {valuation_metrics['PE_Percentile']:.1f}%")
            
            if 'PB_Percentile' in valuation_metrics and valuation_metrics['PB_Percentile'] > 90:
                risk_score += 25
                risk_factors.append(f"PB处于历史高位: {valuation_metrics['PB_Percentile']:.1f}%")
        
        # 趋势强度检查
        trend = self.trend_strength()
        if trend['Slope'] < 0 and trend['R_Squared'] > 0.3:
            risk_score += 15
            risk_factors.append("下降趋势形成")
        
        # 背离检查
        divergences = self.detect_divergence()
        if divergences and len(divergences) > 0:
            recent_divergences = [d for d in divergences if (datetime.now().date() - d[0].date()).days < 30]
            if len(recent_divergences) > 0:
                risk_score += 20
                risk_factors.append(f"近期出现{len(recent_divergences)}次顶背离")
        
        # 风险等级判断
        risk_level = ""
        risk_description = ""
        
        if risk_score >= 100:
            risk_level = "极高"
            risk_description = "强烈的牛市顶部信号，建议立即减仓"
        elif risk_score >= 80:
            risk_level = "高"
            risk_description = "明显的牛市顶部特征，建议大幅减仓"
        elif risk_score >= 60:
            risk_level = "中高"
            risk_description = "存在牛市顶部风险，建议适度减仓"
        elif risk_score >= 40:
            risk_level = "中"
            risk_description = "需要关注的风险信号，建议谨慎操作"
        elif risk_score >= 20:
            risk_level = "低"
            risk_description = "风险信号较少，可继续持有"
        else:
            risk_level = "极低"
            risk_description = "未发现明显的顶部风险信号"
        
        assessment = {
            'Risk_Score': min(100, risk_score),
            'Risk_Level': risk_level,
            'Risk_Description': risk_description,
            'Risk_Factors': risk_factors
        }
        
        return assessment
    
    def plot_technical_indicators(self):
        """绘制技术指标图表"""
        if self.data is None:
            print("请先获取数据")
            return None
        
        # 确保必要的指标已计算
        if 'RSI' not in self.data.columns:
            self.calculate_rsi()
        if 'MACD' not in self.data.columns:
            self.calculate_macd()
        if 'BB_Upper' not in self.data.columns:
            self.calculate_bollinger_bands()
        if 'MA50' not in self.data.columns:
            self.calculate_moving_averages()
        
        # 创建图形
        fig, axes = plt.subplots(4, 1, figsize=(15, 12), gridspec_kw={'height_ratios': [3, 1, 1, 1]})
        fig.suptitle(f'{self.ticker} 技术指标分析', fontsize=16)
        
        # 价格和均线
        axes[0].plot(self.data.index, self.data['Close'], label='价格')
        axes[0].plot(self.data.index, self.data['MA50'], label='MA50')
        axes[0].plot(self.data.index, self.data['MA200'], label='MA200')
        axes[0].plot(self.data.index, self.data['BB_Upper'], 'r--', label='布林带上轨')
        axes[0].plot(self.data.index, self.data['BB_Middle'], 'g--', label='布林带中轨')
        axes[0].plot(self.data.index, self.data['BB_Lower'], 'r--', label='布林带下轨')
        axes[0].set_title('价格和移动平均线')
        axes[0].legend()
        
        # RSI
        axes[1].plot(self.data.index, self.data['RSI'], label='RSI')
        axes[1].axhline(y=70, color='r', linestyle='--', label='超买线(70)')
        axes[1].axhline(y=30, color='g', linestyle='--', label='超卖线(30)')
        axes[1].set_title('RSI指标')
        axes[1].legend()
        
        # MACD
        axes[2].plot(self.data.index, self.data['MACD'], label='MACD')
        axes[2].plot(self.data.index, self.data['MACD_Signal'], label='信号线')
        axes[2].bar(self.data.index, self.data['MACD_Histogram'], label='柱状图')
        axes[2].set_title('MACD指标')
        axes[2].legend()
        
        # 成交量
        axes[3].bar(self.data.index, self.data['Volume'], label='成交量')
        axes[3].plot(self.data.index, self.data['Volume'].rolling(window=20).mean(), 'r', label='成交量20日均线')
        axes[3].set_title('成交量')
        axes[3].legend()
        
        plt.tight_layout()
        plt.subplots_adjust(top=0.95)
        plt.show()

# 示例使用
def main():
    analyzer = BullMarketTopAnalyzer()
    
    # 获取上证指数数据 (可以替换为其他指数或股票)
    # 注意：上证指数的Yahoo Finance代码是^SSEC
    print("正在获取上证指数数据...")
    analyzer.fetch_stock_data('^SSEC')
    
    # 计算各种技术指标
    print("\n计算技术指标...")
    analyzer.calculate_rsi()
    analyzer.calculate_macd()
    analyzer.calculate_bollinger_bands()
    analyzer.calculate_moving_averages()
    
    # 模拟估值数据（实际应用中应从API获取）
    valuation_metrics = analyzer.calculate_valuation_metrics(pe_ratio=15.6, pb_ratio=1.8)
    print("\n估值指标:")
    for key, value in valuation_metrics.items():
        print(f"{key}: {value}")
    
    # 进行风险评估
    print("\n顶部风险评估:")
    assessment = analyzer.top_risk_assessment(valuation_metrics)
    print(f"风险评分: {assessment['Risk_Score']}")
    print(f"风险等级: {assessment['Risk_Level']}")
    print(f"风险描述: {assessment['Risk_Description']}")
    print("风险因素:")
    for factor in assessment['Risk_Factors']:
        print(f"  - {factor}")
    
    # 检测背离
    print("\n检测背离:")
    divergences = analyzer.detect_divergence()
    if divergences:
        print(f"发现{len(divergences)}次背离:")
        for date, type in divergences[-5:]:  # 只显示最近5次
            print(f"  - {date.date()}: {type}")
    else:
        print("未发现明显背离")
    
    # 绘制技术指标图表
    # analyzer.plot_technical_indicators()

if __name__ == "__main__":
    main()