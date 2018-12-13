def filter_unique(oldlist, field):
	obj = {}
	newlist = []
	for ele in oldlist:
		if ele[field] not in obj:
			newlist.append(ele)
			obj[ele[field]] = True
	return newlist