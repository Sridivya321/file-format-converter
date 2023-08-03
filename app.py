# import another_app
# def msg():
#     print('hello world')
#     return

# print(f'the name of the program is {__name__}')

# if __name__=="__main__":
#     msg()

import json
import os
import glob
import pandas as pd
import uuid

def get_columns(ds):
    with open('data/retail_db/schemas.json') as fp:
        schemas=json.load(fp)
    try:
        schema=schemas.get(ds)
        if not schema:
            raise KeyError
        cols=sorted(schema,key=lambda i:i['column_position'])
        columns=[i['column_name'] for i in cols]
        return print(columns)
    except KeyError:
        print(f'schema is not found for {ds}')
        return
    
def main():
    for path in glob.glob('data/retail_db/*'):
        if os.path.isdir(path):
            ds=os.path.split(path)[1]
            for file in glob.glob(f'{path}/part*'):
                df=pd.read_csv(file,names=get_columns(ds))
                os.makedirs(f'data/retail_demo/{ds}',exist_ok=True)
                df.to_json(f'data/retail_demo/{ds}/part-{str(uuid.uuid1())}.json',
                           orient='records',
                           lines=True)
                print(f'n.of records processed for {os.path.split(file)[1]} fro {ds} is {df.shape}')


if __name__=="__main__":
    main()