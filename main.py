"""
main.py - Discord Account Cleaner & Purger CLI
Theme: Minimalist Dark Slate / Monochrome Gray
Language: Python 3.10+ | Dependencies: rich, requests
Run: python main.py
"""

import os
import sys
import time

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
        sys.stdin.reconfigure(encoding="utf-8")
    except Exception:
        pass
    os.system("")

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt, Confirm
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TaskProgressColumn
from rich import box
from discord_api import CleanerAPI

console = Console(legacy_windows=False)

# ─── BANNER ──────────────────────────────────────────────────────────────────

BANNER = """
[bold white]
  ██████╗██╗     ███████╗ █████╗ ███╗   ██╗███████╗██████╗ 
 ██╔════╝██║     ██╔════╝██╔══██╗████╗  ██║██╔════╝██╔══██╗
 ██║     ██║     █████╗  ███████║██╔██╗ ██║█████╗  ██████╔╝
 ██║     ██║     ██╔══╝  ██╔══██║██║╚██╗██║██╔══╝  ██╔══██╗
 ╚██████╗███████╗███████╗██║  ██║██║ ╚████║███████╗██║  ██║
  ╚═════╝╚══════╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝
[/bold white]
[bold grey85]           Discord Account Purge & Cleaner[/bold grey85]
[dim grey62]      DMs   Friends   Servers   Message Sweeper[/dim grey62]
"""

def show_banner():
    console.print(Panel(BANNER, border_style="grey42", padding=(0, 2)))


def error(msg: str):
    console.print(f"[bold red]✕[/bold red] [grey85]{msg}[/grey85]")


def success(msg: str):
    console.print(f"[bold green]✓[/bold green] [grey85]{msg}[/grey85]")


def info(msg: str):
    console.print(f"[bold grey70]ℹ[/bold grey70] [grey85]{msg}[/grey85]")


def warn(msg: str):
    console.print(f"[bold yellow]⚠[/bold yellow] [grey78]{msg}[/grey78]")


def ask_confirmation(target_action: str) -> bool:
    """Explicit safety gate requiring exact keyword confirmation."""
    console.print()
    warn_panel = Panel(
        f"[bold red]WARNING: IRREVERSIBLE OPERATION[/bold red]\n"
        f"[grey85]You are about to execute:[/grey85] [bold white]{target_action}[/bold white]\n"
        f"[dim grey70]Once executed, deleted items cannot be restored by Discord.[/dim grey70]\n\n"
        f"To proceed, please type [bold yellow]CONFIRM[/bold yellow] below.",
        title="[bold red]Safety Confirmation[/bold red]",
        border_style="red",
        padding=(1, 2),
    )
    console.print(warn_panel)
    answer = Prompt.ask("[bold red]Enter verification[/bold red]").strip()
    return answer.upper() == "CONFIRM"


# ─── ACTIONS ─────────────────────────────────────────────────────────────────

def close_all_dms(api: CleanerAPI):
    """Closes all active direct messages and group chats."""
    with console.status("[dim grey70]Fetching open DMs...[/dim grey70]"):
        try:
            channels = api.get_dm_channels()
        except Exception as e:
            error(f"Failed to fetch DMs: {e}")
            return

    if not channels:
        info("No open direct message channels found.")
        return

    info(f"Found {len(channels)} open direct message channel(s).")
    if not ask_confirmation(f"Close {len(channels)} Direct Message channels"):
        info("Operation canceled by user.")
        return

    with Progress(
        SpinnerColumn(style="white"),
        TextColumn("[grey85]{task.description}[/grey85]"),
        BarColumn(bar_width=30, style="grey35", complete_style="white"),
        TaskProgressColumn(),
        console=console,
    ) as progress:
        task = progress.add_task("Closing DMs...", total=len(channels))
        closed = 0
        failed = 0

        for ch in channels:
            cid = ch["id"]
            recipients = [u.get("username", "unknown") for u in ch.get("recipients", [])]
            target_name = ", ".join(recipients) if recipients else f"Channel {cid}"
            progress.update(task, description=f"[dim]Closing DM with {target_name[:25]}...[/dim]")

            try:
                resp = api.close_dm_channel(cid)
                if resp.status_code in (200, 204):
                    closed += 1
                else:
                    failed += 1
            except Exception:
                failed += 1

            time.sleep(1.2)  # Healthy delay
            progress.advance(task)

    success(f"DMs Closed: {closed} successfully, {failed} failed.")


