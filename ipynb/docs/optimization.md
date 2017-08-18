```flow
st=>start: load libraries
e=>end: return optimized weight dataframe
d=>operation: load data
transfer=>operation: transfer_data
risk=>operation: 提取risk model data 并按需求转换
man=>operation: manipulate data to requested form
opts=>operation: multi-period optimization by date index
cal_risk=>operation: target symbols risk calculation
constraint=>operation: setup constraint
prob=>operation: setup problem based on constraint and target
sol=>operation: solve for the problem
cond=>condition: loop end to date index?

st->d->transfer->man->risk->opts->cal_risk->constraint->prob->sol->cond
cond(yes)->e
cond(no)->opts
```

```python
def CvxOptimizer(target_mode, position_limit, risk_model,
                    asset_return, asset_weight, target_risk,
                    target_return, target_date, asset_constraint,
                    group_constraint, exposure_constraint)

	# transfer_data
	if asset_constraint is not None:
        asset_constraint = asset_constraint.asMatrix()
    if group_constraint is not None:
        group_constraint = group_constraint.asMatrix()
    if exposure_constraint is not None:
        exposure_constraint = exposure_constraint.asMatrix()

	# 提取risk model data 并按需求转换
	data = ExtractDictModelData(risk_model)
	risk_data = RiskAnlysis(data)

	# create optmized weight dataframe
	df_opts_weight = pd.DataFrame(data=np.nan, columns=specific_risk.columns,
                                  index=exposure_constraint.index)

	# multi-period optimization by date index
    for target_date in exposure_constraint.index:
		# 提取target symbols
		target_symbols = ...

		# target symbols risk calculation
		big_X = get_factor_exposure(risk_model, ls_factor, target_date,
                                    idx_level_1_value)

        cov_matrix = cov_matrix.reindex(all_factors, all_factors, fill_value=np.nan)

		# Factor model portfolio optimization process.
        w = cvx.Variable(noa)
        G_sum = np.array(matrix(Group_sub))*w
        f = big_X.T.values*w
        gamma = cvx.Parameter(sign='positive')
        Lmax = cvx.Parameter()
        ret = w.T * rets_mean.values
        risk = cvx.quad_form(f, cov_matrix.values) + cvx.quad_form(w, delta.values)

		# setup constraint
        eq_constraint = [cvx.sum_entries(w) == 1,
                         cvx.norm(w, 1) <= Lmax]
        l_eq_constraint = [w >= df_asset_weight.lower.values,
                           w <= df_asset_weight.upper.values,
                           G_sum >= df_group_weight.lower.values,
                           G_sum <= df_group_weight.upper.values]
        if exposure_constraint is not None:
            l_eq_constraint.append(f >= df_factor_exposure_lower_bnd.values)
            l_eq_constraint.append(f <= df_factor_exposure_upper_bnd.values)

        #Portfolio optimization with a leverage limit and a bound on risk
        Lmax.value = 1
        gamma.value = 1

        if target_mode == MinimumRisk:
            # Solve the factor model problem.
            prob_factor = cvx.Problem(cvx.Maximize(-gamma*risk),
                                      eq_constraint+l_eq_constraint)
        if target_mode == MinimumRiskUnderReturn:
            # minimum risk subject to target return, Markowitz Mean_Variance Portfolio
            prob_factor = cvx.Problem(cvx.Maximize(-gamma*risk),
                                      [ret >= target_return]+l_eq_constraint+eq_constraint)
        if target_mode == MaximumReturnUnderRisk:
            # Computes a tangency portfolio, i.e. a maximum Sharpe ratio portfolio
            prob_factor = cvx.Problem(cvx.Maximize(ret),
                                      [risk <= target_risk]+l_eq_constraint+eq_constraint)

		# solve for optimized w
        prob_factor.solve(verbose=False)
        logger.debug(prob_factor.status)
        if prob_factor.status == 'infeasible':
            # relax constraint
			# to do
        else:
            df_opts_weight.loc[target_date, idx_level_1_value] = np.array(w.value.astype(np.float64)).T

	return df_opts_weight.dropna(axis=1, how='all')
 ```
