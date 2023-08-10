# import another_app
# def msg():
#     print('hello world')
#     return

# print(f'the name of the program is {__name__}')

# if __name__=="__main__":
#     msg()

#creating a new branch
#to access or process single files

import json
import os
import glob
import pandas as pd
import uuid
import logging

def get_columns(ds):
    #creating the environment variable for the path schemas
    schemas_file_path=os.environ.setdefault('SCHEMAS_FILE_PATH','data/retail_db/schemas.json')
    with open(schemas_file_path) as fp:
        schemas=json.load(fp)
    try:
        schema=schemas.get(ds)
        if not schema:
            raise KeyError
        cols=sorted(schema,key=lambda i:i['column_position'])
        columns=[i['column_name'] for i in cols]
        return print(columns)
    except KeyError:
        logging.error(f'schema is not found for {ds}')
        # return
        raise
    

def process_file(src_base_dir,ds,tgt_base_dir):
    for file in glob.glob(f'{src_base_dir}/{ds}/part*'):
        try:
            df=pd.read_csv(file,names=get_columns(ds))
            os.makedirs(f'{tgt_base_dir}/{ds}',exist_ok=True)
            df.to_json(f'{tgt_base_dir}/{ds}/part-{str(uuid.uuid1())}.json',
                            orient='records',
                            lines=True)
            logging.info(f'n.of records processed for {os.path.split(file)[1]} fro {ds} is {df.shape}')
        except KeyError:
            raise
    
def main():
    src_base_dir=os.environ['SRC_BASE_DIR']
    tgt_base_dir=os.environ['TGT_BASE_DIR']
    log_file_path=os.environ['LOG_FILE_PATH']

    logging.basicConfig(
        level=logging.INFO,
        filename=log_file_path,
        format='%(asctime)s %(levelname)s %(message)s',
        datefmt='DATE --> %Y-%B-%d time -->%H:%M:%S --> %p'
    )

    #new variable
    datasets=os.environ.get('DATASETS')
    if not datasets:
        for path in glob.glob(f'{src_base_dir}/*'):
            if os.path.isdir(path):
                process_file(src_base_dir,os.path.split(path)[1],tgt_base_dir)
    else:
         dirs=datasets.split(',')
         for dis in dirs:
            try:
                process_file(src_base_dir,dis,tgt_base_dir)
            except Exception as e:
                logging.error(f'file format conversion in Failed')
    logging.info('file format conversion : Successful')
            


if __name__=="__main__":
    main()


