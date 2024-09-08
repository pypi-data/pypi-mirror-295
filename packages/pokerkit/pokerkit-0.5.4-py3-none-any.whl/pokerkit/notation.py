""":mod:`pokerkit.notation` implements classes related to poker
notations.
"""

from __future__ import annotations

from collections.abc import Callable, Iterable, Iterator
from collections import defaultdict, deque
from dataclasses import asdict, dataclass, field, fields, KW_ONLY
from functools import partial
from operator import itemgetter
from tomllib import loads as loads_toml
from typing import Any, ClassVar, BinaryIO
from warnings import warn
import datetime

from pokerkit.state import (
    Automation,
    BoardDealing,
    BringInPosting,
    CheckingOrCalling,
    CompletionBettingOrRaisingTo,
    Folding,
    HoleCardsShowingOrMucking,
    HoleDealing,
    StandingPatOrDiscarding,
    State,
)
from pokerkit.games import (
    FixedLimitBadugi,
    FixedLimitDeuceToSevenLowballTripleDraw,
    FixedLimitOmahaHoldemHighLowSplitEightOrBetter,
    FixedLimitRazz,
    FixedLimitSevenCardStud,
    FixedLimitSevenCardStudHighLowSplitEightOrBetter,
    FixedLimitTexasHoldem,
    NoLimitDeuceToSevenLowballSingleDraw,
    NoLimitShortDeckHoldem,
    NoLimitTexasHoldem,
    Poker,
    PotLimitOmahaHoldem,
)
from pokerkit.utilities import Card, divmod, parse_value, rake


