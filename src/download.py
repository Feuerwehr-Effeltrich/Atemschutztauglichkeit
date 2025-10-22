import requests
import bs4
import os

__email = os.environ["EMAIL"]
__password = os.environ["PASSWORD"]
__url = "https://live.fwportal.de"

def download(toFilename: str):
    session = requests.Session()

    homepage = session.get(__url)
    parsed = bs4.BeautifulSoup(homepage.text, features="html.parser")
    infield = parsed.find("input", attrs={"name": "__RequestVerificationToken"})
    if not infield:
        return
    verificationToken = str(infield.attrs["value"])

    session.post(f"{__url}/account/logon", data={
        "__RequestVerificationToken": verificationToken,
        "UserName": __email,
        "Password": __password,
        "AngemeldetBleiben": "false"
    })

    download = session.get(f"{__url}/Atemschutz/TauglichkeitAsExcel")

    if download.status_code != 200:
        print(f"Got status {download.status_code}: {download.reason} while downloading xlsx")
        return

    with open(toFilename, "wb") as f:
        f.write(download.content)
