import re


class QueryTransformer:
    def rewrite(self, query: str) -> str:
        return " ".join(query.strip().split())

    def multi_query(self, query: str) -> list[str]:
        normalized = self.rewrite(query)
        return [
            normalized,
            f"evidence supporting {normalized}",
            f"policy requirements related to {normalized}",
        ]

    def decompose(self, query: str) -> list[str]:
        normalized = self.rewrite(query)
        parts = [
            part.strip()
            for part in re.split(r"\b(?:and|then|after|before|while)\b|\?", normalized, flags=re.I)
            if part.strip()
        ]
        return parts or [normalized]

