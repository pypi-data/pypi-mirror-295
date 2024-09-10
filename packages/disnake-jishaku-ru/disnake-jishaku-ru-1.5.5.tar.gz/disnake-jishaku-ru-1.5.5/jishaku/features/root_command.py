# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MIT

import math
import sys
import typing
import os
import psutil
import time
import datetime
from datetime import timedelta

import disnake
from disnake.ext import commands

from jishaku.features.baseclass import Feature
from jishaku.flags import Flags, ENABLED_SYMBOLS
from jishaku.modules import package_version
from jishaku.paginators import PaginatorInterface

try:
    import psutil
except ImportError:
    psutil = None


def natural_size(size_in_bytes: int):
    """
    Converts a number of bytes to an appropriately-scaled unit
    E.g.:
        1024 -> 1.00 KiB
        12345678 -> 11.77 MiB
    """
    units = ('B', 'KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB', 'YiB')

    power = int(math.log(size_in_bytes, 1024))

    return f"{size_in_bytes / (1024 ** power):.2f} {units[power]}"


class RootCommand(Feature):
    """
    Feature containing the root jsk command
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.jsk.hidden = Flags.HIDE

    @Feature.Command(name="jishaku", aliases=["jsk"],
                     invoke_without_command=True, ignore_extra=False)
    async def jsk(self, ctx: commands.Context):
        """
        The Jishaku debug and diagnostic commands.

        This command on its own gives a status brief.
        All other functionality is within its subcommands.
        """

        summary = [
            f"disnake-jishaku-ru v{package_version('disnake-jishaku-ru')} Beta, "
            f"disnake `{package_version('disnake')}`, "

            f"`Python {sys.version}` на `{sys.platform}`".replace("\n", ""),
            f"Модуль был загружен <t:{self.load_time.timestamp():.0f}:R>, "
            f"ког был загружен <t:{self.start_time.timestamp():.0f}:R>.",
            ""
        ]

        # detect if [procinfo] feature is installed
        if psutil:
            try:
                proc = psutil.Process()

                with proc.oneshot():
                    try:
                        mem = proc.memory_full_info()
                        summary.append(f"Используя {natural_size(mem.rss)} физической памяти и "
                                       f"{natural_size(mem.vms)} виртуальной памяти, "
                                       f"{natural_size(mem.uss)} из которых уникальны для этого процесса.")
                    except psutil.AccessDenied:
                        pass

                    try:
                        name = proc.name()
                        pid = proc.pid
                        thread_count = proc.num_threads()

                        summary.append(f"Запущен на PID {pid} (`{name}`) с {thread_count} потоком(ами).")
                    except psutil.AccessDenied:
                        pass

                    summary.append("")  # blank line
            except psutil.AccessDenied:
                summary.append(
                    "psutil установлен, но у этого процесса недостаточно высокие права доступа "
                    "для запроса информации о процессах."
                )
                summary.append("")  # blank line

        cache_summary = f"{len(self.bot.guilds)} сервера(ов) и {len(self.bot.users)} пользователь(ей)"

        # Show shard settings to summary
        if isinstance(self.bot, disnake.AutoShardedClient):
            if len(self.bot.shards) > 20:
                summary.append(
                    f"Этот бот автоматически разделен на шарды ({len(self.bot.shards)} шарды из {self.bot.shard_count})"
                    f" и может видеть {cache_summary}."
                )
            else:
                shard_ids = ', '.join(str(i) for i in self.bot.shards.keys())
                summary.append(
                    f"Этот бот автоматически разделен на шарды (Шарды {shard_ids} из {self.bot.shard_count})"
                    f" и может видеть {cache_summary}."
                )
        elif self.bot.shard_count:
            summary.append(
                f"Этот бот разделен на шарды вручную (Шард {self.bot.shard_id} из {self.bot.shard_count})"
                f" и может видеть {cache_summary}."
            )
        else:
            summary.append(f"Этот бот не разделен на шарды и может видеть {cache_summary}.")

        if self.bot._connection.max_messages:
            message_cache = f"Кэш сообщений ограничен (`{self.bot._connection.max_messages}`)"
        else:
            message_cache = "Кэш сообщений отключён."

        if disnake.version_info >= (1, 5, 0):
            presence_intent = f"Presence интент {'включён' if self.bot.intents.presences else 'выключен'}"
            members_intent = f"Members интент {'включён' if self.bot.intents.members else 'выключен'}"

            summary.append(f"{message_cache}.\n\n> - {presence_intent}.\n> - {members_intent}.\n")
        else:
            guild_subscriptions = f"Подписки на сервера {'включены' if self.bot._connection.guild_subscriptions else 'выключены'}"

            summary.append(f"{message_cache} и {guild_subscriptions}.")

        _embed = os.getenv('JISHAKU_EMBEDDED_JSK', None)
        if _embed in ENABLED_SYMBOLS:
            _color = os.getenv('JISHAKU_EMBEDDED_JSK_COLOR', None) or os.getenv('JISHAKU_EMBEDDED_JSK_COLOUR', None)
            if _color is not None:
                try:
                    color = await commands.ColourConverter().convert(ctx, _color)
                except commands.errors.BadColourArgument:
                    color = disnake.Colour.default()
            else:
                color = disnake.Colour.default()

            await ctx.send(embed=disnake.Embed(
                description="\n".join(summary),
                color=color)
                .set_author(
                    name='Jishaku',
                    url=ctx.bot.user.display_avatar.url,
                    icon_url=ctx.bot.user.display_avatar.url)
                .set_footer(text=f"Задержка вебсокета в среднем: {round(self.bot.latency * 1000, 2)}ms")
            )
        else:
            summary.append(f"Задержка вебсокета в среднем: {round(self.bot.latency * 1000, 2)}ms")
            await ctx.send("\n".join(summary))

    @Feature.Command(parent="jsk", name="hide")
    async def jsk_hide(self, ctx: commands.Context):
        """
        Hides Jishaku from the help command.
        """

        if self.jsk.hidden:
            return await ctx.send("Jishaku уже скрыт.")

        self.jsk.hidden = True
        await ctx.send("Jishaku теперь скрыт.")

    @Feature.Command(parent="jsk", name="show")
    async def jsk_show(self, ctx: commands.Context):
        """
        Shows Jishaku in the help command.
        """

        if not self.jsk.hidden:
            return await ctx.send("Jishaku уже виден.")

        self.jsk.hidden = False
        await ctx.send("Jishaku теперь виден.")

    @Feature.Command(parent="jsk", name="tasks")
    async def jsk_tasks(self, ctx: commands.Context):
        """
        Shows the currently running jishaku tasks.
        """

        if not self.tasks:
            return await ctx.send("В данный момент нет запущенных задач.")

        paginator = commands.Paginator(max_size=1985)

        for task in self.tasks:
            paginator.add_line(f"{task.index}: `{task.ctx.command.qualified_name}`, вызывается в "
                               f"{task.ctx.message.created_at.strftime('%Y-%m-%d %H:%M:%S')} UTC")

        interface = PaginatorInterface(ctx.bot, paginator, owner=ctx.author)
        return await interface.send_to(ctx)

    @Feature.Command(parent="jsk", name="cancel")
    async def jsk_cancel(self, ctx: commands.Context, *, index: typing.Union[int, str]):
        """
        Cancels a task with the given index.

        If the index passed is -1, will cancel the last task instead.
        """

        if not self.tasks:
            return await ctx.send("Нет задач для отмены.")

        if index == "~":
            task_count = len(self.tasks)

            for task in self.tasks:
                task.task.cancel()

            self.tasks.clear()

            return await ctx.send(f"Отменено {task_count} задач.")

        if isinstance(index, str):
            raise commands.BadArgument('Литерал для обозначения "индекса" не распознается.')

        if index == -1:
            task = self.tasks.pop()
        else:
            task = disnake.utils.get(self.tasks, index=index)
            if task:
                self.tasks.remove(task)
            else:
                return await ctx.send("Несуществующая задача.")

        task.task.cancel()
        return await ctx.send(f"Отменена задача {task.index}: `{task.ctx.command.qualified_name}`,"
                              f" вызывается в {task.ctx.message.created_at.strftime('%Y-%m-%d %H:%M:%S')} UTC")


    @Feature.Command(parent="jsk", name="host", aliases=["infoserver"])
    async def jsk_host(self, ctx: commands.Context):
        cpu_cores = psutil.cpu_count()
        cpu_percent = psutil.cpu_percent(interval=1)
        
        cpu_usage = f"{cpu_percent * cpu_cores}% / {100 * cpu_cores}%" 

        mem = psutil.virtual_memory()
        memory_usage = f"{mem.used / 1024 / 1024:.2f}MB / {mem.total / 1024 / 1024:.2f}MB"

        uptime_seconds = time.time() - psutil.boot_time()
        uptime = timedelta(seconds=uptime_seconds)

        days = uptime.days
        hours, remainder = divmod(uptime.seconds, 3600)
        minutes, _ = divmod(remainder, 60)

        uptime_formatted = f"{days}д. {hours}ч. {minutes}м."

        disk = psutil.disk_usage('/')
        disk_usage = f"{disk.used / 1024 / 1024 / 1024:.2f}GB / {disk.total / 1024 / 1024 / 1024:.2f}GB"

        system = "Linux" if psutil.LINUX else "Windows" if psutil.WINDOWS else "None"

        embed = disnake.Embed(
            title="Информация о сервере",
        )
        embed.add_field(name="Загрузка ЦП", value=f"```{cpu_usage}```", inline=False)
        embed.add_field(name="ОЗУ", value=f"```{memory_usage}```", inline=False)
        embed.add_field(name="Аптайм сервера", value=f"```{uptime_formatted}```", inline=False)
        embed.add_field(name="Диск", value=f"```{disk_usage}```", inline=False)
        embed.add_field(name="Система", value=f"```{system}```", inline=False)

        await ctx.send(embed=embed)