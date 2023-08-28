from sec_api import QueryApi, RenderApi
import os
from dotenv import load_dotenv
from pathlib import Path
import html2text

load_dotenv()  # take environment variables from .env.
SEC_KEY = os.getenv("SEC_KEY")
queryApi = QueryApi(api_key=SEC_KEY)
render_api = RenderApi(api_key=SEC_KEY)


# download filing and save to "filings" folder
def download_filing(url: str, directory: str = "./filings"):
    try:
        filing = render_api.get_filing(url)
        # print(filing)
        # file_name example: 000156459019027952-msft-10k_20190630.htm
        file_name = url.split("/")[-2] + "-" + url.split("/")[-1]
        download_to = f"{directory}/{file_name}"
        file = Path(download_to)
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_text(html2text.html2text(filing))
        # with open(download_to, "w") as f:
        #    f.write(filing)
    except Exception as e:
        print("Problem with {url}".format(url=url))
        print(e)


def download_10_q(ticker: str = "RF", quantity: int = 5):
    query = {
        "query": {
            "query_string": {
                "query": f'formType:"10-Q" AND ticker:{ticker}',  # only 10-Qs
            }
        },
        "from": "0",  # start returning matches from position null, i.e. the first matching filing
        "size": str(quantity),
        "sort": [{"filedAt": {"order": "desc"}}],
    }

    response = queryApi.get_filings(query)
    for filing in response["filings"]:
        download_filing(filing["linkToFilingDetails"])


if __name__ == "__main__":
    download_10_q()