@dataclass
class HandHistory(Iterable[State]):
    """The class for hand histories.

    :param variant: The variant name. For more information, please refer
                    to :attr:`pokerkit.notation.HandHistory.variant`.
    :param ante_trimming_status: The ante trimming status. For more
                                 information, please refer to
                                 :attr:`pokerkit.notation.HandHistory.ante_trimming_status`.
    :param antes: The antes. For more information, please refer to
                  :attr:`pokerkit.notation.HandHistory.antes`.
    :param blinds_or_straddles: The blinds or straddles. For more
                                information, please refer to
                                :attr:`pokerkit.notation.HandHistory.blinds_or_straddles`.
    :param bring_in: The bring-in. For more information, please refer to
                     :attr:`pokerkit.notation.HandHistory.bring_in`.
    :param small_bet: The small bet. For more information, please refer
                      to
                      :attr:`pokerkit.notation.HandHistory.small_bet`.
    :param big_bet: The big bet. For more information, please refer to
                    :attr:`pokerkit.notation.HandHistory.big_bet`.
    :param min_bet: The minimum bet. For more information, please refer
                    to :attr:`pokerkit.notation.HandHistory.min_bet`.
    :param starting_stacks: The starting stacks. For more information,
                            please refer to
                            :attr:`pokerkit.notation.HandHistory.starting_stacks`.
    :param actions: The actions. For more information, please refer to
                    :attr:`pokerkit.notation.HandHistory.actions`.
    :param author: The author. For more information, please refer to
                   :attr:`pokerkit.notation.HandHistory.author`.
    :param event: The event. For more information, please refer to
                  :attr:`pokerkit.notation.HandHistory.event`.
    :param url: The url. For more information, please refer to
                :attr:`pokerkit.notation.HandHistory.url`.
    :param address: The address. For more information, please refer to
                    :attr:`pokerkit.notation.HandHistory.address`.
    :param city: The city. For more information, please refer to
                 :attr:`pokerkit.notation.HandHistory.city`.
    :param region: The region. For more information, please refer to
                   :attr:`pokerkit.notation.HandHistory.region`.
    :param postal_code: The postal code. For more information, please
                        refer to
                        :attr:`pokerkit.notation.HandHistory.postal_code`.
    :param country: The country. For more information, please refer to
                    :attr:`pokerkit.notation.HandHistory.country`.
    :param time: The time. For more information, please refer to
                 :attr:`pokerkit.notation.HandHistory.time`.
    :param time_zone: The time zone. For more information, please refer
                      to
                      :attr:`pokerkit.notation.HandHistory.time_zone`.
    :param day: The day. For more information, please refer to
                :attr:`pokerkit.notation.HandHistory.day`.
    :param month: The month. For more information, please refer to
                  :attr:`pokerkit.notation.HandHistory.month`.
    :param year: The year. For more information, please refer to
                 :attr:`pokerkit.notation.HandHistory.year`.
    :param hand: The hand number. For more information, please refer to
                 :attr:`pokerkit.notation.HandHistory.hand`.
    :param level: The level. For more information, please refer to
                  :attr:`pokerkit.notation.HandHistory.level`.
    :param seats: The seat numbers. For more information, please refer
                  to :attr:`pokerkit.notation.HandHistory.seats`.
    :param seat_count: The number of seats. For more information, please
                       refer to
                       :attr:`pokerkit.notation.HandHistory.seat_count`.
    :param table: The table number. For more information, please refer
                  to :attr:`pokerkit.notation.HandHistory.table`.
    :param players: The player names. For more information, please refer
                    to :attr:`pokerkit.notation.HandHistory.players`.
    :param finishing_stacks: The finishing stacks. For more information,
                             please refer to
                             :attr:`pokerkit.notation.HandHistory.finishing_stacks`.
    :param currency: The currency. For more information, please refer to
                     :attr:`pokerkit.notation.HandHistory.currency`.
    :param time_limit: The time limit. For more information, please
                       refer to
                       :attr:`pokerkit.notation.HandHistory.time_limit`.
    :param time_banks: The time banks. For more information, please
                       refer to
                       :attr:`pokerkit.notation.HandHistory.time_banks`.
    :param user_defined_fields: The user-defined fields. For more
                                information, please refer to
                                :attr:`pokerkit.notation.HandHistory.user_defined_fields`.
    :param automations: The automations. For more information, please
                        refer to
                        :attr:`pokerkit.notation.HandHistory.automations`.
    :param divmod: The divmod function. For more information, please
                   refer to :attr:`pokerkit.notation.HandHistory.divmod`.
    :param rake: The rake function. For more information, please refer
                 to :attr:`pokerkit.notation.HandHistory.rake`.
    :param parse_value: The value parsing function. For more
                        information, please refer to
                        :attr:`pokerkit.notation.HandHistory.parse_value`.
    """

    game_types: ClassVar[dict[str, type[Poker]]] = {
        'FT': FixedLimitTexasHoldem,
        'NT': NoLimitTexasHoldem,
        'NS': NoLimitShortDeckHoldem,
        'PO': PotLimitOmahaHoldem,
        'FO/8': FixedLimitOmahaHoldemHighLowSplitEightOrBetter,
        'F7S': FixedLimitSevenCardStud,
        'F7S/8': FixedLimitSevenCardStudHighLowSplitEightOrBetter,
        'FR': FixedLimitRazz,
        'N2L1D': NoLimitDeuceToSevenLowballSingleDraw,
        'F2L3D': FixedLimitDeuceToSevenLowballTripleDraw,
        'FB': FixedLimitBadugi,
    }
    """The game codes and the corresponding game types."""
    variants: ClassVar[dict[type[Poker], str]] = dict(
        zip(game_types.values(), game_types.keys()),
    )
    """The game types and the corresponding game codes."""
    required_field_names: ClassVar[dict[str, tuple[str, ...]]] = {
        'FT': (
            'variant',
            'antes',
            'blinds_or_straddles',
            'small_bet',
            'big_bet',
            'starting_stacks',
            'actions',
        ),
        'NT': (
            'variant',
            'antes',
            'blinds_or_straddles',
            'min_bet',
            'starting_stacks',
            'actions',
        ),
        'NS': (
            'variant',
            'antes',
            'blinds_or_straddles',
            'min_bet',
            'starting_stacks',
            'actions',
        ),
        'PO': (
            'variant',
            'antes',
            'blinds_or_straddles',
            'min_bet',
            'starting_stacks',
            'actions',
        ),
        'FO/8': (
            'variant',
            'antes',
            'blinds_or_straddles',
            'small_bet',
            'big_bet',
            'starting_stacks',
            'actions',
        ),
        'F7S': (
            'variant',
            'antes',
            'bring_in',
            'small_bet',
            'big_bet',
            'starting_stacks',
            'actions',
        ),
        'F7S/8': (
            'variant',
            'antes',
            'bring_in',
            'small_bet',
            'big_bet',
            'starting_stacks',
            'actions',
        ),
        'FR': (
            'variant',
            'antes',
            'bring_in',
            'small_bet',
            'big_bet',
            'starting_stacks',
            'actions',
        ),
        'N2L1D': (
            'variant',
            'antes',
            'blinds_or_straddles',
            'min_bet',
            'starting_stacks',
            'actions',
        ),
        'F2L3D': (
            'variant',
            'antes',
            'blinds_or_straddles',
            'small_bet',
            'big_bet',
            'starting_stacks',
            'actions',
        ),
        'FB': (
            'variant',
            'antes',
            'blinds_or_straddles',
            'small_bet',
            'big_bet',
            'starting_stacks',
            'actions',
        ),
    }
    """The required field names."""
    optional_field_names: ClassVar[tuple[str, ...]] = (
        'author',
        'event',
        'url',
        'address',
        'city',
        'region',
        'postal_code',
        'country',
        'time',
        'time_zone',
        'day',
        'month',
        'year',
        'hand',
        'level',
        'seats',
        'seat_count',
        'table',
        'players',
        'finishing_stacks',
        'currency',
        'ante_trimming_status',
        'time_limit',
        'time_banks',
    )
    """The optional field names."""
    ACPC_PROTOCOL_VARIANTS = {'FT', 'NT'}
    """The variant codes supported by the ACPC protocol."""
    PLURIBUS_PROTOCOL_VARIANTS = {'NT'}
    """The variant codes supported by the Pluribus protocol."""
    _: KW_ONLY
    variant: str
    """The variant name."""
    ante_trimming_status: bool = False
    """The ante trimming status."""
    antes: list[int]
    """The antes."""
    blinds_or_straddles: list[int] | None = None
    """The blinds or straddles."""
    bring_in: int | None = None
    """The bring-in."""
    small_bet: int | None = None
    """The small bet."""
    big_bet: int | None = None
    """The big bet."""
    min_bet: int | None = None
    """The minimum bet."""
    starting_stacks: list[int]
    """The starting stacks."""
    actions: list[str]
    """The actions."""
    author: str | None = None
    """The author."""
    event: str | None = None
    """The event."""
    url: str | None = None
    """The url."""
    address: str | None = None
    """The address."""
    city: str | None = None
    """The city."""
    region: str | None = None
    """The region."""
    postal_code: str | None = None
    """The postal code."""
    country: str | None = None
    """The country."""
    time: datetime.time | None = None
    """The time."""
    time_zone: str | None = None
    """The time zone."""
    day: int | None = None
    """The day."""
    month: int | None = None
    """The month."""
    year: int | None = None
    """The year."""
    hand: int | None = None
    """The hand number."""
    level: int | None = None
    """The level."""
    seats: list[int] | None = None
    """The seat numbers."""
    seat_count: int | None = None
    """The number of seats."""
    table: int | None = None
    """The table number."""
    players: list[str] | None = None
    """The player names."""
    finishing_stacks: list[int] | None = None
    """The finishing stacks."""
    currency: str | None = None
    """The currency."""
    time_limit: int | None = None
    """The time limit."""
    time_banks: list[int] | None = None
    """The time banks."""
    user_defined_fields: dict[str, Any] = field(default_factory=dict)
    """The user-defined fields."""
    automations: tuple[Automation, ...] = (
        Automation.ANTE_POSTING,
        Automation.BET_COLLECTION,
        Automation.BLIND_OR_STRADDLE_POSTING,
        Automation.CARD_BURNING,
        Automation.HAND_KILLING,
        Automation.CHIPS_PUSHING,
        Automation.CHIPS_PULLING,
    )
    """The automations."""
    divmod: Callable[[int, int], tuple[int, int]] = divmod
    """The divmod function."""
    rake: Callable[[int], tuple[int, int]] = partial(rake, rake=0)
    """The rake function."""
    parse_value: Callable[[str], int] = parse_value
    """The value parsing function."""

    @classmethod
    def _filter_non_fields(cls, **kwargs: Any) -> dict[str, Any]:
        field_names = {field.name for field in fields(cls)}
        filtered_fields = {}

        if 'user_defined_fields' in kwargs:
            filtered_fields['user_defined_fields'] = kwargs.pop(
                'user_defined_fields',
            )
        else:
            filtered_fields['user_defined_fields'] = {}

        for key, value in kwargs.items():
            if key in field_names:
                filtered_fields[key] = value
            else:
                if not key.startswith('_'):
                    warn(
                        (
                            f'The field {repr(key)} is an unexpected field and'
                            ' should probably be prefixed with an underscore'
                            ' character \'_\'.'
                        ),
                    )

                filtered_fields['user_defined_fields'][key] = value

        return filtered_fields

    @classmethod
    def loads(
            cls,
            s: str,
            *,
            parse_value: Callable[[str], int] = parse_value,
            **kwargs: Any,
    ) -> HandHistory:
        """Load PHH from ``str`` object.

        :param s: The ``str`` object.
        :param parse_value: The value parsing function.
        :param kwargs: The metadata.
        :return: The hand history object.
        """
        return cls(
            **cls._filter_non_fields(
                **kwargs | loads_toml(s, parse_float=parse_value),
            ),
        )

    @classmethod
    def load(cls, fp: BinaryIO, **kwargs: Any) -> HandHistory:
        """Load PHH from a file pointer.

        :param fp: The file pointer.
        :param kwargs: The metadata.
        :return: The hand history object.
        """
        return cls.loads(fp.read().decode(), **kwargs)

    @classmethod
    def from_game_state(
            cls,
            game: Poker,
            state: State,
            compression_status: bool = True,
            **kwargs: Any,
    ) -> HandHistory:
        """Create a hand history from game state.

        :param game: The game.
        :param state: The state.
        :param compression_status: The compression status.
        :param kwargs: The metadata.
        :return: The hand history.
        """

        action: str | None

        def append_dealing_actions() -> None:
            nonlocal action

            for player_index in hole_cards:
                if hole_cards[player_index]:
                    action = (
                        f'd dh p{player_index + 1} '
                        + ''.join(map(repr, hole_cards[player_index]))
                    )

                    actions.append(action.strip())
                    hole_cards[player_index].clear()

            if board_cards:
                action = 'd db ' + ''.join(map(repr, board_cards))

                actions.append(action.strip())
                board_cards.clear()

        variant = cls.variants[type(game)]
        actions = []
        hole_cards = defaultdict[int, list[Card]](list)
        board_cards = list[Card]()

        for operation in state.operations:
            if (
                    not compression_status
                    or not isinstance(operation, HoleDealing | BoardDealing)
            ):
                append_dealing_actions()
            if isinstance(operation, BoardDealing):
                board_cards.extend(operation.cards)

                action = None
            elif isinstance(operation, HoleDealing):
                hole_cards[operation.player_index].extend(operation.cards)

                action = None
            elif isinstance(operation, StandingPatOrDiscarding):
                action = (
                    f'p{operation.player_index + 1} sd '
                    + ''.join(map(repr, operation.cards))
                )
            elif isinstance(operation, BringInPosting):
                action = f'p{operation.player_index + 1} pb'
            elif isinstance(operation, Folding):
                action = f'p{operation.player_index + 1} f'
            elif isinstance(operation, CheckingOrCalling):
                action = f'p{operation.player_index + 1} cc'
            elif isinstance(operation, CompletionBettingOrRaisingTo):
                action = (
                    f'p{operation.player_index + 1} cbr {operation.amount}'
                )
            elif isinstance(operation, HoleCardsShowingOrMucking):
                action = (
                    f'p{operation.player_index + 1} sm '
                    + ''.join(map(repr, operation.hole_cards))
                )
            else:
                action = None

            if operation.commentary is not None:
                if action is None:
                    action = f'# {operation.commentary}'
                else:
                    action = action.strip() + f' # {operation.commentary}'

            if action is not None:
                actions.append(action.strip())

        append_dealing_actions()
        kwargs.setdefault('variant', variant)
        kwargs.setdefault('actions', actions)
        kwargs.setdefault('starting_stacks', list(state.starting_stacks))

        field_names = {field.name for field in fields(cls)}

        for name in cls.required_field_names[variant]:
            if name not in field_names:
                continue

            try:
                attribute = getattr(game, name)
            except AttributeError:
                try:
                    attribute = getattr(state, name)
                except AttributeError:
                    continue

            if isinstance(attribute, Iterable):
                attribute = list(attribute)

            kwargs.setdefault(name, attribute)

        return HandHistory(**cls._filter_non_fields(**kwargs))

    def __iter__(self) -> Iterator[State]:
        yield from map(itemgetter(0), self.state_actions)

    @property
    def state_actions(self) -> Iterator[tuple[State, str | None]]:
        """Iterate through state-actions.

        If an action from the
        :attr:`pokerkit.notation.HandHistory.actions` field was just
        applied, the ``str`` representation of the action is yielded
        alongside the newly transitioned state. Otherwise, the
        corresponding second value of the pair is ``None``.

        :return: The state actions.
        """
        state = self.create_state()
        actions = deque(self.actions)

        yield state, None

        while state.status:
            action = None

            if state.can_post_ante():
                state.post_ante()
            elif state.can_collect_bets():
                state.collect_bets()
            elif state.can_post_blind_or_straddle():
                state.post_blind_or_straddle()
            elif state.can_burn_card():
                state.burn_card('??')

                if Automation.CARD_BURNING in self.automations:
                    continue
            elif state.can_kill_hand():
                state.kill_hand()
            elif state.can_push_chips():
                state.push_chips()
            elif state.can_pull_chips():
                state.pull_chips()
            else:
                if not actions:
                    break

                action = actions.popleft()

                parse_action(state, action, self.parse_value)

            yield state, action

    def iter_state_actions(self) -> Iterator[tuple[State, str | None]]:
        """Deprecated. Now, an alias of
        :attr:`pokerkit.notation.HandHistory.state_actions`.

        This method will be removed in PokerKit Version 0.6.

        :return: The state-actions.
        """
        warn(
            (
                'pokerkit.notation.HandHistory.iter_state_actions() is'
                ' deprecated and will be removed on PokerKit Version 0.6'
            ),
            DeprecationWarning,
        )

        yield from self.state_actions

    @property
    def game_type(self) -> type[Poker]:
        """Return the game type.

        :return: The game type.
        """
        return self.game_types[self.variant]

    def create_game(self) -> Poker:
        """Create the game.

        :return: The game.
        """
        automations = list(self.automations)

        if Automation.CARD_BURNING in self.automations:
            automations.remove(Automation.CARD_BURNING)

        kwargs: dict[str, Any] = {
            'automations': tuple(automations),
            'divmod': self.divmod,
            'ante_trimming_status': self.ante_trimming_status,
        }

        for name in self.required_field_names[self.variant]:
            if name == 'antes' or name == 'blinds_or_straddles':
                key = f'raw_{name}'
            else:
                key = name

            kwargs[key] = getattr(self, name)

        kwargs.pop('variant')
        kwargs.pop('starting_stacks')
        kwargs.pop('actions')

        return self.game_type(**kwargs)

    def create_state(self) -> State:
        """Create the initial state.

        :return: The initial state.
        """
        return self.create_game()(
            self.starting_stacks,
            len(self.starting_stacks),
        )

    def dumps(self) -> str:
        """Dump PHH as a ``str`` object.

        :return: a ``str`` object.
        """

        def clean(value: Any) -> str:
            cleaned_value: str

            if isinstance(value, bool):
                cleaned_value = repr(value).lower()
            elif isinstance(value, datetime.time):
                cleaned_value = str(value)
            else:
                cleaned_value = repr(value)

            return cleaned_value

        lines = []

        for key, value in asdict(self).items():
            if (
                    (
                        key in self.required_field_names[self.variant]
                        or key in self.optional_field_names
                    )
                    and value is not None
            ):
                lines.append(f'{key} = {clean(value)}')

        for key, value in self.user_defined_fields.items():
            lines.append(f'{key} = {clean(value)}')

        return '\n'.join(lines)

    def dump(self, fp: BinaryIO) -> None:
        """Dump PHH to a file pointer.

        :param fp: The file pointer.
        :return: ``None``.
        """
        fp.write(self.dumps().encode())

    def to_acpc_protocol(
            self,
            position: int,
            hand_number: int | None = None,
    ) -> Iterator[tuple[str, str]]:
        """Convert to the ACPC protocol.

        Only the fixed-limit/no-limit Texas hold'em variants are
        supported.

        :param position: The client position.
        :param hand_number: The optional hand number. If ``None``, it is
                            inferred from the field.
        :return: The hand histories in the ACPC protocol.
        :raises ValueError: If the game is not supported or the hand
                            number cannot be determined.
        """
        if self.variant not in self.ACPC_PROTOCOL_VARIANTS:
            raise ValueError(
                (
                    f'The variant {repr(self.variant)} is not among the'
                    ' supported ACPC variants'
                    f' {repr(self.ACPC_PROTOCOL_VARIANTS)}.'
                ),
            )

        if hand_number is None:
            if self.hand is None:
                raise ValueError(
                    (
                        'Since the hand number is not defined in the hand'
                        ' history object, it must be passed as an argument.'
                    ),
                )

            hand_number = self.hand

        index = 0
        actions = ''
        raw_hole_cards = [['', ''] for _ in self.starting_stacks]
        hole_cards = ''
        board_cards = ''
        match_state = ''
        action = ''

        def egress() -> tuple[str, str]:
            if not all(raw_hole_cards[position]):
                raise ValueError(
                    'The hole cards at the desired position must be known.',
                )

            return 'S->', f'{match_state}\r\n'

        def ingress() -> tuple[str, str]:
            return '<-C', f'{match_state}:{action}\r\n'

        for state in self:
            while index < len(state.operations):
                operation = state.operations[index]
                index += 1

                if (
                        isinstance(
                            operation,
                            (
                                Folding
                                | CheckingOrCalling
                                | CompletionBettingOrRaisingTo
                            ),
                        )
                ):
                    yield egress()

                if isinstance(operation, Folding):
                    action = 'f'
                    actions += action
                elif isinstance(operation, CheckingOrCalling):
                    action = 'c'
                    actions += action
                elif isinstance(operation, CompletionBettingOrRaisingTo):
                    match self.variant:
                        case 'FT':
                            action = 'r'
                        case 'NT':
                            amount = -state.payoffs[operation.player_index]
                            action = f'r{amount}'
                        case _:
                            raise AssertionError

                    actions += action

                if (
                        isinstance(
                            operation,
                            (
                                Folding
                                | CheckingOrCalling
                                | CompletionBettingOrRaisingTo
                            ),
                        )
                        and operation.player_index == position
                ):
                    yield ingress()

                if isinstance(operation, HoleDealing):
                    if operation.player_index == position:
                        for i, card in enumerate(operation.cards):
                            if not card.unknown_status:
                                raw_hole_cards[position][i] = repr(card)
                elif isinstance(operation, HoleCardsShowingOrMucking):
                    for i, card in enumerate(operation.hole_cards):
                        if not card.unknown_status:
                            raw_hole_cards[operation.player_index][i] = repr(
                                card,
                            )

                if isinstance(operation, BoardDealing):
                    actions += '/'
                    board_cards += '/' + ''.join(map(repr, operation.cards))

                hole_cards = '|'.join(map(''.join, raw_hole_cards))
                match_state = (
                    f'MATCHSTATE'
                    f':{position}'
                    f':{hand_number}'
                    f':{actions}'
                    f':{hole_cards}{board_cards}'
                )

        if not state.status or state.actor_index is not None:
            yield egress()

    def to_pluribus_protocol(
            self,
            hand_number: int | None = None,
    ) -> str:
        """Convert to the Pluribus protocol.

        Only the no-limit Texas hold'em variant is supported.

        :param hand_number: The optional hand number. If ``None``, it is
                            inferred from the field.
        :return: The hand histories in the Pluribus protocol.
        :raises ValueError: If the game is not supported or the hand
                            number cannot be determined.
        """
        if self.variant not in self.PLURIBUS_PROTOCOL_VARIANTS:
            raise ValueError(
                (
                    f'The variant {repr(self.variant)} is not among the'
                    ' supported variants for pluribus notation'
                    f' {repr(self.PLURIBUS_PROTOCOL_VARIANTS)}.'
                ),
            )

        if hand_number is None:
            if self.hand is None:
                raise ValueError(
                    (
                        'Since the hand number is not defined in the hand'
                        ' history object, it must be passed as an argument.'
                    ),
                )

            hand_number = self.hand

        index = 0
        actions = ''
        raw_hole_cards = [['', ''] for _ in self.starting_stacks]
        board_cards = ''

        for state in self:
            while index < len(state.operations):
                operation = state.operations[index]
                index += 1

                if isinstance(operation, Folding):
                    actions += 'f'
                elif isinstance(operation, CheckingOrCalling):
                    actions += 'c'
                elif isinstance(operation, CompletionBettingOrRaisingTo):
                    amount = -state.payoffs[operation.player_index]
                    actions += f'r{amount}'
                elif isinstance(operation, HoleDealing):
                    for i, card in enumerate(operation.cards):
                        if not card.unknown_status:
                            raw_hole_cards[operation.player_index][i] = repr(
                                card,
                            )
                elif isinstance(operation, HoleCardsShowingOrMucking):
                    for i, card in enumerate(operation.hole_cards):
                        if not card.unknown_status:
                            raw_hole_cards[operation.player_index][i] = repr(
                                card,
                            )
                elif isinstance(operation, BoardDealing):
                    actions += '/'
                    board_cards += '/' + ''.join(map(repr, operation.cards))

        hole_cards = '|'.join(map(''.join, raw_hole_cards))
        raw_payoffs = []

        if self.finishing_stacks is None:
            finishing_stacks = tuple(self)[-1].stacks
        else:
            finishing_stacks = self.finishing_stacks

        for starting_stack, finishing_stack in zip(
                self.starting_stacks,
                finishing_stacks,
        ):
            raw_payoffs.append(finishing_stack - starting_stack)

        payoffs = '|'.join(map(str, raw_payoffs))

        if self.players is None:
            raw_players = [
                f'p{i + 1}' for i in range(len(self.starting_stacks))
            ]
        else:
            raw_players = self.players

        players = '|'.join(raw_players)
        match_state = (
            f'STATE'
            f':{hand_number}'
            f':{actions}'
            f':{hole_cards}{board_cards}'
            f':{payoffs}'
            f':{players}'
        )

        return match_state


