import os
from collections.abc import Callable
from datetime import datetime
import time

import pandas as pd

from cypherdataframe.model.Config import Config
from cypherdataframe.model.Property import Property
from cypherdataframe.model.Query import Query
from py2neo import Graph

MAX_RUNS_WITHOUT_DATA = 3
MAX_EXCEPTIONS = 100
def query_to_dataframe(query: Query, config: Config) -> pd.DataFrame:
    cypher = query.to_cypher()
    print(cypher)
    graph = Graph(
        config.neo4j_url,
        auth=(config.neo4j_username, config.neo4j_password)
    )
    v = graph.run(cypher)
    print("done fetch")
    df = v.to_data_frame()
    print("converted to dataframe")
    assignment: str
    prop: Property
    for assignment, prop in query.all_properties_by_final_assigment().items():
        if assignment in df:
            if prop.datatype == datetime:
                df[assignment] = df[assignment].agg(
                    lambda x: x.to_native() if x else None
                )
            elif prop.datatype == list[datetime]:
                df[assignment] = df[assignment].agg(
                    lambda x: [y.to_native() for y in x]
                )
            elif prop.datatype == list[str]:
                pass
            elif prop.datatype == str:
                pass
            else:
                df[assignment] = df[assignment].astype(prop.datatype)

    return df.reset_index(drop=True)


def all_for_query_in_steps(
        query: Query
        , config: Config
        , step: int
        , limit: int
        , start_skip: int
        ) -> pd.DataFrame | None:
    skip = start_skip
    len_df = 1
    df_list = []

    while (len_df > 0 and skip<(start_skip+limit)):
        print(
            f"skip: {skip}, step (query limit): {step}, " 
            f"start_skip: {start_skip}, limit (chunk limit): {limit}"
        )
        this_query = Query(
            core_node=query.core_node,
            branches=query.branches,
            skip=skip,
            limit=step,
            enforce_complete_chunks=query.enforce_complete_chunks,
            disable_scan=query.disable_scan
        )
        start_time = time.time()
        df = query_to_dataframe(this_query, config)

        len_df = df.shape[0]
        print(f"rows returned {len_df}")
        print(f"--- {(time.time() - start_time)} seconds ---")
        print()
        if (len_df>0):
            df_list.append(df)
        skip = skip + step
    if len(df_list)>0:
        return pd.concat(df_list).reset_index(drop=True)
    else:
        return None

def __make_meta(meta_path: str) -> None:
    df_meta = pd.DataFrame(
        columns=[
            'increment',
            'keys',
            'rows',
            'row_rate',
            'chunk_size',
            'start_time',
            'data_extracted_time',
            'data_stored_time',
            'extraction_time',
            'storage_time',
            'total_time'
        ]
    )
    df_meta.to_csv(meta_path, index=False)


def __drop_gather_from_meta(
        meta_path: str
):
    df_meta = pd.read_csv(meta_path)
    df_meta = df_meta[df_meta['chunk_size'] > 0]
    df_meta.to_csv(meta_path, index=False)


def __add_to_meta(
    meta_path: str,
    increment: str,
    chunk_size: int,
    keys: int,
    rows: int,
    start_time,
    data_extracted_time,
    data_stored_time,
    extraction_time,
    storage_time,
    total_time
) -> None:


    new_meta = {
        'increment': increment,
        'row_rate': rows/total_time,
        'keys': keys,
        'rows': rows,
        'chunk_size': chunk_size,
        'start_time': start_time,
        'data_extracted_time': data_extracted_time,
        'data_stored_time': data_stored_time,
        'extraction_time': extraction_time,
        'storage_time': storage_time,
        'total_time': total_time
    }
    df_meta = pd.read_csv(meta_path)
    df_meta = pd.concat(
        [df_meta, pd.DataFrame(new_meta, index=[0])]
    )
    df_meta.to_csv(meta_path, index=False)


def __gather_to_meta(meta_path, meta_gather_path):
    df_meta = pd.read_csv(meta_path)
    df_meta.to_csv(meta_gather_path, index=False)


