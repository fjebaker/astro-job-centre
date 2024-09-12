import sys
import os
from datetime import datetime
from dataclasses import dataclass

import bs4
from feedgen.feed import FeedGenerator

AAS_ROOT_URL = "https://aas.org/jobregister"
FEED_URL = "https://cosroe.com/astro-job-centre.atom"

def parse_date(s: str) -> datetime:
    return datetime.strptime(s, "%Y/%m/%d")

@dataclass()
class Posting:
    title: str
    institution: str
    location: str
    posted: datetime
    deadline: datetime
    link: str

# read from stdin
content = sys.stdin.read()

parser = bs4.BeautifulSoup(content, "html.parser")

table = parser.find("table", class_="views-table")

tr_itt = (i for i in table.find_all("tr"))

# skip the heading column
headings = next(tr_itt)

postings: list[Posting] = []
for tr in tr_itt:
    tds = (i for i in tr.find_all("td"))
    title = next(tds)
    link = title.find("a").attrs.get("href")

    p = Posting(
        title.text.strip(),
        next(tds).text.strip(),
        next(tds).text.strip(),
        parse_date(next(tds).text.strip()),
        parse_date(next(tds).text.strip()),
        os.path.join(AAS_ROOT_URL, link),
    )
    postings.append(p)

# sort the register by when they were posted (most recent at
# the top)
postings = sorted(postings, key = lambda i: i.posted, reverse=True)

# now create atom feed from postings
feed = FeedGenerator()
feed.language("en")
feed.title("Astrophysics Job Centre+")
feed.link(href = FEED_URL, rel = "self")
feed.link(href = AAS_ROOT_URL, rel = "via")
feed.description("An RSS feed that mirrors the job listings posted to the AAS job register")
feed.author({"name": "Fergus Baker", "email": "fergus@cosroe.com"})
feed.id(FEED_URL)

for posting in postings:
    entry = feed.add_entry()
    entry.title(posting.title)
    entry.link(href=posting.link, rel="self")
    entry.id(posting.link)
    entry.content(
        """
        Instituion: {}

        Location: {}

        Deadline: {}
        """.format(posting.institution, posting.location, posting.deadline)
    )

feed.atom_file("astro-job-centre.atom", pretty=True)
