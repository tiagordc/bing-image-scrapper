import argparse, requests, cv2, os, re

# defaults
API_KEY = os.environ['BING_SEARCH_KEY']
URL =  os.environ['BING_SEARCH_URL']
GROUP_SIZE = 50

if __name__ == '__main__':

	# parse the arguments
	ap = argparse.ArgumentParser()
	ap.add_argument("-q", "--query", required=True, help="search query to search Bing Image API for")
	ap.add_argument("-f", "--folder", required=True, help="path to output directory of images")
	ap.add_argument("-s", "--size", required=False, help="image size: Small, Medium, Large, Wallpaper, All", default='All')
	ap.add_argument("-c", "--color", required=False, help="image color: ColorOnly, Monochrome, Black, Blue, Brown, Gray, Green, Orange, Pink, Purple, Red, Teal, White, Yellow")
	ap.add_argument("-t", "--time", required=False, help="image discovered: Day, Week, Month")
	ap.add_argument("-m", "--max", required=False, help="max results", default="1000")
	args, unknown = ap.parse_known_args()

	# check output directory
	directory = os.path.sep.join(["data", args.folder])
	if not os.path.exists(directory): os.makedirs(directory)

	# search parameters
	term = args.query
	headers = {"Ocp-Apim-Subscription-Key" : API_KEY}
	params = {"q": term, "offset": 0, "count": GROUP_SIZE, 'size': args.size, 'color': args.color, 'freshness': args.time}

	# make the search
	print("[INFO] searching Bing API for '{}'".format(term))
	search = requests.get(URL, headers=headers, params=params)
	search.raise_for_status()
	results = search.json()
	estNumResults = min(results["totalEstimatedMatches"], int(args.max))
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
				match = re.search(r"\.(\w{3,4})(?:$|\?)", v["contentUrl"])
				if not match: continue
				ext = match.group(1).lower()
				if ext not in ['png', 'jpg', 'jpeg', 'tiff', 'bmp', 'gif']: continue
				p = os.path.sep.join(["data", args.folder, "{}.{}".format(str(total).zfill(8), ext)])
				f = open(p, "wb")
				f.write(r.content)
				f.close()
			except Exception:
				continue
		
			image = cv2.imread(p)

			if image is None:
				try:
					os.remove(p)
					print("[INFO] {} deleted".format(p))
				except Exception:
					print("[ERROR] could not delete {}".format(p))
				continue

			total += 1

