import akshare as ak
from sqlalchemy import create_engine, Column, Float, String, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

# 定义数据模型
Base = declarative_base()

class Stock(Base):
    __tablename__ = 'stock_zh_a_spot_em'
    
    code = Column(String, primary_key=True)
    name = Column(String)
    latest_price = Column(Float)
    change_percent = Column(Float)
    change_amount = Column(Float)
    volume = Column(Float)
    turnover = Column(Float)
    amplitude = Column(Float)
    high = Column(Float)
    low = Column(Float)
    open = Column(Float)
    previous_close = Column(Float)
    volume_ratio = Column(Float)
    turnover_rate = Column(Float)
    pe_ratio = Column(Float)
    pb_ratio = Column(Float)
    fetch_time = Column(DateTime, default=datetime.utcnow)

def fetch_and_store_stock_data(database_path):
    # 获取股票行情数据
    stock_data = ak.stock_zh_a_spot_em()

    # 打印数据以确认获取成功
    print(stock_data.head())

    # 创建SQLAlchemy引擎
    engine = create_engine(f'duckdb:///{database_path}')

    # 创建表
    Base.metadata.create_all(engine)

    # 创建会话
    Session = sessionmaker(bind=engine)
    session = Session()

    # 插入数据
    fetch_time = datetime.utcnow()
    for index, row in stock_data.iterrows():
        stock = Stock(
            code=row['代码'],
            name=row['名称'],
            latest_price=row['最新价'],
            change_percent=row['涨跌幅'],
            change_amount=row['涨跌额'],
            volume=row['成交量'],
            turnover=row['成交额'],
            amplitude=row['振幅'],
            high=row['最高'],
            low=row['最低'],
            open=row['今开'],
            previous_close=row['昨收'],
            volume_ratio=row['量比'],
            turnover_rate=row['换手率'],
            pe_ratio=row['市盈率-动态'],
            pb_ratio=row['市净率'],
            fetch_time=fetch_time
        )
        session.add(stock)

    # 提交事务
    session.commit()

    # 关闭会话
    session.close()

# 使用示例
if __name__ == "__main__":
    fetch_and_store_stock_data('stock_data.duckdb')