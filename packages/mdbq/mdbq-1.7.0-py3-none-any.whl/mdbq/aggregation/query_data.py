# -*- coding: UTF-8 –*-
from mdbq.mongo import mongo
from mdbq.mysql import mysql
from mdbq.mysql import s_query
from mdbq.aggregation import optimize_data
from mdbq.config import get_myconf
import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd
import numpy as np
from functools import wraps
import platform
import getpass
import json
import os

from sqlalchemy.event import remove

"""
程序用于下载数据库(调用 s_query.py 下载并清洗), 并对数据进行聚合清洗, 不会更新数据库信息;

添加新库流程：
1.  在 MysqlDatasQuery 类中创建函数，从数据库取出数据
2.  在 GroupBy 类中创建函数，处理聚合数据
3.  在 data_aggregation 类中添加 data_dict 字典键值，回传数据到数据库

"""


class MongoDatasQuery:
    """
    从 数据库 中下载数据
    self.output: 数据库默认导出目录
    self.is_maximize: 是否最大转化数据
    """
    def __init__(self, target_service):
        # target_service 从哪个服务器下载数据
        self.months = 0  # 下载几个月数据, 0 表示当月, 1 是上月 1 号至今
        # 实例化一个下载类
        username, password, host, port = get_myconf.select_config_values(target_service=target_service, database='mongodb')
        self.download = mongo.DownMongo(username=username, password=password, host=host, port=port, save_path=None)

    def tg_wxt(self):
        self.download.start_date, self.download.end_date = self.months_data(num=self.months)
        projection = {
            '日期': 1,
            '场景名字': 1,
            '主体id': 1,
            '花费': 1,
            '展现量': 1,
            '点击量': 1,
            '总购物车数': 1,
            '总成交笔数': 1,
            '总成交金额': 1,
            '自然流量曝光量': 1,
            '直接成交笔数': 1,
            '直接成交金额': 1,
        }
        df = self.download.data_to_df(
            db_name='推广数据2',
            collection_name='主体报表',
            projection=projection,
        )
        return df

    @staticmethod
    def days_data(days, end_date=None):
        """ 读取近 days 天的数据 """
        if not end_date:
            end_date = datetime.datetime.now()
        start_date = end_date - datetime.timedelta(days=days)
        return pd.to_datetime(start_date), pd.to_datetime(end_date)

    @staticmethod
    def months_data(num=0, end_date=None):
        """ 读取近 num 个月的数据, 0 表示读取当月的数据 """
        if not end_date:
            end_date = datetime.datetime.now()
        start_date = end_date - relativedelta(months=num)  # n 月以前的今天
        start_date = f'{start_date.year}-{start_date.month}-01'  # 替换为 n 月以前的第一天
        return pd.to_datetime(start_date), pd.to_datetime(end_date)


