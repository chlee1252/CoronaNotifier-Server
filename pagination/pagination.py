def getPaginatedList(results, url, start, limit):
  count = len(results)
  if not start: start = 1
  if not limit: limit = count
  start = int(start)
  limit = int(limit)
  if (count < start):
    raise '404 Error'
  
  obj = {}
  obj['start'] = start
  obj['limit'] = limit
  obj['count'] = count


  if start == 1:
    obj['previous'] = ''
  else:
    start_copy = max(1, start - limit)
    limit_copy = start - 1
    obj['previous'] = url + '?start=%d&limit=%d' % (start_copy, limit_copy)
  
  if start + limit > count:
    obj['next'] = ''
  else:
    start_copy = start + limit
    obj['next'] = url + '?start=%d&limit=%d' % (start_copy, limit)
  
  obj['results'] = results[(start-1):(start - 1 + limit)]

  return obj