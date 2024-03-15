import pandas as pd
from tqdm import tqdm


def extract_match_data(parquet_file_path, output_file_path):
    # Read the parquet file
    df = pd.read_parquet(parquet_file_path)

    # Fill NA values and convert IDs to integers using vectorized operations
    df['winner_id'] = df['winner_id'].fillna(-1).astype('int32')
    df['radiant_team_id'] = df['radiant_team_id'].fillna(-1).astype('int32')

    # Use vectorized operations to construct the hero ID strings
    # This avoids applying functions row-wise, which is slower
    radiant_hero_ids = df[[f'radiant_player_{i}_hero_id' for i in range(1, 6)]].astype(str).agg(','.join, axis=1)
    dire_hero_ids = df[[f'dire_player_{i}_hero_id' for i in range(1, 6)]].astype(str).agg(','.join, axis=1)

    # Determine the winner side using a vectorized operation
    winner_side = (df['winner_id'] != df['radiant_team_id']).astype(int)  # 0 if Radiant wins, 1 if Dire wins

    # Combine all information into a new DataFrame
    # Note: No need for tqdm here as this is not the bottleneck step
    extracted_data = pd.DataFrame({
        'radiant_hero_ids': radiant_hero_ids,
        'dire_hero_ids': dire_hero_ids,
        'winner_side': winner_side
    })

    # Writing to a text file, line by line
    with open(output_file_path, 'w') as file:
        for line in tqdm(extracted_data.itertuples(index=False, name=None), total=len(extracted_data)):
            file.write(','.join(map(str, line)) + '\n')


# Specify the path to your parquet file and the output text file
parquet_file_path = 'dota2_matches.parquet'
output_file_path = 'match_outcomes.txt'

# Call the function to extract data and write to the text file
extract_match_data(parquet_file_path, output_file_path)
