import datetime
import requests
import pandas as pd
import json

# Generates base file for the simplified data, which i think are the necessary ones to obtain ingredients and category trends

# URL and Query
BASE_URL = "https://clinicaltrials.gov/api/v2/studies"
DIETARY_SUPPLEMENT_QUERY = "(dietary supplement OR food supplement OR nutrient OR nutraceutical) AND Interventional"

# Date Range
END_DATE = datetime.date(2025, 12, 31)
START_DATE = END_DATE - datetime.timedelta(days=4 * 365.25)
START_DATE_STR = START_DATE.strftime("%Y/%m/%d")

def fetch_trials(search_query):
    all_studies = []
    page_number = 1
    page_size = 100 # Maximum recommended page size

    while True:
        params = {
            "query.full_search": search_query,
            "fields": "NCTId,BriefTitle,Condition,Intervention,Keyword,OverallStatus,StartDate,Phase",
            "pageSize": page_size,
            "pageNumber": page_number,
            "format": "json"
        }
        
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status() # Raise an error for bad status codes
        data = response.json()
        
        # Extract the list of studies
        studies = data.get('studies', [])
        all_studies.extend(studies)
        
        # Check for pagination
        total_count = data.get('totalCount', 0)
        
        if total_count <= len(all_studies):
            break
        
        page_number += 1
        print(f"Fetched page {page_number-1}. Total fetched: {len(all_studies)} / {total_count}")
        
    return pd.json_normalize(all_studies)


search_query = DIETARY_SUPPLEMENT_QUERY


def get_studies_last_4_years():
    today = datetime.date.today()
    four_years_ago = today - datetime.timedelta(days=365 * 4)
    start_from = four_years_ago.isoformat()

    params = {
        "format": "json",
        "query.intr": "ashwagandha", #chosen ingredient to test
        "query.term": f"AREA[StartDate]RANGE[{start_from},MAX]",
        "fields": "ProtocolSection,BriefTitle,NCTId,StartDate,InterventionName",
        "pageSize": 200
    }

    all_studies = []
    simplified_studies = []
    next_token = None

    while True:
        if next_token:
            params["pageToken"] = next_token
        else:
            params.pop("pageToken", None)

        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()

        # API returns studies in "studies"
        studies = data.get("studies", [])
        all_studies.extend(studies)

        next_token = data.get("nextPageToken")
        if not next_token:
            break

    for study in all_studies:
        protocol = study.get("protocolSection", {}) or {}

        identification = protocol.get("identificationModule", {}) or {}
        status_module = protocol.get("statusModule", {}) or {}
        description = protocol.get("descriptionModule", {}) or {}
        conditions = protocol.get("conditionsModule", {}) or {}
        arms_interventions = protocol.get("armsInterventionsModule", {}) or {}
        outcomes = protocol.get("outcomesModule", {}) or {}
        references_module = protocol.get("referencesModule", {}) or {}

        pmids = []
        for ref in references_module.get("references", []) or []:
            pmid = ref.get("pmid")
            if pmid:
                pmids.append(pmid)
        
        simplified_studies.append(
            {
                "nctId": identification.get("nctId", None),
                "description": description.get("detailedDescription", None),
                "start_date": status_module.get("startDateStruct", {}).get("date", None),
                "conditions": conditions.get("conditions", []),
                "interventions": arms_interventions.get("interventions", []),
                "outcome": outcomes,
                "references": pmids,
            }
        )
    
    return simplified_studies


if __name__ == "__main__":
    studies = get_studies_last_4_years()

    output_file = "simplified_data_ashwagandha.json"

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(studies, f, indent=2, ensure_ascii=False)

    print(f"Saved {len(studies)} studies to {output_file}")