import multiprocessing
from db.get_items_by_pk import get_items_by_pk
from db.update_item import update_item

print('--> Loading function...')


def lambda_handler(event, context):
    pk = event['PK']
    new_text = event['Text']
    items = get_items_by_pk(pk)

    processes = []
    for item in items['Items']:
        p = multiprocessing.Process(
            target=update_item,
            args=(pk, item['SK'], new_text),
        )
        print()
        processes.append(p)
        p.start()

    for process in processes:
        process.join()

    return {
        "msg": 'Running Multi Process Lambda'
    }
