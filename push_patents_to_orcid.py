"""
Push all 15 US patents to ORCID profile for Dr. Narasimha Kamath.
ORCID iD: 0000-0002-3959-0541

BEFORE RUNNING:
1. Go to https://orcid.org/developer-tools
2. Click "Register for the free ORCID public API"
3. Fill in:
     Name:         NK Patent Uploader
     Website URL:  https://github.com/NarasimhaKamathB
     Description:  Personal tool to upload patents to ORCID
     Redirect URI: https://narasimhakamathb.github.io/portfolio/callback.html
4. Click Save — copy your CLIENT_ID and CLIENT_SECRET below.
5. Run:  python push_patents_to_orcid.py
6. Your browser opens ORCID — click Authorize.
7. Browser shows a "connection refused" error on https://localhost — that is expected.
8. Copy the FULL URL from the address bar and paste it into the terminal prompt.
"""

import json
import webbrowser
import requests
from urllib.parse import urlparse, parse_qs, urlencode

# ── CONFIG — fill these in after registering at orcid.org/developer-tools ──
CLIENT_ID     = "APP-XXXXXXXXXXXXXXXX"   # replace with your client ID
CLIENT_SECRET = "your-client-secret"     # replace with your client secret
ORCID_ID      = "0000-0002-3959-0541"
REDIRECT_URI  = "https://narasimhakamathb.github.io/portfolio/callback.html"
# ────────────────────────────────────────────────────────────────────────────

ORCID_AUTH_URL  = "https://orcid.org/oauth/authorize"
ORCID_TOKEN_URL = "https://orcid.org/oauth/token"
ORCID_API_BASE  = f"https://api.orcid.org/v3.0/{ORCID_ID}"

PATENTS = [
    {
        "title": "Read-Write Network Visualization",
        "patent_number": "US12506669B2",
        "year": "2025", "month": "12", "day": "23",
        "inventors": "Mayuri Deb, Narasimha Kamath, S. Pandiarajan, Prashant Jhaba, Rohit Jangid, Koustuv Chatterjee"
    },
    {
        "title": "Dynamic Memoryless Demand-Supply Pegging",
        "patent_number": "US12462205B2",
        "year": "2025", "month": "11", "day": "04",
        "inventors": "Narasimha Kamath, Kshitiz Uttam"
    },
    {
        "title": "Aggregated Physical and Logical Network Mesh View",
        "patent_number": "US12086185B2",
        "year": "2024", "month": "09", "day": "10",
        "inventors": "Mayuri Deb, Narasimha Kamath, S. Pandiarajan, Prashant Jhaba, Koustuv Chatterjee"
    },
    {
        "title": "System and Method of Root Cause Analysis of Objective Violations",
        "patent_number": "US11853940B1",
        "year": "2023", "month": "12", "day": "26",
        "inventors": "Tushar Shekhar, Narasimha Kamath"
    },
    {
        "title": "Aggregated Physical and Logical Network Mesh View",
        "patent_number": "US11809495B2",
        "year": "2023", "month": "11", "day": "07",
        "inventors": "Mayuri Deb, Narasimha Kamath, S. Pandiarajan, Prashant Jhaba, Koustuv Chatterjee"
    },
    {
        "title": "Read-Write Network Visualization",
        "patent_number": "US11792094B2",
        "year": "2023", "month": "10", "day": "17",
        "inventors": "Mayuri Deb, Narasimha Kamath, S. Pandiarajan, Prashant Jhaba, Rohit Jangid, Koustuv Chatterjee"
    },
    {
        "title": "System and Method of Root Cause Analysis of Objective Violations and Query Analysis",
        "patent_number": "US11755993B2",
        "year": "2023", "month": "09", "day": "12",
        "inventors": "Tushar Shekhar, Narasimha Kamath"
    },
    {
        "title": "Dynamic Memoryless Demand-Supply Pegging",
        "patent_number": "US11615357B2",
        "year": "2023", "month": "03", "day": "28",
        "inventors": "Narasimha Kamath, Kshitiz Uttam"
    },
    {
        "title": "System and Method of Root Cause Analysis of Objective Violations and Query Analysis",
        "patent_number": "US11416809B2",
        "year": "2022", "month": "08", "day": "16",
        "inventors": "Tushar Shekhar, Narasimha Kamath"
    },
    {
        "title": "System and Method for Solving Large Scale Supply Chain Planning Problems with Integer Constraints",
        "patent_number": "US10325237B2",
        "year": "2019", "month": "06", "day": "18",
        "inventors": "Narasimha Kamath B., Tushar Shekhar"
    },
    {
        "title": "System and Method of Solving Supply Chain Campaign Planning Problems Involving Major and Minor Setups",
        "patent_number": "US10068192B2",
        "year": "2018", "month": "09", "day": "04",
        "inventors": "Narasimha Kamath B., Devender Chauhan, Debkalayan Mohanty, Dinesh Damodaran"
    },
    {
        "title": "System and Method of Solving Supply Chain Campaign Planning Problems Involving Major and Minor Setups",
        "patent_number": "US9785900B2",
        "year": "2017", "month": "10", "day": "10",
        "inventors": "Narasimha Kamath B., Devender Chauhan, Debkalayan Mohanty, Dinesh Damodaran"
    },
    {
        "title": "System and Method for Solving Large Scale Supply Chain Planning Problems with Integer Constraints",
        "patent_number": "US9754232B2",
        "year": "2017", "month": "09", "day": "05",
        "inventors": "Narasimha Kamath B., Tushar Shekhar"
    },
    {
        "title": "System and Method of Solving Supply Chain Campaign Planning Problems Involving Major and Minor Setups",
        "patent_number": "US8965548B1",
        "year": "2015", "month": "02", "day": "24",
        "inventors": "Narasimha Kamath B., Devender Chauhan, Debkalayan Mohanty, Dinesh Damodaran"
    },
    {
        "title": "System and Method of Solving Large Scale Supply Chain Planning Problems with Integer Constraints",
        "patent_number": "US8429035B1",
        "year": "2013", "month": "04", "day": "23",
        "inventors": "Narasimha Kamath B., Tushar Shekhar"
    },
]


