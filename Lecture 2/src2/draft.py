# # from pomegranate.distributions import Categorical
# # from pomegranate.distributions import ConditionalCategorical
# # from pomegranate.bayesian_network import BayesianNetwork
# #
# # rain = Categorical({
# #     "none": 0.7,
# #     "light": 0.2,
# #     "heavy": 0.1
# # })
# #
# # maintenance = ConditionalCategorical([
# #     ["none", "yes", 0.4],
# #     ["none", "no", 0.6],
# #     ["light", "yes", 0.2],
# #     ["light", "no", 0.8],
# #     ["heavy", "yes", 0.1],
# #     ["heavy", "no", 0.9]
# # ], [rain.distribution])
# #
# #
# # """
# # [
# #     [0.4, 0.6],
# #     [0.2, 0.8],
# #     [0.1, 0.9]
# #
# # ]
# # """
# #
# #
# # train = ConditionalCategorical([
# #     ["none", "yes", "on time", 0.8],
# #     ["none", "yes", "delayed", 0.2],
# #     ["none", "no", "on time", 0.9],
# #     ["none", "no", "delayed", 0.1],
# #     ["light", "yes", "on time", 0.6],
# #     ["light", "yes", "delayed", 0.4],
# #     ["light", "no", "on time", 0.7],
# #     ["light", "no", "delayed", 0.3],
# #     ["heavy", "yes", "on time", 0.4],
# #     ["heavy", "yes", "delayed", 0.6],
# #     ["heavy", "no", "on time", 0.5],
# #     ["heavy", "no", "delayed", 0.5],
# # ], [rain.distribution, maintenance.distribution])
# #
# #
# # """
# # [
# #     [0.8, 0.2],
# #     [0.9, 0.1],
# #     [0.6, 0.4],
# #     [0.7, 0.3],
# #     [0.4, 0.6],
# #     [0.5, 0.5]
# # ]
# # """
# #
# #
# # appointment = ConditionalCategorical([
# #     ["on time", "attend", 0.9],
# #     ["on time", "miss", 0.1],
# #     ["delayed", "attend", 0.6],
# #     ["delayed", "miss", 0.4]
# # ], [train.distribution])
# #
# # """
# # [
# #     [0.9, 0.1],
# #     [0.6, 0.4]
# # ]
# # """
# #
# # model = BayesianNetwork()
# # model.add_distributions([rain, maintenance, train, appointment])
# # model.add_edge(rain, maintenance)
# # model.add_edge(rain, train)
# # model.add_edge(maintenance, train)
# # model.add_edge(train, appointment)
# import random
# import os
# import re
# import sys
#
#
# def transition_model(corpus, page, damping_factor):
#     """
#     Return a probability distribution over which page to visit next,
#     given a current page.
#
#     With probability `damping_factor`, choose a link at random
#     linked to by `page`. With probability `1 - damping_factor`, choose
#     a link at random chosen from all pages in the corpus.
#     """
#
#     model = dict()
#     one_minus_d_prob = (1 - damping_factor) / len(corpus)  # 0.15 / 3 = 0.05
#     if len(corpus[page]) != 0:
#         d_prob = damping_factor/len(corpus[page])  # 0.85 / 2 = 0.425
#         for key in corpus:
#             if key in corpus[page]:
#                 model[key] = d_prob + one_minus_d_prob
#             else:
#                 model[key] = one_minus_d_prob
#
#     else:
#         for key in corpus:
#             model[key] = one_minus_d_prob
#
#     return model
#
#
# corpus = {
#         "1.html": {"2.html", "3.html"},
#         "2.html": {"3.html"},
#         "3.html": {"2.html"}
#     }
#
# d = 0.85
# page = "1.html"
#
# from collections import Counter
#
#
# def sample_pagerank(corpus, damping_factor, n):
#     """
#     Return PageRank values for each page by sampling `n` pages
#     according to transition model, starting with a page at random.
#
#     Return a dictionary where keys are page names, and values are
#     their estimated PageRank value (a value between 0 and 1). All
#     PageRank values should sum to 1.
#     """
#
#     pagerank_list = []
#     sample = random.choice(list(corpus.keys()))
#     pagerank_list.append(sample)
#
#     """next sample should be generated from sample
#
#     use the transition model to get the new sample
#
#     """
#
#     """
#     sample = 1.html
#
#     transition_model {
#         "1.html": 0.05,
#         "2.html": 0.475,
#         "3.html": 0.475
#     }
#
#     should choose the maximum of the two you say?
#
#     max_prob = max(transition_model.keys())
#     if prob == max(keys), add their el into list, and randomly choose among those
#     """
#
#     for i in range(n-1):
#         current_sample_list = []
#         # the problem is that it is choosing by max probability and there's no point in using the damping factor.
#         # it should somehow choose by the percentage of transition mode.
#         # shall I multiply that to probability of transition model?
#         """
#         it's gong to be this way:
#         transition_model {
#         "1.html": 0.05,
#         "2.html": 0.475,
#         "3.html": 0.475
#         }
#         If I understood the manual correctly, 5% percent of samples should be 1.html and 47.5% 2.html and 47.5% 3.html
#
#         if so,
#         10,000 -- 100%
#                   5%
#
#         n = 50000/100 = 500
#         n = 4750
#         """
#         max_prob = max(transition_model(corpus, sample, damping_factor).values())
#         for key, val in transition_model(corpus, sample, damping_factor).items():
#             if val == max_prob:
#                 current_sample_list.append(key)
#         sample = random.choice(current_sample_list)
#         pagerank_list.append(sample)
#
#     page_rank = dict(Counter(pagerank_list))
#     for key in page_rank.keys():
#         page_rank[key] /= n
#
#     return page_rank
#
#
# def crawl(directory):
#     """
#     Parse a directory of HTML pages and check for links to other pages.
#     Return a dictionary where each key is a page, and values are
#     a list of all other pages in the corpus that are linked to by the page.
#     """
#     pages = dict()
#
#     # Extract all links from HTML files
#     for filename in os.listdir(directory):
#         if not filename.endswith(".html"):
#             continue
#         with open(os.path.join(directory, filename)) as f:
#             contents = f.read()
#             links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
#             pages[filename] = set(links) - {filename}
#
#             """
#             return format
#
#             pages = {
#                 "2.html": {"1.html", "3.html"},
#                 "1.html": {"2.html"},
#                 "3.html": {"2.html", "4.html"}
#                 "4.html": {"2.html"}
#             }
#             """
#
#     # Only include links to other pages in the corpus
#     for filename in pages:
#         pages[filename] = set(
#             link for link in pages[filename]
#             if link in pages
#         )
#
#     return pages
#
#
# print(sample_pagerank(crawl("C:\Python3\Introduction to AI with Python\Lecture 2\Project 2\Pagerank\corpus0"), d, 10000))
#
# summa = 0
# for page in corpus.keys():
#
#     for link_i in page:
#         PR_i = pagerank[link_i]
#
#         if len(link_i) == 0:
#             NumLink_i = len(corpus)
#             summa += (PR_i / NumLink_i)
#         else:
#             NumLink_i = len(page)
#             summa += (PR_i / NumLink_i)
#
#     pagerank[page] = summa + first_condition
#
# # what I want to do?
import random

corpus = {
        "1.html": {"2.html", "3.html"},
        "2.html": {"3.html"},
        "3.html": {"2.html"}
    }


# for page_name in corpus:
#     for othe_page in corpus:
#         print(page_name, '->', othe_page)

print(random.random())