#! /usr/bin/python3

from bs4 import BeautifulSoup
from csv import writer

# from cfscrape import create_scraper


def get_titles():
    p = soup.select(".content p")
    titles = []
    try:
        for n, title in enumerate(p):
            title = p[n].get_text()
            try:
                title = title[0 : title.index("\n")]
            except ValueError:
                pass
            titles.append(title)
    except Exception as error:
        raise Exception("Something went wrong:\n {}".format(error))

    return titles


def get_list_of_grouped_links():
    unparsed_lists = soup.select(".content ul li")
    parsed_lists = []
    for li in unparsed_lists:
        unformatted_links = li.findAll()
        formatted_links = []
        for n, link in enumerate(unformatted_links):
            try:
                link = unformatted_links[n]["href"]
                linkText = unformatted_links[n].get_text()
                try:
                    int(linkText[0:3])
                except:
                    continue
            except KeyError:
                link = "Missing"
                linkText = unformatted_links[n].get_text()[8:]

            formatted_links.append((linkText, link))
        parsed_lists.append(formatted_links)
    return parsed_lists


def write_to_csv():
    with open("qidianunderground.csv", "w") as csv_file:
        csv_writer = writer(csv_file)
        headers = ["Title", "Chapter Range", "Link"]
        csv_writer.writerow(headers)
        for title, links in combined.items():
            for link in links:
                csv_writer.writerow([title, link[0], link[1]])


if __name__ == "__main__":

    # scraper = create_scraper()
    # data = scraper.get("https://toc.qidianunderground.org/").content
    with open("./QU ToC ReUploaded.html", "r") as f:
        data = f.read()
        soup = BeautifulSoup(data, "html.parser")

        titles = get_titles()
        list_of_grouped_links = get_list_of_grouped_links()
        combined = {}

        for i, group_of_links in enumerate(list_of_grouped_links):
            combined[titles[i]] = group_of_links

        write_to_csv()
