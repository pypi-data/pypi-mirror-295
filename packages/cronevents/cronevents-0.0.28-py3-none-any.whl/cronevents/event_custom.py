import math

from db import s3_db, env_db
import s3, time, datetime, helpful, job_manager, os
helpful.load_dot_env()
from MySQLite3 import SQL
from pipe_editor import test_code_pipelines
from event_manager import event
from job_api_update_all import update as _update_apis
from hcloud import Client
import datarova, pipe_manage, asyncio
from pipe_run import upload_code_from_file
from pipe_worker_temp_cleanup import cleanup_temp_tables_for_event

db = None
if __name__ == '__main__':
    os.environ['EVENTS_STATUS'] = 'ON'
    db = env_db()

# version = '1.0.4'

pg = {
    'pg_host': '5.161.204.150',
    'pg_port': '5433',
    'pg_user': 'elizabeth',
    'pg_password': 'e382050a-8b05-11ee-9d6c-acde48001122-6ef10ab6-38b7-43f8-938e-9c6ba7613fc3',
    'pg_database': 'junglr',
    'pg_public': 'false'
}


def report_status_snapshot(*args):

    q = '''select type, status, sum("count") from (
	select 'requests' as type, status, count(status) 
	from report_requests
	group by status
	union all
	select 
	'report' as type, status, count(status)
	from report_status
	group by status
	union all
	select 
	'report' as type, status, count(status) 
	from report_status_archive
	group by status
) as t
-- where type = 'report'
group by type, status;'''
    t1 = time.time()
    d, t, rd = \
        datetime.datetime.utcnow().strftime('%Y-%m-%d'), \
        datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'), \
        helpful.datetime_to_readable_str(datetime.datetime.utcnow())
    print("report_status_snapshot")
    db = env_db()  # s3_db(s3)
    data = db.download_table(sql=q)
    data = [
        {**row, 'date': d, 'time': t, 'readable_date': rd, 'epoch': t1}
        for row in data
    ]
    db.upload_table('report_status_snapshot', data)



@event('every 15 minutes', db=db)
def snapshots(*args):
    """
    Gather Snapshots of tables within "queries"
    """
    queries = [
#         {'table': 'pipe_steps_snapshots', 'query': '''
#     select status, sum("count") as "count"
# from (
# 	select status, count(status) as "count" from pipe_steps group by status
# 	union all
# 	select status, count(status) as "count" from pipe_steps_archive group by status
# 	union all
# 	select status, count(status) as "count" from pipe_steps_wait_list group by status
# ) as b group by status order by status desc;'''
#          },
        {'table': 'pipe_steps_snapshots',
         'final': 'select status, sum("count") as "count" from pipe_steps_snapshots group by status order by status desc;',
         'queries': ['select status, count(status) as "count" from pipe_steps group by status',
    	'select status, count(status) as "count" from pipe_steps_archive group by status',
    	'select status, count(status) as "count" from pipe_steps_wait_list group by status',]},
        {'table': 'pipe_snap', 'query': '''select status, count(status) as "count" from pipe_steps group by status;'''}
    ]

    for row in queries:
        if 'query' in row:
            table_name, query = row['table'], row['query']
            print(table_name)
            db = env_db()  # s3_db(s3)
            data = db.download_table(sql=query)
            t1 = time.time()
            d, t, rd = \
                datetime.datetime.utcnow().strftime('%Y-%m-%d'), \
                    datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'), \
                    helpful.datetime_to_readable_str(datetime.datetime.utcnow())
            data = [
                {**row, 'date': d, 'time': t, 'readable_date': rd, 'epoch': t1}
                for row in data
            ]
            db.upload_table(table_name, data, partition='date')
        elif 'queries' in row:
            try:
                db = env_db()
                sql = SQL({'location': 't.db'})
                try:
                    sql.query(f"drop table {row['table']};")
                    sql.connection.commit()
                except: pass

                for q in row['queries']:
                    sql.upload_table(row['table'], db.download_table(sql=q))


                table_name = row['table']
                print(table_name)
                data = sql.download_table(sql=row['final'])
                t1 = time.time()
                d, t, rd = \
                    datetime.datetime.utcnow().strftime('%Y-%m-%d'), \
                        datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'), \
                        helpful.datetime_to_readable_str(datetime.datetime.utcnow())
                data = [
                    {**row, 'date': d, 'time': t, 'readable_date': rd, 'epoch': t1}
                    for row in data
                ]
                db.upload_table(table_name, data, partition='date')
            except:
                pass


def update_business_reports():
    return test_code_pipelines('ac182e482a67c11ee97bfacde48001122226833eab4624382ad55f575f1150a9c')


@event('every 1 hour 1 minute', db=db)
def test():
    print('yay!!!')


@event('every 1 day @ 1 am', db=db)
def update_apis():
    _update_apis()


