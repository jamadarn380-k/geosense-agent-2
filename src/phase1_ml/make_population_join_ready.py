from pathlib import Path
import shutil

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

INPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "population"
    / "pune_zone_population_2011.csv"
)

BACKUP_FILE = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "population"
    / "pune_zone_population_2011_backup_before_name_fix.csv"
)


def read_csv_safely(file_path):
    encodings = ["utf-8", "utf-8-sig", "cp1252", "latin1"]

    for encoding in encodings:
        try:
            dataframe = pd.read_csv(file_path, encoding=encoding)
            print(f"CSV encoding read successfully: {encoding}")
            return dataframe
        except UnicodeDecodeError:
            pass

    raise RuntimeError("Could not read CSV with supported encodings.")


def main():
    if not INPUT_FILE.exists():
        raise FileNotFoundError(f"Population CSV not found:\n{INPUT_FILE}")

    population = read_csv_safely(INPUT_FILE)

    required_columns = {"Boundary Name", "2011 Population"}

    if not required_columns.issubset(population.columns):
        raise ValueError(
            "Expected columns were not found.\n"
            f"Expected: {required_columns}\n"
            f"Found: {population.columns.tolist()}"
        )

    if not BACKUP_FILE.exists():
        shutil.copy2(INPUT_FILE, BACKUP_FILE)
        print(f"\nBackup created:\n{BACKUP_FILE}")
    else:
        print(f"\nBackup already exists:\n{BACKUP_FILE}")

    exact_boundary_names = {
        "Admin Ward 01 Aundh": "Admin Ward 01 Aundh",
        "Admin Ward 02 Ghole Road": "Admin Ward 02 Ghole Road",
        "Admin Ward 03 Kothrud Karve Road": "Admin Ward 03 Kothrud Karveroad",
        "Admin Ward 04 Warje Karve Nagar": "Admin Ward 04 Warje Karvenagar",
        "Admin Ward 05 Dhole Patil Road": "Admin Ward 05 Dhole Patil Rd",
        "Admin Ward 06 Yerawada–Sangamwadi": "Admin Ward 06 Yerawda - Sangamwadi",
        "Admin Ward 07 Nagar Road": "Admin Ward 07 Nagar Road",
        "Admin Ward 08 Kasba–Vishrambaug Wada": "Admin Ward 08 KasbaVishrambaugwada",
        "Admin Ward 09 Tilak Road": "Admin Ward 09 Tilak Road",
        "Admin Ward 10 Sahakar Nagar": "Admin Ward 10 Sahakarnagar",
        "Admin Ward 11 Bibwewadi": "Admin Ward 11 Bibwewadi",
        "Admin Ward 12 Bhavani Peth": "Admin Ward 12 Bhavani Peth",
        "Admin Ward 13 Hadapsar": "Admin Ward 13 Hadapsar",
        "Admin Ward 14 Dhankawadi": "Admin Ward 14 Dhankawadi",
        "Admin Ward 15 Kondhwa–Wanawadi": "Admin Ward 15 Kondhwa Wanavdi",
    }

    population["Boundary Name"] = (
        population["Boundary Name"]
        .astype(str)
        .str.strip()
    )

    population["Boundary Name"] = population["Boundary Name"].replace(
        exact_boundary_names
    )

    population = population.rename(
        columns={
            "Boundary Name": "Name",
            "2011 Population": "population_2011",
        }
    )

    population["population_2011"] = (
        population["population_2011"]
        .astype(str)
        .str.replace(",", "", regex=False)
        .str.strip()
    )

    population["population_2011"] = pd.to_numeric(
        population["population_2011"],
        errors="coerce"
    )

    if population["population_2011"].isna().any():
        invalid_rows = population[
            population["population_2011"].isna()
        ]
        raise ValueError(
            "Some population values are invalid:\n"
            + invalid_rows.to_string(index=False)
        )

    final_population = population[
        ["Name", "population_2011"]
    ].copy()

    final_population.to_csv(
        INPUT_FILE,
        index=False,
        encoding="utf-8-sig"
    )

    print("\n" + "=" * 70)
    print("SUCCESS: Clean population CSV created.")
    print("=" * 70)

    print("\nFinal CSV table:")
    print(final_population.to_string(index=False))

    print(f"\nTotal rows: {len(final_population)}")
    print(f"Total population: {final_population['population_2011'].sum():,.0f}")


if __name__ == "__main__":
    main()