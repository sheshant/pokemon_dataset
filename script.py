import csv
import os

from pokemon.models import Pokemon, FileUpload
from pokemon.upload_utils.upload_to_s3_utils import UploadToS3


def upload_pokemon_databases(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file, delimiter=',', quotechar='"', lineterminator="")  # Assumes the first row is header
        pokemons = []

        for row in reader:
            # Create an instance of MyModel for each row
            obj = Pokemon(
                name=row['Pokemon'].strip() or None,
                species=row["Species"].strip() or None,
                height=(row["Height"].split() and row["Height"].split()[0].strip()) or None,
                weight=(row["Weight"].split() and row["Weight"].split()[0].strip()) or None,
                growth_rate=row["Growth Rate"].strip() or None,
            )
            pokemons.append(obj)
        Pokemon.objects.bulk_create(pokemons)

    with open(file_path, 'r') as file:
        reader = csv.DictReader(file, delimiter=',', quotechar='"', lineterminator="")  # Assumes the first row is header
        pokemons = {record.name: record for record in Pokemon.objects.all()}
        count = 0
        for row in reader:
            count += 1
            print(count)
            pokemons[row['Pokemon']].type.set([record.strip() for record in row["Type"].split(',')])
            pokemons[row['Pokemon']].abilities.set(list(map(lambda x: x.strip("2, "), row["Abilities"].split(".")[1:])))
            pokemons[row['Pokemon']].egg_groups.set([record.strip() for record in row["Egg Groups"].split(',')])
            pokemons[row['Pokemon']].ev_yield.set([record.strip() for record in row["EV Yield"].split(',')])


def add_images(folder_path):
    pokemons = {record.name: record.pk for record in Pokemon.objects.all()}
    file_uploads = []
    count = 0

    for directory in os.listdir(folder_path):
        if not directory.startswith("."):
            label = "general"
            name = directory.replace("(", "").replace(")", "")
            pokemon_id = pokemons.get(name)
            new_path = os.path.join(folder_path, directory)
            for file in os.listdir(new_path):
                if "new" in file and pokemon_id:
                    image_path = os.path.join(new_path, file)
                    status, url = UploadToS3.upload_file_from_path(file_path=image_path, name=file)
                    if status:
                        count += 1
                        print(count)
                        file_uploads.append(
                            FileUpload(file_label=label, file_url=url, user_id=1, pokemon_id=pokemon_id))

    FileUpload.objects.bulk_create(file_uploads)









if __name__ == "__main__":
    # upload_pokemon_databases("/Users/sheshantsingh/Downloads/testing.csv")
    # add_images("/Users/sheshantsingh/Downloads/untitled folder")

    # upload_pokemon_databases("/Users/sheshantsingh/Downloads/archive (1)/pokemonDB_dataset.csv")
    add_images("/Users/sheshantsingh/Downloads/archive (1)/Pokemon Images DB/Pokemon Images DB")
