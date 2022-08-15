import threading
from db.get_items_by_pk import get_items_by_pk
from db.update_item import update_item

print('--> Loading function...')


def lambda_handler(event, context):
    pk = event['PK']
    new_text = event['Text']
    items = get_items_by_pk(pk)

    thread_list = []
    for item in items['Items']:
        thread = threading.Thread(
            target=update_item,
            args=(pk, item['SK'], new_text),
        )
        thread_list.append(thread)
        thread.start()

    for thread in thread_list:
        thread.join()

    return {
        "msg": 'Running Multi Thread Lambda'
    }
