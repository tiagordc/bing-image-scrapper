from imagededup.methods import PHash
import argparse, requests, cv2, os, glob

# defaults
API_KEY = os.environ['BING_SEARCH_KEY']
URL =  os.environ['BING_SEARCH_URL']
MAX_RESULTS = 250
GROUP_SIZE = 50
EXCEPTIONS = set([IOError, FileNotFoundError, requests.exceptions.RequestException, requests.exceptions.HTTPError, requests.exceptions.ConnectionError, requests.exceptions.Timeout])

if __name__ == '__main__':

	# parse the arguments
	ap = argparse.ArgumentParser()
	ap.add_argument("-q", "--query", required=True, help="search query to search Bing Image API for")
	ap.add_argument("-o", "--output", required=True, help="path to output directory of images")
	ap.add_argument("-s", "--size", required=False, help="image size: Small, Medium, Large, Wallpaper, All", default='All')
	args = vars(ap.parse_args())

	# check output directory
	directory = os.path.sep.join(["data", args["output"]])
	if not os.path.exists(directory): os.makedirs(directory)
	directoryFiles = glob.glob(directory + os.path.sep + "*")
	if len(directoryFiles) == 0: nameOffset = 0
	else:
		latestFile = max(directoryFiles, key=os.path.getctime)
		nameOffset = int(os.path.splitext(os.path.basename(latestFile))[0]) + 1

	# search parameters
	term = args["query"]
	headers = {"Ocp-Apim-Subscription-Key" : API_KEY}
	params = {"q": term, "offset": 0, "count": GROUP_SIZE, 'size': args['size']}

	# make the search
	print("[INFO] searching Bing API for '{}'".format(term))
	search = requests.get(URL, headers=headers, params=params)
	search.raise_for_status()
	results = search.json()
	estNumResults = min(results["totalEstimatedMatches"], MAX_RESULTS)
	print("[INFO] {} total results for '{}'".format(estNumResults, term))
	total = 0

	for offset in range(0, estNumResults, GROUP_SIZE):
		
		print("[INFO] making request for group {}-{} of {}...".format(offset, offset + GROUP_SIZE, estNumResults))		
		params["offset"] = offset
		search = requests.get(URL, headers=headers, params=params)
		search.raise_for_status()
		results = search.json()
		print("[INFO] saving images for group {}-{} of {}...".format(offset, offset + GROUP_SIZE, estNumResults))

		for v in results["value"]:

			try:
				print("[INFO] fetching: {}".format(v["contentUrl"]))
				r = requests.get(v["contentUrl"], timeout=30)
				ext = v["contentUrl"][v["contentUrl"].rfind("."):]
				p = os.path.sep.join(["data", args["output"], "{}{}".format(str(nameOffset + total).zfill(8), ext)])
				f = open(p, "wb")
				f.write(r.content)
				f.close()
			except Exception as e:
				if type(e) in EXCEPTIONS:
					print("[INFO] skipping: {}".format(v["contentUrl"]))
					continue
		
			image = cv2.imread(p)
			if image is None:
				print("[INFO] deleting: {}".format(p))
				os.remove(p)
				continue

			total += 1

	# remove duplicates
	phasher = PHash()
	duplicates = phasher.find_duplicates_to_remove(image_dir=directory)
	print("[INFO] removing {} duplicates".format(str(len(duplicates))))
	for duplicate in duplicates: os.remove(os.path.join(directory, duplicate))
	