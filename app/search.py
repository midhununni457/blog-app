from flask import current_app, app
# from threading import Timer

def add_to_index(index, model):
    #  with app.app_context():
        # if not current_app.elasticsearch.indices.exists(index=index):
        #     current_app.elasticsearch.indices.create(index=index, ignore=400)
    if not current_app.elasticsearch:
        return
    payload = {}
    for field in model.__searchable__:
        payload[field] = getattr(model, field)
    current_app.elasticsearch.index(index=index, id=model.id, document=payload)

def remove_from_index(index, model):
    if not current_app.elasticsearch:
        return
    current_app.elasticsearch.delete(index=index, id=model.id)

def query_index(index, query, page, per_page):
    if not current_app.elasticsearch:
        return [], 0
    search = current_app.elasticsearch.search(
        index=index,
        query={'multi_match': {'query': query, 'fields': ['*']}},
        from_=(page - 1) * per_page,
        size=per_page)
    ids = [int(hit['_id']) for hit in search['hits']['hits']]
    return ids, search['hits']['total']['value']

# def create_index_periodically():
#     index_name = 'post'
#     if not current_app.elasticsearch.indices.exists(index=index_name):
#         current_app.elasticsearch.indices.create(index=index_name, ignore=400)

# # Schedule the creation to run in the background
# Timer(5, create_index_periodically).start()  # Run after 5 seconds

# print(current_app.elasticsearch.indices.exists(index='post'))  # Check if the index exists
