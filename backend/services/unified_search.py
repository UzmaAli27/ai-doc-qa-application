from services.unified_store import UNIFIED_STORE


def unified_search(query):

    print("SEARCH QUERY:", query)

    print("TOTAL STORED:", len(UNIFIED_STORE))

    results = []

    for item in UNIFIED_STORE:

        if query.lower() in item["content"].lower():

            results.append(item)

    print("MATCHED:", len(results))

    return results