def sweep_dm_messages(api: CleanerAPI, my_id: str):
    """Scans open DMs and deletes messages sent by the user."""
    with console.status("[dim grey70]Fetching open DMs for message sweep...[/dim grey70]"):
        try:
            channels = api.get_dm_channels()
        except Exception as e:
            error(f"Failed to fetch DMs: {e}")
            return

    if not channels:
        info("No open DM channels found.")
        return

    info(f"Scanning up to {len(channels)} DMs to delete your sent messages.")
    if not ask_confirmation("Delete your sent messages in all open DMs"):
        info("Operation canceled by user.")
        return

    total_deleted = 0
    for ch in channels:
        cid = ch["id"]
        recipients = [u.get("username", "unknown") for u in ch.get("recipients", [])]
        target_name = ", ".join(recipients) if recipients else f"Channel {cid}"

        console.print(f"[dim grey70]Sweeping messages in DM: {target_name}...[/dim grey70]")
        try:
            deleted = api.purge_my_messages_in_channel(cid, my_id, max_msgs=100)
            total_deleted += deleted
            if deleted > 0:
                console.print(f"[grey78]  ↳ Deleted {deleted} message(s)[/grey78]")
        except Exception as e:
            console.print(f"[dim red]  ↳ Error sweeping {cid}: {e}[/dim red]")

    success(f"Total sent messages deleted across DMs: {total_deleted}")


def remove_all_friends(api: CleanerAPI):
    """Removes all friends, pending requests, and blocked users."""
    with console.status("[dim grey70]Fetching relationships...[/dim grey70]"):
        try:
            rels = api.get_relationships()
        except Exception as e:
            error(f"Failed to fetch relationships: {e}")
            return

    if not rels:
        info("No friends or relationships found.")
        return

    # Types: 1=Friend, 2=Blocked, 3=Incoming, 4=Outgoing
    friends = [r for r in rels if r.get("type") == 1]
    pending = [r for r in rels if r.get("type") in (3, 4)]
    blocked = [r for r in rels if r.get("type") == 2]

    console.print(
        f"[grey85]Found:[/grey85] "
        f"[bold white]{len(friends)}[/bold white] friends, "
        f"[bold white]{len(pending)}[/bold white] pending requests, "
        f"[bold white]{len(blocked)}[/bold white] blocked users."
    )

    clean_blocked = Confirm.ask("[grey85]Also unblock all blocked users?[/grey85]", default=False)
    targets = friends + pending + (blocked if clean_blocked else [])

    if not targets:
        info("Nothing selected to remove.")
        return

    if not ask_confirmation(f"Remove {len(targets)} friendship(s) & request(s)"):
        info("Operation canceled by user.")
        return

    with Progress(
        SpinnerColumn(style="white"),
        TextColumn("[grey85]{task.description}[/grey85]"),
        BarColumn(bar_width=30, style="grey35", complete_style="white"),
        TaskProgressColumn(),
        console=console,
    ) as progress:
        task = progress.add_task("Removing relationships...", total=len(targets))
        removed = 0
        failed = 0

        for rel in targets:
            user = rel.get("user", {})
            uid = user.get("id")
            uname = user.get("username", uid)
            progress.update(task, description=f"[dim]Removing {uname}...[/dim]")

            try:
                resp = api.remove_relationship(uid)
                if resp.status_code in (200, 204):
                    removed += 1
                else:
                    failed += 1
            except Exception:
                failed += 1

            time.sleep(1.2)  # Avoid rate limits & safety flags
            progress.advance(task)

    success(f"Relationships removed: {removed} successful, {failed} failed.")


