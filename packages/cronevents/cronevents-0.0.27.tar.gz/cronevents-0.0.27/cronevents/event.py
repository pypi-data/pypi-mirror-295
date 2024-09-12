import os, sys, time, shlex, subprocess  # , io, threading, uuid, time, traceback
import datetime
from cronevents.event_manager import get_db
import buelon.helpers.sqlite3_helper
import buelon.helpers.postgres


LOG_CRON_EVENT_LOGS = os.environ.get('LOG_CRON_EVENT_LOGS', None) == 'true'


def main():
    try:
        # get event id
        event_id = sys.argv[-5]

        # get module
        og_module = module = sys.argv[-4]

        # get function name
        func = sys.argv[-3]

        # get args
        args = sys.argv[-2]

        # get kwargs
        kwargs = sys.argv[-1]

        # print(module, func, args, kwargs)

        script = '-c "import cronevents.event_run;cronevents.event_run.main()"'  # os.path.join(os.getcwd(), 'event_run.py')
        cmd = f'{sys.executable} {script} {module} {func} {args} {kwargs}'
        # print('running', f'"{cmd}"')

        process = subprocess.Popen(
            shlex.split(cmd),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=os.getcwd(),
            env=dict(os.environ)
        )

        if not LOG_CRON_EVENT_LOGS:
            process.wait()
        else:
            # wait for the process to terminate
            out, err = process.communicate()
            t = time.time()
            logs = [
                {'event_id': event_id, 'index': i, 'line': line, 'epoch': t, 'utc_time': datetime.datetime.utcfromtimestamp(t)}
                for i, line in enumerate(out.decode().splitlines() + err.decode().splitlines())
            ]
            db = get_db()
            kwargs = {}
            index_query = 'create index if not exists event_logs_event_id_idx on cron_events_log (event_id);'
            if isinstance(db, buelon.helpers.postgres.Postgres):
                index_query = 'create index if not exists event_logs_event_id_idx on cron_events_log using hash (event_id);'
                kwargs['partition'] = 'event_id'
                kwargs['partition_query'] = f'''CREATE TABLE if not exists "cron_events_log_{event_id}" 
                        PARTITION OF "cron_events_log" FOR VALUES IN ('{event_id}');'''
            if logs:
                db.upload_table(
                    f'cron_events_log',
                    logs,
                    id_column=['event_id', 'index']
                )
                db.query(index_query)
            errcode = process.returncode
    finally:
        try:
            os.remove(sys.argv[-2])
        except:
            pass
        try:
            os.remove(sys.argv[-1])
        except:
            pass


if __name__ == '__main__':
    main()

























# import os, sys, json, importlib, io, threading, uuid, time, traceback
# from event_manager import get_db
# from MySQLite3 import SQL
#
# # ID = f'e{uuid.uuid1()}{uuid.uuid4()}'.replace('-', '')
# # if not os.path.exists('events'):
# #     try:
# #         os.makedirs('events')
# #     except: pass
# # db_path = os.path.join('events', f'events_{ID}.db')
# # db = SQL({'location': db_path})
# try:
# #     logging = True
# #     def logger():
# #         global logging, og_module
# #         def update():
# #             global logging, og_module
# #             try:
# #                 tb = db.download_table(sql='SELECT * FROM event_py_logs order by epoch desc limit 20;')
# #                 get_db().upload_table(
# #                     'event_py_logs',
# #                     tb,
# #                     id_column='id'
# #                 )
# #                 ids = ','.join([f"'{row['id']}'" for row in tb])
# #                 db.query('delete from event_py_logs where id in (' + ids + ');')
# #             except: pass
# #         while logging:
# #             update()
# #             time.sleep(1.)
# #         update()
# #     _logger = threading.Thread(target=logger)
# #     # _logger.start()
# #
# #     class SysOverride(io.StringIO):
# #         error = False
# #
# #         def write(self, s):
# #             # self.stdout.write(s)
# #             if self.error:
# #                 ogs[-1].write(s)
# #                 db.upload_table('event_py_logs', [{
# #                     'id': str(uuid.uuid1())+str(uuid.uuid4()),
# #                     'module':  og_module,
# #                     'function': func,
# #                     'session': ID,
# #                     'epoch': time.time(),
# #                     'error':  True,
# #                     'message': s,
# #                     'trace': traceback.format_exc(),
# #                 }], id_column='id')
# #             else:
# #                 ogs[0].write(s)
# #                 db.upload_table('event_py_logs', [{
# #                     'id': str(uuid.uuid1())+str(uuid.uuid4()),
# #                     'module':  og_module,
# #                     'function': func,
# #                     'session': ID,
# #                     'error': False,
# #                     'epoch': time.time(),
# #                     'message': s,
# #                 }], id_column='id')
# #     ogs = (sys.stdout, sys.stderr)
#     try:
#         # logs = SysOverride()
#         # err_logs = SysOverride()
#         # err_logs.error = True
#         # sys.stdout = logs
#         # sys.stderr = err_logs
#         # _logger.start()
#
#         # get module
#         og_module = module = sys.argv[-4]
#
#         # get function name
#         func = sys.argv[-3]
#
#         # get args
#         with open(sys.argv[-2], "r") as f:
#             args = json.load(f)
#         try:
#             os.remove(sys.argv[-2])
#         except Exception as e:
#             print('Error deleting ', sys.argv[-2], e)
#
#         # get kwargs
#         with open(sys.argv[-1], "r") as f:
#             kwargs = json.load(f)
#         try:
#             os.remove(sys.argv[-1])
#         except Exception as e:
#             print('Error deleting ', sys.argv[-1], e)
#
#
#         print(module, func, args, kwargs)
#
#
#         # import module
#         module = importlib.import_module(module)
#
#
#         # call function
#         if hasattr(module, func):
#             getattr(module, func)(*args, **kwargs)
#         else:
#             print(f"Function {func} not found in module {og_module}")
#             # sys.exit(1)
#     finally:
#         try:
#             os.remove(sys.argv[-2])
#         except:
#             pass
#         try:
#             os.remove(sys.argv[-1])
#         except:
#             pass
#
#     # print('stopping log')
#     # logging = False
#     # _logger.join()
#     #
#     # print('log stopped')
#     # sys.stdout, sys.stderr = ogs
#
#     # print('committing and closing')
#     # db.connection.commit()
#     # db.connection.close()
#     # print('closing')
# finally:
#     pass
# #     try:
# #         os.remove(db.location)
# #     except Exception as e:
# #         print(e)
# #         traceback.print_exc()
# #     print('done')
# #     del db
#
#
#
#
#
#
#
#
#
#
#
#
#
#
