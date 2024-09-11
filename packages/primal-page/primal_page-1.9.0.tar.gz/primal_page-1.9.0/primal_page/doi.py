import requests


def get_harvard_citation(doi):
    url = "https://api.crossref.org/works/" + doi + "/text"
    headers = {
        "type": "text",
        "style": "harvard3",
        "locale": "en-US",
    }
    response = requests.get(url, headers=headers, allow_redirects=True)
    response.raise_for_status()

    return response.text


def get_citation(doi):
    doi_url = f"https://doi.org/{doi}"
    print(doi_url)
    response = requests.get(
        doi_url,
        headers={
            "Accept": "application/vnd.citationstyles.csl+json",
            "style": "harvard-cite-them-right",
        },
    )
    response.raise_for_status()
    return response.text


if __name__ == "__main__":
    doi = "10.1038/nprot.2017.066"
    print(get_harvard_citation(doi))
    print(get_citation(doi))
