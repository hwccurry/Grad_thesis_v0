# 摘要

中国上市公司为何分红？本文构建"机器学习预测 + 双重差分因果推断"的双路径框架，从统计关联与因果识别两个层面回答这一问题。第一路径以2006—2022年沪深A股为样本，采用随机森林和梯度提升树在一年期滚动预测框架下比较71个候选特征，发现集成学习模型的样本外R²约为0.25，显著优于OLS（0.16）；特征重要性排序中，上期股利水平、资产收益率和留存收益资产比稳居前三，代理成本变量（其他应收款资产比）进入前十且对分红表现出非线性抑制效应。第二路径以2023年《上市公司现金分红指引》修订为准自然实验，基于2020—2024年双向固定效应DiD模型估计发现，政策使处理组分红概率提高约8.3个百分点、股利支付率提高约10.8个百分点（均在1%水平显著），且高代理成本企业的政策效应显著更强。上述结论在平行趋势、安慰剂、PSM-DiD等多项稳健性检验下保持稳定。本文表明，生命周期与代理成本是理解中国企业分红行为的核心维度，"硬约束"分红监管对代理问题突出的企业效果尤为明显。

**关键词：** 上市公司分红；机器学习预测；双重差分法；代理成本；公司治理

# Abstract

Why do Chinese listed firms pay dividends? This paper combines machine learning prediction with a difference-in-differences (DiD) quasi-natural experiment to address this question from both predictive and causal perspectives. Using 2006–2022 data on Shanghai-Shenzhen A-share firms, Random Forest and Gradient Boosting models in a one-year rolling framework achieve an out-of-sample R² of approximately 0.25, substantially outperforming OLS (0.16). Lagged dividends, return on assets, and retained-earnings-to-assets ratio rank as the top three predictors, while agency cost proxies enter the top ten and exhibit nonlinear suppressive effects on payouts. Exploiting the 2023 revision of China's Cash Dividend Guidelines as a policy shock, two-way fixed effects DiD estimates show that the regulation raised treated firms' dividend probability by 8.3 percentage points and payout ratio by 10.8 percentage points (both significant at 1%), with significantly stronger effects among high-agency-cost firms. Results survive parallel trends, placebo, and PSM-DiD checks. Life cycle stage and agency costs emerge as the core dimensions of Chinese firms' dividend behavior, and binding dividend regulation is most effective where agency problems are acute.

**Keywords:** Corporate Dividends; Machine Learning Prediction; Difference-in-Differences; Agency Costs; Corporate Governance
