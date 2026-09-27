from pathlib import Path
import random
import shutil

SOURCE = Path(
    "/Users/mac/Downloads/erythrocytesIDB_2017/"
    "Version 2, erythrocytesIDB/"
    "erythrocytesIDB1/individual cells"
)

DEST = Path("data/sickle/classification")

CLASSES = ["circular", "elongated", "other"]

random.seed(42)

for split in ["train", "val", "test"]:
    for cls in CLASSES:
        (DEST / split / cls).mkdir(parents=True, exist_ok=True)

for cls in CLASSES:
    images = list((SOURCE / cls).glob("*.jpg"))
    random.shuffle(images)

    n = len(images)
    train_end = int(n * 0.70)
    val_end = int(n * 0.85)

    splits = {
        "train": images[:train_end],
        "val": images[train_end:val_end],
        "test": images[val_end:],
    }

    for split, files in splits.items():
        for image in files:
            shutil.copy2(
                image,
                DEST / split / cls / image.name,
            )

    print(
        f"{cls}: "
        f"{len(splits['train'])} train, "
        f"{len(splits['val'])} val, "
        f"{len(splits['test'])} test"
    )

print("\nDataset prepared at:", DEST)