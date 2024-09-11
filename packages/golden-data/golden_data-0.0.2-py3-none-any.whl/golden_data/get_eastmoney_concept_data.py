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

class EastMoneyConceptComponent(Base):
    __tablename__ = 'eastmoney_concept_components'
    
    id = Column(String, primary_key=True)
    concept_name = Column(String)
    stock_code = Column(String)
    stock_name = Column(String)
    latest_price = Column(Float)
    change_percent = Column(Float)
    change_amount = Column(Float)
    volume = Column(Float)
    turnover = Column(Float)
    amplitude = Column(Float)
    high = Column(Float)
    low = Column(Float)
    open_price = Column(Float)
    previous_close = Column(Float)
    turnover_rate = Column(Float)
    pe_ratio_dynamic = Column(Float)
    pb_ratio = Column(Float)
    fetch_time = Column(String, default=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))  # 使用当前时区的当前时间

def fetch_eastmoney_concept_list():
    # 获取东方财富概念板块列表
    concept_list = ak.stock_board_concept_name_em()
    return concept_list[['板块名称']]

def fetch_eastmoney_concept_components(concept_name):
    try:
        # 获取东方财富概念板块成分股数据
        components_data = ak.stock_board_concept_cons_em(symbol=concept_name)
        logging.info(f"Fetched components data for concept name: {concept_name}")
        return concept_name, components_data
    except Exception as e:
        logging.error(f"Error fetching components data for concept name: {concept_name}, error: {e}")
        return concept_name, None

def store_eastmoney_concept_components(session, concept_name, components_data, fetch_time):
    if components_data is not None:
        try:
            # 准备数据映射列表
            data_mappings = []
            for index, row in components_data.iterrows():
                data_mappings.append({
                    'id': f"{concept_name}_{row['代码']}",
                    'concept_name': concept_name,
                    'stock_code': row['代码'],
                    'stock_name': row['名称'],
                    'latest_price': row['最新价'],
                    'change_percent': row['涨跌幅'],
                    'change_amount': row['涨跌额'],
                    'volume': row['成交量'],
                    'turnover': row['成交额'],
                    'amplitude': row['振幅'],
                    'high': row['最高'],
                    'low': row['最低'],
                    'open_price': row['今开'],
                    'previous_close': row['昨收'],
                    'turnover_rate': row['换手率'],
                    'pe_ratio_dynamic': row['市盈率-动态'],
                    'pb_ratio': row['市净率'],
                    'fetch_time': fetch_time
                })
            
            # 批量插入数据
            session.bulk_insert_mappings(EastMoneyConceptComponent, data_mappings)
            session.commit()
            logging.info(f"Stored components data for concept name: {concept_name}")
        except Exception as e:
            logging.error(f"Error storing components data for concept name: {concept_name}, error: {e}")
            session.rollback()

def fetch_and_store_all_eastmoney_concept_components(database_path, max_workers=10):
    # 创建SQLAlchemy引擎
    engine = create_engine(f'duckdb:///{database_path}')

    # 检查表是否存在
    inspector = inspect(engine)
    if not inspector.has_table(EastMoneyConceptComponent.__tablename__):
        Base.metadata.create_all(engine)
        logging.info("Created table: eastmoney_concept_components")
    else:
        logging.info("Table already exists: eastmoney_concept_components")

    # 创建会话
    Session = sessionmaker(bind=engine)
    session = Session()

    # 获取东方财富概念板块列表
    concept_list = fetch_eastmoney_concept_list()

    # 创建线程池
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # 提交任务
        futures = {executor.submit(fetch_eastmoney_concept_components, row['板块名称']): row for index, row in concept_list.iterrows()}

        # 处理结果
        fetch_time = datetime.now(pytz.timezone('Asia/Shanghai')).strftime('%Y-%m-%d %H:%M:%S')  # 使用当前时区的当前时间
        for future in as_completed(futures):
            concept_name, components_data = future.result()
            if components_data is not None:
                store_eastmoney_concept_components(session, concept_name, components_data, fetch_time)

    # 关闭会话
    session.close()

# 使用示例
if __name__ == "__main__":
    fetch_and_store_all_eastmoney_concept_components('stock_industry_datas.duckdb', max_workers=10)