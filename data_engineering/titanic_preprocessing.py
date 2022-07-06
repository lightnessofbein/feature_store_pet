import yaml
import pandas as pd
from os import path
from sklearn.impute import SimpleImputer

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OrdinalEncoder, StandardScaler


def preprocess_raw_file(rawfile_path, pipe, output_path, timestamp):
    raw_df = pd.read_csv(rawfile_path)
    preprocessed_df = pd.DataFrame(pipe.fit_transform(raw_df), columns=pipe.get_feature_names_out())
    preprocessed_df['dummy_timestamp'] = timestamp
    preprocessed_df.to_csv(output_path, index=False, mode='a', header = not path.exists(output_path))
    print(f'saved {preprocessed_df.shape[0]} rows to {output_path}')


if __name__ == '__main__':
    with open('data_engineering/raw_data/titanic_config.yaml') as f:
        config = yaml.load(f, Loader=yaml.loader.SafeLoader)

    preproc_pipe = Pipeline([
                             ('sex_encoder', OrdinalEncoder()),
                             ('imputer', SimpleImputer(strategy='median'))
                             ],
                              verbose=True)

    preprocess_raw_file(rawfile_path=config['train']['path'], 
                        pipe=preproc_pipe, 
                        output_path=config['output_path'],
                        timestamp=config['train']['timestamp'])
    print('train data has been ingested!')

    for period in config['prod']:
        preprocess_raw_file(rawfile_path=config['prod'][period]['path'], 
                            pipe=preproc_pipe, 
                            output_path=config['output_path'],
                            timestamp=config['prod'][period]['timestamp'])
        print(f'{period} data has been ingested!')

        


