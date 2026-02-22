#!/usr/bin/env python3
"""Export latest tweets (including quote tweet metadata) to CSV.

Usage:
  TWITTER_BEARER_TOKEN=... python _scripts/export_tweets_csv.py \
    --username batra99 --limit 20 --output tweets.csv
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import sys
import time
import urllib.parse
import urllib.request
from dataclasses import dataclass
from typing import Any
from urllib.error import HTTPError

API_BASE = "https://api.twitter.com/2"
STATE_PATH = ".cache/tweets_export_state.json"


@dataclass
class TweetBundle:
    tweets: list[dict[str, Any]]
    includes_tweets: dict[str, dict[str, Any]]
    includes_users: dict[str, dict[str, Any]]
    next_token: str | None


class RateLimitError(RuntimeError):
    def __init__(self, message: str, reset_in_seconds: int | None = None):
        super().__init__(message)
        self.reset_in_seconds = reset_in_seconds


class TwitterClient:
    def __init__(self, bearer_token: str):
        self.bearer_token = bearer_token

    def _get(self, path: str, params: dict[str, Any]) -> dict[str, Any]:
        query = urllib.parse.urlencode(params)
        url = f"{API_BASE}{path}?{query}"
        req = urllib.request.Request(url)
        req.add_header("Authorization", f"Bearer {self.bearer_token}")
        req.add_header("User-Agent", "tweets-csv-export/1.0")

        try:
            with urllib.request.urlopen(req) as resp:
                payload = resp.read().decode("utf-8")
                return json.loads(payload)
        except HTTPError as exc:
            raw = exc.read().decode("utf-8", errors="replace")
            try:
                api_error = json.loads(raw)
                detail = api_error.get("detail") or api_error.get("title") or raw
            except json.JSONDecodeError:
                detail = raw or str(exc)

            if exc.code == 429:
                retry_after = exc.headers.get("retry-after")
                reset_epoch = exc.headers.get("x-rate-limit-reset")
                hint_parts = []
                wait_seconds = None
                if retry_after:
                    hint_parts.append(f"retry after ~{retry_after}s")
                if reset_epoch and reset_epoch.isdigit():
                    wait_seconds = max(0, int(reset_epoch) - int(time.time()))
                    hint_parts.append(f"rate window resets in ~{wait_seconds}s")
                hint = f" ({'; '.join(hint_parts)})" if hint_parts else ""
                raise RateLimitError(
                    f"HTTP 429 Too Many Requests{hint}. API says: {detail}",
                    reset_in_seconds=wait_seconds,
                ) from exc

            raise RuntimeError(f"HTTP {exc.code}. API says: {detail}") from exc

    def get_user(self, username: str) -> dict[str, Any]:
        data = self._get(
            f"/users/by/username/{urllib.parse.quote(username)}",
            {"user.fields": "name,username"},
        )
        return data["data"]

    def get_recent_tweets(
        self,
        user_id: str,
        limit: int,
        include_replies: bool,
        since_id: str | None = None,
        until_id: str | None = None,
        start_time: str | None = None,
        end_time: str | None = None,
        pagination_token: str | None = None,
        max_pages: int = 1,
    ) -> TweetBundle:
        tweets: list[dict[str, Any]] = []
        includes_tweets: dict[str, dict[str, Any]] = {}
        includes_users: dict[str, dict[str, Any]] = {}
        page_token = pagination_token

        pages_fetched = 0
        while len(tweets) < limit and pages_fetched < max_pages:
            max_results = min(100, limit - len(tweets))
            excludes = ["retweets"]
            if not include_replies:
                excludes.append("replies")

            params: dict[str, Any] = {
                "max_results": max_results,
                "exclude": ",".join(excludes),
                "tweet.fields": "author_id,created_at,referenced_tweets,text",
                "expansions": "author_id,referenced_tweets.id,referenced_tweets.id.author_id",
                "user.fields": "name,username",
            }
            if page_token:
                params["pagination_token"] = page_token
            if since_id:
                params["since_id"] = since_id
            if until_id:
                params["until_id"] = until_id
            if start_time:
                params["start_time"] = start_time
            if end_time:
                params["end_time"] = end_time

            try:
                payload = self._get(f"/users/{user_id}/tweets", params)
            except RateLimitError:
                if tweets:
                    break
                raise

            pages_fetched += 1
            batch = payload.get("data", [])
            if not batch:
                break

            tweets.extend(batch)

            includes = payload.get("includes", {})
            for included_tweet in includes.get("tweets", []):
                includes_tweets[included_tweet["id"]] = included_tweet
            for included_user in includes.get("users", []):
                includes_users[included_user["id"]] = included_user

            page_token = payload.get("meta", {}).get("next_token")
            if not page_token:
                break

        return TweetBundle(
            tweets=tweets[:limit],
            includes_tweets=includes_tweets,
            includes_users=includes_users,
            next_token=page_token,
        )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Fetch latest tweets and export to CSV."
    )
    parser.add_argument("--username", help="X username without @")
    parser.add_argument(
        "--user-id",
        help="X numeric user id. If provided, skips username lookup API call.",
    )
    parser.add_argument(
        "--display-username",
        help="Username used in URL when --user-id is supplied. Optional.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=20,
        help="Maximum number of latest tweets to pull (default: 20)",
    )
    parser.add_argument(
        "--output",
        default="tweets.csv",
        help="Output CSV path (default: tweets.csv)",
    )
    parser.add_argument(
        "--include-replies",
        action="store_true",
        help="Include reply tweets (default: false)",
    )
    parser.add_argument(
        "--max-pages",
        type=int,
        default=1,
        help="Max API pages to fetch (default: 1, safer for free-tier limits)",
    )
    parser.add_argument(
        "--since-id",
        help="Fetch only tweets newer than this tweet id.",
    )
    parser.add_argument(
        "--until-id",
        help="Fetch only tweets older than this tweet id.",
    )
    parser.add_argument(
        "--start-time",
        help="Lower time bound (inclusive), RFC3339 UTC like 2026-02-01T00:00:00Z.",
    )
    parser.add_argument(
        "--end-time",
        help="Upper time bound (exclusive), RFC3339 UTC like 2026-02-15T00:00:00Z.",
    )
    parser.add_argument(
        "--pagination-token",
        help="Continue from a previous page token for manual backfill pagination.",
    )
    parser.add_argument(
        "--state-path",
        default=STATE_PATH,
        help=f"State file path for incremental fetches (default: {STATE_PATH})",
    )
    parser.add_argument(
        "--no-state",
        action="store_true",
        help="Disable loading/saving incremental state.",
    )
    args = parser.parse_args()
    if not args.username and not args.user_id:
        parser.error("Provide either --username or --user-id.")
    if args.max_pages < 1:
        parser.error("--max-pages must be >= 1.")
    return args


def sanitize_text(text: str) -> str:
    return " ".join(text.replace("\r", "\n").splitlines()).strip()


def load_existing_rows(path: str) -> list[dict[str, str]]:
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        return [dict(row) for row in reader]


def load_state(path: str) -> dict[str, Any]:
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, dict):
            return data
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        return {}
    return {}


def save_state(path: str, state: dict[str, Any]) -> None:
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, sort_keys=True)
        f.write("\n")


def row_from_tweet(
    tweet: dict[str, Any],
    username: str | None,
    includes_tweets: dict[str, dict[str, Any]],
    includes_users: dict[str, dict[str, Any]],
) -> dict[str, str]:
    tweet_id = tweet["id"]
    quoted_tweet: dict[str, Any] | None = None

    for ref in tweet.get("referenced_tweets", []):
        if ref.get("type") == "quoted":
            quoted_tweet = includes_tweets.get(ref.get("id", ""))
            break

    quoted_author_username = ""
    quoted_tweet_id = ""
    quoted_text = ""

    if quoted_tweet:
        quoted_tweet_id = quoted_tweet.get("id", "")
        quoted_text = sanitize_text(quoted_tweet.get("text", ""))
        quoted_author_id = quoted_tweet.get("author_id")
        if quoted_author_id:
            quoted_author_username = includes_users.get(quoted_author_id, {}).get(
                "username", ""
            )

    if username:
        url = f"https://x.com/{username}/status/{tweet_id}"
    else:
        url = f"https://x.com/i/web/status/{tweet_id}"

    return {
        "tweet_id": tweet_id,
        "created_at": tweet.get("created_at", ""),
        "url": url,
        "text": sanitize_text(tweet.get("text", "")),
        "is_quote_tweet": "true" if quoted_tweet else "false",
        "quoted_tweet_id": quoted_tweet_id,
        "quoted_author_username": quoted_author_username,
        "quoted_text": quoted_text,
    }


def main() -> int:
    args = parse_args()
    token = os.environ.get("TWITTER_BEARER_TOKEN") or os.environ.get("X_BEARER_TOKEN")
    if not token:
        print(
            "Missing bearer token. Set TWITTER_BEARER_TOKEN (or X_BEARER_TOKEN).",
            file=sys.stderr,
        )
        return 1

    client = TwitterClient(token)
    state = {} if args.no_state else load_state(args.state_path)
    state_key = (args.username or args.user_id or "").lower()
    state_entry = state.get(state_key, {}) if isinstance(state.get(state_key), dict) else {}

    manual_backfill_mode = bool(
        args.until_id or args.start_time or args.end_time or args.pagination_token
    )
    state_since_id = state_entry.get("since_id") if not args.no_state else None
    since_id = args.since_id or (None if manual_backfill_mode else state_since_id)

    try:
        username = args.display_username or args.username
        user_id = args.user_id
        if not user_id:
            user = client.get_user(args.username)
            user_id = user["id"]
            username = user["username"]

        bundle = client.get_recent_tweets(
            user_id=user_id,
            limit=args.limit,
            include_replies=args.include_replies,
            since_id=since_id,
            until_id=args.until_id,
            start_time=args.start_time,
            end_time=args.end_time,
            pagination_token=args.pagination_token,
            max_pages=args.max_pages,
        )
    except Exception as exc:  # noqa: BLE001
        print(f"Failed to fetch tweets: {exc}", file=sys.stderr)
        return 1

    rows = [
        row_from_tweet(
            tweet=tweet,
            username=username,
            includes_tweets=bundle.includes_tweets,
            includes_users=bundle.includes_users,
        )
        for tweet in bundle.tweets
    ]
    existing_rows = load_existing_rows(args.output)
    seen_ids = {row.get("tweet_id", "") for row in rows}
    merged_rows = rows + [row for row in existing_rows if row.get("tweet_id", "") not in seen_ids]

    os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)
    with open(args.output, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "tweet_id",
                "created_at",
                "url",
                "text",
                "is_quote_tweet",
                "quoted_tweet_id",
                "quoted_author_username",
                "quoted_text",
            ],
        )
        writer.writeheader()
        writer.writerows(merged_rows)

    if not args.no_state and bundle.tweets:
        latest_id = bundle.tweets[0].get("id")
        if latest_id:
            state[state_key] = {
                "since_id": latest_id,
                "user_id": user_id,
                "username": username or "",
            }
            save_state(args.state_path, state)

    print(
        "Wrote "
        f"{len(rows)} new tweets ({len(merged_rows)} total rows) to {args.output}. "
        f"(since_id={since_id or 'none'}, next_token={bundle.next_token or 'none'}, max_pages={args.max_pages})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