class MysqlDatasQuery:
    """
    从数据库中下载数据
    """
    def __init__(self, target_service):
        # target_service 从哪个服务器下载数据
        self.months = 0  # 下载几个月数据, 0 表示当月, 1 是上月 1 号至今
        # 实例化一个下载类
        username, password, host, port = get_myconf.select_config_values(target_service=target_service, database='mysql')
        self.download = s_query.QueryDatas(username=username, password=password, host=host, port=port)

    def tg_wxt(self):
        start_date, end_date = self.months_data(num=self.months)
        projection = {
            '日期': 1,
            '场景名字': 1,
            '主体id': 1,
            '花费': 1,
            '展现量': 1,
            '点击量': 1,
            '总购物车数': 1,
            '总成交笔数': 1,
            '总成交金额': 1,
            '自然流量曝光量': 1,
            '直接成交笔数': 1,
            '直接成交金额': 1,
        }
        df = self.download.data_to_df(
            db_name='推广数据2',
            table_name='主体报表',
            start_date=start_date,
            end_date=end_date,
            projection=projection,
        )
        return df

    def syj(self):
        start_date, end_date = self.months_data(num=self.months)
        projection = {
            '日期': 1,
            '宝贝id': 1,
            '商家编码': 1,
            '行业类目': 1,
            '销售额': 1,
            '销售量': 1,
            '订单数': 1,
            '退货量': 1,
            '退款额': 1,
            '退款额（发货后）': 1,
            '退货量（发货后）': 1,
        }
        df = self.download.data_to_df(
            db_name='生意经2',
            table_name='宝贝指标',
            start_date=start_date,
            end_date=end_date,
            projection=projection,
        )
        return df

    def tg_rqbb(self):
        start_date, end_date = self.months_data(num=self.months)
        projection = {
            '日期': 1,
            '场景名字': 1,
            '主体id': 1,
            '花费': 1,
            '展现量': 1,
            '点击量': 1,
            '总购物车数': 1,
            '总成交笔数': 1,
            '总成交金额': 1,
            '直接成交笔数': 1,
            '直接成交金额': 1,
            '人群名字': 1,
        }
        df = self.download.data_to_df(
            db_name='推广数据2',
            table_name='人群报表',
            start_date=start_date,
            end_date=end_date,
            projection=projection,
        )
        return df

    def tg_gjc(self):
        start_date, end_date = self.months_data(num=self.months)
        projection = {
            '日期': 1,
            '场景名字': 1,
            '宝贝id': 1,
            '词类型': 1,
            '词名字/词包名字': 1,
            '花费': 1,
            '展现量': 1,
            '点击量': 1,
            '总购物车数': 1,
            '总成交笔数': 1,
            '总成交金额': 1,
            '直接成交笔数': 1,
            '直接成交金额': 1,
        }
        df = self.download.data_to_df(
            db_name='推广数据2',
            table_name='关键词报表',
            start_date=start_date,
            end_date=end_date,
            projection=projection,
        )
        return df

    def tg_cjzb(self):
        start_date, end_date = self.months_data(num=self.months)
        projection = {
            '日期': 1,
            '场景名字': 1,
            '人群名字': 1,
            '计划名字': 1,
            '花费': 1,
            '展现量': 1,
            '进店量': 1,
            '粉丝关注量': 1,
            '观看次数': 1,
            '总购物车数': 1,
            '总成交笔数': 1,
            '总成交金额': 1,
            '直接成交笔数': 1,
            '直接成交金额': 1,
        }
        df = self.download.data_to_df(
            db_name='推广数据2',
            table_name='超级直播',
            start_date=start_date,
            end_date=end_date,
            projection=projection,
        )
        return df

    def idbm(self):
        """ 用生意经日数据制作商品 id 和编码对照表 """
        data_values = self.download.columns_to_list(
            db_name='生意经2',
            table_name='宝贝指标',
            columns_name=['宝贝id', '商家编码', '行业类目'],
        )
        df = pd.DataFrame(data=data_values)
        return df

    def sp_picture(self):
        """ 用生意经日数据制作商品 id 和编码对照表 """
        data_values = self.download.columns_to_list(
            db_name='属性设置2',
            table_name='商品素材导出',
            columns_name=['日期', '商品id', '商品白底图', '方版场景图'],
        )
        df = pd.DataFrame(data=data_values)
        return df

    def dplyd(self):
        """ 新旧版取的字段是一样的 """
        start_date, end_date = self.months_data(num=self.months)
        projection = {
            '日期': 1,
            '一级来源': 1,
            '二级来源': 1,
            '三级来源': 1,
            '访客数': 1,
            '支付金额': 1,
            '支付买家数': 1,
            '支付转化率': 1,
            '加购人数': 1,
        }
        df = self.download.data_to_df(
            db_name='生意参谋2',
            table_name='店铺来源_日数据',
            start_date=start_date,
            end_date=end_date,
            projection=projection,
        )
        return df

    def dplyd_old(self):
        start_date, end_date = self.months_data(num=self.months)
        projection = {
            '日期': 1,
            '一级来源': 1,
            '二级来源': 1,
            '三级来源': 1,
            '访客数': 1,
            '支付金额': 1,
            '支付买家数': 1,
            '支付转化率': 1,
            '加购人数': 1,
        }
        df = self.download.data_to_df(
            db_name='生意参谋2',
            table_name='店铺来源_日数据_旧版',
            start_date=start_date,
            end_date=end_date,
            projection=projection,
        )
        return df

    def sp_cost(self):
        """ 电商定价 """
        data_values = self.download.columns_to_list(
            db_name='属性设置2',
            table_name='电商定价',
            columns_name=['日期', '款号', '年份季节', '吊牌价', '商家平台', '成本价', '天猫页面价', '天猫中促价'],
        )
        df = pd.DataFrame(data=data_values)
        return df

    def jdjzt(self):
        start_date, end_date = self.months_data(num=self.months)
        projection = {
            '日期': 1,
            '产品线': 1,
            '触发sku id': 1,
            '跟单sku id': 1,
            '花费': 1,
            '展现数': 1,
            '点击数': 1,
            '直接订单行': 1,
            '直接订单金额': 1,
            '总订单行': 1,
            '总订单金额': 1,
            '直接加购数': 1,
            '总加购数': 1,
            'spu id': 1,
        }
        df = self.download.data_to_df(
            db_name='京东数据2',
            table_name='推广数据_京准通',
            start_date=start_date,
            end_date=end_date,
            projection=projection,
        )
        return df
    def jdqzyx(self):
        start_date, end_date = self.months_data(num=self.months)
        projection = {
            '日期': 1,
            '产品线': 1,
            '花费': 1,
            '全站roi': 1,
            '全站交易额': 1,
            '全站订单行': 1,
            '全站订单成本': 1,
            '全站费比': 1,
            '核心位置展现量': 1,
            '核心位置点击量': 1,
        }
        df = self.download.data_to_df(
            db_name='京东数据2',
            table_name='推广数据_全站营销',
            start_date=start_date,
            end_date=end_date,
            projection=projection,
        )
        return df
    def sku_sales(self):
        start_date, end_date = self.months_data(num=self.months)
        projection = {
            '日期': 1,
            '商品id': 1,
            '货号': 1,
            '成交单量': 1,
            '成交金额': 1,
            '访客数': 1,
            '成交客户数': 1,
            '加购商品件数': 1,
            '加购人数': 1,
        }
        df = self.download.data_to_df(
            db_name='京东数据2',
            table_name='sku_商品明细',
            start_date=start_date,
            end_date=end_date,
            projection=projection,
        )
        return df

    @staticmethod
    def months_data(num=0, end_date=None):
        """ 读取近 num 个月的数据, 0 表示读取当月的数据 """
        if not end_date:
            end_date = datetime.datetime.now()
        start_date = end_date - relativedelta(months=num)  # n 月以前的今天
        start_date = f'{start_date.year}-{start_date.month}-01'  # 替换为 n 月以前的第一天
        return pd.to_datetime(start_date), pd.to_datetime(end_date)


