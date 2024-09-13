import akshare as ak
from sqlalchemy import create_engine, Column, Float, String, inspect
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging
import pytz  # 导入 pytz 库以处理时区
import pandas as pd
# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 定义数据模型
Base = declarative_base()

class DailyStock(Base):
    __tablename__ = 'daily_stock_data'
    
    code = Column(String, primary_key=True)
    date = Column(String, primary_key=True)  # 使用字符串存储日期
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(Float)
    amount = Column(Float)
    amplitude = Column(Float)  # 振幅
    change_percent = Column(Float)  # 涨跌幅
    change_amount = Column(Float)  # 涨跌额
    turnover_rate = Column(Float)  # 换手率
    fetch_time = Column(String, default=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))  # 使用当前时区的当前时间

def fetch_stock_list():
    # 获取股票列表
    stock_list = ak.stock_zh_a_spot_em()
    return stock_list['代码'].tolist()

def fetch_daily_stock_data(code, start_date, end_date, adjust="qfq"):
    try:
        # 获取股票日线行情数据
        stock_data = ak.stock_zh_a_hist(symbol=code, period="daily", start_date=start_date, end_date=end_date, adjust=adjust)
        logging.info(f"Fetched data for stock code: {code}")
        return code, stock_data
    except Exception as e:
        logging.error(f"Error fetching data for stock code: {code}, error: {e}")
        return code, None

def store_daily_stock_data(session, code, stock_data, fetch_time):
    if stock_data is not None:
        try:
            for index, row in stock_data.iterrows():
                # 确保日期字段是字符串类型
                date_str = row['日期'].strftime('%Y-%m-%d') if isinstance(row['日期'], datetime) else str(row['日期'])
                daily_stock = DailyStock(
                    code=code,
                    date=date_str,
                    open=row['开盘'],
                    high=row['最高'],
                    low=row['最低'],
                    close=row['收盘'],
                    volume=row['成交量'],
                    amount=row['成交额'],
                    amplitude=row['振幅'],
                    change_percent=row['涨跌幅'],
                    change_amount=row['涨跌额'],
                    turnover_rate=row['换手率'],
                    fetch_time=fetch_time
                )
                session.add(daily_stock)
            session.commit()
            logging.info(f"Stored data for stock code: {code}")
        except Exception as e:
            logging.error(f"Error storing data for stock code: {code}, error: {e}")
            session.rollback()

def fetch_and_store_daily_stock_data(database_path, start_date, end_date, adjust="qfq", max_workers=10):
    # 检查日期格式
    if not (is_valid_date_format(start_date) and is_valid_date_format(end_date)):
        logging.error("Invalid date format. Dates should be in 'YYYYMMDD' format.")
        return

    # 获取股票列表
    stock_codes = fetch_stock_list()

    # 创建SQLAlchemy引擎
    engine = create_engine(f'duckdb:///{database_path}')

    # 检查表是否存在
    inspector = inspect(engine)
    if not inspector.has_table(DailyStock.__tablename__):
        Base.metadata.create_all(engine)
        logging.info("Created table: daily_stock_data")
    else:
        logging.info("Table already exists: daily_stock_data")

    # 创建会话
    Session = sessionmaker(bind=engine)
    session = Session()

    # 创建线程池
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # 提交任务
        futures = {executor.submit(fetch_daily_stock_data, code, start_date, end_date, adjust): code for code in stock_codes}

        # 处理结果
        fetch_time = datetime.now(pytz.timezone('Asia/Shanghai')).strftime('%Y-%m-%d %H:%M:%S')  # 使用当前时区的当前时间
        for future in as_completed(futures):
            code, stock_data = future.result()
            if stock_data is not None:
                store_daily_stock_data(session, code, stock_data, fetch_time)

    # 关闭会话
    session.close()

def is_valid_date_format(date_str):
    try:
        datetime.strptime(date_str, '%Y%m%d')
        return True
    except ValueError:
        return False


def read_daily_stock_data(database_path):
    # 创建SQLAlchemy引擎
    engine = create_engine(f'duckdb:///{database_path}')
    
    # 读取数据
    query = "SELECT * FROM daily_stock_data"
    df = pd.read_sql(query, engine)
    
    # 将 'code' 和 'date' 列设置为 MultiIndex
    df['date'] = pd.to_datetime(df['date'])  # 确保日期列是datetime类型
    df.set_index(['code', 'date'], inplace=True)
    
    # 对 MultiIndex 进行排序
    df.sort_index(inplace=True)
    
    return df

# 使用示例
if __name__ == "__main__":
    #fetch_and_store_daily_stock_data('stock_data.duckdb', '20230101', '20240731', adjust="hfq", max_workers=10)
    # 读取数据示例
    df = read_daily_stock_data('stock_data.duckdb')
    print(df.head())