import argparse
import yaml
import joblib
import pandas as pd
from os import listdir
from sklearn.impute import SimpleImputer

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OrdinalEncoder


if __name__ == '__main__':
    print(listdir())
    parser = argparse.ArgumentParser()
    parser.add_argument('--type', help='train or production processing')
    args = parser.parse_args()

    with open('data_engineering/raw_data/titanic_config.yaml') as f:
        config = yaml.load(f, Loader=yaml.loader.SafeLoader)

    if args.type == 'train':
        preproc_pipe = Pipeline([
                                ('sex_encoder', OrdinalEncoder()),
                                ('imputer', SimpleImputer(strategy='median'))
                                ],
                                verbose=True)
    elif args.type == 'production':
        preproc_pipe = joblib.load(config['articat_pipe_path'])

    raw_df = pd.read_csv(config[args.type]['path'])
    preprocessed_df = pd.DataFrame(preproc_pipe.fit_transform(raw_df), columns=preproc_pipe.get_feature_names_out())
    preprocessed_df['dummy_timestamp'] = config[args.type]['timestamp']
    preprocessed_df.to_parquet(config[args.type]['output_path'], index=False)

    # dumping trained pipe so preprocessing is gonna be the same for production data
    if args.type == 'train':
        joblib.dump(preproc_pipe, config['articat_pipe_path'])
        print('pipe was dumped after ingestion')

    print(f'{args.type} data has been ingested!')