class GroupBy:
    """
    数据聚合和导出
    """
    def __init__(self):
        # self.output: 数据库默认导出目录
        if platform.system() == 'Darwin':
            self.output = os.path.join('/Users', getpass.getuser(), '数据中心/数据库导出')
        elif platform.system() == 'Windows':
            self.output = os.path.join('C:\\同步空间\\BaiduSyncdisk\\数据库导出')
        else:
            self.output = os.path.join('数据中心/数据库导出')
        self.data_tgyj = {}  # 推广综合聚合数据表
        self.data_jdtg = {}  # 京东推广数据，聚合数据
        self.sp_index_datas = pd.DataFrame()  # 商品 id 索引表

    @staticmethod
    def try_except(func):  # 在类内部定义一个异常处理方法
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                print(f'{func.__name__}, {e}')  # 将异常信息返回

        return wrapper

    @try_except
    def groupby(self, df, table_name, is_maximize=True):
        """
        self.is_maximize: 是否最大转化数据
        table_name： 聚合数据库处的名称，不是原始数据库
        """
        if isinstance(df, pd.DataFrame):
            if len(df) == 0:
                print(f' query_data.groupby函数中 {table_name} 传入的 df 数据长度为0')
                return pd.DataFrame()
        else:
            print(f'query_data.groupby函数中 {table_name} 传入的 df 不是 dataframe 结构')
            return pd.DataFrame()
        # print(table_name)
        if '天猫_主体报表' in table_name:
            df.rename(columns={
                '场景名字': '营销场景',
                '主体id': '商品id',
                '总购物车数': '加购量',
                '总成交笔数': '成交笔数',
                '总成交金额': '成交金额'
            }, inplace=True)
            df.fillna(0, inplace=True)
            df = df.astype({
                '商品id': str,
                '花费': float,
                '展现量': int,
                '点击量': int,
                '加购量': int,
                '成交笔数': int,
                '成交金额': float,
                '自然流量曝光量': int,
                '直接成交笔数': int,
                '直接成交金额': float,
            }, errors='raise')
            if is_maximize:
                df = df.groupby(['日期', '营销场景', '商品id', '花费', '展现量', '点击量'], as_index=False).agg(
                    **{'加购量': ('加购量', np.max),
                       '成交笔数': ('成交笔数', np.max),
                       '成交金额': ('成交金额', np.max),
                       '自然流量曝光量': ('自然流量曝光量', np.max),
                       '直接成交笔数': ('直接成交笔数', np.max),
                       '直接成交金额': ('直接成交金额', np.max)
                       }
                )
            else:
                df = df.groupby(['日期', '营销场景', '商品id', '花费', '展现量', '点击量'], as_index=False).agg(
                    **{
                        '加购量': ('加购量', np.min),
                        '成交笔数': ('成交笔数', np.min),
                        '成交金额': ('成交金额', np.min),
                        '自然流量曝光量': ('自然流量曝光量', np.min),
                        '直接成交笔数': ('直接成交笔数', np.max),
                        '直接成交金额': ('直接成交金额', np.max)
                       }
                )
            df.insert(loc=1, column='推广渠道', value='万相台无界版')  # df中插入新列
            df_new = df.groupby(['日期', '商品id'], as_index=False).agg(
                    **{
                        '花费': ('花费', np.sum),
                        '成交笔数': ('成交笔数', np.max),
                        '成交金额': ('成交金额', np.max),
                        '自然流量曝光量': ('自然流量曝光量', np.max),
                        '直接成交笔数': ('直接成交笔数', np.max),
                        '直接成交金额': ('直接成交金额', np.max)
                       }
                )
            self.data_tgyj.update(
                {
                    table_name: df_new,
                }
            )
            self.data_tgyj.update(
                {
                    '天猫汇总表调用': df,
                }
            )
            # df_pic：商品排序索引表, 给 powerbi 中的主推款排序用的,(从上月1号到今天的总花费进行排序)
            today = datetime.date.today()
            last_month = today - datetime.timedelta(days=30)
            if last_month.month == 12:
                year_my = today.year - 1
            else:
                year_my = today.year
            # 截取 从上月1日 至 今天的花费数据, 推广款式按此数据从高到低排序（商品图+排序）
            df_pic = df.groupby(['日期', '商品id'], as_index=False).agg({'花费': 'sum'})
            df_pic = df_pic[~df_pic['商品id'].isin([''])]  # 指定列中删除包含空值的行
            df_pic = df_pic[(df_pic['日期'] >= f'{year_my}-{last_month.month}-01')]
            df_pic = df_pic.groupby(['商品id'], as_index=False).agg({'花费': 'sum'})
            df_pic.sort_values('花费', ascending=False, ignore_index=True, inplace=True)
            df_pic.reset_index(inplace=True)
            df_pic['index'] = df_pic['index'] + 100
            df_pic.rename(columns={'index': '商品索引'}, inplace=True)
            df_pic_new = pd.merge(df, df_pic, how='left', on=['商品id'])
            df_pic_new['商品索引'].fillna(1000, inplace=True)
            self.sp_index_datas = df_pic_new[['商品id', '商品索引']]
            return df
        elif '商品索引表' in table_name:
            return df
        elif '人群报表' in table_name:
            df.rename(columns={
                '场景名字': '营销场景',
                '主体id': '商品id',
                '总购物车数': '加购量',
                '总成交笔数': '成交笔数',
                '总成交金额': '成交金额'
            }, inplace=True)
            df.fillna(0, inplace=True)
            df = df.astype({
                '商品id': str,
                '花费': float,
                '展现量': int,
                '点击量': int,
                '加购量': int,
                '成交笔数': int,
                '成交金额': float,
                '直接成交笔数': int,
                '直接成交金额': float,
            }, errors='raise')
            if is_maximize:
                df = df.groupby(['日期', '营销场景', '商品id', '花费', '展现量', '点击量', '人群名字'], as_index=False).agg(
                    **{'加购量': ('加购量', np.max),
                       '成交笔数': ('成交笔数', np.max),
                       '成交金额': ('成交金额', np.max),
                       '直接成交笔数': ('直接成交笔数', np.max),
                       '直接成交金额': ('直接成交金额', np.max)
                       }
                )
            else:
                df = df.groupby(['日期', '营销场景', '商品id', '花费', '展现量', '点击量', '人群名字'], as_index=False).agg(
                    **{
                        '加购量': ('加购量', np.min),
                        '成交笔数': ('成交笔数', np.min),
                        '成交金额': ('成交金额', np.min),
                        '直接成交笔数': ('直接成交笔数', np.max),
                        '直接成交金额': ('直接成交金额', np.max)
                       }
                )
            df.insert(loc=1, column='推广渠道', value='万相台无界版')  # df中插入新列
            return df
        elif '关键词报表' in table_name:
            df.rename(columns={
                '场景名字': '营销场景',
                '宝贝id': '商品id',
                '总购物车数': '加购量',
                '总成交笔数': '成交笔数',
                '总成交金额': '成交金额'
            }, inplace=True)
            df.fillna(0, inplace=True)
            df = df.astype({
                '商品id': str,
                '花费': float,
                '展现量': int,
                '点击量': int,
                '加购量': int,
                '成交笔数': int,
                '成交金额': float,
                '直接成交笔数': int,
                '直接成交金额': float,
            }, errors='raise')
            if is_maximize:
                df = df.groupby(['日期', '营销场景', '商品id', '词类型', '词名字/词包名字', '花费', '展现量', '点击量'], as_index=False).agg(
                    **{'加购量': ('加购量', np.max),
                       '成交笔数': ('成交笔数', np.max),
                       '成交金额': ('成交金额', np.max),
                       '直接成交笔数': ('直接成交笔数', np.max),
                       '直接成交金额': ('直接成交金额', np.max)
                       }
                )
            else:
                df = df.groupby(['日期', '营销场景', '商品id', '词类型', '词名字/词包名字', '花费', '展现量', '点击量'], as_index=False).agg(
                    **{
                        '加购量': ('加购量', np.min),
                        '成交笔数': ('成交笔数', np.min),
                        '成交金额': ('成交金额', np.min),
                        '直接成交笔数': ('直接成交笔数', np.max),
                        '直接成交金额': ('直接成交金额', np.max)
                       }
                )
            df.insert(loc=1, column='推广渠道', value='万相台无界版')  # df中插入新列
            return df
        elif '天猫_超级直播' in table_name:
            df.rename(columns={
                '观看次数': '观看次数',
                '总购物车数': '加购量',
                '总成交笔数': '成交笔数',
                '总成交金额': '成交金额',
                '场景名字': '营销场景',
            }, inplace=True)
            df.fillna(0, inplace=True)
            df = df.astype({
                '花费': float,
                # '点击量': int,
                '加购量': int,
                '成交笔数': int,
                '成交金额': float,
                '进店量': int,
                '粉丝关注量': int,
                '观看次数': int,
            }, errors='raise')
            if is_maximize:
                df = df.groupby(['日期', '营销场景', '人群名字', '计划名字', '花费', '观看次数', '展现量'],
                                as_index=False).agg(
                    **{
                        '进店量': ('进店量', np.max),
                        '粉丝关注量': ('粉丝关注量', np.max),
                        '加购量': ('加购量', np.max),
                        '成交笔数': ('成交笔数', np.max),
                        '成交金额': ('成交金额', np.max),
                        '直接成交笔数': ('直接成交笔数', np.max),
                        '直接成交金额': ('直接成交金额', np.max),
                       }
                )
            else:
                df = df.groupby(['日期', '营销场景', '人群名字', '计划名字', '花费', '观看次数', '展现量'],
                                as_index=False).agg(
                    **{
                        '进店量': ('进店量', np.min),
                        '粉丝关注量': ('粉丝关注量', np.min),
                        '加购量': ('加购量', np.min),
                        '成交笔数': ('成交笔数', np.min),
                        '成交金额': ('成交金额', np.min),
                        '直接成交笔数': ('直接成交笔数', np.min),
                        '直接成交金额': ('直接成交金额', np.min),
                    }
                )
            df.insert(loc=1, column='推广渠道', value='万相台无界版')  # df中插入新列
            # df.insert(loc=2, column='营销场景', value='超级直播')  # df中插入新列
            # df = df.loc[df['日期'].between(start_day, today)]
            df_new = df.groupby(['日期', '推广渠道', '营销场景'], as_index=False).agg(
                **{
                    '花费': ('花费', np.sum),
                    '展现量': ('展现量', np.sum),
                    '观看次数': ('观看次数', np.sum),
                    '加购量': ('加购量', np.sum),
                    '成交笔数': ('成交笔数', np.sum),
                    '成交金额': ('成交金额', np.sum),
                    '直接成交笔数': ('直接成交笔数', np.sum),
                    '直接成交金额': ('直接成交金额', np.sum),
                }
            )
            self.data_tgyj.update(
                {
                    table_name: df_new,
                }
            )
            return df
        elif '宝贝指标' in table_name:
            """ 聚合时不可以加商家编码，编码有些是空白，有些是 0 """
            df['宝贝id'] = df['宝贝id'].astype(str)
            df.fillna(0, inplace=True)
            # df = df[(df['销售额'] != 0) | (df['退款额'] != 0)]  # 注释掉, 因为后续使用生意经作为基准合并推广表，需确保所有商品id 齐全
            df = df.groupby(['日期', '宝贝id', '行业类目'], as_index=False).agg(
                **{'销售额': ('销售额', np.min),
                   '销售量': ('销售量', np.min),
                   '订单数': ('订单数', np.min),
                   '退货量': ('退货量', np.max),
                   '退款额': ('退款额', np.max),
                   '退款额（发货后）': ('退款额（发货后）', np.max),
                   '退货量（发货后）': ('退货量（发货后）', np.max),
                   }
            )
            df['件均价'] = df.apply(lambda x: x['销售额'] / x['销售量'] if x['销售量'] > 0 else 0, axis=1).round(
                0)  # 两列运算, 避免除以0
            df['价格带'] = df['件均价'].apply(
                lambda x: '2000+' if x >= 2000
                else '1000+' if x >= 1000
                else '500+' if x >= 500
                else '300+' if x >= 300
                else '300以下'
            )
            self.data_tgyj.update(
                {
                    table_name: df[['日期', '宝贝id', '销售额', '销售量', '退款额（发货后）', '退货量（发货后）']],
                }
            )
            return df
        elif '店铺来源_日数据' in table_name and '旧版' not in table_name:
            # 包含三级来源名称和预设索引值列
            # 截取 从上月1日 至 今天的花费数据, 推广款式按此数据从高到低排序（商品图+排序）
            df_visitor3 = df.groupby(['日期', '三级来源'], as_index=False).agg({'访客数': 'sum'})
            df_visitor3 = df_visitor3[~df_visitor3['三级来源'].isin([''])]  # 指定列中删除包含空值的行
            # df_visitor = df_visitor[(df_visitor['日期'] >= f'{year_my}-{last_month.month}-01')]
            df_visitor3 = df_visitor3.groupby(['三级来源'], as_index=False).agg({'访客数': 'sum'})
            df_visitor3.sort_values('访客数', ascending=False, ignore_index=True, inplace=True)
            df_visitor3.reset_index(inplace=True)
            df_visitor3['index'] = df_visitor3['index'] + 100
            df_visitor3.rename(columns={'index': '三级访客索引'}, inplace=True)
            df_visitor3 = df_visitor3[['三级来源', '三级访客索引']]

            # 包含二级来源名称和预设索引值列
            df_visitor2 = df.groupby(['日期', '二级来源'], as_index=False).agg({'访客数': 'sum'})
            df_visitor2 = df_visitor2[~df_visitor2['二级来源'].isin([''])]  # 指定列中删除包含空值的行
            # df_visitor2 = df_visitor2[(df_visitor2['日期'] >= f'{year_my}-{last_month.month}-01')]
            df_visitor2 = df_visitor2.groupby(['二级来源'], as_index=False).agg({'访客数': 'sum'})
            df_visitor2.sort_values('访客数', ascending=False, ignore_index=True, inplace=True)
            df_visitor2.reset_index(inplace=True)
            df_visitor2['index'] = df_visitor2['index'] + 100
            df_visitor2.rename(columns={'index': '二级访客索引'}, inplace=True)
            df_visitor2 = df_visitor2[['二级来源', '二级访客索引']]

            df = pd.merge(df, df_visitor2, how='left', left_on='二级来源', right_on='二级来源')
            df = pd.merge(df, df_visitor3, how='left', left_on='三级来源', right_on='三级来源')
            return df
        elif '天猫_店铺来源_日数据_旧版' in table_name:

            # 包含三级来源名称和预设索引值列
            # 截取 从上月1日 至 今天的花费数据, 推广款式按此数据从高到低排序（商品图+排序）
            df_visitor3 = df.groupby(['日期', '三级来源'], as_index=False).agg({'访客数': 'sum'})
            df_visitor3 = df_visitor3[~df_visitor3['三级来源'].isin([''])]  # 指定列中删除包含空值的行
            # df_visitor = df_visitor[(df_visitor['日期'] >= f'{year_my}-{last_month.month}-01')]
            df_visitor3 = df_visitor3.groupby(['三级来源'], as_index=False).agg({'访客数': 'sum'})
            df_visitor3.sort_values('访客数', ascending=False, ignore_index=True, inplace=True)
            df_visitor3.reset_index(inplace=True)
            df_visitor3['index'] = df_visitor3['index'] + 100
            df_visitor3.rename(columns={'index': '三级访客索引'}, inplace=True)
            df_visitor3 = df_visitor3[['三级来源', '三级访客索引']]

            # 包含二级来源名称和预设索引值列
            df_visitor2 = df.groupby(['日期', '二级来源'], as_index=False).agg({'访客数': 'sum'})
            df_visitor2 = df_visitor2[~df_visitor2['二级来源'].isin([''])]  # 指定列中删除包含空值的行
            # df_visitor2 = df_visitor2[(df_visitor2['日期'] >= f'{year_my}-{last_month.month}-01')]
            df_visitor2 = df_visitor2.groupby(['二级来源'], as_index=False).agg({'访客数': 'sum'})
            df_visitor2.sort_values('访客数', ascending=False, ignore_index=True, inplace=True)
            df_visitor2.reset_index(inplace=True)
            df_visitor2['index'] = df_visitor2['index'] + 100
            df_visitor2.rename(columns={'index': '二级访客索引'}, inplace=True)
            df_visitor2 = df_visitor2[['二级来源', '二级访客索引']]

            df = pd.merge(df, df_visitor2, how='left', left_on='二级来源', right_on='二级来源')
            df = pd.merge(df, df_visitor3, how='left', left_on='三级来源', right_on='三级来源')
            return df
        elif '商品id编码表' in table_name:
            df['宝贝id'] = df['宝贝id'].astype(str)
            df.drop_duplicates(subset='宝贝id', keep='last', inplace=True, ignore_index=True)
            # df['行业类目'] = df['行业类目'].apply(lambda x: re.sub(' ', '', x))
            try:
                df[['一级类目', '二级类目', '三级类目']] = df['行业类目'].str.split(' -> ', expand=True).loc[:, 0:2]
            except:
                try:
                    df[['一级类目', '二级类目']] = df['行业类目'].str.split(' -> ', expand=True).loc[:, 0:1]
                except:
                    df['一级类目'] = df['行业类目']
            df.drop('行业类目', axis=1, inplace=True)
            df.sort_values('宝贝id', ascending=False, inplace=True)
            df = df[(df['宝贝id'] != '973') & (df['宝贝id'] != '973')]
            self.data_tgyj.update(
                {
                    table_name: df[['宝贝id', '商家编码']],
                }
            )
            return df
        elif '商品id图片对照表' in table_name:
            df['商品id'] = df['商品id'].astype('int64')
            df['日期'] = df['日期'].astype('datetime64[ns]')
            df = df[(df['商品白底图'] != '0') | (df['方版场景图'] != '0')]
            # 白底图优先
            df['商品图片'] = df[['商品白底图', '方版场景图']].apply(
                lambda x: x['商品白底图'] if x['商品白底图'] !='0' else x['方版场景图'], axis=1)
            # # 方版场景图优先
            # df['商品图片'] = df[['商品白底图', '方版场景图']].apply(
            #     lambda x: x['方版场景图'] if x['方版场景图'] != '0' else x['商品白底图'], axis=1)
            df.sort_values(by=['商品id', '日期'], ascending=[False, True], ignore_index=True, inplace=True)
            df.drop_duplicates(subset=['商品id'], keep='last', inplace=True, ignore_index=True)
            df = df[['商品id', '商品图片', '日期']]
            df['商品图片'] = df['商品图片'].apply(lambda x: x if 'http' in x else None)  # 检查是否是 http 链接
            df.dropna(how='all', subset=['商品图片'], axis=0, inplace=True)  # 删除指定列含有空值的行
            df['商品链接'] = df['商品id'].apply(
                lambda x: f'https://detail.tmall.com/item.htm?id={str(x)}' if x and '.com' not in str(x) else x)
            df.sort_values(by='商品id', ascending=False, ignore_index=True, inplace=True)  # ascending=False 降序排列
            self.data_tgyj.update(
                {
                    table_name: df[['商品id', '商品图片']],
                }
            )
            df['商品id'] = df['商品id'].astype(str)
            return df
        elif '商品成本' in table_name:
            df.sort_values(by=['款号', '日期'], ascending=[False, True], ignore_index=True, inplace=True)
            df.drop_duplicates(subset=['款号'], keep='last', inplace=True, ignore_index=True)
            self.data_tgyj.update(
                {
                    table_name: df[['款号', '成本价']],
                }
            )
            return df
        elif '京东_京准通' in table_name and '全站营销' not in table_name:
            df = df.groupby(['日期', '产品线', '触发sku id', '跟单sku id', 'spu id', '花费', '展现数', '点击数'], as_index=False).agg(
                **{'直接订单行': ('直接订单行', np.max),
                   '直接订单金额': ('直接订单金额', np.max),
                   '总订单行': ('总订单行', np.max),
                   '总订单金额': ('总订单金额', np.max),
                   '直接加购数': ('直接加购数', np.max),
                   '总加购数': ('总加购数', np.max),
                   }
            )
            df = df[df['花费'] > 0]
            self.data_jdtg.update(
                {
                    table_name: df[['日期', '产品线', '触发sku id', '跟单sku id', '花费']],
                }
            )
            return df
        elif '京东_京准通_全站营销' in table_name:
            df = df.groupby(['日期', '产品线', '花费'], as_index=False).agg(
                **{'全站roi': ('全站roi', np.max),
                   '全站交易额': ('全站交易额', np.max),
                   '全站订单行': ('全站订单行', np.max),
                   '全站订单成本': ('全站订单成本', np.max),
                   '全站费比': ('全站费比', np.max),
                   '核心位置展现量': ('核心位置展现量', np.max),
                   '核心位置点击量': ('核心位置点击量', np.max),
                   }
            )
            df = df[df['花费'] > 0]
            return df
        elif '京东_sku_商品明细' in table_name:
            df = df[df['商品id'] != '合计']
            df = df.groupby(['日期', '商品id', '货号', '访客数', '成交客户数', '加购商品件数', '加购人数'],
                            as_index=False).agg(
                **{
                    '成交单量': ('成交单量', np.max),
                    '成交金额': ('成交金额', np.max),
                   }
            )
            self.data_jdtg.update(
                {
                    table_name: df,
                }
            )
            return df
        else:
            print(f'<{table_name}>: Groupby 类尚未配置，数据为空')
            return pd.DataFrame({})

    # @try_except
    def performance(self, bb_tg=True):
         # print(self.data_tgyj)
        tg, syj, idbm, pic, cost = (
            self.data_tgyj['天猫_主体报表'],
            self.data_tgyj['天猫生意经_宝贝指标'],
            self.data_tgyj['商品id编码表'],
            self.data_tgyj['商品id图片对照表'],
            self.data_tgyj['商品成本'])  # 这里不要加逗号
        pic['商品id'] = pic['商品id'].astype(str)
        df = pd.merge(idbm, pic, how='left', left_on='宝贝id', right_on='商品id')  # id 编码表合并图片表
        df = df[['宝贝id', '商家编码', '商品图片']]
        df = pd.merge(df, cost, how='left', left_on='商家编码', right_on='款号')  # df 合并商品成本表
        df = df[['宝贝id', '商家编码', '商品图片', '成本价']]
        df = pd.merge(tg, df, how='left', left_on='商品id', right_on='宝贝id')  # 推广表合并 df
        df.drop(labels='宝贝id', axis=1, inplace=True)
        if bb_tg is True:
            # 生意经合并推广表，完整的数据表，包含全店所有推广、销售数据
            df = pd.merge(syj, df, how='left', left_on=['日期', '宝贝id'], right_on=['日期', '商品id'])
            df.drop(labels='商品id', axis=1, inplace=True)  # 因为生意经中的宝贝 id 列才是完整的
            df.rename(columns={'宝贝id': '商品id'}, inplace=True)
            # df.to_csv('/Users/xigua/Downloads/test.csv', encoding='utf-8_sig', index=False, header=True)
        else:
            # 推广表合并生意经 , 以推广数据为基准，销售数据不齐全
            df = pd.merge(df, syj, how='left', left_on=['日期', '商品id'], right_on=['日期', '宝贝id'])
            df.drop(labels='宝贝id', axis=1, inplace=True)
        df.drop_duplicates(subset=['日期', '商品id', '花费', '销售额'], keep='last', inplace=True, ignore_index=True)
        df.fillna(0, inplace=True)
        df['成本价'] = df['成本价'].astype('float64')
        df['销售额'] = df['销售额'].astype('float64')
        df['销售量'] = df['销售量'].astype('int64')
        df['商品成本'] = df.apply(lambda x: (x['成本价'] + x['销售额']/x['销售量'] * 0.11 + 6) * x['销售量'] if x['销售量'] > 0 else 0, axis=1)
        df['商品毛利'] = df.apply(lambda x: x['销售额'] - x['商品成本'], axis=1)
        df['毛利率'] = df.apply(lambda x: round((x['销售额'] - x['商品成本']) / x['销售额'], 4) if x['销售额'] > 0 else 0, axis=1)
        df['盈亏'] = df.apply(lambda x: x['商品毛利'] - x['花费'], axis=1)
        return df

    def performance_concat(self, bb_tg=True):
        tg,  zb = self.data_tgyj['天猫汇总表调用'], self.data_tgyj['天猫_超级直播']
        zb.rename(columns={
            '观看次数': '点击量',
        }, inplace=True)
        zb.fillna(0, inplace=True)  # astype 之前要填充空值
        tg.fillna(0, inplace=True)
        zb = zb.astype({
            '花费': float,
            '展现量': int,
            '点击量': int,
            '加购量': int,
            '成交笔数': int,
            '成交金额': float,
            '直接成交笔数': int,
            '直接成交金额': float,
        }, errors='raise')
        tg = tg.astype({
            '商品id': str,
            '花费': float,
            '展现量': int,
            '点击量': int,
            '加购量': int,
            '成交笔数': int,
            '成交金额': float,
            '直接成交笔数': int,
            '直接成交金额': float,
            '自然流量曝光量': int,
        }, errors='raise')
        df = pd.concat([tg, zb], axis=0, ignore_index=True)
        df.fillna(0, inplace=True)  # concat 之后要填充空值
        df = df.astype(
            {
                '自然流量曝光量': int,
        }
        )
        return df

    def performance_jd(self, jd_tg=True):
        jdtg, sku_sales = self.data_jdtg['京东_京准通'], self.data_jdtg['京东_sku_商品明细']
        jdtg = jdtg.groupby(['日期', '跟单sku id'],
                        as_index=False).agg(
            **{
                '花费': ('花费', np.sum)
            }
        )
        cost = self.data_tgyj['商品成本']
        df = pd.merge(sku_sales, cost, how='left', left_on='货号', right_on='款号')
        df = df[['日期', '商品id', '货号', '成交单量', '成交金额', '成本价']]
        df['商品id'] = df['商品id'].astype(str)
        jdtg['跟单sku id'] = jdtg['跟单sku id'].astype(str)
        if jd_tg is True:
            # 完整的数据表，包含全店所有推广、销售数据
            df = pd.merge(df, jdtg, how='left', left_on=['日期', '商品id'], right_on=['日期', '跟单sku id'])  # df 合并推广表
        else:
            df = pd.merge(jdtg, df, how='left', left_on=['日期', '跟单sku id'], right_on=['日期', '商品id'])  # 推广表合并 df
        df = df[['日期', '跟单sku id', '花费', '货号', '成交单量', '成交金额', '成本价']]
        df.fillna(0, inplace=True)
        df['成本价'] = df['成本价'].astype('float64')
        df['成交金额'] = df['成交金额'].astype('float64')
        df['花费'] = df['花费'].astype('float64')
        df['成交单量'] = df['成交单量'].astype('int64')
        df['商品成本'] = df.apply(
            lambda x: (x['成本价'] + x['成交金额'] / x['成交单量'] * 0.11 + 6) * x['成交单量'] if x['成交单量'] > 0 else 0,
            axis=1)
        df['商品毛利'] = df.apply(lambda x: x['成交金额'] - x['商品成本'], axis=1)
        df['毛利率'] = df.apply(
            lambda x: round((x['成交金额'] - x['商品成本']) / x['成交金额'], 4) if x['成交金额'] > 0 else 0, axis=1)
        df['盈亏'] = df.apply(lambda x: x['商品毛利'] - x['花费'], axis=1)
        return df

    def as_csv(self, df, filename, path=None, encoding='utf-8_sig',
               index=False, header=True, st_ascend=None, ascend=None, freq=None):
        """
        path: 默认导出目录 self.output, 这个函数的 path 作为子文件夹，可以不传，
        st_ascend: 排序参数 ['column1', 'column2']
        ascend: 升降序 [True, False]
        freq: 将创建子文件夹并按月分类存储,  freq='Y', 或 freq='M'
        """
        if len(df) == 0:
            return
        if not path:
            path = self.output
        else:
            path = os.path.join(self.output, path)
        if not os.path.exists(path):
            os.makedirs(path)
        if filename.endswith('.csv'):
            filename = filename[:-4]
        if st_ascend and ascend:
            try:
                df.sort_values(st_ascend, ascending=ascend, ignore_index=True, inplace=True)
            except:
                print(f'{filename}: sort_values排序参数错误！')
        if freq:
            if '日期' not in df.columns.tolist():
                return print(f'{filename}: 数据缺少日期列，无法按日期分组')
            groups = df.groupby(pd.Grouper(key='日期', freq=freq))
            for name1, df in groups:
                if freq == 'M':
                    sheet_name = name1.strftime('%Y-%m')
                elif freq == 'Y':
                    sheet_name = name1.strftime('%Y年')
                else:
                    sheet_name = '_未分类'
                new_path = os.path.join(path, filename)
                if not os.path.exists(new_path):
                    os.makedirs(new_path)
                new_path = os.path.join(new_path, f'{filename}{sheet_name}.csv')
                if st_ascend and ascend:  # 这里需要重新排序一次，原因未知
                    try:
                        df.sort_values(st_ascend, ascending=ascend, ignore_index=True, inplace=True)
                    except:
                        print(f'{filename}: sort_values排序参数错误！')

                df.to_csv(new_path, encoding=encoding, index=index, header=header)
        else:
            df.to_csv(os.path.join(path, filename + '.csv'), encoding=encoding, index=index, header=header)

    def as_json(self, df, filename, path=None, orient='records', force_ascii=False, st_ascend=None, ascend=None):
        if len(df) == 0:
            return
        if not path:
            path = self.output
        else:
            path = os.path.join(self.output, path)
        if not os.path.exists(path):
            os.makedirs(path)
        if st_ascend and ascend:
            try:
                df.sort_values(st_ascend, ascending=ascend, ignore_index=True, inplace=True)
            except:
                print(f'{filename}: sort_values排序参数错误！')
        df.to_json(os.path.join(path, filename + '.json'),
                   orient=orient, force_ascii=force_ascii)

    def as_excel(self, df, filename, path=None, index=False, header=True, engine='openpyxl',
                 freeze_panes=(1, 0), st_ascend=None, ascend=None):
        if len(df) == 0:
            return
        if not path:
            path = self.output
        else:
            path = os.path.join(self.output, path)
        if not os.path.exists(path):
            os.makedirs(path)
        if st_ascend and ascend:
            try:
                df.sort_values(st_ascend, ascending=ascend, ignore_index=True, inplace=True)
            except:
                print(f'{filename}: sort_values排序参数错误！')
        df.to_excel(os.path.join(path, filename + '.xlsx'), index=index, header=header, engine=engine, freeze_panes=freeze_panes)
        

