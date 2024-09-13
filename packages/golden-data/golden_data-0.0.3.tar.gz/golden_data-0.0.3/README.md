使用akshare爬取数据，
使用duckdb存储数据，

duckdb可以使用dbeaver这个GUI工具查看。

# 数据获取
- 获取ETF日线
- 获取股票日线
- 获取ETF描述信息 TODO
- 行业数据集（用于行业中性化）
- 东方财富概念板块数据和历史行情
- 指数日线 TODO
- 主营业务 TODO
- 历史分笔数据 积累（需要每日运行）TODO
- 东方财富网-数据中心-股市日历-公司动态 可以用AI进行情感分析 TODO

# 使用方法

目前还在单个数据下载测试，每个文件都有main函数，待开发完成后合并成一个下载器。

# 开发和测试

```
invoke build
invoke pypitest
invoke pypiupload
```

# 开发使用

```
from golden_data import read_daily_stock_data
df=read_daily_stock_data('stock_data.duckdb')
print(df.head())
```