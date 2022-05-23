from youtube_search import YoutubeSearch

results = YoutubeSearch("jfla", max_results=10).to_dict()

print(results)
