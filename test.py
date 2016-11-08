from watson_developer_cloud import AlchemyLanguageV1
from cloudant import cloudant
from cloudant.client import Cloudant
from cloudant.document import Document
from flask import jsonify
import json
import pygal
from pygal.style import DarkSolarizedStyle
import requests

list = [    "http://www.news.uwa.edu.au/201611049179/aboriginal-people-inhabited-was-mid-west-coast-much-earlier-previously-thought",
            "http://www.news.uwa.edu.au/201610289154/would-you-return-lost-letter",
            "http://www.news.uwa.edu.au/201609149027/research/astronomers-shed-light-different-galaxy-types",
            "http://www.news.uwa.edu.au/201609059000/research/new-find-puts-people-dampier-archipelago-last-ice-age",
            "http://www.news.uwa.edu.au/201608248962/awards-and-prizes/research-help-premature-babies-recognised-national-awards",
            "http://www.news.uwa.edu.au/201608238961/august-2016/uwa-joins-un-global-compact",
            "http://www.news.uwa.edu.au/201608178949/research/research-helps-treatment-heart-attacks-and-angina-aboriginal-people",
            "http://www.news.uwa.edu.au/201608118927/research/lack-copper-ancient-soil-regulates-nitrification",
            "http://www.news.uwa.edu.au/201607138853/business-and-industry/uwa-sponsors-evening-steve-wozniak",
            "http://www.news.uwa.edu.au/201606308790/uwa-engineering-students-visit-broome",
            "http://www.news.uwa.edu.au/201611049178/grant-win-lung-fibrosis-research",
            "http://www.news.uwa.edu.au/201610279149/research/new-chair-pioneer-next-generation-treatments-eye-disease",
            "http://www.news.uwa.edu.au/201610209134/arts-and-culture/art-event-set-draw-crowd",
            "http://www.news.uwa.edu.au/201608188951/research/carbon-levels-soil-affected-climatic-conditions",
            "http://www.news.uwa.edu.au/201607268879/exciting-young-violinist-wins-helpmann-award",
            "http://www.news.uwa.edu.au/201606278776/awards-and-prizes/st-hildas-student-wins-was-brain-bee-challenge",
            "http://www.news.uwa.edu.au/201610319159/international/most-meth-users-too-embarrassed-seek-treatment",
            "http://www.news.uwa.edu.au/201610209133/international/astrophysicists-map-milky-way",
            "http://www.news.uwa.edu.au/201609209041/international/uwa-drug-offers-new-hope-young-muscular-dystrophy-sufferers",
            "http://www.news.uwa.edu.au/201609139020/three-s-crowd-arrival-new-centrifuge",
            "http://www.news.uwa.edu.au/201608098920/international/first-australian-universities-join-global-collaboration",
            "http://www.news.uwa.edu.au/201607048798/arts-and-culture/naidoc-week-celebrate-indigenous-achievements",
            "http://www.news.uwa.edu.au/201610259143/research/new-tool-detects-malignant-breast-cancer-tissue-during-surgery",
            "http://www.news.uwa.edu.au/201610109103/alumni/ten-years-impact-was-only-nobel-prize",
            "http://www.news.uwa.edu.au/201609279063/business-and-industry/uwa-and-dafwa-dig-deep-soil-science-alliance",
            "http://www.news.uwa.edu.au/201609058998/awards-and-prizes/uwa-awards-and-achievements-august-2016",
            "http://www.news.uwa.edu.au/201608318984/embrace-power-natural-experiments",
            "http://www.news.uwa.edu.au/201608118929/awards-and-prizes/swimmer-tamsin-cook-takes-home-silver-rio",
            "http://www.news.uwa.edu.au/201608088915/research/researchers-aim-boost-physical-activity-preschoolers",
            "http://www.news.uwa.edu.au/201608028897/international/stable-housing-homeless-will-save-millions-each-year",
            "http://www.news.uwa.edu.au/201607258876/awards-and-prizes/leading-researchers-named-finalists-premiers-science-awards",
            "http://www.news.uwa.edu.au/201607078819/perth-and-peel-students-get-taste-campus-life",
            "http://www.news.uwa.edu.au/201606278775/july-2016/researchers-uwa-awarded-fulbright-scholarships",
            "http://www.news.uwa.edu.au/201611019163/awards-and-prizes/uwa-awarded-178-million-national-research-funding",
            "http://www.news.uwa.edu.au/201610319162/awards-and-prizes/astrophysicist-wins-2016-young-tall-poppy-award",
            "http://www.news.uwa.edu.au/201610179117/awards-and-prizes/pre-term-babies-learn-night-day",
            "http://www.news.uwa.edu.au/201609018987/decoding-clover-dna-leads-better-livestock-productivity",
            "http://www.news.uwa.edu.au/201608258967/awards-and-prizes/ceme-offshore-engineer-wins-prestigious-science-award",
            "http://www.news.uwa.edu.au/201608038902/international/growing-legumes-solution-human-health-and-sustainable-food-production",
            "http://www.news.uwa.edu.au/201607068812/research/anxious-western-australians-less-prepared-bushfires",
            "http://www.news.uwa.edu.au/201607058805/uwa-awards-and-achievements-june-2016",
            "http://www.news.uwa.edu.au/201611049177/ocean-glider-sets-sail-sri-lanka",
            "http://www.news.uwa.edu.au/201609069003/awards-and-prizes/uwa-law-dean-wins-national-academic-honour",
            "http://www.news.uwa.edu.au/201608158942/events/future-students-and-families-enjoy-uwa-open-day",
            "http://www.news.uwa.edu.au/201608038906/research/perpretual-ice-water-solid-liquid-state-revealed-gallium-nanoparticles",
            "http://www.news.uwa.edu.au/201607288890/international/new-engineering-program-aims-deliver-medical-breakthroughs",
            "http://www.news.uwa.edu.au/201607128850/alumni/uwa-student-and-alumni-chase-olympic-glory",
            "http://www.news.uwa.edu.au/201609149025/international/research-aims-show-how-plastic-surgery-will-really-look",
            "http://www.news.uwa.edu.au/201609129014/arts-and-culture/uwa-pays-tribute-artist-miriam-stannage",
            "http://www.news.uwa.edu.au/201609018988/innovation-science-recognised-2016-eureka-awards",
            "http://www.news.uwa.edu.au/201608198954/alumni/young-uwa-researchers-recognised-premiers-science-awards",
            "http://www.news.uwa.edu.au/201607128849/events/holiday-science-fun-indigenous-school-students",
            "http://www.news.uwa.edu.au/201611039173/awards-and-prizes/seed-flamer-wins-wa-innovator-year",
            "http://www.news.uwa.edu.au/201610289158/uwa-student-awarded-2017-rhodes-scholarship",
            "http://www.news.uwa.edu.au/201610249138/international/hopping-genes-provide-clue-frogs-origin",
            "http://www.news.uwa.edu.au/201610189122/research/study-finds-pesticide-levels-wa-breast-milk-lowest-world",
            "http://www.news.uwa.edu.au/201610049086/international/breast-density-matters-detection-breast-cancer",
            "http://www.news.uwa.edu.au/201610039080/research/how-much-gluten-foods-labelled-gluten-free",
            "http://www.news.uwa.edu.au/201608118926/august-2016/uwa-book-sale-friday-19-wednesday-24-august",
            "http://www.news.uwa.edu.au/201608108922/students/uwa-goes-public-atar-entry-scores",
            "http://www.news.uwa.edu.au/201607288888/awards-and-prizes/uwa-flaming-seed-team-finalists-wa-innovator-year-competition",
            "http://www.news.uwa.edu.au/201607198862/research/3d-printing-used-explore-superconductivity-materials",
            "http://www.news.uwa.edu.au/201607088828/kelp-forests-great-southern-reef-wiped-out-marine-heatwave",
            "http://www.news.uwa.edu.au/201607068808/reversible-contraceptive-use-high-among-aboriginal-women-western-desert",
            "http://www.news.uwa.edu.au/201607048795/international/shark-shield-proves-effective-deterring-white-sharks",
            "http://www.news.uwa.edu.au/201611039170/perth-international-arts-festival-launches-2017-program",
            "http://www.news.uwa.edu.au/201610049093/awards-and-prizes/uwa-awards-and-achievements-september-2016",
            "http://www.news.uwa.edu.au/201609279065/arts-and-culture/new-season-art-exhibitions-opens-uwa",
            "http://www.news.uwa.edu.au/201609269056/international/australian-technology-installed-world-s-largest-single-dish-radio-telesco",
            "http://www.news.uwa.edu.au/201608248963/international/worlds-biggest-telescope-meets-worlds-second-fastest-supercomputer",
            "http://www.news.uwa.edu.au/201608198953/international/rising-sea-levels-could-benefit-some-reef-systems",
            "http://www.news.uwa.edu.au/201608128930/events/science-event-brings-life-fascinating-world-biology",
            "http://www.news.uwa.edu.au/201608048910/awards-and-prizes/uwa-awards-and-achievements-july-2016",
            "http://www.news.uwa.edu.au/201610269146/stricter-speed-enforcement-can-impair-driver-safety",
            "http://www.news.uwa.edu.au/201609099011/students/online-course-help-musicians-around-world",
            "http://www.news.uwa.edu.au/201608308978/research/doctors-urged-be-cautious-when-treating-low-testosterone",
            "http://www.news.uwa.edu.au/201608298971/events/discover-something-new-uwa-research-week",
            "http://www.news.uwa.edu.au/201608028898/international/male-bees-fight-back-against-stds",
            "http://www.news.uwa.edu.au/201608018894/international/uwa-welcomes-chinese-and-vietnamese-students",
            "http://www.news.uwa.edu.au/201607218870/arts-and-culture/miriam-stannage-exhibition-opens-uwa",
            "http://www.news.uwa.edu.au/201610319160/research/services-support-homeless-need-alternative-funding-sources",
            "http://www.news.uwa.edu.au/201610289155/international/fossilised-dinosaur-brain-tissue-identified-first-time",
            "http://www.news.uwa.edu.au/201610279148/research/new-invention-aids-detection-prevalent-parasitic-disease",
            "http://www.news.uwa.edu.au/201610119106/international/walking-dog-keeps-owners-healthy-and-neighbourhoods-feeling-safe",
            "http://www.news.uwa.edu.au/201609099009/research/simple-blood-test-could-be-used-detect-breast-cancer",
            "http://www.news.uwa.edu.au/201609058999/vice-chancellor/message-uwa-vice-chancellor",
            "http://www.news.uwa.edu.au/201607088827/research/community-given-vital-input-advancing-medical-research"]

