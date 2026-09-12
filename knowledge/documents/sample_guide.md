# Apex Cloud Platform — Product Guide & Documentation

## 1. Product Overview
Apex Cloud Platform is a modern cloud infrastructure and developer platform designed to help teams deploy, monitor, and scale distributed applications effortlessly.

### Key Capabilities
- **Serverless Compute**: Deploy stateless containerized functions with automatic horizontal scaling and sub-50ms cold starts.
- **Edge Data Storage**: Ultra-low latency global key-value store and distributed object caching replicated across 30+ regional edge points of presence.
- **Unified Observability**: Real-time distributed tracing, metrics collection, and live log streaming integrated out of the box.

---

## 2. Getting Started & Authentication

### Generating API Keys
1. Sign in to your Apex Cloud Management Console.
2. Navigate to **Organization Settings** > **API Credentials**.
3. Click **Create New Key**, assign your desired permission scope (`read-only` or `full-access`), and securely save the token.

### API Request Authentication
All HTTP requests to the Apex Cloud API must include your API key in the `Authorization` header formatted as a Bearer token:
```http
Authorization: Bearer apex_live_xxxxxxxxxxxxxxxx
```

---

## 3. Subscription Plans & Pricing Tiers

Apex Cloud offers three transparent subscription tiers designed for teams at every stage:

| Plan | Price | Included Bandwidth | Compute Limits | Support Level |
| :--- | :--- | :--- | :--- | :--- |
| **Starter** | Free forever | 100 GB / month | 2 Concurrent Workers | Community Forum |
| **Growth** | $29 / month | 1 TB / month | 10 Concurrent Workers | Standard Email (24h SLA) |
| **Enterprise** | $299 / month | Unlimited (fair use) | Dedicated clusters | 24/7 Dedicated Slack & Phone |

Upgrading or downgrading plans can be completed instantly from the Billing tab in the management console.

---

## 4. Rate Limiting & Quotas

To maintain platform stability for all users, API endpoints enforce standard rate limits based on your subscription tier:
- **Starter Tier**: 60 requests per minute per IP.
- **Growth Tier**: 1,200 requests per minute.
- **Enterprise Tier**: Custom negotiated quotas (default 10,000+ RPM).

If an application exceeds these limits, the API responds with HTTP status code `429 Too Many Requests` accompanied by a `Retry-After` header indicating the number of seconds to wait before retrying.

---

## 5. Troubleshooting & FAQ

### What should I do if I receive a 401 Unauthorized response?
A `401 Unauthorized` error indicates that the provided API key is missing, expired, or revoked. Check that your `Authorization` header begins with `Bearer ` and verify in the console that the token remains active.

### How do I configure webhook alerts?
Go to **Monitoring** > **Alert Channels**, click **Add Webhook**, enter your target HTTPS endpoint URL, and select the system events you wish to subscribe to (such as latency spikes or deployment failures).
