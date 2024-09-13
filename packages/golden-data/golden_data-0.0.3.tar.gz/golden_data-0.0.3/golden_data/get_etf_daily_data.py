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

class DailyETF(Base):
    __tablename__ = 'daily_etf_data'
    
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

def fetch_etf_list():
    # 获取ETF列表
    etf_list = ak.fund_etf_spot_em()
    return etf_list['代码'].tolist()

def fetch_daily_etf_data(code, start_date, end_date, adjust="", period="daily"):
    try:
        # 获取ETF日线行情数据
        etf_data = ak.fund_etf_hist_em(symbol=code, period=period, start_date=start_date, end_date=end_date, adjust=adjust)
        
        etf_data['日期'] = etf_data['日期'].astype(str)  # 确保日期字段是字符串类型
        etf_data = etf_data[(etf_data['日期'] >= start_date) & (etf_data['日期'] <= end_date)]
        logging.info(f"Fetched data for ETF code: {code}")
        return code, etf_data
    except Exception as e:
        logging.error(f"Error fetching data for ETF code: {code}, error: {e}")
        return code, None

def store_daily_etf_data(session, code, etf_data, fetch_time):
    if etf_data is not None:
        try:
            # 准备数据映射列表
            data_mappings = []
            for index, row in etf_data.iterrows():
                data_mappings.append({
                    'code': code,
                    'date': row['日期'],
                    'open': row['开盘'],
                    'high': row['最高'],
                    'low': row['最低'],
                    'close': row['收盘'],
                    'volume': row['成交量'],
                    'amount': row['成交额'],
                    'amplitude': row['振幅'],
                    'change_percent': row['涨跌幅'],
                    'change_amount': row['涨跌额'],
                    'turnover_rate': row['换手率'],
                    'fetch_time': fetch_time
                })
            
            # 批量插入数据
            session.bulk_insert_mappings(DailyETF, data_mappings)
            session.commit()
            logging.info(f"Stored data for ETF code: {code}")
        except Exception as e:
            logging.error(f"Error storing data for ETF code: {code}, error: {e}")
            session.rollback()

def get_latest_trade_date(session):
    # 获取最新的交易日
    latest_date = session.query(DailyETF.date).order_by(DailyETF.date.desc()).first()
    return latest_date[0] if latest_date else None

def fetch_and_store_daily_etf_data(database_path, start_date, end_date, adjust="", period="daily", max_workers=10):
    # 检查日期格式
    if not (is_valid_date_format(start_date) and is_valid_date_format(end_date)):
        logging.error("Invalid date format. Dates should be in 'YYYYMMDD' format.")
        return

    # 获取ETF列表
    etf_codes = fetch_etf_list()

    # 创建SQLAlchemy引擎
    engine = create_engine(f'duckdb:///{database_path}')

    # 检查表是否存在
    inspector = inspect(engine)
    if not inspector.has_table(DailyETF.__tablename__):
        Base.metadata.create_all(engine)
        logging.info("Created table: daily_etf_data")
    else:
        logging.info("Table already exists: daily_etf_data")

    # 创建会话
    Session = sessionmaker(bind=engine)
    session = Session()

    # 获取最新的交易日
    latest_trade_date = get_latest_trade_date(session)
    if latest_trade_date:
        start_date = latest_trade_date
        logging.info(f"Latest trade date found: {latest_trade_date}. Updating data from this date.")

    # 创建线程池
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # 提交任务
        futures = {executor.submit(fetch_daily_etf_data, code, start_date, end_date, adjust, period): code for code in etf_codes}

        # 处理结果
        fetch_time = datetime.now(pytz.timezone('Asia/Shanghai')).strftime('%Y-%m-%d %H:%M:%S')  # 使用当前时区的当前时间
        for future in as_completed(futures):
            code, etf_data = future.result()
            if etf_data is not None:
                store_daily_etf_data(session, code, etf_data, fetch_time)

    # 关闭会话
    session.close()

def is_valid_date_format(date_str):
    try:
        datetime.strptime(date_str, '%Y%m%d')
        return True
    except ValueError:
        return False


def read_daily_etf_data(database_path):
    # 创建SQLAlchemy引擎
    engine = create_engine(f'duckdb:///{database_path}')
    
    # 读取数据
    query = "SELECT * FROM daily_etf_data"
    df = pd.read_sql(query, engine)
    
    # 将 'code' 和 'date' 列设置为 MultiIndex
    df['date'] = pd.to_datetime(df['date'])  # 确保日期列是datetime类型
    df.set_index(['code', 'date'], inplace=True)
    
    # 对 MultiIndex 进行排序
    df.sort_index(inplace=True)
    
    return df

# 使用示例
if __name__ == "__main__":
    #print('更新ETF数据至当前时间')
    #current_time = datetime.now(pytz.timezone('Asia/Shanghai')).strftime('%Y%m%d')  # 使用当前时区的当前时间
    #fetch_and_store_daily_etf_data('etf_data.duckdb', '20120101', current_time, adjust="", period="daily", max_workers=10)
    df=read_daily_etf_data("etf_data.duckdb")
    print(df.head())