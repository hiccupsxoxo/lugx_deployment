// 🔁 Configurable API endpoint — works in Kubernetes & cloud
const API_ENDPOINT = "/api/analytics/track";

// 🕵️ Get page info
const path = window.location.pathname;
const user_agent = navigator.userAgent;
const sessionStart = Date.now();
let maxScroll = 0;

// 📦 Reusable function to send events
function sendAnalyticsEvent(eventType, data = {}) {
  return fetch(API_ENDPOINT, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      type: eventType,
      path: path,
      timestamp: new Date().toISOString(),
      ...data
    })
  }).catch((err) => console.error("Analytics error:", err));
}

// ✅ 1. Track page view
sendAnalyticsEvent("page_view");

// ✅ 2. Track user agent
sendAnalyticsEvent("user_agent", { user_agent });

// ✅ 3. Track clicks on elements with [data-track-click]
document.querySelectorAll("[data-track-click]").forEach((el) => {
  el.addEventListener("click", (e) => {
    e.preventDefault();
    const href = el.getAttribute("href");

    sendAnalyticsEvent("click", {
      element: el.tagName.toLowerCase(),
      element_id: el.id || "",
      class_name: el.className || ""
    }).finally(() => {
      if (href) window.location.href = href;
    });
  });
});

// ✅ 4. Track scroll depth
window.addEventListener("scroll", () => {
  const scrollTop = window.scrollY;
  const docHeight = document.documentElement.scrollHeight - window.innerHeight;
  const scrolled = docHeight > 0 ? Math.round((scrollTop / docHeight) * 100) : 0;
  if (scrolled > maxScroll) maxScroll = scrolled;
});

// ✅ 5. Track session duration + scroll depth on exit
window.addEventListener("beforeunload", () => {
  const sessionEnd = Date.now();
  const duration_ms = sessionEnd - sessionStart;

  sendAnalyticsEvent("scroll_depth", {
    max_scroll: maxScroll
  });

  sendAnalyticsEvent("session_duration", {
    duration_ms: duration_ms
  });
});
