import easyquotation

quotation = easyquotation.use('qq') # 新浪 ['sina'] 腾讯 ['tencent', 'qq']
data = quotation.market_snapshot(prefix=True) # prefix 参数指定返回的行情字典中的股票代码 key 是否带 sz/sh 前缀
for i in data:
    print(i)
print(data['sh600001']['name'])
