import requests
import pandas as pd
from pathlib import Path


API_URL = "https://api.fda.gov/drug/label.json"


MEDICINES = [
    "acetaminophen",
    "ibuprofen",
    "amoxicillin",
    "metformin",
    "loratadine"
]


def clean_value(value):

    if not value:
        return ""

    if isinstance(value, list):

        return " ".join(
            str(item).strip()
            for item in value
            if item
        )

    return str(value).strip()


def first_value(data, field):

    value = data.get(
        field,
        []
    )

    if isinstance(
        value,
        list
    ) and value:

        return clean_value(
            value[0]
        )

    return clean_value(
        value
    )


def fetch_medicine(
    medicine_name
):

    params = {
        "search": (
            f'openfda.generic_name:'
            f'"{medicine_name}"'
        ),
        "limit": 10
    }

    try:

        response = requests.get(
            API_URL,
            params=params,
            timeout=30
        )

    except requests.RequestException as error:

        print(
            f"Request error for "
            f"{medicine_name}: {error}"
        )

        return None

    if response.status_code != 200:

        print(
            f"API request failed for "
            f"{medicine_name}: "
            f"{response.status_code}"
        )

        return None

    try:

        data = response.json()

    except ValueError:

        print(
            f"Invalid API response for "
            f"{medicine_name}"
        )

        return None

    results = data.get(
        "results",
        []
    )

    if not results:

        return None

    medicine_lower = (
        medicine_name
        .strip()
        .lower()
    )

    for result in results:

        openfda = result.get(
            "openfda",
            {}
        )

        generic_names = [
            str(name)
            .strip()
            .lower()
            for name in openfda.get(
                "generic_name",
                []
            )
        ]

        if medicine_lower in generic_names:

            return result

    return None


def create_record(
    result,
    searched_name
):

    openfda = result.get(
        "openfda",
        {}
    )

    brand_name = first_value(
        openfda,
        "brand_name"
    )

    generic_name = first_value(
        openfda,
        "generic_name"
    )

    dosage_form = first_value(
        result,
        "dosage_form"
    )

    pharm_class = first_value(
        result,
        "pharm_class"
    )

    description = first_value(
        result,
        "description"
    )

    indications = first_value(
        result,
        "indications_and_usage"
    )

    purpose = first_value(
        result,
        "purpose"
    )

    warnings = first_value(
        result,
        "warnings"
    )

    adverse_reactions = first_value(
        result,
        "adverse_reactions"
    )

    if not indications:

        indications = purpose

    if not description:

        description = (
            "No description available "
            "in this label."
        )

    return {
        "searched_name": searched_name,
        "medicine_name": (
            brand_name
            if brand_name
            else searched_name
        ),
        "generic_name": generic_name,
        "category": pharm_class,
        "form": dosage_form,
        "description": description,
        "indications": indications,
        "warnings": warnings,
        "adverse_reactions": adverse_reactions,
        "source": "openFDA Drug Labeling"
    }


def main():

    records = []

    for medicine in MEDICINES:

        print(
            f"Fetching: {medicine}"
        )

        result = fetch_medicine(
            medicine
        )

        if result is None:

            print(
                f"Not found: {medicine}"
            )

            continue

        record = create_record(
            result,
            medicine
        )

        records.append(
            record
        )

    df = pd.DataFrame(
        records
    )

    project_root = (
        Path(__file__)
        .resolve()
        .parent
        .parent
    )

    output_path = (
        project_root
        / "data"
        / "real_medicines.csv"
    )

    df.to_csv(
        output_path,
        index=False
    )

    print()

    print(
        "Dataset created successfully!"
    )

    print(
        f"Records: {len(df)}"
    )

    print(
        f"Saved to: {output_path}"
    )

    print()

    print("Columns:")

    print(
        list(df.columns)
    )


if __name__ == "__main__":

    main()