def get_latest_rds_snapshot_id(event, context):
    print('In get latest snapshot')
    print('event', event)
    print('context', context)
    print('try to import boto')
    import boto3
    client = boto3.client('rds')
    paginator = client.get_paginator('describe_db_snapshots')
    response = paginator.paginate()
    print(list(response))
