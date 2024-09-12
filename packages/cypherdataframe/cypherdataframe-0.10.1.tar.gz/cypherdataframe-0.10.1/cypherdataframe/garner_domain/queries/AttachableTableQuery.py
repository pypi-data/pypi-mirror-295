from dataclasses import dataclass, field

from cypherdataframe.garner_domain.BranchMaker import BranchMaker
from cypherdataframe.garner_domain.properties_defaults import ID_PROP
from cypherdataframe.garner_domain.queries.LogisticsTableQuery import \
    LogisticsTableQuery
from cypherdataframe.model.LabelNode import LabelNode
from cypherdataframe.model.Property import Property
from cypherdataframe.model.Query import Query

@dataclass
class AttachableTableQuery:
    attachable_label: str
    domain_label: str
    attachable_props: list[Property]
    post_label: str | None = None
    attachable_return_id: str = "a"
    disable_scan: bool = False
    relationship: str | None = None
    away_from_core: str | None = None

    def to_query(self, skip: int | None = None, limit: int | None = None):
        domain_branch = BranchMaker(
            props=[ID_PROP],
            label=self.domain_label,
            post_label=None,
            relationship=self.relationship,
            relationship_postfix=None,
            required=True,
            away_from_core=self.away_from_core,
            domain_label=None
        )

        table_current = LogisticsTableQuery(
            branchMakers=[domain_branch],
            label=self.attachable_label,
            post_label=self.post_label,
            return_id=self.attachable_return_id,
            props=self.attachable_props,
            disable_scan=self.disable_scan
        )
        return table_current.to_query(skip=skip, limit=limit)



