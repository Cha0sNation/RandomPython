#! /usr/bin/python3

from argparse import ArgumentParser
from bs4 import BeautifulSoup
from csv import writer
from cfscrape import create_scraper


# Center title
def center_heading(heading):
    print()
    print(heading.center(26))


# Decorator function
def star_wrapper(quiet):
    def check_quiet(orig_func):
        if not quiet:

            def temp_func(*args, **kwargs):
                print("*" * 26)
                val = orig_func(*args, **kwargs)
                print("*" * 26)
                return val

            return temp_func
        else:
            return orig_func

    return check_quiet


# Basic scraper class
class Scraper:
    # Class variables
    scraper = create_scraper()
    data = scraper.get("https://toc.qidianunderground.org/").content
    titles = []
    list_of_grouped_links = []
    combined = {}

    # Create soup
    soup = BeautifulSoup(data, "html.parser")

    # Argument parser
    parser = ArgumentParser(description="A scraper for the QidianUnderground ToC")
    parser.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        default=False,
        help="Print only success or failure",
    )
    args = parser.parse_args()

    quiet = args.quiet

    # Main method
    def scrape(self):
        if not self.quiet:
            center_heading("Titles")
            self.titles = self.get_titles()
            center_heading("Chapters")
            self.list_of_grouped_links = self.get_list_of_grouped_links()
            center_heading("Combining titles and links")
            self.combine_titles_and_links()
            center_heading("Writing to CSV")
            self.write_to_csv()
        else:
            self.titles = self.get_titles()
            self.list_of_grouped_links = self.get_list_of_grouped_links()
            self.combine_titles_and_links()
            self.write_to_csv()

    @star_wrapper(quiet)
    def get_titles(self):
        p = self.soup.select(".content p")
        titles = []
        # Print out how many items in p
        if not self.quiet:
            print("{} titles found".format(len(p)))
        try:
            for n, title in enumerate(p):
                # Get p text
                title = p[n].get_text()
                # Seperate title from "updated x time ago"
                try:
                    title = title[0 : title.index("\n")]
                # If it can't it's not a valid title
                except ValueError:
                    pass
                titles.append(title)
            print("Titles: Success")
            return titles
        # If somehow something goes wrong
        except Exception as error:
            raise Exception("Something went wrong:\n {}".format(error))

    @star_wrapper(quiet)
    def get_list_of_grouped_links(self):
        # one novel = one li
        # Get all li from site
        unparsed_lists = self.soup.select(".content ul li")
        parsed_lists = []
        missing = 0
        for n, li in enumerate(unparsed_lists):
            # Get all chapter links
            unformatted_links = li.findAll()
            formatted_links = []
            if not self.quiet:
                print(
                    '* Getting {} chapter links for "{}"'.format(
                        len(unformatted_links), self.titles[n]
                    )
                )
            # For each link
            for n, link in enumerate(unformatted_links):
                # If it has a href it's a link
                try:
                    link = unformatted_links[n]["href"]
                    linkText = unformatted_links[n].get_text()
                    # If the first 3 chars can't be converted to int it's not a chapter link
                    try:
                        int(linkText[0:3])
                    # So ignore it
                    except:
                        continue
                # If it's not a link
                except KeyError:
                    missing += 1
                    link = "Missing"
                    # Remove "Missing " and get missing chapter number
                    linkText = unformatted_links[n].get_text()[8:]
                # Add (chapter length, chapter link) to book list
                formatted_links.append((linkText, link))
            # Add book list to scraper list
            parsed_lists.append(formatted_links)
        if not missing:
            print("Chapters: Success")
        else:
            print("Chapters: {} missing".format(missing))
        return parsed_lists

    @star_wrapper(quiet)
    def combine_titles_and_links(self):
        for i, group_of_links in enumerate(self.list_of_grouped_links):
            # For every book in titles create a dictionary entry and assign to it a list of tuples
            self.combined[self.titles[i]] = group_of_links
        if self.quiet:
            print("Combining: Success")
        else:
            print("* Success")

    @star_wrapper(quiet)
    def write_to_csv(self):
        with open("qidianunderground.csv", "w") as csv_file:
            csv_writer = writer(csv_file)
            headers = ["Title", "Chapter Range", "Link"]
            csv_writer.writerow(headers)
            # For every book in scraper list
            for title, links in self.combined.items():
                # For every link in book list
                for link in links:
                    # Title Chapter | Length Chapter | Links
                    csv_writer.writerow([title, link[0], link[1]])
        if self.quiet:
            print("CSV Write: Success")
        else:
            print("* Success")


if __name__ == "__main__":
    Scraper().scrape()
