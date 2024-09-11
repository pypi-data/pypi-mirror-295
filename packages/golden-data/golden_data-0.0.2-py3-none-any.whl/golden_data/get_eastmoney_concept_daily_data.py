import akshare as ak
from sqlalchemy import create_engine, Column, String, Float, Integer, inspect
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
import logging
import pytz  # 导入 pytz 库以处理时区
from concurrent.futures import ThreadPoolExecutor, as_completed

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 定义数据模型
Base = declarative_base()

class EastMoneyConceptIndexHist(Base):
    __tablename__ = 'eastmoney_concept_index_hist'
    
    id = Column(String, primary_key=True)
    concept_name = Column(String)
    date = Column(String)
    open_price = Column(Float)
    close_price = Column(Float)
    high = Column(Float)
    low = Column(Float)
    change_percent = Column(Float)
    change_amount = Column(Float)
    volume = Column(Integer)
    turnover = Column(Float)
    amplitude = Column(Float)
    turnover_rate = Column(Float)
    fetch_time = Column(String, default=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))  # 使用当前时区的当前时间

def fetch_eastmoney_concept_list():
    # 获取东方财富概念板块列表
    concept_list = ak.stock_board_concept_name_em()
    return concept_list[['板块名称']]

def fetch_eastmoney_concept_hist(concept_name, period, start_date, end_date, adjust):
    try:
        # 获取东方财富概念板块历史行情数据
        hist_data = ak.stock_board_concept_hist_em(symbol=concept_name, period=period, start_date=start_date, end_date=end_date, adjust=adjust)
        logging.info(f"Fetched historical data for concept name: {concept_name}")
        return concept_name, hist_data
    except Exception as e:
        logging.error(f"Error fetching historical data for concept name: {concept_name}, error: {e}")
        return concept_name, None

def store_eastmoney_concept_hist(session, concept_name, hist_data, fetch_time):
    if hist_data is not None:
        try:
            # 准备数据映射列表
            data_mappings = []
            for index, row in hist_data.iterrows():
                data_mappings.append({
                    'id': f"{concept_name}_{row['日期']}",
                    'concept_name': concept_name,
                    'date': row['日期'],
                    'open_price': row['开盘'],
                    'close_price': row['收盘'],
                    'high': row['最高'],
                    'low': row['最低'],
                    'change_percent': row['涨跌幅'],
                    'change_amount': row['涨跌额'],
                    'volume': row['成交量'],
                    'turnover': row['成交额'],
                    'amplitude': row['振幅'],
                    'turnover_rate': row['换手率'],
                    'fetch_time': fetch_time
                })
            
            # 批量插入数据
            session.bulk_insert_mappings(EastMoneyConceptIndexHist, data_mappings)
            session.commit()
            logging.info(f"Stored historical data for concept name: {concept_name}")
        except Exception as e:
            logging.error(f"Error storing historical data for concept name: {concept_name}, error: {e}")
            session.rollback()

def fetch_and_store_all_eastmoney_concept_hist(database_path, period="daily", start_date="20220101", end_date="20221128", adjust="", max_workers=10):
    # 创建SQLAlchemy引擎
    engine = create_engine(f'duckdb:///{database_path}')

    # 检查表是否存在
    inspector = inspect(engine)
    if not inspector.has_table(EastMoneyConceptIndexHist.__tablename__):
        Base.metadata.create_all(engine)
        logging.info("Created table: eastmoney_concept_index_hist")
    else:
        logging.info("Table already exists: eastmoney_concept_index_hist")

    # 创建会话
    Session = sessionmaker(bind=engine)
    session = Session()

    # 获取东方财富概念板块列表
    concept_list = fetch_eastmoney_concept_list()

    # 创建线程池
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # 提交任务
        futures = {executor.submit(fetch_eastmoney_concept_hist, row['板块名称'], period, start_date, end_date, adjust): row for index, row in concept_list.iterrows()}

        # 处理结果
        fetch_time = datetime.now(pytz.timezone('Asia/Shanghai')).strftime('%Y-%m-%d %H:%M:%S')  # 使用当前时区的当前时间
        for future in as_completed(futures):
            concept_name, hist_data = future.result()
            if hist_data is not None:
                store_eastmoney_concept_hist(session, concept_name, hist_data, fetch_time)

    # 关闭会话
    session.close()

# 使用示例
if __name__ == "__main__":
    current_time = datetime.now(pytz.timezone('Asia/Shanghai')).strftime('%Y%m%d')  # 使用当前时区的当前时间
    fetch_and_store_all_eastmoney_concept_hist('stock_industry_datas.duckdb', period="daily", start_date="20120101", end_date=current_time, adjust="", max_workers=10)