# Country Information Service

A lightweight Python REST web service built with **Flask** that retrieves and
simplifies country data from the free
[REST Countries API](https://restcountries.com).

---

## Project Structure

```
CountryInformationService/
│
├── app.py            # Flask application – single endpoint, single function
├── requirements.txt  # Python package dependencies
└── README.md         # This file
```

---

## Features

| Feature | Detail |
|---|---|
| Framework | Flask 3.x |
| External API | REST Countries v3.1 (`https://restcountries.com`) |
| Endpoint | `GET /country/<country_name>` |
| Response format | JSON |
| Error handling | 404 country-not-found, 500 network/parse errors |

---

## Prerequisites

- Python 3.10 or later
- `pip` package manager
- Internet access (the service calls an external API at runtime)

---

## Installation

```bash
# 1. Clone or download the project folder
cd CountryInformationService

# 2. (Recommended) Create and activate a virtual environment
python -m venv venv

# On macOS / Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
```

---

## Running the Service

```bash
python app.py
```

The development server starts on **http://localhost:5000**.

You will see output similar to:

```
 * Running on http://0.0.0.0:5000
 * Debug mode: on
```

---

## API Reference

### Get Country Information

```
GET /country/<country_name>
```

| Parameter | Type | Description |
|---|---|---|
| `country_name` | `string` (URL path) | Name of the country to look up |

#### Success Response — `200 OK`

```json
{
    "country_name": "Sri Lanka",
    "official_name": "Democratic Socialist Republic of Sri Lanka",
    "capital": "Sri Jayawardenepura Kotte",
    "region": "Asia",
    "subregion": "Southern Asia",
    "population": 21919000,
    "currency": "Sri Lankan rupee",
    "flag": "https://flagcdn.com/w320/lk.png"
}
```

#### Not Found Response — `404 Not Found`

```json
{
    "error": "Country not found"
}
```

#### Server Error Response — `500 Internal Server Error`

```json
{
    "error": "Unable to connect to the REST Countries API"
}
```

---

## Example Requests

### Using `curl`

```bash
# Single-word country name
curl http://localhost:5000/country/France

# Multi-word country name (URL-encode the space or use %20)
curl "http://localhost:5000/country/Sri%20Lanka"
curl "http://localhost:5000/country/New%20Zealand"
```

### Using a browser

Simply paste the URL into your browser's address bar:

```
http://localhost:5000/country/Germany
http://localhost:5000/country/Sri Lanka
```

### Using Python `requests`

```python
import requests

response = requests.get("http://localhost:5000/country/Japan")
print(response.json())
```

---

## Response Fields

| Field | Type | Description |
|---|---|---|
| `country_name` | `string` | Common name of the country |
| `official_name` | `string` | Official / formal name |
| `capital` | `string` | Capital city (comma-separated if multiple) |
| `region` | `string` | Broad geographic region (e.g. Asia, Europe) |
| `subregion` | `string` | More specific subregion |
| `population` | `integer` | Total population |
| `currency` | `string` | Currency name(s), comma-separated if multiple |
| `flag` | `string` | Direct URL to the country's flag image (PNG) |

---

## Error Handling

| Scenario | HTTP Status | Response |
|---|---|---|
| Country not found | `404` | `{"error": "Country not found"}` |
| Cannot connect to upstream API | `500` | `{"error": "Unable to connect to the REST Countries API"}` |
| Upstream API timeout | `500` | `{"error": "Request to REST Countries API timed out"}` |
| Unexpected upstream HTTP error | `500` | `{"error": "Upstream API error: …"}` |
| Response parsing failure | `500` | `{"error": "Failed to parse country data: …"}` |

---

## Design Decisions

- **Single endpoint, single function** – the project intentionally exposes only
  `GET /country/<country_name>` and contains one business function
  (`fetch_country_info`). No databases, authentication, or CRUD operations are
  included.
- **`<path:country_name>`** – Flask's `path` converter is used instead of the
  default `string` converter so that country names containing spaces (e.g.
  "Sri Lanka", "New Zealand") work correctly in URLs without any special
  client-side encoding.
- **Timeout** – every call to the external API enforces a 10-second timeout to
  prevent the service from hanging indefinitely.
- **Safe field extraction** – all fields use `.get()` with sensible defaults
  (`"N/A"`) so a missing key in the upstream response never causes an
  unhandled `KeyError`.

---

## License

This project is released for educational purposes. The country data is provided
by [REST Countries](https://restcountries.com) under the
[Mozilla Public License 2.0](https://www.mozilla.org/en-US/MPL/2.0/).