def g_group():
    pass


def data_aggregation_one(service_databases=[{}], months=1):
    """
    # 单独处理某一个聚合数据库，修改添加 data_dict 的值
    """
    for service_database in service_databases:
        for service_name, database in service_database.items():
            sdq = MysqlDatasQuery(target_service=service_name)  # 实例化数据处理类
            sdq.months = months  # 设置数据周期， 1 表示近 2 个月
            g = GroupBy()  # 实例化数据聚合类
            # 实例化数据库连接
            username, password, host, port = get_myconf.select_config_values(target_service=service_name, database=database)
            m = mysql.MysqlUpload(username=username, password=password, host=host, port=port)

            # 从数据库中获取数据, 返回包含 df 数据的字典
            # 单独处理某一个聚合数据库，在这里修改添加 data_dict 的值
            ######################################################
            #################    修改这里    ##########################
            ######################################################
            data_dict = [
                {
                    '数据库名': '聚合数据',
                    '集合名': '天猫_超级直播',
                    '唯一主键': ['日期', '推广渠道', '营销场景', '花费'],
                    '数据主体': sdq.tg_cjzb(),
                },
            ]
            ######################################################
            #################    修改这里    ##########################
            ######################################################

            for items in data_dict:  # 遍历返回结果
                db_name, table_name, unique_key_list, df = items['数据库名'], items['集合名'], items['唯一主键'], items['数据主体']
                df = g.groupby(df=df, table_name=table_name, is_maximize=True)  # 2. 聚合数据
                # g.as_csv(df=df, filename=table_name + '.csv')  # 导出 csv
                m.df_to_mysql(
                    df=df,
                    db_name=db_name,
                    table_name=table_name,
                    drop_duplicates=False,
                    icm_update=unique_key_list,
                    service_database=service_database,
                )  # 3. 回传数据库


