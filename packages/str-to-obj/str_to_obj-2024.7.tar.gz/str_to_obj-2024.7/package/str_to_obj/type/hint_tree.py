"""
Copyright CNRS/Inria/UniCA
Contributor(s): Eric Debreuve (eric.debreuve@cnrs.fr) since 2023
SEE COPYRIGHT NOTICE BELOW
"""

import dataclasses as d
import re as regx
import types as t
import typing as h

from logger_36.format import FormattedMessage
from str_to_obj.catalog.choices import choices_t
from str_to_obj.task.inspection import HintComponents
from str_to_obj.type.annotation import annotation_t
from str_to_obj.type.hint import (
    any_hint_h,
    complex_hint_additions_h,
    non_complex_hint_h,
    simple_hint_h,
)


@d.dataclass(slots=True, repr=False, eq=False)
class _hint_node_t:
    """
    Leave elements to the tree.
    literal_s: the accepted (literal) values if the hint is a typing.Literal, None
    otherwise.
    """

    type: non_complex_hint_h | t.UnionType | t.EllipsisType | type[t.NoneType]
    annotations: tuple[annotation_t, ...] = d.field(default_factory=tuple)
    literal_s: tuple[h.Any, ...] | None = None


@d.dataclass(slots=True, repr=False, eq=False)
class hint_t(_hint_node_t):
    """
    elements: tuple if the hint is a container, None otherwise. In terms of tree
    structure, it plays the role of the (hint) node children.
    """
    elements: tuple[h.Self, ...] | None = None

    @classmethod
    def NewForHint(cls, hint: any_hint_h | complex_hint_additions_h, /) -> h.Self:
        """
        Note that type hints cannot translate into hint trees with an OR-node having a child
        OR-node. For example: str | (int | float) is interpreted as str | int | float. This
        is important when creating a type selector for multi-type parameters since only
        direct child nodes are taken into account for widget creation, so these nodes must
        be types, not an OR subtree.
        """
        if isinstance(hint, annotation_t):
            # This is a common mistake in specifications.
            raise ValueError(
                FormattedMessage(
                    "Invalid hint type", actual=type(hint).__name__, expected=any_hint_h
                )
            )

        # Dealing with complex_hint_additions_h first.
        if hint is Ellipsis:
            return cls(type=t.EllipsisType)
        if (hint is None) or (hint is t.NoneType):
            return cls(type=t.NoneType)

        # nnts: Do not use "annotations" since it shadows __future__.annotations.
        raw_hint, nnts = HintComponents(hint)

        if (origin := h.get_origin(raw_hint)) is None:
            return cls(type=raw_hint, annotations=nnts)

        # Handled types: list, set, tuple, with sets using the dict delimiters { and }.
        if origin is dict:
            raise TypeError(f"Unhandled type: {origin.__name__}.")

        if origin is h.Literal:
            literal_s = h.get_args(raw_hint)
            if any(isinstance(_elm, choices_t) for _elm in nnts):
                raise ValueError(
                    f"Literal hint with values {literal_s} "
                    f"must not be annotated with {choices_t.__name__} as it leads to "
                    f"either redundancy or mismatch."
                )
            stripes = tuple(set(type(_elm) for _elm in literal_s))
            if stripes.__len__() > 1:
                origin = t.UnionType
                elements = tuple(cls.NewForHint(_elm) for _elm in stripes)
            else:
                origin = stripes[0]
                elements = None
            return cls(
                type=origin, annotations=nnts, elements=elements, literal_s=literal_s
            )

        if origin is h.Union:
            origin = t.UnionType
        # get_args returns NoneType for None. This must be taken into account above.
        elements = tuple(cls.NewForHint(_elm) for _elm in h.get_args(raw_hint))
        return cls(type=origin, annotations=nnts, elements=elements)

    @property
    def all_annotations(self) -> list[annotation_t]:
        """"""
        output = list(self.annotations)

        if self.elements is not None:
            for element in self.elements:
                output.extend(element.all_annotations)

        return output

    @property
    def template(self) -> simple_hint_h | dict[int, h.Any] | None:
        """"""
        if self.type is t.NoneType:
            return None

        if self.type is t.UnionType:
            return {_key: _elm.template for _key, _elm in enumerate(self.elements)}

        if self.elements is None:
            return self.type

        try:
            output = self.type(_elm.template for _elm in self.elements)
        except TypeError:
            output = None
        if output is not None:
            return output

        # TODO: Does it work all the time?
        if self.elements.__len__() == 1:
            # For example, self.type is typing.Sequence.
            return self.type[self.elements[0].template]

        # TODO: Can something better be done?
        return self.type

    @property
    def template_as_str(self) -> str:
        """"""
        output = (
            str(self.template)
            .replace(str(t.EllipsisType), "...")
            .replace("<class '", "")
            .replace("'>", "")
        )
        output = regx.sub(r"{\d: ", "{", output, flags=regx.ASCII)
        output = regx.sub(r", \d:", " |", output, flags=regx.ASCII)

        return output


# Potential additions for _hint_node_t:
# def __str__(self) -> str:
#     """"""
#     return text_t.from_markup(self.__rich__()).plain
#
# def __rich__(self) -> str:
#     """"""
#     output = [TypeAsRichStr(self)]
#
#     names = (_fld.name for _fld in d.fields(self))
#     for name in names:
#         value = getattr(self, name)
#         output.append(f"    {NameValueTypeAsRichStr(name, value, separator='@=@')}")
#
#     output = AlignedOnSeparator(output, "@=@", " = ")
#
#     return "\n".join(output)

"""
COPYRIGHT NOTICE

This software is governed by the CeCILL  license under French law and
abiding by the rules of distribution of free software.  You can  use,
modify and/ or redistribute the software under the terms of the CeCILL
license as circulated by CEA, CNRS and INRIA at the following URL
"http://www.cecill.info".

As a counterpart to the access to the source code and  rights to copy,
modify and redistribute granted by the license, users are provided only
with a limited warranty  and the software's author,  the holder of the
economic rights,  and the successive licensors  have only  limited
liability.

In this respect, the user's attention is drawn to the risks associated
with loading,  using,  modifying and/or developing or reproducing the
software by the user in light of its specific status of free software,
that may mean  that it is complicated to manipulate,  and  that  also
therefore means  that it is reserved for developers  and  experienced
professionals having in-depth computer knowledge. Users are therefore
encouraged to load and test the software's suitability as regards their
requirements in conditions enabling the security of their systems and/or
data to be ensured and,  more generally, to use and operate it in the
same conditions as regards security.

The fact that you are presently reading this means that you have had
knowledge of the CeCILL license and that you accept its terms.

SEE LICENCE NOTICE: file README-LICENCE-utf8.txt at project source root.

This software is being developed by Eric Debreuve, a CNRS employee and
member of team Morpheme.
Team Morpheme is a joint team between Inria, CNRS, and UniCA.
It is hosted by the Centre Inria d'Université Côte d'Azur, Laboratory
I3S, and Laboratory iBV.

CNRS: https://www.cnrs.fr/index.php/en
Inria: https://www.inria.fr/en/
UniCA: https://univ-cotedazur.eu/
Centre Inria d'Université Côte d'Azur: https://www.inria.fr/en/centre/sophia/
I3S: https://www.i3s.unice.fr/en/
iBV: http://ibv.unice.fr/
Team Morpheme: https://team.inria.fr/morpheme/
"""
