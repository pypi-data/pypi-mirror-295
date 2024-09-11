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

class SWThirdIndustryInfo(Base):
    __tablename__ = 'sw_third_industry_info'
    
    id = Column(String, primary_key=True)
    industry_code = Column(String)
    industry_name = Column(String)
    constituent_count = Column(Integer)
    static_pe_ratio = Column(Float)
    ttm_pe_ratio = Column(Float)
    pb_ratio = Column(Float)
    static_dividend_yield = Column(Float)
    fetch_time = Column(String, default=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))  # 使用当前时区的当前时间

def fetch_sw_third_industry_info():
    try:
        # 获取申万三级行业信息
        sw_industry_info = ak.sw_index_third_info()
        logging.info("Fetched SW third industry info")
        return sw_industry_info
    except Exception as e:
        logging.error(f"Error fetching SW third industry info, error: {e}")
        return None

def store_sw_third_industry_info(session, sw_industry_info, fetch_time):
    if sw_industry_info is not None:
        try:
            # 准备数据映射列表
            data_mappings = []
            for index, row in sw_industry_info.iterrows():
                data_mappings.append({
                    'id': f"{row['行业代码']}_{fetch_time}",
                    'industry_code': row['行业代码'],
                    'industry_name': row['行业名称'],
                    'constituent_count': row['成份个数'],
                    'static_pe_ratio': row['静态市盈率'],
                    'ttm_pe_ratio': row['TTM(滚动)市盈率'],
                    'pb_ratio': row['市净率'],
                    'static_dividend_yield': row['静态股息率'],
                    'fetch_time': fetch_time
                })
            
            # 批量插入数据
            session.bulk_insert_mappings(SWThirdIndustryInfo, data_mappings)
            session.commit()
            logging.info("Stored SW third industry info")
        except Exception as e:
            logging.error(f"Error storing SW third industry info, error: {e}")
            session.rollback()

def fetch_and_store_sw_third_industry_info(database_path):
    # 创建SQLAlchemy引擎
    engine = create_engine(f'duckdb:///{database_path}')

    # 检查表是否存在
    inspector = inspect(engine)
    if not inspector.has_table(SWThirdIndustryInfo.__tablename__):
        Base.metadata.create_all(engine)
        logging.info("Created table: sw_third_industry_info")
    else:
        logging.info("Table already exists: sw_third_industry_info")

    # 创建会话
    Session = sessionmaker(bind=engine)
    session = Session()

    # 获取申万三级行业信息
    sw_industry_info = fetch_sw_third_industry_info()

    # 处理结果
    fetch_time = datetime.now(pytz.timezone('Asia/Shanghai')).strftime('%Y-%m-%d %H:%M:%S')  # 使用当前时区的当前时间
    if sw_industry_info is not None:
        store_sw_third_industry_info(session, sw_industry_info, fetch_time)

    # 关闭会话
    session.close()

# 使用示例
if __name__ == "__main__":
    fetch_and_store_sw_third_industry_info('stock_industry_datas.duckdb')