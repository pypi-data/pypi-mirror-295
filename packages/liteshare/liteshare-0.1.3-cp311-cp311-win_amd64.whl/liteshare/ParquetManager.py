import os

from concurrent.futures import ThreadPoolExecutor, as_completed

import pandas as pd
from tqdm import tqdm
import re

class ParquetDataManager:
    def __init__(self, root_dir, max_workers = 10):
        """Initialize with the root directory to store all parquet files."""
        self.root_dir = root_dir
        self.max_workers = max_workers
        if not os.path.exists(self.root_dir):
            os.makedirs(self.root_dir)



    def _if_exists_unstack_category(self,category):
        dir_path = self._get_unstack_file_path(category)
        if os.path.exists(dir_path):
            return True
        else:
            return False


    def _if_exists_pivot_category(self,category):
        dir_path = self._get_category_path(category)
        if os.path.exists(dir_path):
            return True
        else:
            return False

    def _get_category_path(self, category):
        """Create and return the directory path for a specific category, optionally with year and month."""
        # dir_path = f"{self.root_dir}/{category}/"
        dir_path = os.path.join(self.root_dir, category)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        return dir_path


    @staticmethod
    def GSOI(choice,df):
        if choice == 1:
            return df.columns
        elif choice == 0:
            return df.index
        else:
            return "Invalid input. Please enter 1 for columns or 0 for index."

    @staticmethod
    def extract_year_month(input_string):
        match = re.search(r'_(\d{4})-(\d{2})\.', input_string)
        if match:
            year = match.group(1)
            month = match.group(2)
            return year, month
        else:
            return None, None

    def _get_pivot_year_month(self,category):
        directory = self._get_category_path(category)
        return [ParquetDataManager.extract_year_month(x) for x in  os.listdir(directory)]


    def _get_pivot_file_path(self, category, year, month):
        """Generate the full file path for a parquet file based on category, year, and month."""
        directory = self._get_category_path(category)
        return f"{directory}/{category}_{year}-{month:02d}.parquet"

    def _get_unstack_file_path(self, category):
        """Generate the full file path for a parquet file based on category."""
        directory = self._get_category_path(category)
        return f"{directory}/{category}.parquet"


    # def store_dataframe(self, df, category, year, month):
    #     """Store a dataframe in a specific category folder and partition it by year and month."""
    #     file_path = self._get_pivot_file_path(category, year, month)
    #     if df.columns.dtype != str:
    #         df.columns = pd.to_datetime(df.columns).strftime("%Y-%m-%d")
    #     df.sort_index(axis=1, inplace=True)
    #     df.to_parquet(file_path, index=True)
    #     self.update_time_index(category, df.columns, operation='add')
    #     return

    def update_pivot_category(self, df, category, strf='%Y-%m-%d'):
        '''
        多线程更新pivot类型的数据
        '''
        """Update category data by merging with existing data."""
        # 按年份和月份对数据进行分区存储
        df.columns = pd.to_datetime(df.columns)
        grouped = df.groupby([df.columns.year, df.columns.month], axis=1)
        work_function = ParquetDataManager.update_pivot_parquet
        iterators = [[self._get_pivot_file_path(category, year, month), sub_df, strf] for (year, month), sub_df in grouped]
        # 使用concurrent进行存储
        ParquetDataManager.run_concurrently(iterators, work_function, max_workers=self.max_workers,
                                            task_desc=f"Updating {category}")
        return

    def read_pivot_category(self, category, start_date=None, end_date=None,column_type='str'):
        """Read all dataframes from a specific category."""
        directory = self._get_category_path(category)
        exists_parquets = [f for f in os.listdir(directory) if f.endswith('.parquet')]
        date_pattern_general = re.compile(r'(\d{4})-(\d{2})\.parquet')
        # exists_ms = sorted([f"{match.group(1)}-{match.group(2)}" for name in exists_parquets if
        #                     (match := date_pattern_general.search(name))])

        result = []
        for name in exists_parquets:
            match = date_pattern_general.search(name)
            if match:
                result.append(f"{match.group(1)}-{match.group(2)}")
        exists_ms = sorted(result)

        if exists_ms:
            if start_date == None:
                start_date = f"{exists_ms[-1]}-01"
            if end_date == None:
                end_date = (pd.Timestamp(exists_ms[-1]) + pd.offsets.MonthEnd(0)).strftime("%Y-%m-%d")


        target_ms = pd.date_range(start=start_date, end=end_date, freq='MS').strftime('%Y-%m').tolist()
        ms_delta = sorted(list(set(target_ms) - set(exists_ms)))
        if exists_ms.__len__() > 0:
            task_info = f"Reading {category} From {start_date} To {end_date}: "
            worker_func = ParquetDataManager.read_parquet
            iterators = [[f"{directory}/{category}_{ms}.parquet"] for ms in target_ms]
            results = ParquetDataManager.run_concurrently(iterators, worker_func, max_workers=self.max_workers,task_desc=f"{task_info}")
            if results:
                dfs = pd.concat([x for x in results], axis=1)
                if column_type =='datetime':
                    dfs.columns = pd.to_datetime(dfs.columns)
                    dfs.sort_index(axis=1, inplace=True)
                    start = pd.to_datetime(start_date) if start_date else dfs.min()
                    end = pd.to_datetime(end_date) if end_date else dfs.max()
                    return dfs.loc[:, (dfs.columns >= start) & (dfs.columns <= end)]
                else:
                    dfs.sort_index(axis=1, inplace=True)
                    start = pd.to_datetime(start_date).strftime("%Y-%m-%d") if start_date else dfs.min()
                    end = pd.to_datetime(end_date).strftime("%Y-%m-%d") if end_date else dfs.max()
                    return dfs.loc[:, (dfs.columns >= start) & (dfs.columns <= end)]
            else:
                raise ValueError("读取失败")
        else:
            print(f"数据不存在 {category}: {ms_delta} 数据不存在")
            return pd.DataFrame()
            # raise Exception(f"数据不存在 {category}: {ms_delta} 数据不存在")


    @staticmethod
    def read_parquet(file_path):
        return pd.read_parquet(file_path)

    def update_unstack_category(self, category, sub_df, key_columns=[]):
        '''
        更新unstack数据
        '''
        file_path = self._get_unstack_file_path(category)
        if os.path.exists(file_path):
            existing_df = pd.read_parquet(file_path)
            are_equal = existing_df.equals(sub_df)
            if not are_equal:
                existing_df = ParquetDataManager.update_unstack_df(original_df=existing_df, new_data=sub_df,
                                                                   key_columns=key_columns)
                existing_df.to_parquet(file_path)
                print(f"{file_path}: 更新 Unstack Parquet")
            else:
                # 无需合并，因为sub_df和existing_df完全相同
                print(f"{file_path}: No need to combine, dataframes are identical.")
        else:
            # 如果文件不存在，则直接存储新的DataFrame
            sub_df.to_parquet(file_path)
            print(f"{file_path}: 初始化 Unstack Parquet")

    def read_unstack_category(self, category,):
        file_path = self._get_unstack_file_path(category)
        return pd.read_parquet(file_path)


    @staticmethod
    def update_unstack_df(original_df, new_data, key_columns):
        # 确保 key_columns 是列表
        if not isinstance(key_columns, list):
            key_columns = [key_columns]

        # 首先将新数据与原始数据合并，使用 concat 进行纵向合并
        combined_df = pd.concat([original_df, new_data])

        # 使用 drop_duplicates 函数，基于 key_columns 去除重复数据
        # keep='last' 确保保留最新的记录（因为新数据是最后加入的）
        updated_df = combined_df.drop_duplicates(subset=key_columns, keep='last')

        # 返回更新后的 DataFrame
        return updated_df

    # @staticmethod

    @staticmethod
    def update_pivot_parquet(file_path, sub_df, date_format='%Y-%m-%d', ):
        """
        更新或创建一个Parquet文件。
        针对某一分区下的Parquet数据进行更新
        参数:
        - file_path: str，Parquet文件的存储路径。
        - sub_df: pd.DataFrame，要合并或存储的新DataFrame。
        - date_format: str，日期列的格式字符串，默认为'%Y-%m-%d'。

        如果Parquet文件存在，函数会尝试合并旧数据和新数据。
        如果列名或数据有差异，合并后的数据将被存储回同一文件。
        如果文件不存在，sub_df将直接保存为新文件。
        """
        if os.path.exists(file_path):
            existing_df = pd.read_parquet(file_path)
            # 确保列名是 datetime 类型
            existing_df.columns = pd.to_datetime(existing_df.columns)
            # 去除整行空值
            sub_df.columns = pd.to_datetime(sub_df.columns)
            sub_df = sub_df[sub_df.notnull().sum(1) > 0]
            # 检查是否需要合并

            different_columns = existing_df.columns.difference(existing_df.columns)
            different_index = existing_df.index.difference(sub_df.index)
            # 计算不同的值（基于索引排序后的 DataFrame）
            try:
                if (len(different_columns) > 0 or len(different_index) > 0) or (existing_df.sort_index().compare(sub_df.sort_index()).any().any()):
                # if not sub_df.columns.equals(existing_df.columns) or not sub_df.sort_index().equals(existing_df.sort_index()):
                    # 列不相同或数据有差异，执行合并
                    # 只显示不同值及其位置

                    existing_df = existing_df.combine_first(sub_df)
                    # 存储更新后的DataFrame
                    existing_df = existing_df[existing_df.notnull().sum(1) > 0]
                    # 更新列，可能是为了格式化日期字符串
                    existing_df.columns = pd.to_datetime(existing_df.columns).strftime(date_format)
                    existing_df.to_parquet(file_path)
                    print(f"{file_path}: UpdatingDF  From {existing_df.columns[0]} To {existing_df.columns[-1]} Total Shape {existing_df.shape}")
                    print()
                else:
                    # 无需合并，因为sub_df和existing_df完全相同
                    print(f"{file_path}: Dataframes are identical. From {existing_df.columns[0]} To {existing_df.columns[-1]} Total Shape {existing_df.shape}")
            except Exception as e:
                print(e)
        else:
            # 如果文件不存在，则直接存储新的DataFrame
            # 确保列名是按指定的日期格式字符串
            sub_df = sub_df[sub_df.notnull().sum(1) > 0]
            sub_df.columns = pd.to_datetime(sub_df.columns).strftime(date_format)
            sub_df.to_parquet(file_path)
            print(f"{file_path}: Initializing: Shape {sub_df.shape} From {sub_df.columns[0]} To {sub_df.columns[-1]}")
        return

    @staticmethod
    def run_concurrently(tasks, worker_function, max_workers=5, task_desc="Processing tasks"):
        results = []
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # 提交带多个参数的任务
            future_to_task = {executor.submit(worker_function, *task): task for task in tasks}
            # 使用 tqdm 包装 as_completed，显示进度条
            futures_iterator = tqdm(as_completed(future_to_task), total=len(future_to_task), desc=task_desc)

            # 收集处理结果
            for future in futures_iterator:
                # try:
                result = future.result()
                results.append(result)
            # except Exception as e:
            #     print(f"Operation failed: {e}")
            return results


    def get_download_days(self,category,template_date):
        exists_df = self.read_pivot_category(category=category,start_date=min(template_date),end_date=max(template_date))
        update_dates = sorted(list(set(template_date) - set(pd.to_datetime(exists_df.columns))))
        return [exists_df, update_dates]


