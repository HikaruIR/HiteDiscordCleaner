"""
cleaner_api.py
Discord User REST API client — specialized for account cleaning operations:
closing DMs, deleting sent messages, removing relationships, leaving & deleting servers.

Language: Python 3.10+
Runtime: requests, rich
"""

import time
import requests
from typing import Optional, Generator
from rich.console import Console

console = Console()
BASE_URL = "https://discord.com/api/v10"


class CleanerAPI:
    """Wrapper around the Discord REST API using a user token for account sanitization."""

    def __init__(self, token: str):
        # Strip any quotes or whitespace
        clean_token = token.strip().strip('"').strip("'")
        self.headers = {
            "Authorization": clean_token,
            "Content-Type": "application/json",
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/126.0.0.0 Safari/537.36"
            ),
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        self.user_data: dict = {}

    # ─── Rate-limit handled request ──────────────────────────────────────────

    def _request(self, method: str, path: str, **kwargs) -> requests.Response:
        url = f"{BASE_URL}{path}"
        if "timeout" not in kwargs:
            kwargs["timeout"] = 25

        max_retries = 5
        attempts = 0

        while attempts < max_retries:
            attempts += 1
            try:
                resp = self.session.request(method, url, **kwargs)
            except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as e:
                console.print(f"[dim grey70]⚠ Network timeout/retry in 3s... ({e})[/dim grey70]")
                time.sleep(3)
                continue

            if resp.status_code == 429:
                try:
                    data = resp.json()
                    retry_after = float(data.get("retry_after", 5.0))
                except Exception:
                    retry_after = 5.0

                console.print(f"[yellow]⏳ Discord Rate Limited. Waiting {retry_after:.1f}s...[/yellow]")
                end_time = time.time() + retry_after + 0.3
                while time.time() < end_time:
                    remaining = int(end_time - time.time())
                    if remaining > 0 and remaining % 10 == 0:
                        console.print(f"[dim grey50]Waiting... {remaining}s remaining[/dim grey50]")
                    time.sleep(1)
                continue

            return resp

        raise requests.exceptions.RetryError(f"Failed after {max_retries} attempts on {path}")

    # ─── Account Verification ────────────────────────────────────────────────

    def get_me(self) -> dict:
        """Fetch current authenticated user profile."""
        resp = self._request("GET", "/users/@me")
        resp.raise_for_status()
        self.user_data = resp.json()
        return self.user_data

    # ─── Direct Messages (DMs & Group DMs) ───────────────────────────────────

    def get_dm_channels(self) -> list[dict]:
        """Fetch list of open DMs and Group DMs."""
        resp = self._request("GET", "/users/@me/channels")
        resp.raise_for_status()
        return resp.json()

    def close_dm_channel(self, channel_id: str) -> requests.Response:
        """Closes a DM / leaves a Group DM."""
        return self._request("DELETE", f"/channels/{channel_id}")

    def get_channel_messages(self, channel_id: str, limit: int = 100, before: Optional[str] = None) -> list[dict]:
        """Fetch recent messages from a channel."""
        path = f"/channels/{channel_id}/messages?limit={limit}"
        if before:
            path += f"&before={before}"
        resp = self._request("GET", path)
        if resp.status_code == 200:
            return resp.json()
        return []

    def delete_message(self, channel_id: str, message_id: str) -> requests.Response:
        """Delete an individual message sent by the user."""
        return self._request("DELETE", f"/channels/{channel_id}/messages/{message_id}")

    def purge_my_messages_in_channel(self, channel_id: str, my_id: str, max_msgs: int = 200) -> int:
        """Find and delete messages sent by current user in the channel."""
        deleted_count = 0
        last_id = None

        while deleted_count < max_msgs:
            messages = self.get_channel_messages(channel_id, limit=50, before=last_id)
            if not messages:
                break

            for msg in messages:
                last_id = msg.get("id")
                if msg.get("author", {}).get("id") == my_id:
                    # Message type 0 is normal, 19 is reply
                    del_resp = self.delete_message(channel_id, msg["id"])
                    if del_resp.status_code in (200, 204):
                        deleted_count += 1
                        time.sleep(1.2)  # Delay between message deletions to prevent flags
                    elif del_resp.status_code == 403:
                        # Cannot delete or message forbidden
                        continue
                    if deleted_count >= max_msgs:
                        break

            if len(messages) < 50:
                break

        return deleted_count

    # ─── Friends & Relationships ─────────────────────────────────────────────

    def get_relationships(self) -> list[dict]:
        """Fetch all relationships (friends, outgoing, incoming, blocked)."""
        resp = self._request("GET", "/users/@me/relationships")
        resp.raise_for_status()
        return resp.json()

    def remove_relationship(self, user_id: str) -> requests.Response:
        """Remove friend, cancel pending request, or unblock user."""
        return self._request("DELETE", f"/users/@me/relationships/{user_id}")

    # ─── Guilds (Servers) ────────────────────────────────────────────────────

    def get_my_guilds(self) -> list[dict]:
        """Fetch all guilds the user is currently a member of."""
        resp = self._request("GET", "/users/@me/guilds")
        resp.raise_for_status()
        return resp.json()

    def leave_guild(self, guild_id: str) -> requests.Response:
        """Leave a joined guild (where user is NOT the owner)."""
        return self._request("DELETE", f"/users/@me/guilds/{guild_id}")

    def delete_guild(self, guild_id: str) -> requests.Response:
        """Delete an owned guild."""
        return self._request("DELETE", f"/guilds/{guild_id}")
