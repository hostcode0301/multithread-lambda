import json
import random
import string
from dynamodb_json import json_util as dynamodb_json_utils


def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    print("Random string of length", length, "is:", result_str)


parent_folder = '.'

with open(f'{parent_folder}/raw_data.json', 'r') as f:
    data = json.load(f)

batch_write_data = {
    "multithread-lambda-dynamodb-table": [
    ]
}

for item in data:
    email = item.get('Email', None)
    if email:
        item.update({
            "PK": "ACC#929B5657-2A63-9052-BCE9-FB22C655B98B",
            "SK": f"ACC#{email}",
        })
    else:
        item.update({
            "PK": "ACC#929B5657-2A63-9052-BCE9-FB22C655B98B",
            "SK": f"ACC#{get_random_string(10)}",
        })

    batch_write_data["multithread-lambda-dynamodb-table"].append({
        "PutRequest": {
            "Item": dynamodb_json_utils.dumps(item, as_dict=True)
        }
    })

with open(f'{parent_folder}/processed_data.json', 'w') as f:

    json.dump(batch_write_data, f, indent=4)
    print(f'{len(data)} items written to processed_data.json')
