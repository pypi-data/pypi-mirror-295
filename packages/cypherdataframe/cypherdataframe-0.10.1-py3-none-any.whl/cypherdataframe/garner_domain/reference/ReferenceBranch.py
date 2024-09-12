from dataclasses import dataclass, field

from cypherdataframe.garner_domain.BranchMaker import BranchMaker
from cypherdataframe.garner_domain.properties_defaults import REFERENCED_RELATIONSHIP, REFERENCED_RETURN_POSTFIX
from cypherdataframe.model.Property import Property


@dataclass
class ReferenceBranch(BranchMaker):
    props: list[Property]
    post_label: str | None = None
    relationship: str = field(default_factory=lambda: REFERENCED_RELATIONSHIP)
    relationship_postfix: str | None = field(default_factory=lambda: REFERENCED_RETURN_POSTFIX)
    required: bool = False
    away_from_core: bool = True
    domain_label: str | None = None