def all_for_query_in_chunks(
        query: Query
        , config: Config
        , step: int
        , chunk_size: int
        , save_directory: str
        , table_name_root: str
        , max_total_chunks: int
        , gather_to_dir: str
        , meta_gather_dir: str
        , gather_csv: bool = False
        , just_gather: bool = False
        , top_up: bool = False
        , deduplicate_gather: bool = False
        , first_chunk_set_size: int | None = None
        , post_gather_map: Callable[[pd.DataFrame], pd.DataFrame] | None = None
        ) -> None:
    meta_path = f'{save_directory}/meta.csv'
    if first_chunk_set_size is None and top_up:
        first_chunk_set_size = 10

    if not os.path.isdir(meta_gather_dir):
        os.makedirs(meta_gather_dir)

    if not os.path.isdir(save_directory):
        os.makedirs(save_directory)

    if not os.path.isfile(meta_path):
        __make_meta(meta_path)


    process_start_time = time.time()
    df_meta = pd.read_csv(meta_path)

    if df_meta.shape[0] > 0:
        if ('gather' not in df_meta['increment'].values.tolist()) or top_up:
            df_meta_inc = df_meta[df_meta['chunk_size'] > 0]
            start_chunk = int(df_meta_inc['increment'].max()) + 1
            total_keys = df_meta_inc['keys'].sum()
        elif just_gather:
            pass
        else:
            print("Already Gathered")
            print()
            return None
    else:
        total_keys = 0
        start_chunk = 1

    exceptions = 0
    inc_chunk = 0
    runs_without_data = 0
    this_chunk_size = chunk_size
    while not just_gather:
        try:
            chunk_start_time = time.time()
            current_chunk = start_chunk + inc_chunk

            if current_chunk > max_total_chunks:
                print("breaking")
                break
            print()
            print(
                f"Chunk: {current_chunk} "
                f"Keys So Far: {total_keys} "
                f"Time: {time.strftime('%H:%M:%S', time.localtime())}"
            )

            if (first_chunk_set_size is not None) & (inc_chunk == 0):
                this_chunk_size = first_chunk_set_size
                this_step = first_chunk_set_size
            else:
                this_chunk_size = chunk_size
                this_step = step

            df: pd.DataFrame | None = all_for_query_in_steps(
                query
                , config
                , step=this_step
                , limit=this_chunk_size
                , start_skip=total_keys
            )
            data_extracted_time = time.time()
            if df is not None:
                df.to_csv(
                    f"{save_directory}/{table_name_root}_{current_chunk}.csv",
                    index=False
                )
                df.to_feather(
                    f"{save_directory}/{table_name_root}_{current_chunk}.feather"
                )
                data_stored_time = time.time()
                df_keys = df[df.columns[0]].nunique()
                df_rows = df.shape[0]
            else:
                data_stored_time = time.time()
                df_keys = 0
                df_rows = 0

        except Exception as e:
            print(f"Whoops {exceptions} waiting 10 s")
            print(e)
            time.sleep(10)
            exceptions = exceptions + 1
            if exceptions >= MAX_EXCEPTIONS:
                print(f"Exceptions: {exceptions} "
                      f"exceeded max: {MAX_EXCEPTIONS}")
                print("Process Abandoned")
                return None
            else:
                continue



        __add_to_meta(
            meta_path,
            increment=current_chunk,
            keys=df_keys,
            rows=df_rows,
            chunk_size=this_chunk_size,
            start_time=datetime.fromtimestamp(chunk_start_time, tz=None),
            data_extracted_time=datetime.fromtimestamp(data_extracted_time, tz=None),
            data_stored_time=datetime.fromtimestamp(data_stored_time, tz=None),
            extraction_time=(data_extracted_time - chunk_start_time) / 60,
            storage_time=(data_stored_time - data_extracted_time) / 60,
            total_time=(data_stored_time - chunk_start_time) /60
        )
        total_keys += df_keys
        if df_rows < 1:
            runs_without_data += 1
        else:
            runs_without_data = 0

        if df_keys < this_chunk_size and query.enforce_complete_chunks:
            print(f"Incomplete chunk with enforce_complete_chunks turned on")
            print("Chunk Done")
            break

        if runs_without_data == MAX_RUNS_WITHOUT_DATA:
            print(f"Consecutive runs_without_data: {runs_without_data} "
                  f"exceeded max: {MAX_RUNS_WITHOUT_DATA}")
            print("Chunk Done")
            break

        inc_chunk += 1

    start_gather_time = time.time()

    gather_success = gather_chunks_from_dir(
        gather_to_dir=gather_to_dir,
        read_directory=save_directory,
        table_name_root=table_name_root,
        gather_csv=gather_csv,
        deduplicate_gather=deduplicate_gather,
        post_gather_map=post_gather_map
    )
    if (gather_success):
        df_meta = pd.read_csv(meta_path)
        __drop_gather_from_meta(meta_path)
        __add_to_meta(
            meta_path,
            increment="gather",
            rows=0,
            keys=0,
            chunk_size=0,
            start_time=datetime.fromtimestamp(start_gather_time, tz=None),
            data_extracted_time=None,
            data_stored_time=None,
            extraction_time=0,
            storage_time=0,
            total_time=(time.time() - start_gather_time) /60
        )
        __add_to_meta(
            meta_path,
            increment="process_total",
            rows=df_meta['rows'].sum(),
            keys=df_meta['keys'].sum(),
            chunk_size=0,
            start_time=datetime.fromtimestamp(process_start_time, tz=None),
            data_extracted_time=None,
            data_stored_time=None,
            extraction_time=0,
            storage_time=0,
            total_time=(time.time() - process_start_time) / 60
        )
        meta_gather_path = f'{meta_gather_dir}/{table_name_root}_meta.csv'
        __gather_to_meta(meta_path, meta_gather_path)


def gather_chunks_from_dir(
        gather_to_dir: str
        , read_directory: str
        , table_name_root: str
        , gather_csv: bool
        , deduplicate_gather: bool
        ,  post_gather_map: Callable[[pd.DataFrame], pd.DataFrame] | None
        ) -> bool:
    if os.path.isdir(read_directory):
        df_list = []
        for file_name in os.listdir(read_directory):
            file_size = os.path.getsize(f"{read_directory}/{file_name}")
            if ".feather" in file_name \
                    and "-gathered.feather" not in file_name \
                    and file_size > 10:
                feather_to_gather = f"{read_directory}/{file_name}"
                try:
                    df1 = pd.read_feather(feather_to_gather)
                except Exception as e:
                    print(feather_to_gather)
                    print(e)
                    return False
                df_list.append(df1)
        if len(df_list) > 0:
            df = pd.concat(df_list).reset_index(drop=True)
            if(df.shape[0]>0):
                if deduplicate_gather:
                    df = df.drop_duplciates()

                if post_gather_map:
                    df = post_gather_map(df)

                if not os.path.isdir(gather_to_dir):
                    os.makedirs(gather_to_dir)
                if gather_csv:
                    df.to_csv(
                        f"{gather_to_dir}/{table_name_root}-gathered.csv",
                        index=False
                    )
                df.to_feather(
                    f"{gather_to_dir}/{table_name_root}-gathered.feather"
                )
                return True
        return False
