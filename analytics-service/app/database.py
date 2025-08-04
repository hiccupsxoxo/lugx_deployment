import os
import time
from typing import Optional
from clickhouse_connect import get_client
from clickhouse_connect.driver.exceptions import Error

# 🔁 Get ClickHouse client for each request/thread
def get_clickhouse_client():
    return get_client(
        host=os.getenv("CLICKHOUSE_HOST", "clickhouse"),
        port=int(os.getenv("CLICKHOUSE_PORT", 8123)),
        username=os.getenv("CLICKHOUSE_USER", "default"),
        password=os.getenv("CLICKHOUSE_PASSWORD", "mypassword123")  # 🔐 Never print this
    )

# ✅ Initialize DB and tables at FastAPI startup
def init_clickhouse():
    print("⏳ Waiting for ClickHouse readiness check...")
    client: Optional[object] = None
    retry_delay = int(os.getenv("CLICKHOUSE_RETRY_DELAY", "3"))

    # 🔁 Try connecting with retries
    for attempt in range(1, 6):
        try:
            client = get_clickhouse_client()
            client.command("SELECT 1")
            print("✅ ClickHouse is ready.")
            break
        except Error as e:
            print(f"⏳ Attempt {attempt}/5 - ClickHouse not ready yet: {e}")
            time.sleep(retry_delay)
    else:
        raise RuntimeError("❌ ClickHouse not reachable after multiple attempts.")

    # 📦 Ensure analytics database exists
    client.command("CREATE DATABASE IF NOT EXISTS analytics")

    # 📌 Table: Page Views
    client.command("""
        CREATE TABLE IF NOT EXISTS analytics.page_views (
            id UUID DEFAULT generateUUIDv4(),
            type String,
            path String,
            timestamp DateTime DEFAULT now()
        ) ENGINE = MergeTree()
        ORDER BY (timestamp)
    """)

    # 📌 Table: Click Events
    client.command("""
        CREATE TABLE IF NOT EXISTS analytics.clicks (
            id UUID DEFAULT generateUUIDv4(),
            type String,
            path String,
            element Nullable(String),
            element_id Nullable(String),
            class_name Nullable(String),
            timestamp DateTime DEFAULT now()
        ) ENGINE = MergeTree()
        ORDER BY (timestamp)
    """)

    # 📌 Table: Scroll Depth
    client.command("""
        CREATE TABLE IF NOT EXISTS analytics.scroll_depth (
            id UUID DEFAULT generateUUIDv4(),
            type String,
            path String,
            max_scroll Nullable(Int32),
            timestamp DateTime DEFAULT now()
        ) ENGINE = MergeTree()
        ORDER BY (timestamp)
    """)

    # 📌 Table: User Agents
    client.command("""
        CREATE TABLE IF NOT EXISTS analytics.user_agents (
            id UUID DEFAULT generateUUIDv4(),
            type String,
            path String,
            user_agent Nullable(String),
            timestamp DateTime DEFAULT now()
        ) ENGINE = MergeTree()
        ORDER BY (timestamp)
    """)

    # 📌 Table: Session Duration
    client.command("""
        CREATE TABLE IF NOT EXISTS analytics.session_duration (
            id UUID DEFAULT generateUUIDv4(),
            type String,
            path String,
            duration_ms Nullable(UInt32),
            timestamp DateTime DEFAULT now()
        ) ENGINE = MergeTree()
        ORDER BY (timestamp)
    """)

    print("✅ ClickHouse database and all tables initialized.")
