from dataclasses import dataclass, field

from cypherdataframe.garner_domain.BranchMaker import BranchMaker
from cypherdataframe.garner_domain.properties_defaults import ID_PROP
from cypherdataframe.model.LabelNode import LabelNode
from cypherdataframe.model.Property import Property
from cypherdataframe.model.Query import Query

@dataclass
class LogisticsTableQuery:
    branchMakers: list[BranchMaker]
    label: str
    post_label: str | None = None
    return_id: str = "l"
    props: list[Property] = field(default_factory=lambda: [ID_PROP])
    disable_scan: bool = False
    def to_query(self, skip: int | None = None, limit: int | None = None):
        return Query(
            LabelNode(
                return_id=self.return_id,
                label=self.label,
                properties=self.props,
                collect=False,
                post_label_str=self.post_label
            ),
            branches=[b.to_branch() for b in self.branchMakers],
            disable_scan=self.disable_scan,
            skip=skip,
            limit=limit
        )



