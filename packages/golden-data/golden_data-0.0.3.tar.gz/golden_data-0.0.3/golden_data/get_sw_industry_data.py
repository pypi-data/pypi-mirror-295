import akshare as ak
from sqlalchemy import create_engine, Column, String, Float, inspect
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
import logging
import pytz  # 导入 pytz 库以处理时区

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 定义数据模型
Base = declarative_base()

class SWIndustryComponent(Base):
    __tablename__ = 'sw_industry_components'
    
    id = Column(String, primary_key=True)
    stock_code = Column(String)
    stock_name = Column(String)
    inclusion_date = Column(String)
    sw_level_1 = Column(String)
    sw_level_2 = Column(String)
    sw_level_3 = Column(String)
    price = Column(Float)
    pe_ratio = Column(Float)
    pe_ratio_ttm = Column(Float)
    pb_ratio = Column(Float)
    dividend_yield = Column(Float)
    market_cap = Column(Float)
    net_profit_growth_09_30 = Column(Float)
    net_profit_growth_06_30 = Column(Float)
    revenue_growth_09_30 = Column(Float)
    revenue_growth_06_30 = Column(Float)
    fetch_time = Column(String, default=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))  # 使用当前时区的当前时间

def fetch_sw_industry_list():
    # 获取申万三级行业列表
    industry_list = ak.sw_index_third_info()
    return industry_list[['行业代码', '行业名称']]

def fetch_sw_industry_components(industry_code):
    try:
        # 获取申万三级行业成分数据
        components_data = ak.sw_index_third_cons(symbol=industry_code)
        logging.info(f"Fetched components data for industry code: {industry_code}")
        return industry_code, components_data
    except Exception as e:
        logging.error(f"Error fetching components data for industry code: {industry_code}, error: {e}")
        return industry_code, None

def store_sw_industry_components(session, industry_code, components_data, fetch_time):
    if components_data is not None:
        try:
            # 准备数据映射列表
            data_mappings = []
            for index, row in components_data.iterrows():
                data_mappings.append({
                    'id': f"{industry_code}_{row['股票代码']}",
                    'stock_code': row['股票代码'],
                    'stock_name': row['股票简称'],
                    'inclusion_date': row['纳入时间'],
                    'sw_level_1': row['申万1级'],
                    'sw_level_2': row['申万2级'],
                    'sw_level_3': row['申万3级'],
                    'price': row['价格'],
                    'pe_ratio': row['市盈率'],
                    'pe_ratio_ttm': row['市盈率ttm'],
                    'pb_ratio': row['市净率'],
                    'dividend_yield': row['股息率'],
                    'market_cap': row['市值'],
                    'net_profit_growth_09_30': row['归母净利润同比增长(09-30)'],
                    'net_profit_growth_06_30': row['归母净利润同比增长(06-30)'],
                    'revenue_growth_09_30': row['营业收入同比增长(09-30)'],
                    'revenue_growth_06_30': row['营业收入同比增长(06-30)'],
                    'fetch_time': fetch_time
                })
            
            # 批量插入数据
            session.bulk_insert_mappings(SWIndustryComponent, data_mappings)
            session.commit()
            logging.info(f"Stored components data for industry code: {industry_code}")
        except Exception as e:
            logging.error(f"Error storing components data for industry code: {industry_code}, error: {e}")
            session.rollback()

def fetch_and_store_all_sw_industry_components(database_path):
    # 创建SQLAlchemy引擎
    engine = create_engine(f'duckdb:///{database_path}')

    # 检查表是否存在
    inspector = inspect(engine)
    if not inspector.has_table(SWIndustryComponent.__tablename__):
        Base.metadata.create_all(engine)
        logging.info("Created table: sw_industry_components")
    else:
        logging.info("Table already exists: sw_industry_components")

    # 创建会话
    Session = sessionmaker(bind=engine)
    session = Session()

    # 获取申万三级行业列表
    industry_list = fetch_sw_industry_list()

    # 处理每个行业的成分数据
    fetch_time = datetime.now(pytz.timezone('Asia/Shanghai')).strftime('%Y-%m-%d %H:%M:%S')  # 使用当前时区的当前时间
    for index, row in industry_list.iterrows():
        industry_code = row['行业代码']
        industry_name = row['行业名称']
        logging.info(f"Fetching components data for industry code: {industry_code} - {industry_name}")
        industry_code, components_data = fetch_sw_industry_components(industry_code)
        if components_data is not None:
            store_sw_industry_components(session, industry_code, components_data, fetch_time)

    # 关闭会话
    session.close()

# 使用示例
if __name__ == "__main__":
    fetch_and_store_all_sw_industry_components('stock_industry_datas.duckdb')