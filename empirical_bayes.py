df.index = pd.to_datetime(df['DateTime'])
print("holy crap I'm done!")
df = pd.pivot_table(df,index=[pd.TimeGrouper('d'),'RuleName'],columns='OrigCaseStatus',aggfunc='count').fillna(0)
#%%
df = df.reindex(method='bfill')
df['count'] = df['RSMRuleID'].sum(axis=1)
df['frauds'] = df['RSMRuleID']['Closed Confirmed Fraud']+df['RSMRuleID']['Closed Unconfirmed Fraud']

df = df.groupby(level=['RuleName']).apply(lambda x:x.rolling(window=14).sum())
df['rate'] = df['frauds']/df['count']

#%%

_alpha,_beta,loc,scale = beta.fit(df[df['count']>=0]['rate'])
#%%
df['empbayes'] = (df['frauds']+_alpha)/(df['count']+_alpha+_beta)
df['fpr'] = (1-df['empbayes'])/df['empbayes']
print(df['empbayes'])
x = np.linspace(0.001,
                0.999, 10000)
plt.plot(x, beta.pdf(x, _alpha,_beta))
plt.show()
#%%
idx = pd.IndexSlice
for rule in df.index.levels[1]:
    df.loc[idx[:,rule],'empbayes'].reset_index(level=1)['empbayes'].plot(label=rule)
    plt.hlines(0.33,-1000,9999999,color='red',linestyle='--')
    plt.ylim(0,1)
    plt.title(rule)
#plt.legend(bbox_to_anchor=(2, 1.025,1,1))

    plt.show()