print(len(list))
#
# cl_username = "1a818337-f029-449a-8a03-d34f30877d1d-bluemix"
# cl_password = "b20bcbf26bac5fa4ed56df09b07755ac1d8ccf6e3d3ad1177902957c1ca192c0",
# cl_url      = "https://1a818337-f029-449a-8a03-d34f30877d1d-bluemix:b20bcbf26bac5fa4ed56df09b07755ac1d8ccf6e3d3ad1177902957c1ca192c0@1a818337-f029-449a-8a03-d34f30877d1d-bluemix.cloudant.com"
#
# auth = (cl_username, cl_password)
# client = Cloudant(cl_username, cl_password, url=cl_url)
#
# # Connect to the server
# client.connect()
#
# # Perform client tasks...
# session = client.session()
# my_database = client['x']
#
# if my_database.exists():
#     print('SUCCESS!')
#
# alchemy = AlchemyLanguageV1(api_key='6026adae6314a2a74df3c7a23a8e99d7f6e20c28')
# url = 'http://www.news.uwa.edu.au/201611019163/awards-and-prizes/uwa-awarded-178-million-national-research-funding'
# combined_operations = ['title', 'authors', 'pub-date', 'entities', 'keywords',  'taxonomy', 'relations', 'concepts',
#                        'doc-emotion']
# data = alchemy.combined(url=url, extract=combined_operations)
# doc = my_database.create_document(data)
# if doc.exists():
#     print('SUCCESS 2!')
# print(json.dumps(data, indent=2))
# end_point = '{0}/{1}'.format(cl_url, 'x/_design/des/_view/new-view1')
# #params = {'include_docs': 'true'}
# r = requests.get(end_point)
# print(r.json())
# r = r.json()
# t = []
# for item in r.get('rows'):
#     dict={}
#     dict['key'] = item.get('key')
#     dict['value'] = item.get('value')
#     t.append(dict)
# #print(t)
# doc = my_database['1d8c54f34b43c94894f01744608dbf46']
# #print(json.dumps(doc))
# # Disconnect from the server
# relevance =  [float(i['value']) for i in t]
# title = 'Most Relevant Topics'
# bar_chart = pygal.Bar(width=1200, height=600,
#                       explicit_size=True, title=title, style=DarkSolarizedStyle)
# bar_chart.x_labels = ['%s' % str(i['key']) for i in t]
# bar_chart.add('Relevance', relevance)
# html = """
#         <html>
#              <head>
#                   <title>%s</title>
#              </head>
#               <body>
#                  %s
#              </body>
#         </html>
#         """ % (title, bar_chart.render())
# #bar_chart.render_to_png('chart.png')
# client.disconnect()

#doc = my_database['1d8c54f34b43c94894f01744608dbf46']
#end_point = 'https://1a818337-f029-449a-8a03-d34f30877d1d-bluemix
# :b20bcbf26bac5fa4ed56df09b07755ac1d8ccf6e3d3ad1177902957c1ca192c0@1a818337-f029-449a-8a03-d34f30877d1d-bluemix.cloudant.com/x/_design/des/_view/new-view'
# params = {"include_docs" : "true"}
#  response = client.r_session.get(end_point, params=params)
#return response.json()
# Define the end point and parameters
# Issue the request
#params = {'include_docs': 'true'}
# response = client.r_session.get(end_point, params=params)
# Display the response content
#return response.json()
#j = requests.get('https://1a818337-f029-449a-8a03-d34f30877d1d-bluemix
# :b20bcbf26bac5fa4ed56df09b07755ac1d8ccf6e3d3ad1177902957c1ca192c0@1a818337-f029-449a-8a03-d34f30877d1d-bluemix.cloudant.com/x/_design/des/_view/new-view')
#return j