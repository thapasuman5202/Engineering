from itertools import product
from typing import Dict, List, Optional


class Negotiator:
    """Generate design variants by exploring combinations of attributes.

    The negotiator holds a set of base options representing design attributes
    (e.g. color, material). ``generate_variants`` combines these attributes using
    a Cartesian product to produce concrete variant strings.
    """

    def __init__(self, base_options: Optional[Dict[str, List[str]]] = None) -> None:
        self.base_options: Dict[str, List[str]] = base_options or {
            "color": ["red", "blue"],
            "material": ["steel", "plastic"],
            "finish": ["matte", "gloss"],
        }

    def generate_variants(
        self, options: Optional[Dict[str, List[str]]] = None
    ) -> List[str]:
        """Return all variant combinations.

        Args:
            options: Optional mapping of attribute name to possible values. If not
                provided, the negotiator's ``base_options`` are used.

        Returns:
            List[str]: Variant names created by joining attribute choices with
            underscores. An empty options mapping yields an empty list.
        """

        opts = options or self.base_options
        if not opts:
            return []

        combinations = product(*opts.values())
        return ["_".join(map(str, combo)) for combo in combinations]


negotiator = Negotiator()