def leave_all_joined_guilds(api: CleanerAPI):
    """Leaves all servers where the account is NOT the owner."""
    with console.status("[dim grey70]Fetching server list...[/dim grey70]"):
        try:
            guilds = api.get_my_guilds()
        except Exception as e:
            error(f"Failed to fetch servers: {e}")
            return

    joined_guilds = [g for g in guilds if not g.get("owner")]

    if not joined_guilds:
        info("No joined (non-owned) servers found.")
        return

    info(f"Found {len(joined_guilds)} joined server(s).")
    if not ask_confirmation(f"Leave {len(joined_guilds)} joined server(s)"):
        info("Operation canceled by user.")
        return

    with Progress(
        SpinnerColumn(style="white"),
        TextColumn("[grey85]{task.description}[/grey85]"),
        BarColumn(bar_width=30, style="grey35", complete_style="white"),
        TaskProgressColumn(),
        console=console,
    ) as progress:
        task = progress.add_task("Leaving servers...", total=len(joined_guilds))
        left = 0
        failed = 0

        for g in joined_guilds:
            gid = g["id"]
            gname = g.get("name", gid)
            progress.update(task, description=f"[dim]Leaving {gname[:25]}...[/dim]")

            try:
                resp = api.leave_guild(gid)
                if resp.status_code in (200, 204):
                    left += 1
                else:
                    failed += 1
            except Exception:
                failed += 1

            time.sleep(1.5)  # Leave delay
            progress.advance(task)

    success(f"Servers Left: {left} successful, {failed} failed.")


def delete_all_owned_guilds(api: CleanerAPI):
    """Deletes all servers created/owned by this account."""
    with console.status("[dim grey70]Fetching server list...[/dim grey70]"):
        try:
            guilds = api.get_my_guilds()
        except Exception as e:
            error(f"Failed to fetch servers: {e}")
            return

    owned_guilds = [g for g in guilds if g.get("owner")]

    if not owned_guilds:
        info("No owned servers found.")
        return

    info(f"Found {len(owned_guilds)} owned server(s):")
    for idx, g in enumerate(owned_guilds, 1):
        console.print(f"  [grey70]{idx}.[/grey70] [white]{g.get('name')}[/white] [dim]({g.get('id')})[/dim]")

    if not ask_confirmation(f"PERMANENTLY DELETE {len(owned_guilds)} owned server(s)"):
        info("Operation canceled by user.")
        return

    with Progress(
        SpinnerColumn(style="white"),
        TextColumn("[grey85]{task.description}[/grey85]"),
        BarColumn(bar_width=30, style="grey35", complete_style="white"),
        TaskProgressColumn(),
        console=console,
    ) as progress:
        task = progress.add_task("Deleting owned servers...", total=len(owned_guilds))
        deleted = 0
        failed = 0

        for g in owned_guilds:
            gid = g["id"]
            gname = g.get("name", gid)
            progress.update(task, description=f"[dim]Deleting {gname[:25]}...[/dim]")

            try:
                resp = api.delete_guild(gid)
                if resp.status_code in (200, 204):
                    deleted += 1
                else:
                    # In case of 2FA / MFA requirements on guild deletion
                    failed += 1
                    console.print(f"[dim red]  ↳ Failed to delete {gname} (Status: {resp.status_code})[/dim red]")
            except Exception as e:
                failed += 1
                console.print(f"[dim red]  ↳ Error deleting {gname}: {e}[/dim red]")

            time.sleep(2.0)
            progress.advance(task)

    success(f"Owned Servers Deleted: {deleted} successful, {failed} failed.")


def full_nuke_account(api: CleanerAPI, my_id: str):
    """Executes full account sanitation: DMs, Friends, Left Servers, and Deleted Servers."""
    console.print()
    warn_panel = Panel(
        "[bold red]DANGER: COMPLETE ACCOUNT SANITIZATION[/bold red]\n\n"
        "[grey85]This operation will perform the following steps sequentially:[/grey85]\n"
        " • [bold white]Close all Direct Messages & Group Chats[/bold white]\n"
        " • [bold white]Remove all Friends & Cancel Pending Requests[/bold white]\n"
        " • [bold white]Leave all Joined Servers[/bold white]\n"
        " • [bold white]Delete all Created/Owned Servers[/bold white]\n\n"
        "[dim grey70]Type 'CONFIRM' to begin this full purge.[/dim grey70]",
        title="[bold red]TOTAL NUKE MODE[/bold red]",
        border_style="red",
        padding=(1, 2),
    )
    console.print(warn_panel)

    if not ask_confirmation("TOTAL ACCOUNT PURGE"):
        info("Full purge aborted.")
        return

    info("Phase 1: Closing all Direct Messages...")
    close_all_dms(api)

    info("Phase 2: Removing all Friends & Relationships...")
    remove_all_friends(api)

    info("Phase 3: Leaving all Joined Servers...")
    leave_all_guilds = True
    leave_all_joined_guilds(api)

    info("Phase 4: Deleting Owned Servers...")
    delete_all_owned_guilds(api)

    success("Account sanitization sequence finished.")


