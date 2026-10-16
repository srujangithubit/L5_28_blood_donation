"""Demonstration of a simple blood donation management system."""

import tempfile
from datetime import date, timedelta

MIN_DONOR_AGE = 18
MAX_DONOR_AGE = 65
DONATION_INTERVAL_DAYS = 90

DONORS = []
STOCK = {
    "A+": 0,
    "A-": 0,
    "B+": 0,
    "B-": 0,
    "O+": 0,
    "O-": 0,
    "AB+": 0,
    "AB-": 0,
}
COMPATIBLE = {
    "O-": ["O-"],
    "O+": ["O-", "O+"],
    "A-": ["O-", "A-"],
    "A+": ["O-", "O+", "A-", "A+"],
    "B-": ["O-", "B-"],
    "B+": ["O-", "O+", "B-", "B+"],
    "AB-": ["O-", "A-", "B-", "AB-"],
    "AB+": list(STOCK),
}


def register_donor(
    donor_name,
    blood_group,
    age,
    last_donation=None,
    notes=None,
):
    """Register a donor if the blood group and age are valid."""
    if blood_group not in STOCK:
        raise ValueError("Unknown blood group")

    if notes is None:
        notes = []

    if age < MIN_DONOR_AGE or age > MAX_DONOR_AGE:
        notes.append(f"{donor_name} is not eligible because of age")
        return False

    DONORS.append(
        {
            "name": donor_name,
            "group": blood_group,
            "last": last_donation,
        }
    )
    return True


def can_donate(donor):
    """Return whether a donor may donate under the 90-day rule."""
    last_donation = donor["last"]
    if last_donation is None:
        return True

    return date.today() - last_donation >= timedelta(
        days=DONATION_INTERVAL_DAYS
    )


def record_donation(donor_name, units=1):
    """Record a donation and update stock when the donor is eligible."""
    if not isinstance(units, int) or isinstance(units, bool) or units <= 0:
        return False

    for donor in DONORS:
        if donor["name"] == donor_name and can_donate(donor):
            STOCK[donor["group"]] += units
            donor["last"] = date.today()
            return True

    return False


def units_for(patient_group):
    """Return compatible stock units, or zero for an unknown group."""
    compatible_groups = COMPATIBLE.get(patient_group)
    if compatible_groups is None:
        return 0

    return sum(STOCK[group] for group in compatible_groups)


def is_universal(blood_group):
    """Check for O-negative universal donor or AB-positive recipient."""
    return blood_group in {"O-", "AB+"}


def low_stock(threshold=2):
    """Return blood groups with fewer units than the threshold."""
    return [
        group
        for group, units in STOCK.items()
        if units < threshold
    ]


def donor_sheet_path():
    """Create an empty temporary CSV file and return its path."""
    with tempfile.NamedTemporaryFile(
        mode="w",
        suffix=".csv",
        delete=False,
        encoding="utf-8",
    ) as temp_file:
        return temp_file.name


def main():
    """Run a demonstration of donor registration and stock checks."""
    DONORS.clear()
    for blood_group in STOCK:
        STOCK[blood_group] = 0

    register_donor("Arjun", "O+", 25)
    register_donor(
        "Priya",
        "A+",
        30,
        date.today() - timedelta(days=30),
    )
    register_donor("Old Donor", "B+", 70)
    register_donor("Farah", "O-", 41)

    record_donation("Arjun", 2)
    record_donation("Priya")
    record_donation("Farah")

    print("Stock:", STOCK)
    print("Units for an A+ patient:", units_for("A+"))
    print("Units for a Z+ patient:", units_for("Z+"))
    print("Is O- universal?", is_universal("O-"))
    print("Low stock groups:", low_stock())

    eligible = [donor["name"] for donor in DONORS if can_donate(donor)]
    print("Donors eligible today:", eligible)


if __name__ == "__main__":
    main()
