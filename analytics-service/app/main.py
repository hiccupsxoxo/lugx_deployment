from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse  # 🔹 Added this line
from uuid import uuid4
from datetime import datetime
from dateutil import parser
from app.database import get_clickhouse_client, init_clickhouse
from app.schemas import AnalyticsEvent

app = FastAPI(title="Analytics Service API")

# ✅ Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    init_clickhouse()
    print("🚀 FastAPI started and ClickHouse initialized.")

@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")  # 🔹 Updated this line only

@app.post("/track")
def track_event(event: AnalyticsEvent):
    try:
        event_id = str(uuid4())

        # ⏱️ Safe timestamp parsing with fallback
        try:
            parsed_time = parser.isoparse(event.timestamp)
        except Exception:
            print("❌ Invalid timestamp, using current time")
            parsed_time = datetime.utcnow()

        client = get_clickhouse_client()
        path = event.path.strip("/")

        if event.type == "page_view":
            print("📦 Inserting page_view event into ClickHouse")
            client.insert("analytics.page_views", [[
                event_id, event.type, path, parsed_time
            ]], column_names=["id", "type", "path", "timestamp"])

        elif event.type == "click":
            print("📦 Inserting click event into ClickHouse")
            client.insert("analytics.clicks", [[
                event_id, event.type, path,
                event.element or "",
                event.element_id or "",
                event.class_name or "",
                parsed_time
            ]], column_names=["id", "type", "path", "element", "element_id", "class_name", "timestamp"])

        elif event.type == "scroll_depth":
            print("📦 Inserting scroll_depth event into ClickHouse")
            client.insert("analytics.scroll_depth", [[
                event_id, event.type, path,
                event.max_scroll or 0,
                parsed_time
            ]], column_names=["id", "type", "path", "max_scroll", "timestamp"])

        elif event.type == "user_agent":
            print("📦 Inserting user_agent event into ClickHouse")
            client.insert("analytics.user_agents", [[
                event_id, event.type, path,
                event.user_agent or "",
                parsed_time
            ]], column_names=["id", "type", "path", "user_agent", "timestamp"])

        elif event.type == "session_duration":
            print("📦 Inserting session_duration event into ClickHouse")
            client.insert("analytics.session_duration", [[
                event_id, event.type, path,
                event.duration_ms or 0,
                parsed_time
            ]], column_names=["id", "type", "path", "duration_ms", "timestamp"])

        else:
            raise HTTPException(status_code=400, detail="Invalid event type")

        return {"status": "success", "event_type": event.type}

    except Exception as e:
        print(f"❌ Error while processing event: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
