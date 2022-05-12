import boto3


def get_rds_client():
    return boto3.client('rds')


def get_describe_db_snapshots_paginator(client):
    return client.get_paginator('describe_db_snapshots')


def make_query(paginator, **kwargs):
    return paginator.paginate(**kwargs)


def get_results(query):
    for result in query:
        for snapshot in result['DBSnapshots']:
            yield snapshot


def sort_results_by_create_time(results):
    return sorted(
        results,
        key=lambda result: result['SnapshotCreateTime'],
        reverse=True
    )


def get_latest_result(sorted_results):
    return list(sorted_results)[0]


def get_latest_rds_snapshot_id(event, context):
    print('In get latest snapshot')
    print('event', event)
    print('context', context)

    client = get_rds_client()
    paginator = get_describe_db_snapshots_paginator(client)
    query = make_query(paginator)
    results = get_results(query)
    sorted_results = sort_results_by_create_time(
        results
    )
    latest_result = get_latest_result(sorted_results)
    return latest_result
