from dataclasses import dataclass, field

from cypherdataframe.garner_domain.BranchMaker import BranchMaker
from cypherdataframe.garner_domain.properties_defaults import \
    MEASURE_RELATIONSHIP, MEASURE_RETURN_POSTFIX
from cypherdataframe.model.Property import Property


@dataclass
class MeasureBranch(BranchMaker):
    props: list[Property]
    post_label: str | None = None
    relationship: str = field(default_factory=lambda: MEASURE_RELATIONSHIP)
    relationship_postfix: str | None = field(default_factory=lambda: MEASURE_RETURN_POSTFIX)
    required: bool = False
    archived: bool = False
    domain_label: str | None = None