# ─── MAIN PROGRAM LOOP ───────────────────────────────────────────────────────

def main():
    show_banner()

    console.print(
        Panel(
            "[bold white]Discord Account Cleaner & Purger[/bold white]\n"
            "[grey78]Cleans DMs, removes friends, leaves servers, and deletes created guilds.\n"
            "Runs securely using your personal Discord user token.[/grey78]\n\n"
            "[dim grey62]Note: Keep rate limits in mind. Operations include built-in delays.[/dim grey62]",
            border_style="grey42",
            padding=(0, 2),
        )
    )

    # 1. Prompt for User Token
    while True:
        token = Prompt.ask("[bold white]Enter your Discord User Token[/bold white]", password=True).strip()
        if not token:
            error("Token cannot be empty.")
            continue

        api = CleanerAPI(token)
        with console.status("[dim grey70]Validating token and fetching profile...[/dim grey70]"):
            try:
                me = api.get_me()
                break
            except Exception as e:
                error(f"Invalid token or connection error: {e}")
                if not Confirm.ask("[grey85]Try entering token again?[/grey85]", default=True):
                    sys.exit(0)

    # Display Account Info
    my_id = me.get("id", "")
    username = me.get("username", "Unknown")
    global_name = me.get("global_name") or username

    account_table = Table(box=box.ROUNDED, border_style="grey42", title="Authenticated User")
    account_table.add_column("Property", style="dim grey70", width=18)
    account_table.add_column("Value", style="bold white")

    account_table.add_row("Username", username)
    account_table.add_row("Display Name", global_name)
    account_table.add_row("User ID", my_id)
    if me.get("email"):
        account_table.add_row("Email", me.get("email"))

    console.print()
    console.print(account_table)
    console.print()

    # 2. Main Menu Loop
    while True:
        console.print("[bold grey85]Select an Operation:[/bold grey85]")
        console.print(" [bold white]1[/bold white]  Close All Direct Messages (DMs & Groups)")
        console.print(" [bold white]2[/bold white]  Sweep Sent Messages in Open DMs")
        console.print(" [bold white]3[/bold white]  Remove All Friends & Cancel Pending Requests")
        console.print(" [bold white]4[/bold white]  Leave All Joined Servers (Non-owned)")
        console.print(" [bold white]5[/bold white]  Delete All Owned Servers (Created by you)")
        console.print(" [bold white]6[/bold white]  [bold red]Complete Account Purge (Nuke Everything)[/bold red]")
        console.print(" [bold white]0[/bold white]  Exit")
        console.print()

        choice = Prompt.ask("[bold white]Choose option[/bold white]", choices=["0", "1", "2", "3", "4", "5", "6"], default="0")

        if choice == "0":
            console.print("[dim grey70]Exiting cleaner. Goodbye.[/dim grey70]")
            break
        elif choice == "1":
            close_all_dms(api)
        elif choice == "2":
            sweep_dm_messages(api, my_id)
        elif choice == "3":
            remove_all_friends(api)
        elif choice == "4":
            leave_all_joined_guilds(api)
        elif choice == "5":
            delete_all_owned_guilds(api)
        elif choice == "6":
            full_nuke_account(api, my_id)

        console.print()
        console.print("[dim grey50]" + "─" * 60 + "[/dim grey50]")
        console.print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[dim grey70]Process aborted by user.[/dim grey70]")
        sys.exit(0)