def parse_action(
        state: State,
        action: str,
        parse_value: Callable[[str], int] = parse_value,
) -> None:
    """Parse the action.

    :param state: The state.
    :param action: The string action.
    :param parse_value: The value parsing function.
    :return: ``None``.
    """
    def verify_player(index: int | None) -> None:
        label, parsed_index = player[:1], int(player[1:]) - 1

        if label != 'p' or parsed_index != index:
            raise ValueError(
                (
                    f'The player {repr(player)} is not a valid player for the'
                    f' action {repr(action)}.'
                ),
            )

    commentary = action[action.index('#') + 2:] if '#' in action else None
    words = action.split()

    if '#' in words:
        words = words[:words.index('#')]

    match words:
        case 'd', 'db', cards:
            state.deal_board(cards)
        case 'd', 'dh', player, cards:
            verify_player(state.hole_dealee_index)
            state.deal_hole(cards, commentary=commentary)
        case player, 'sd':
            verify_player(state.stander_pat_or_discarder_index)
            state.stand_pat_or_discard(commentary=commentary)
        case player, 'sd', cards:
            verify_player(state.stander_pat_or_discarder_index)
            state.stand_pat_or_discard(cards, commentary=commentary)
        case player, 'pb':
            verify_player(state.actor_index)
            state.post_bring_in(commentary=commentary)
        case player, 'f':
            verify_player(state.actor_index)
            state.fold(commentary=commentary)
        case player, 'cc':
            verify_player(state.actor_index)
            state.check_or_call(commentary=commentary)
        case player, 'cbr', amount:
            verify_player(state.actor_index)
            state.complete_bet_or_raise_to(
                parse_value(amount),
                commentary=commentary,
            )
        case player, 'sm':
            verify_player(state.showdown_index)
            state.show_or_muck_hole_cards(False, commentary=commentary)
        case player, 'sm', '-':
            verify_player(state.showdown_index)
            state.show_or_muck_hole_cards(True, commentary=commentary)
        case player, 'sm', cards:
            verify_player(state.showdown_index)
            state.show_or_muck_hole_cards(cards, commentary=commentary)
        case ():
            state.no_operate(commentary=commentary)
        case _:
            raise ValueError(
                f'The action {repr(action)} is an invalid action.',
            )
