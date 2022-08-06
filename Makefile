cd-hit_threshold = 0.80
length = 26
n_gram = True

RAW_DATASET = data/raw/finish
ONE_FASTA_HIV1 = data/one_fasta/hiv1.fasta
ONE_FASTA_HIV2 = data/one_fasta/hiv2.fasta
INPUT_HIV1 = data/input/hiv1_threshold$(cd-hit_threshold).fasta
INPUT_HIV2 = data/input/hiv1.fasta
DATASET_HIV1 = data/processed/hiv1_threshold$(cd-hit_threshold).pickle
DATASET_HIV2 = data/processed/hiv2.pickle

all: $(DATASET_HIV1) $(DATASET_HIV2)

$(RAW_DATASET):
	python3 src/get_dataset.py
	touch $(RAW_DATASET)

$(ONE_FASTA_HIV1) $(ONE_FASTA_HIV2): $(RAW_DATASET)
	mkdir -p data/one_fasta/
	python3 src/conbine_in_one_fasta.py

$(INPUT_HIV1) $(INPUT_HIV2): $(ONE_FASTA_HIV1) $(ONE_FASTA_HIV2)
	mkdir -p data/input/
	./cd-hit -i $(FASTA_HIV1) -o $(CD-HIT_HIV1) -c $(cd-hit_threshold) -n 5
	cp $(ONE_FASTA_HIV2) $(INPUT_HIV2)

$(DATASET_HIV1) $(DATASET_HIV2): $(INPUT_HIV1) $(INPUT_HIV2)
	mkdir -p data/processed/
	python3 src/make_dataset.py
		$(length)
		--n_gram $(n_gram)
