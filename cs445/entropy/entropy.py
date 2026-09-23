import math
import csv
from pathlib import Path
from typing import Optional

class DataScraper:
    def __init__(self):
        self.data: list[dict[str, str]] = []
        self.headers: list[str] = []
        self.klass: Optional[str] = None
        self.unique_classes: list[str] = []

    @property
    def num_samples(self) -> int:
        return len(self.data)

    @property
    def num_unique_classes(self) -> int:
        return len(self.unique_classes)

    def from_csv(self, fname: str, headers: bool = True, class_label: str = None):
        """Load data from a CSV file.

        If `headers` is False, the class label is assumed to be the last column.
        """
        with open(fname, "r", encoding="utf-8") as f:
            reader = csv.reader(f)

            if headers:
                self._set_headers(next(reader), class_label)
            else:
                first_row = next(reader)
                self.headers = [f"col_{i}" for i in range(len(first_row) - 1)] + ["class"]
                self.klass = "class"
                self._add_row(first_row)

            for row in reader:
                self._add_row(row)

    def _add_row(self, row: list[str]):
        record = {header: value.strip() for header, value in zip(self.headers, row)}
        self.data.append(record)

        class_value = record["class"]
        if class_value not in self.unique_classes:
            self.unique_classes.append(class_value)

    def _set_headers(self, raw_headers: list[str], class_label: str):
        cleaned_class_label = self._clean_label(class_label)
        cleaned_headers = [self._clean_label(h) for h in raw_headers]

        if cleaned_class_label not in cleaned_headers:
            raise ValueError(
                f"Could not find a header matching the given class label: {class_label}"
            )

        self.klass = cleaned_class_label
        idx = cleaned_headers.index(cleaned_class_label)
        cleaned_headers[idx] = "class"
        self.headers = cleaned_headers

    @staticmethod
    def _clean_label(label: str) -> str:
        return label.strip().lower().replace(" ", "_")

    def __str__(self):
        return str(self.data)




class DataPoint:
    def __init__(self):
        pass


# class DataPoint:
#     def __init__(self, home_owner, marital_status, annual_income, defaulted_borrower):
#         self.home_owner = home_owner
#         self.marital_status = marital_status
#         self.annual_income = annual_income
#         self.defaulted_borrower = defaulted_borrower


def create_datapoint(datapoint):
    home_owner, marital_status, annual_income, defaulted_borrower = datapoint
    return DataPoint(home_owner, marital_status, annual_income, defaulted_borrower)


def create_datapoints(datapoints):
    data = []
    for datapoint in datapoints:
        data.append(create_datapoint(datapoint))
    return data


class Node:
    def __init__(self, samples):
        self.samples = self.generate_samples(samples)

    def generate_samples(samples):
        pass


def entropy(counts):
    """ Entropy of a node, in bits.

        Args:
            counts: sequence of class counts, one entry per class.
    """

    s = sum(counts)
    res = 0
    for v in counts:
        res += ((v / s) * (math.log2(v / s)))
    return -(res)

# def weighted_entropy()


def main():
    # print(entropy([13, 20]))
    # print(entropy([4, 3]))
    # print(entropy([3, 4]) - (3/7 * entropy([0, 3])) + (4/7 * entropy([1, 3])))
    data_construct = DataScraper()
    data_construct.from_csv("cs445/entropy/data-2.csv", True, "Defaulted Borrower")
    print(data_construct)

if __name__ == "__main__":
    main()