def build_patent_payload(patent):
    return {
        "work-type": "patent",
        "title": {
            "title": {"value": patent["title"]}
        },
        "publication-date": {
            "year":  {"value": patent["year"]},
            "month": {"value": patent["month"]},
            "day":   {"value": patent["day"]}
        },
        "external-ids": {
            "external-id": [
                {
                    "external-id-type": "patent-number",
                    "external-id-value": patent["patent_number"],
                    "external-id-url": {
                        "value": f"https://patents.google.com/patent/{patent['patent_number']}"
                    },
                    "external-id-relationship": "self"
                }
            ]
        },
        "contributors": {
            "contributor": [
                {
                    "contributor-attributes": {"contributor-role": "author"},
                    "credit-name": {"value": name.strip()}
                }
                for name in patent["inventors"].split(",")
            ]
        },
        "country": {"value": "US"}
    }


# ── Main flow ─────────────────────────────────────────────────────────────────
def main():
    if CLIENT_ID.startswith("APP-XXX"):
        print("\n  ERROR: Please fill in CLIENT_ID and CLIENT_SECRET at the top of this script.")
        print("  Get them from: https://orcid.org/developer-tools\n")
        return

    # 1. Open browser for user authorization
    params = {
        "client_id":     CLIENT_ID,
        "response_type": "code",
        "scope":         "/read-limited /activities/update",
        "redirect_uri":  REDIRECT_URI,
    }
    auth_url = f"{ORCID_AUTH_URL}?{urlencode(params)}"
    print("\nOpening ORCID authorization in your browser...")
    print("After clicking 'Authorize', you will land on your GitHub Pages callback page.\n")
    webbrowser.open(auth_url)

    # 2. User copies code from GitHub Pages callback page
    print("The GitHub Pages callback page will show your authorization code.")
    print("Click 'Copy to clipboard' on that page, then paste the code here:")
    redirect_url = input("  Paste the full URL or just the code: ").strip()
    # accept either the full URL or just the bare code
    if redirect_url.startswith("http"):
        pass  # will be parsed below
    else:
        auth_code = redirect_url
        auth_code = auth_code if auth_code else None
        if auth_code:
            # skip URL parsing, go straight to token exchange
            pass
    if redirect_url.startswith("http"):
        params_out = parse_qs(urlparse(redirect_url).query)
        auth_code = params_out.get("code", [None])[0]
    if not auth_code:
        print("\nERROR: Could not find the authorization code. Please try again.")
        return

    # 3. Exchange code for access token
    print("Authorization received. Exchanging for access token...")
    token_resp = requests.post(ORCID_TOKEN_URL, data={
        "client_id":     CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type":    "authorization_code",
        "code":          auth_code,
        "redirect_uri":  REDIRECT_URI,
    }, headers={"Accept": "application/json"})
    token_resp.raise_for_status()
    access_token = token_resp.json()["access_token"]
    print(f"Access token obtained.\n")

    # 5. POST each patent
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type":  "application/vnd.orcid+json",
        "Accept":        "application/vnd.orcid+json",
    }

    success, failed = 0, []
    for patent in PATENTS:
        payload = build_patent_payload(patent)
        resp = requests.post(
            f"{ORCID_API_BASE}/work",
            headers=headers,
            data=json.dumps(payload)
        )
        if resp.status_code in (200, 201):
            print(f"  [OK]  {patent['patent_number']}  {patent['title']}")
            success += 1
        else:
            print(f"  [FAIL] {patent['patent_number']}  {resp.status_code}: {resp.text[:120]}")
            failed.append(patent["patent_number"])

    print(f"\nDone. {success}/{len(PATENTS)} patents pushed to ORCID.")
    if failed:
        print(f"Failed: {', '.join(failed)}")


if __name__ == "__main__":
    main()