@event('every 1 day @ 10 pm', db=db)
def finish_gathering():
    return
    for i in range(5):
        job_manager.JobManager().run_job(
            'job_report_gather.py',
            env={**dict(os.environ), **pg}
        )
    return
    q = '''select type, status, sum("count") from (
	select 'requests' as type, status, count(status) 
	from report_requests
	group by status
	union all
	select 
	'report' as type, status, count(status)
	from report_status
	group by status
	union all
	select 
	'report' as type, status, count(status) 
	from report_status_archive
	group by status
) as t
-- where type = 'report'
group by type, status;'''
    db = env_db()  # s3_db(s3)
    data = db.download_table(sql=q)
    for row in data:
        if row['type'] == 'report' and row['status'] == 'waiting':
            n = helpful.try_number(row['sum'], on_fail_return_value=None)
            print('n', n, row['sum'], row)
            if isinstance(n, (float, int)):
                if n > 1000:
                    for i in range(5):
                        job_manager.JobManager().run_job(
                            'job_report_gather.py',
                            env={**dict(os.environ), **pg}
                        )


@event('every 1 day @ 10 pm', db=db)
def finish_requesting():
    return
    for i in range(5):
        job_manager.JobManager().run_job(
            'job_report_request.py',
            env={**dict(os.environ), **pg}
        )
    return
    def calculate_amount_of_vms_to_generate(now, last):
        reports_per_hour_goal = 1000
        daily_limit = 17000
        if now > daily_limit:
            return 2
        if now - last > 500:  # skip if new reports added to list
            return 0
        # print(f'(1000 - ({last} - {now})) / {500})', (1000 - (last - now)) / 500, f'(1000 - {last - now}) / 500)')
        return max(0,  # not lower than 0
                   min(2,  # not higher than 2
                       math.floor((reports_per_hour_goal - (last - now)) / 500)))

    q = '''select 
	"time", "type", status, "sum"
from report_status_snapshot
where status = 'pending' 
-- and time::timestamp < now() - interval '1 day'
order by epoch desc limit 2;'''
    db = env_db()  # s3_db(s3)
    data = db.download_table(sql=q)
    if len(data) > 2:
        current_snapshot, last_snapshot = data[0]['sum'], data[1]['sum']
        print('current_snapshot', current_snapshot, 'last_snapshot', last_snapshot)
        for vm_i in range(calculate_amount_of_vms_to_generate(current_snapshot, last_snapshot)):
            print('starting vm #', vm_i + 1)
            job_manager.JobManager().run_job(
                'job_report_request.py',
                env={**dict(os.environ), **pg}
            )




# q = '''select
# 	"time", "type", status, "sum"
# from report_status_snapshot
# where status = 'waiting'
# -- and time::timestamp < now()
# order by epoch desc limit 2;'''



# client = Client(token=os.environ['hz_write'])
servers = [
    # {
    #     'id': 40459205,
    #     'name': 'junglr'
    # },
    {
        'id': 40555689,
        'name': 'amazon-ads-requester-1-plus-server'
    },
    # {
    #     'id': 40556468,
    #     'name': 'amazon-ads-requester-2-plus-events'
    # },
    {
        'id': 40557133,
        'name': 'amazon-ads-gatherer-1'
    },
    {
        'id': 40557333,
        'name': 'amazon-ads-gatherer-2'
    }

]

def reboot(client, id):
    server = client.servers.get_by_id(id)
    server.power_off()
    while server.status not in {'off'}:
        time.sleep(1)
        server = client.servers.get_by_id(id)
    time.sleep(5)
    server.power_on()


@event('every 1 day @ 0:30 am', db=db)
def reboot_servers():
    client = Client(token=os.environ['hz_write'])
    for server in servers:
        reboot(client, server['id'])


def check_server_is_on(client: Client, id):
    server = client.servers.get_by_id(id)
    if server.status not in {'running', 'starting'}:
        server.reboot()


@event('every 1 day @ 0:50 am', db=db)
def check_servers_are_on():
    client = Client(token=os.environ['hz_write'])
    for server in servers:
        check_server_is_on(client, server['id'])


@event('every 1 day @ 11:00 am', db=db)
def datarova_google_sheet_pull():
    datarova.pull_and_push_google_sheet()


@event('every 1 hour', db=db)
def reset_errors():
    db = env_db()  # s3_db(s3)
    db.query("update pipe_steps set status = 'waiting' where status = 'error'")


@event('every 1 day @ 0:20 am', db=db)  # UTC
def upload_reports_to_process():
    # with open('pipe_amazon_ads_api_reports.pipe') as f:
    #     code = f.read()
    # upload_code(code)
    upload_code_from_file('pipe_amazon_ads_api_reports.pipe')
    # with open('pipe_amazon_ads_api_reports.pipe') as f:
    #     upload_code_v2(f.read())

    # with open('pipe_amazon_ads_brand_metrics.pipe') as f:
    #     code = f.read()
    # upload_code(code)
    # upload_code_from_file('pipe_amazon_ads_brand_metrics.pipe')
    #
    # upload_code_from_file('pipe_amazon_ads_api_entity_lists.pipe')


@event('every 5 minutes', db=db)
def check_pipe_status():
    # return
    asyncio.run(pipe_manage.manage())


@event('every 1 hour', db=db)
def cleanup_temp_tables_for_etl():
    cleanup_temp_tables_for_event()


if __name__ == '__main__':
    # os.environ['EVENTS_STATUS'] = 'ON'
    # upload_reports_to_process()
    print('done')
    exit(0)








