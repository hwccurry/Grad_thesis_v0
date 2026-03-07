# 摘要

在中国资本市场从"软约束"向"硬约束"监管转型的背景下，厘清上市公司分红的动因及其对监管政策的响应，是公司金融领域的重要议题。本文构建"机器学习预测+双重差分因果推断"的双路径研究框架，从统计关联与因果识别两个维度，系统剖析中国上市公司的分红行为。

第一路径基于2006—2022年沪深A股数据，采用随机森林（RF）与梯度提升树（GBDT）构建非线性预测模型。经模型泛化性能对比发现，上述集成学习模型的样本外精度显著优于OLS、Lasso等传统线性预测模型。据此，本文对71个候选特征进行系统预测与排序。特征重要性结果显示，上一期股利水平、资产收益率和留存收益资产比稳居前三，代理成本变量（如其他应收款资产比）进入前十并表现出非线性抑制效应，验证了股利平滑理论、生命周期理论及代理理论等在中国市场的适用性。主成分分析进一步确认，生命周期与代理成本构成解释分红行为的主导经济维度。

第二路径以2023年《上市公司现金分红指引》修订为准自然实验，基于2020—2024年数据的双向固定效应DID模型估计发现，政策使处理组企业分红概率提高约8.3个百分点、股利支付率提高约10.8个百分点（均在1%水平显著），该结论在安慰剂检验、PSM-DID、熵平衡匹配、Hausman-Taylor估计等多项稳健性和内生性检验下保持稳定。异质性分析表明，分红监管对代理问题突出的企业影响尤为显著。进一步的经济后果分析表明，政策引致企业分红提升，显著改善了市场流动性（表现为交易量与换手率上升）并降低了错误定价程度，说明分红监管有助于提升资本市场定价效率。

综上，本文从预测与因果双重视角证实了生命周期与代理成本是理解中国企业分红行为的核心维度，而"硬约束"分红监管能够有效矫正代理问题引发的分红不足，也带来了积极的市场效应。上述发现为完善常态化分红制度、优化公司治理提供了理论依据与经验支持。

**关键词：** 上市公司分红；机器学习预测；双重差分法；代理成本；公司治理

# Abstract

Why do Chinese listed firms pay dividends? Against the backdrop of China's capital market transitioning from "soft constraints" to "hard constraints" in dividend regulation, clarifying the determinants of corporate dividends and their responsiveness to regulatory policy constitutes an important issue in corporate finance. This paper constructs a dual-pathway research framework combining machine learning prediction with difference-in-differences (DiD) causal inference, systematically analyzing the dividend behavior of Chinese listed firms from both predictive and causal perspectives.

The first pathway employs Random Forest (RF) and Gradient Boosting (GBDT) to build nonlinear prediction models using 2006–2022 Shanghai-Shenzhen A-share data. Generalization performance comparisons demonstrate that these ensemble learning models significantly outperform traditional linear models such as OLS and Lasso in out-of-sample accuracy. Based on systematic prediction and ranking of 71 candidate features, lagged dividend level, return on assets, and retained-earnings-to-assets ratio consistently rank among the top three predictors, while agency cost proxies (such as other receivables-to-assets ratio) enter the top ten and exhibit nonlinear suppressive effects, validating the applicability of dividend smoothing theory, life cycle theory, and agency theory in the Chinese market. Principal component analysis further confirms that life cycle and agency costs constitute the dominant economic dimensions explaining dividend behavior.

The second pathway exploits the 2023 revision of China's Cash Dividend Guidelines as a quasi-natural experiment. Two-way fixed effects DiD estimates based on 2020–2024 data show that the policy increased treated firms' dividend probability by approximately 8.3 percentage points and payout ratio by approximately 10.8 percentage points (both significant at the 1% level). These findings remain robust across multiple robustness and endogeneity tests including placebo tests, PSM-DiD, entropy balancing, and Hausman-Taylor estimation. Heterogeneity analysis reveals that dividend regulation has a particularly significant impact on firms with acute agency problems. Further economic consequence analysis demonstrates that policy-induced dividend increases significantly improve market liquidity (reflected in higher trading volume and turnover) and reduce mispricing, suggesting that dividend regulation contributes to enhanced capital market pricing efficiency.

In summary, this paper provides evidence from both predictive and causal perspectives confirming that life cycle stage and agency costs are the core dimensions for understanding Chinese firms' dividend behavior, while "hard constraint" dividend regulation can effectively correct dividend deficiency arising from agency problems and generates positive market effects. These findings offer theoretical foundations and empirical support for improving normalized dividend systems and optimizing corporate governance.

**Keywords:** Corporate Dividends; Machine Learning Prediction; Difference-in-Differences; Agency Costs; Corporate Governance
