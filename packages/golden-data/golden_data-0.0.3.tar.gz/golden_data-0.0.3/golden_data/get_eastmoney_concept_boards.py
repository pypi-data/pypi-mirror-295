import akshare as ak
from sqlalchemy import create_engine, Column, String, Float, Integer, inspect
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
import logging
import pytz  # 导入 pytz 库以处理时区

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 定义数据模型
Base = declarative_base()

class EastMoneyConceptBoard(Base):
    __tablename__ = 'eastmoney_concept_boards'
    
    id = Column(String, primary_key=True)
    rank = Column(Integer)
    concept_name = Column(String)
    concept_code = Column(String)
    latest_price = Column(Float)
    change_amount = Column(Float)
    change_percent = Column(Float)
    total_market_cap = Column(Float)
    turnover_rate = Column(Float)
    rising_count = Column(Float)  # 上涨家数
    falling_count = Column(Float)  # 下跌家数
    leading_stock = Column(String)
    leading_stock_change_percent = Column(Float)
    fetch_time = Column(String, default=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))  # 使用当前时区的当前时间

def fetch_eastmoney_concept_board():
    try:
        # 获取东方财富概念板块数据
        concept_board_data = ak.stock_board_concept_name_em()
        logging.info("Fetched concept board data")
        return concept_board_data
    except Exception as e:
        logging.error(f"Error fetching concept board data, error: {e}")
        return None

def store_eastmoney_concept_board(session, concept_board_data, fetch_time):
    if concept_board_data is not None:
        try:
            # 准备数据映射列表
            data_mappings = []
            for index, row in concept_board_data.iterrows():
                data_mappings.append({
                    'id': f"{row['板块代码']}_{fetch_time}",
                    'rank': row['排名'],
                    'concept_name': row['板块名称'],
                    'concept_code': row['板块代码'],
                    'latest_price': row['最新价'],
                    'change_amount': row['涨跌额'],
                    'change_percent': row['涨跌幅'],
                    'total_market_cap': row['总市值'],
                    'turnover_rate': row['换手率'],
                    'rising_count': row['上涨家数'],
                    'falling_count': row['下跌家数'],
                    'leading_stock': row['领涨股票'],
                    'leading_stock_change_percent': row['领涨股票-涨跌幅'],
                    'fetch_time': fetch_time
                })
            
            # 批量插入数据
            session.bulk_insert_mappings(EastMoneyConceptBoard, data_mappings)
            session.commit()
            logging.info("Stored concept board data")
        except Exception as e:
            logging.error(f"Error storing concept board data, error: {e}")
            session.rollback()

def fetch_and_store_eastmoney_concept_board(database_path):
    # 创建SQLAlchemy引擎
    engine = create_engine(f'duckdb:///{database_path}')

    # 检查表是否存在
    inspector = inspect(engine)
    if not inspector.has_table(EastMoneyConceptBoard.__tablename__):
        Base.metadata.create_all(engine)
        logging.info("Created table: eastmoney_concept_boards")
    else:
        logging.info("Table already exists: eastmoney_concept_boards")

    # 创建会话
    Session = sessionmaker(bind=engine)
    session = Session()

    # 获取东方财富概念板块数据
    concept_board_data = fetch_eastmoney_concept_board()

    # 处理结果
    fetch_time = datetime.now(pytz.timezone('Asia/Shanghai')).strftime('%Y-%m-%d %H:%M:%S')  # 使用当前时区的当前时间
    if concept_board_data is not None:
        store_eastmoney_concept_board(session, concept_board_data, fetch_time)

    # 关闭会话
    session.close()

# 使用示例
if __name__ == "__main__":
    fetch_and_store_eastmoney_concept_board('stock_industry_datas.duckdb')