from dataclasses import dataclass

from cypherdataframe.model.LabelNode import LabelNode


# optional match(corenode)<back>-[<relationship>]-<forward>(<label>:<label>)

@dataclass(frozen=True)
class Branch:
    relationship: str | None
    away_from_core: bool | None
    branch_node: LabelNode
    optional: bool

    def property_fragments_by_cypher_assignments(
            self
            , core_node_assignment: str
            ):
        prop_by = {}
        if self.relationship == None:
            prop_by = {
               self.relationship_cypher_assignment(): (
                    f" type({self.relationship_cypher_assignment()})"
                    f" as {self.relationship_cypher_assignment()} "
                )
            }
        if self.away_from_core is None:
            prop_by = prop_by | {
                self.relationship_direction_cypher_assignment(): (
                    f" (startNode({self.relationship_cypher_assignment()}) = {core_node_assignment})"
                    f" as {self.relationship_direction_cypher_assignment()} "
                )
            }
        return prop_by

    def relationship_direction_cypher_assignment(self) -> str:
        return self.relationship_cypher_assignment()+"d"
    def relationship_cypher_assignment(self) -> str:
        return f"{self.branch_node.label.lower()}_rel"

    def relationship_cypher_final_assignment(self) -> str | None:
        if self.relationship == None:
            return f"TYPE({self.relationship_cypher_assignment()}) as {self.relationship_cypher_assignment()}"
        else:
            return None

    def match_statement(self, corenode: LabelNode, with_assignment: bool):
        if self.branch_node.post_label_str:
            post_label = self.branch_node.post_label_str
        else:
            post_label = ""

        if self.away_from_core == True:
            back = ''
            forward = '>'
        elif self.away_from_core == False:
            back = '<'
            forward = ''
        else:
            back = ''
            forward = ''

        if with_assignment:
            node_id = self.branch_node.return_id
        else:
            node_id = ""

        if self.optional:
            optional = "optional"
        else:
            optional = ""

        if self.relationship == None:
            relationship_str = self.relationship_cypher_assignment()
        else:
            relationship_str = f":{self.relationship}"

        fragment = (
            f" {optional} " 
            f"match({corenode.return_id}){back}" 
            f"-[{relationship_str}]-"
            f"{forward}({node_id}:{self.branch_node.label}{post_label})"
        )

        return fragment



