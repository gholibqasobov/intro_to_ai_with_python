import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

            """
            return format
            
            pages = {
                "2.html": {"1.html", "3.html"},
                "1.html": {"2.html"},
                "3.html": {"2.html", "4.html"}
                "4.html": {"2.html"}
            }
            """

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """

    model = dict()
    d_prob = damping_factor / len(corpus[page])
    one_minus_d_prob = (1 - damping_factor) / len(corpus)
    # what we did in here: 0.85 / 2
    # we have to assign it to the keys of model dict
    linked_pages = list(corpus[page])
    for page in linked_pages:
        model[page] = d_prob + one_minus_d_prob


    """
    ** how to use damping factor**
        
    current_page = 1.html
    d = 0.85
    
    corpus = {
        "1.html": {"2.html", "3.html"},
        "2.html": {"3.html"},
        "3.html": {"2.html"}
    }
    
    return should be
    
    transition_model {
        "1.html": 0.05,
        "2.html": 0.475,
        "3.html": 0.475
    }
    
    BECAUSE, 
    
    page is 1.html and it links to 2.html and 3.html
    0.85 / 2 = 0.425
    and
    0.15/3 = 0.05
    
    1.html = 0.05
    2.html = 0.05 + 0.425
    3.html = 0.05 + 0.425
    
    
    WATCH OUT!!!
    if
    page = 1.html
    and
    corpus = {
        "1.html": set(),
        "2.html": {"3.html"},
        "3.html": {"2.html"}
    }
    
    pretend that
    "1.html": {"1.html", "2.html", "3.html"}
    
    **return format**
    ex, page = 2.html
    
    transition_model = {
        "1.html": 0.4,
        "3.html": 0.6
    }
    """
    # raise NotImplementedError







def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """


    """The aim is to calculate the PR(p) by sampling"""
    """The output is a dict
    
    page_rank = {
        "2.html": 0.444,
        "1.html": 0.111,
        "3.html": 0.333
        "4.html": 0.222    
    }
    
    """
    raise NotImplementedError


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    """Iterative form. The same format of output - dict()"""
    raise NotImplementedError


if __name__ == "__main__":
    main()











"""
While searching, Google places more important pages higher than the others.

definition of IMPORTANT PAGE:

1. Many other pages link to it. Therefore rank of the webpage is equal to number of incoming links
    rank = num(links)

BUT this method is not perfect, as it can be artificially inflated (impacted).





THEREFORE, a PageRank algorithm was created.

1. A website is more "Important" if links are from other important websites. 
Links of less important websites have less weight. 



MULTIPLE STRATEGIES TO CALCULATE THESE RANKINGS

1.
RANDOM SURFER MODEL



"""