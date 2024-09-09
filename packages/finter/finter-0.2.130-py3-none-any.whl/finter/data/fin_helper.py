import pandas as pd

class FinHelper:
    @staticmethod
    def _check_df_format(df: pd.DataFrame):
        assert (
           isinstance(df, pd.DataFrame)
           and set(df.columns) == {'id', 'fiscal', 'pit', 'value'}
        ), "Dataframe column must be ('id', 'fiscal', 'pit', 'value'); This func is made for financial data with 'unpivot'"            
            
    
    @staticmethod
    def filter_unchanged(df: pd.DataFrame) -> pd.DataFrame:
        """
        remove reannounce value
        ----------------------------------------
        ID      FISCAL  PIT         VALUE
        ----------------------------------------
        60331   202103	2021-11-07	12220.917
                        2022-05-10	12220.917 <- remove
        ----------------------------------------

        """
        FinHelper._check_df_format(df)
        
        return df.sort_values(['id', 'fiscal' 'pit']).drop_duplicates(['id', 'fiscal', 'value'])

    @staticmethod
    def unify_idx(*args):
        '''
        input(*args) : dataframes
        Create and apply a multi-index that unions index of all args dataframes.
        '''
        
        copy_args = []
        for arg in args:
            FinHelper._check_df_format(arg)
            copy_arg = arg.copy()
            copy_arg['fiscal'] = copy_arg['fiscal'].astype(int)
            copy_args.append(copy_arg.set_index(["id", "fiscal", "pit"]))
        
        # make union multi-index
        idx = pd.MultiIndex.from_tuples(
            sorted(set().union(*map(lambda x: x.index, copy_args))),
            names=["id", "fiscal", "pit"])

        result = []
        for arg in copy_args:
            arg = arg.reindex(idx)
            arg = arg.reset_index()
            
            values = arg['value'].values
            ids = arg['id'].values
            fiscals = arg['fiscal'].values

            # groupby [id, fiscal] and value ffill()
            for i in range(1, len(values)):
                if pd.isna(values[i]) and ids[i] == ids[i-1] and fiscals[i] == fiscals[i-1]:
                    values[i] = values[i-1]

            arg['value'] = values

            arg = arg.drop_duplicates(subset=["id", "fiscal", "pit"], keep="last")
            arg = arg.set_index(["id", "fiscal", "pit"])

            result.append(arg)

        return result[0] if len(result) == 1 else result
    
    @staticmethod
    def shift_fundamental(
        df: pd.DataFrame, periods: int, fiscal: str='quarter'
        ) -> pd.DataFrame:
        '''
        Shift the financial data by n quarters.
        '''
        FinHelper._check_df_format(df)
        
        assert periods > 0, "periods should be positive"
        assert fiscal in ["quarter", "annual"], \
            "possible arguments are ['annual', 'quarter']"

        data_original = df.copy()
        data_original = data_original.sort_values(["id", "fiscal", "pit"])

        # create order column that yyyyqq to fiscal value
        # 202001Q -> 8081
        data_original['fiscal'] = data_original['fiscal'].astype(int)
        data_original["order"] = data_original["fiscal"].floordiv(100) * 4 + data_original["fiscal"].mod(100)
        data_shifted = data_original.copy()
        if fiscal == "quarter":
            data_shifted["order"] += periods
        else:
            data_shifted["order"] += periods * 4


        data_original = data_original.set_index(["id", "order"])
        data_shifted = data_shifted.set_index(["id", "order"])

        merge_df = pd.merge(data_original, data_shifted, how="left", left_index=True, right_index=True)
        
        df_normal = merge_df[merge_df.pit_x >= merge_df.pit_y][["fiscal_x", "pit_x", "value_y"]].reset_index()
        df_normal = df_normal.rename(columns={"fiscal_x": "fiscal", "pit_x": "pit", "value_y": "value"})
        df_normal = (df_normal
                     .drop_duplicates(['id', 'fiscal', 'value'])
                     .drop_duplicates(['id', 'fiscal', 'pit'], keep='last'))
        
        df_late_revision = merge_df[merge_df.pit_x < merge_df.pit_y][["fiscal_x", "pit_y", "value_y"]].reset_index()
        df_late_revision = df_late_revision.rename(
            columns={"fiscal_x": "fiscal", "pit_y": "pit", "value_y": "value"})
        df_late_revision = df_late_revision.drop_duplicates()
        
        result = pd.concat([df_normal, df_late_revision])
        result = result.drop(columns=["order"])
        result = result.drop_duplicates(subset=["id", "fiscal", "pit"], keep="last")

        return result.sort_values(["id", "fiscal", "pit"])