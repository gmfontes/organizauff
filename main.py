import sys
from reader import read_subjects_csv

if len(sys.argv) < 2:
    print("Insira o caminho do arquivo .csv")
    sys.exit(1)

csv_path = sys.argv[1]

subjects = read_subjects_csv(csv_path)

print(subjects["MMO00083"])