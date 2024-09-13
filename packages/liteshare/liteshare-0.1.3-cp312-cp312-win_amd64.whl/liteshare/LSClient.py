import os
import pickle
import time

import pandas as pd
import redis
from tqdm import tqdm

from ParquetManager import ParquetDataManager

def timing_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} Running: {end_time - start_time:.3f} Seconds")
        return result
    return wrapper

class LiteShareClient:
    def __init__(self, account, api_token, save_path):
        """
        Initializes a new instance of the StockDataDownloader with API token authentication.

        Args:
        api_token (str): The API token for authentication.
        server_url (str): The base URL for the stock data API server.
        """
        self.account = account
        self.api_token = api_token
        self.auth(account, api_token)

        if os.path.exists(save_path) == False:
            os.makedirs(save_path)
            print(f"Creating Saving Dir: {save_path}")
        else:
            print(f"Found Saving Dir: {save_path}")
        self.save_path = save_path
        self.LS_db = ParquetDataManager(save_path)

    @staticmethod
    def get_auth_ping(host, account, api_token):
        try:
            temp_r = redis.Redis(host=host,
                                 port=6379,
                                 password=f'{account}:{api_token}')
            temp_ping = LiteShareClient.measure_latency(temp_r)
            return temp_ping
        except Exception as e:
            return 999

    @staticmethod
    def measure_latency(r):
        start_time = time.time()
        r.ping()
        latency_ms = (time.time() - start_time) * 1000  # 将秒转换为毫秒
        return round(latency_ms, 2)

    def get_host_info(self):
        host_dict = {
            "上海-1": "r-uf65ptpkck2xg94dm2pd.tairpena.rds.aliyuncs.com",
        }
        return host_dict

    def auth(self, account, api_token):
        host_dict = self.get_host_info()
        ping_dict = {k: LiteShareClient.get_auth_ping(host_dict[k], account, api_token) for k in host_dict}
        min_key = min(ping_dict, key=ping_dict.get)
        print(f"LiteShare {min_key} | Ping: {ping_dict[min_key]}ms")
        try:
            self.r = redis.Redis(host=host_dict[min_key],
                                 port=6379,
                                 password=f'{account}:{api_token}')
            if self.r.ping():
                print(f"Auth Succeeded: {account}")
                self.keys = [x.decode("utf-8") for x in self.r.keys()]
                self.r_category = sorted(list(set(
                    (s.split("-")[1] for s in self.keys)
                )))
        except Exception as e:
            raise e

    def load_df_from_lsdb(self, key):
        data_ = self.r.get(key)
        df = pickle.loads(data_)
        return df

    def UpdateUnstackParquet(self, category):
        unstack_df = self.load_df_from_lsdb(f"ls1-{category}")
        self.LS_db.update_unstack_category(category=category, sub_df=unstack_df,
                                           key_columns=['order_book_id', 'start_date', 'end_date'])
        return

    def UpdatePivotParquet(self, category, start_date: str, end_date: str, strf="%Y-%m-%d"):
        ms = pd.date_range(start=start_date, end=end_date, freq='MS').strftime("%Y%m").tolist()

        target_columns = [f"ls1-{category}-{x}" for x in ms if f"ls1-{category}-{x}" in self.keys]
        if len(target_columns) > 0:
            df = pd.concat([self.load_df_from_lsdb(column) for column in tqdm(target_columns)], axis=1)
            self.LS_db.update_pivot_category(df=df, category=category, strf=strf)
        else:
            df = self.GetPivotCategory(category, None, None)
            print(f"{category} are Latest Date: {df.columns[-1]}")

    def GetUnstackCategory(self, category):
        return self.LS_db.read_unstack_category(category)

    def GetPivotCategory(self, category, start_date, end_date):
        return self.LS_db.read_pivot_category(category, start_date, end_date)



