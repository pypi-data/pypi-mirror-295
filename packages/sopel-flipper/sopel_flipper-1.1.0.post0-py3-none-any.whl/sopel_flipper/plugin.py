"""sopel-flipper

A Sopel plugin that flips text in response to CTCP ACTIONs.
"""
from __future__ import annotations

from upsidedown import transform as flip_transform

from sopel import plugin, tools

from .mirror import transform as mirror_transform


LOGGER = tools.get_logger('flipper')


@plugin.commands('flip', 'roll', 'hflip', 'mirror')
@plugin.action_commands('flips', 'rolls', 'mirrors')
def flip_and_roll(bot, trigger):
    target = (trigger.group(2) or '').strip()
    if not target:
        # people likely do *not* expect the bot to respond to flip/roll actions
        # without any arguments
        return plugin.NOLIMIT

    mode = trigger.group(1)
    if mode.endswith('s'):
        # action commands must be stripped of the trailing 's'
        mode = mode[:-1]

    if mode == 'flip':
        if target in ['a table', 'the table']:
            target = '┻━┻'
        else:
            target = flip_transform(target)

        bot.say("(╯°□°）╯︵ " + target)
    elif mode == 'roll':
        if target.endswith(' down a hill'):
            # upon dropping Python 3.8, this `if` block can be replaced with
            # `target = target.removesuffix(' down a hill')`
            # (`str.removesuffix()` was added in py3.9)
            target = target[:-12]

        tegrat = flip_transform(target)
        bot.say("(╮°-°)╯︵ %s %s %s %s %s (@_@;)" % (tegrat, target, tegrat, target, tegrat))
    elif mode in ('hflip', 'mirror'):
        bot.say("╰( ⁰ ਊ ⁰ )━💨🪞 %s" % mirror_transform(target))
    else:
        # panic!
        LOGGER.error(
            'Reached mode fallthrough. Message was: {!r}'.format(trigger))
        bot.reply(
            "This code is never supposed to run… You must be a very special "
            "person. I have logged the error; please ask {} to report this."
            .format(bot.settings.core.owner)
        )
