"""
Copyright CNRS/Inria/UniCA
Contributor(s): Eric Debreuve (eric.debreuve@cnrs.fr) since 2023
SEE COPYRIGHT NOTICE BELOW
"""

import dataclasses as d
import types as t
import typing as h

from logger_36 import LOGGER
from str_to_obj.type.annotation import annotation_t
from str_to_obj.type.hint import any_hint_h
from str_to_obj.type.type import type_t


@d.dataclass(slots=True, repr=False, eq=False)
class collection_t(annotation_t):
    ACCEPTED_TYPES: h.ClassVar[tuple[type, ...]] = (list, set, tuple)

    # Items of any type but None.
    ANY_ITEMS_TYPES: h.ClassVar[h.Any | tuple[h.Any, ...]] = h.Any
    ANY_LENGTH: h.ClassVar[tuple[int, ...]] = (0,)

    items_types: any_hint_h | tuple[any_hint_h, ...] | type_t | tuple[type_t, ...] = (
        ANY_ITEMS_TYPES
    )
    lengths: int | tuple[int, ...] = ANY_LENGTH

    def __post_init__(self) -> None:
        """"""
        original_item_types = self.items_types
        original_lengths = self.lengths

        if isinstance(self.items_types, h.Sequence):
            items_types = []
            for stripe in self.items_types:
                if isinstance(stripe, type_t):
                    items_types.append(stripe)
                else:
                    items_types.append(type_t.NewForHint(stripe))
            self.items_types = items_types
        elif not isinstance(self.items_types, type_t):
            self.items_types = type_t.NewForHint(self.items_types)

        if isinstance(self.lengths, int):
            self.lengths = (self.lengths,)
        else:
            self.lengths = tuple(sorted(self.lengths))

        with LOGGER.AddedContextLevel("Collection Annotation"):
            if isinstance(self.items_types, h.Sequence):
                if max(self.lengths) > self.items_types.__len__():
                    LOGGER.StageIssue(
                        f'Allowed length(s) ("{original_lengths}") must not exceed '
                        f"the length of the item types sequence "
                        f'("{original_item_types}")'
                    )
            if self.lengths != self.__class__.ANY_LENGTH:
                for length in self.lengths:
                    if (not isinstance(length, int)) or (length < 0):
                        LOGGER.StageIssue(
                            f"Invalid length in {self.lengths}",
                            actual=length,
                            expected="strictly positive integer",
                        )

    @classmethod
    def NewForType(
        cls,
        stripe: any_hint_h | tuple[any_hint_h, ...] | type_t | tuple[type_t, ...],
        /,
    ) -> h.Self:
        """"""
        if not isinstance(stripe, (type_t | tuple[type_t, ...])):
            stripe = type_t.NewForHint(stripe)

        if stripe.type not in cls.ACCEPTED_TYPES:
            with LOGGER.AddedContextLevel("Collection Annotation"):
                LOGGER.StageIssue(
                    f"Invalid type",
                    actual=stripe.type.__name__,
                    expected=", ".join(_elm.__name__ for _elm in cls.ACCEPTED_TYPES),
                )
                return collection_t()

        if stripe.elements is None:
            return collection_t()

        if (n_elements := stripe.elements.__len__()) == 1:
            return collection_t(items_types=stripe.elements[0], lengths=1)

        if (n_elements == 2) and (stripe.elements[1].type is t.EllipsisType):
            return collection_t(items_types=stripe.elements[0], lengths=cls.ANY_LENGTH)

        return collection_t(items_types=stripe.elements, lengths=n_elements)

    def ValueIssues(self, value: list | set | tuple | h.Any, /) -> list[str]:
        """"""
        issues = annotation_t.ValueIssues(self, value)
        if issues.__len__() > 0:
            return issues

        if (self.lengths != self.__class__.ANY_LENGTH) and (
            value.__len__() not in self.lengths
        ):
            return [
                f"{value}: Sequence of invalid length; "
                f"Expected={' or '.join(map(str, self.lengths))}."
            ]

        if isinstance(self.items_types, h.Sequence):
            if value.__len__() > self.items_types.__len__():
                return [
                    f"{value}: Sequence too long. "
                    f"Expected=At most {self.items_types.__len__()} element(s)."
                ]

            output = []
            for stripe, element in zip(self.items_types, value):
                output.extend(stripe.ValueIssues(element))
            return output

        stripe: type_t = self.items_types
        output = []
        for element in value:
            output.extend(stripe.ValueIssues(element))
        return output


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
