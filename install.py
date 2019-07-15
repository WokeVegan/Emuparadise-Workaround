import requests
import bs4
import os
import urllib


def get_links(url):
    links = []
    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.text, features="html5lib")
    for tag in soup.find_all("div", attrs={"class": "file-wrap"}):
        for x in tag.find_all('a', attrs={"class": "js-navigation-open"}, href=True):
            response = requests.get(f"https://github.com{x.get('href')}")
            soup = bs4.BeautifulSoup(response.text, 'html5lib')
            raw_link = soup.find(id="raw-url")  # try to find raw url
            if raw_link:
                print("found link for", urllib.parse.unquote(raw_link.get("href")).split('/')[-1])
                links.append(raw_link.get("href"))
            else:
                for tag in soup.find_all(attrs={"class": "file-wrap"}):
                    for x in tag.find_all('a', attrs={"class": "js-navigation-open"}, href=True):
                        response = requests.get(f"https://github.com{x.get('href')}")
                        soup = bs4.BeautifulSoup(response.text, 'html5lib')
                        raw_link = soup.find(id="raw-url")  # try to find raw url
                        if raw_link:
                            print("found link for", urllib.parse.unquote(raw_link.get("href")).split('/')[-1])
                            links.append(raw_link.get("href"))
    return links


if __name__ == '__main__':
    update = input("Do you wish to install Emuparadise_Workaround? [Y/n] ")
    if update.lower() != "y":
        raise SystemExit

    remove1 = "/WokeVegan/Emuparadise-Workaround/blob/master/"
    remove2 = "https://github.com/"
    remove3 = "/WokeVegan/Emuparadise-Workaround/raw/master/"
    url = 'https://github.com/WokeVegan/Emuparadise-Workaround'
    links = get_links(url)

    for link in links:
        url = f"https://github.com/{link}"
        filename = url.replace(remove1, "")
        filename = filename.replace(remove2, "")
        filename = filename.replace(remove3, "")
        filename = urllib.parse.unquote(filename)
        print("Downloading '%s'" % filename)
        response = requests.get(url, stream=True)
        head, tail = os.path.split(filename)

        if head:
            try:
                os.makedirs(os.path.join(head))
            except BaseException as f:
                pass

        with open(os.path.join(filename), 'wb') as f:
            for chunk in response.iter_content(1024**2):
                f.write(chunk)
            f.close()