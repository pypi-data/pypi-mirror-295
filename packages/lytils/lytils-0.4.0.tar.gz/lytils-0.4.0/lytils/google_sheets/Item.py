from dataclasses import dataclass, fields


@dataclass
class Item:
    def to_dict(self):
        """
        Converts the dataclass attributes to a dictionary.

        Returns:
            dict: A dictionary with attribute names as keys and their values.
        """
        return {field.name: getattr(self, field.name) for field in fields(self)}
