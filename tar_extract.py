import tarfile
from pathlib import Path

data_path = Path("zipped_dataset/")

for i in data_path.iterdir():
    tf = tarfile.open(i)
    tf.extractall("dataset")
    tf.close()
