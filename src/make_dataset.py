import os
import argparse
import json
import pickle

from src.data.dataset import Dataset, extract


# コマンドライン引数を取得
parser = argparse.ArgumentParser()

parser.add_argument('length', help="Amino acids are fragmentated by this length.",
                    type=int)
parser.add_argument('fasta_dir', help="Path to FASTA files.",
                    type=str)
parser.add_argument('out_dir', help="Path to output files.",
                    type=str)
parser.add_argument('--n_gram', help="If True, n_gram dataset are generated.",
                    type=bool, default=True)

args = parser.parse_args()


def main():
    motif_data_path = 'references/LYPXL_data.json'
    with open(motif_data_path, 'r') as f:
        motif_data = json.load(f)

    for data in motif_data:
        virusname = motif_data['virus'].replace(' ', '_')
        fasta_path = os.path.join('data/input/', f'{virusname}.fasta')

        records = extract(fasta_path)
        dataset_maker = Dataset(
                SLiM=data['SLiM'],
                idx=data['start_index'],
                length=args.length,
                proteins=data['proteins'],
                SLiM_protein=data['SLiM_protein'],
                neighbor=data['neighbor'],
                replacement_tolerance=data['replacement_tolerance'],
                threshold=len(data['SLiM']),
                n_gram=args.n_gram)

        x, y = dataset_maker.make_dataset(records, dict=False)

        y_positive = (y == 1).astype(int)
        x_positive = x[y_positive]
        for seq in x_positive:
            if not 'LYP' in seq:
                print(seq)

        # out_path = os.path.join(args.out_dir, f'{virusname}.pickle')
        # with open(out_path, 'wb') as f:
        #     pickle.dump(x, f)
        #     pickle.dump(y, f)


if __name__ == '__main__':
    main()