def data_aggregation(service_databases=[{}], months=1):
    """
    1. 从数据库中读取数据
    2. 数据聚合清洗
    3. 统一回传数据库: <聚合数据>  （不再导出为文件）
    公司台式机调用
    """
    for service_database in service_databases:
        for service_name, database in service_database.items():
            sdq = MysqlDatasQuery(target_service=service_name)  # 实例化数据处理类
            sdq.months = months  # 设置数据周期， 1 表示近 2 个月
            g = GroupBy()  # 实例化数据聚合类
            # 实例化数据库连接
            username, password, host, port = get_myconf.select_config_values(target_service=service_name, database=database)
            m = mysql.MysqlUpload(username=username, password=password, host=host, port=port)

            # 从数据库中获取数据, 返回包含 df 数据的字典
            data_dict = [
                {
                    '数据库名': '聚合数据',
                    '集合名': '天猫_主体报表',
                    '唯一主键': ['日期', '推广渠道', '营销场景', '商品id', '花费'],
                    '数据主体': sdq.tg_wxt(),
                },
                # {
                #     '数据库名': '聚合数据',
                #     '集合名': '天猫生意经_宝贝指标',
                #     '唯一主键': ['日期', '宝贝id'],
                #     '数据主体': sdq.syj(),
                # },
                # {
                #     '数据库名': '聚合数据',
                #     '集合名': '天猫_店铺来源_日数据',
                #     '唯一主键': ['日期', '一级来源', '二级来源', '三级来源'],
                #     '数据主体': sdq.dplyd(),
                # },
                # {
                #     '数据库名': '聚合数据',
                #     '集合名': '天猫_店铺来源_日数据_旧版',
                #     '唯一主键': ['日期', '一级来源', '二级来源', '三级来源'],
                #     '数据主体': sdq.dplyd_old(),
                # },
                # {
                #     '数据库名': '聚合数据',
                #     '集合名': '商品id编码表',
                #     '唯一主键': ['宝贝id'],
                #     '数据主体': sdq.idbm(),
                # },
                # {
                #     '数据库名': '聚合数据',
                #     '集合名': '商品id图片对照表',
                #     '唯一主键': ['商品id'],
                #     '数据主体': sdq.sp_picture(),
                # },
                # {
                #     '数据库名': '聚合数据',
                #     '集合名': '商品成本',
                #     '唯一主键': ['款号'],
                #     '数据主体': sdq.sp_cost(),
                # },
                # {
                #     '数据库名': '聚合数据',
                #     '集合名': '京东_京准通',
                #     '唯一主键': ['日期', '产品线', '触发sku id', '跟单sku id', '花费', ],
                #     '数据主体': sdq.jdjzt(),
                # },
                # {
                #     '数据库名': '聚合数据',
                #     '集合名': '京东_京准通_全站营销',
                #     '唯一主键': ['日期', '产品线', '花费'],
                #     '数据主体': sdq.jdqzyx(),
                # },
                # {
                #     '数据库名': '聚合数据',
                #     '集合名': '京东_sku_商品明细',
                #     '唯一主键': ['日期', '商品id', '成交单量'],
                #     '数据主体': sdq.sku_sales(),
                # },
                # {
                #     '数据库名': '聚合数据',
                #     '集合名': '天猫_人群报表',
                #     '唯一主键': ['日期', '推广渠道', '营销场景', '商品id', '花费', '人群名字'],
                #     '数据主体': sdq.tg_rqbb(),
                # },
                # {
                #     '数据库名': '聚合数据',
                #     '集合名': '天猫_关键词报表',
                #     '唯一主键': ['日期', '推广渠道', '营销场景', '商品id', '花费', '词类型', '词名字/词包名字',],
                #     '数据主体': sdq.tg_gjc(),
                # },
                {
                    '数据库名': '聚合数据',
                    '集合名': '天猫_超级直播',
                    '唯一主键': ['日期', '推广渠道', '营销场景', '花费'],
                    '数据主体': sdq.tg_cjzb(),
                },
            ]
            for items in data_dict:  # 遍历返回结果
                db_name, table_name, unique_key_list, df = items['数据库名'], items['集合名'], items['唯一主键'], items['数据主体']
                df = g.groupby(df=df, table_name=table_name, is_maximize=True)  # 2. 聚合数据
                if len(g.sp_index_datas) != 0:
                    # # 由推广主体报表，写入一个商品索引表，索引规则：从上月 1 号至今花费从高到低排序
                    # m.df_to_mysql(
                    #     df=g.sp_index_datas,
                    #     db_name='属性设置2',
                    #     table_name='商品索引表',
                    #     drop_duplicates=False,
                    #     icm_update=['商品id'],
                    #     service_database=service_database,
                    # )
                    g.sp_index_datas = pd.DataFrame()  # 重置，不然下个循环会继续刷入数据库
                # g.as_csv(df=df, filename=table_name + '.csv')  # 导出 csv
                m.df_to_mysql(
                    df=df,
                    db_name=db_name,
                    table_name=table_name,
                    drop_duplicates=False,
                    icm_update=unique_key_list,
                    service_database=service_database,
                )  # 3. 回传数据库
            # res = g.performance(bb_tg=True)   # 盈亏表，依赖其他表，单独做
            # m.df_to_mysql(
            #     df=res,
            #     db_name='聚合数据',
            #     table_name='_全店商品销售',
            #     drop_duplicates=False,
            #     icm_update=['日期', '商品id'],  # 设置唯一主键
            #     service_database=service_database,
            # )
            # res = g.performance(bb_tg=False)  # 盈亏表，依赖其他表，单独做
            # m.df_to_mysql(
            #     df=res,
            #     db_name='聚合数据',
            #     table_name='_推广商品销售',
            #     drop_duplicates=False,
            #     icm_update=['日期', '商品id'],  # 设置唯一主键
            #     service_database=service_database,
            # )

            res = g.performance_concat(bb_tg=False)  # 推广主体合并直播表，依赖其他表，单独做
            m.df_to_mysql(
                df=res,
                db_name='聚合数据',
                table_name='天猫_推广汇总',
                drop_duplicates=False,
                icm_update=['日期', '商品id'],  # 设置唯一主键
                service_database=service_database,
            )


            # res = g.performance_jd(jd_tg=False)  # 盈亏表，依赖其他表，单独做
            # m.df_to_mysql(
            #     df=res,
            #     db_name='聚合数据',
            #     table_name='_京东_推广商品销售',
            #     drop_duplicates=False,
            #     icm_update=['日期', '跟单sku id', '货号', '花费'],  # 设置唯一主键
            #     service_database=service_database,
            # )


    # 这里要注释掉，不然 copysh.py 可能有问题，这里主要修改配置文件，后续触发 home_lx 的 optimize_datas.py(有s)程序进行全局清理
    # optimize_data.op_data(service_databases=service_databases, days=3650)  # 立即启动对聚合数据的清理工作


def main():
    pass


if __name__ == '__main__':
    data_aggregation(service_databases=[{'company': 'mysql'}], months=24)  # 正常的聚合所有数据
    # data_aggregation_one(service_databases=[{'company': 'mysql'}], months=1)  # 单独聚合某一个数据库，具体库进函数编辑
    # optimize_data.op_data(service_databases=[{'company': 'mysql'}], days=3650)  # 立即启动对聚合数据的清理工作

