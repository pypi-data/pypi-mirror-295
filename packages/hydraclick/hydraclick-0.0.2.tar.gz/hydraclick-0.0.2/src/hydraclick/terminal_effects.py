from typing import Optional, Callable
import os

import click
from click import Context, Option


def get_no_terminal_efects() -> bool:
    """Get the no terminal effects environment variable."""
    val = os.environ.get(
        "OMEGACLICK_NO_TERMINAL_EFFECTS", os.environ.get("OMEGACLICK_NO_TERMINAL_EFFECTS")
    )
    if val is None:
        return False
    return val.lower() in {"true", "1", "yes"}


NO_TERMINAL_EFFECTS = get_no_terminal_efects()


def display_terminal_effect(value):
    """Display the terminal effect."""
    # from terminaltexteffects.effects.effect_random_sequence import RandomSequence
    from terminaltexteffects.effects.effect_print import Print  # noqa: PLC0415
    from terminaltexteffects.utils.graphics import Color  # noqa: PLC0415

    effect = Print(value)
    # effect.effect_config.speed = 0.025
    effect.effect_config.print_speed = 5
    effect.effect_config.print_head_return_speed = 3
    effect.effect_config.final_gradient_stops = (Color("00ffae"), Color("00D1FF"), Color("FFFFFF"))
    with effect.terminal_output() as terminal:
        for frame in effect:
            terminal.print(frame)


_TERMINAL_EFFECT = display_terminal_effect


def set_terminal_effect(value: Callable | None = None):
    """Set the terminal effect."""
    global _TERMINAL_EFFECT  # noqa: PLW0603
    if value is None:
        value = display_terminal_effect
    _TERMINAL_EFFECT = value


def parse_args(self, ctx: Context, args: list[str]) -> list[str]:
    """Display the help message when no arguments are provided."""
    if not args and self.no_args_is_help and not ctx.resilient_parsing:
        _TERMINAL_EFFECT(ctx.get_help())
        ctx.exit()

    rest = super(click.core.MultiCommand, self).parse_args(ctx, args)

    if self.chain:
        ctx.protected_args = rest
        ctx.args = []
    elif rest:
        ctx.protected_args, ctx.args = rest[:1], rest[1:]

    return ctx.args


def get_help_option(self, ctx: Context) -> Optional["Option"]:
    """Return the help option object."""
    from gettext import gettext  # noqa: PLC0415

    help_options = self.get_help_option_names(ctx)

    if not help_options or not self.add_help_option:
        return None

    def show_help(ctx: Context, param: "click.Parameter", value: str) -> None:  # noqa: ARG001
        if value and not ctx.resilient_parsing:
            display_terminal_effect(ctx.get_help())
            ctx.exit()

    return Option(
        help_options,
        is_flag=True,
        is_eager=True,
        expose_value=False,
        callback=show_help,
        help=gettext("Show this message and exit."),
    )


if not NO_TERMINAL_EFFECTS:
    set_terminal_effect(display_terminal_effect)
    click.core.Command.get_help_option = get_help_option
    click.core.MultiCommand.parse_args = parse_args
