"""
This module contains related classes for monitoring the pipeline progress status.

The following classes are available:

    * :class:`PipelineProgressStatusMonitor`
    * :class:`SimplePipelineProgressStatusMonitor`
"""

# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=too-few-public-methods
# pylint: disable=too-many-instance-attributes
# pylint: disable=protected-access, bare-except
# pylint: disable=no-else-continue
# pylint: disable=broad-except
# pylint: disable=superfluous-parens
# pylint: disable=simplifiable-if-statement
# pylint: disable=no-self-use
# pylint: disable=no-else-break
# pylint: disable=invalid-name
# pylint: disable=unused-argument
import os
import threading
import time
import json
import pandas as pd
from prettytable import PrettyTable
from hana_ml.dataframe import ConnectionContext
from hana_ml.visualizers.shared import EmbeddedUI


def create_interrupt_file(iframe_id):
    EmbeddedUI.generate_file(EmbeddedUI.get_resource_temp_file_path(iframe_id), '')


class AutomaticObjProxy(object):
    def __init__(self, automatic_obj, connection_context: ConnectionContext):
        self.target_obj = automatic_obj
        self.progress_indicator_id = None
        self.connection_context = connection_context
        self.highlight_metric = None

        self.connection_id = None

        self.target_obj._exist_auto_sql_content_log(self.connection_context)
        self.use_auto_sql_content = self.target_obj._use_auto_sql_content
        self.auto_sql_content_schema = self.target_obj.auto_sql_content_schema

        self.is_simple_mode = False

    def create_fetch_table_task(self, task_manager, fetch_table_interval):
        fetch_table_task = None
        if self.use_auto_sql_content:
            fetch_table_task = FetchProgressStatusFromAutoSQLContent(task_manager, fetch_table_interval, self.connection_context, self.auto_sql_content_schema)
        else:
            fetch_table_task = FetchProgressStatusFromSystemTableTask(task_manager, fetch_table_interval, self.connection_context)
        return fetch_table_task

    def reset_data(self):
        if self.target_obj.progress_indicator_id is None:
            self.target_obj.progress_indicator_id = "AutoML-{}".format(self.target_obj.gen_id)
        self.progress_indicator_id = self.target_obj.progress_indicator_id

        self.highlight_metric = self.target_obj._get_highlight_metric()
        self.target_obj.persist_progress_log()
        self.target_obj._status = 0

    def clear_data(self):
        self.target_obj.cleanup_progress_log(EmbeddedUI.create_connection_context(self.connection_context))

    def cancel_task(self):
        # sql = "ALTER SYSTEM DISCONNECT SESSION '{}'"
        # sql = "ALTER SYSTEM CANCEL WORK IN SESSION '{}'"
        if self.connection_id is None:
            self.connection_id = self.target_obj.fit_data.connection_context.connection_id
        cancel_task_connection_context = EmbeddedUI.create_connection_context(self.connection_context)
        cancel_task_connection_context.execute_sql("ALTER SYSTEM CANCEL WORK IN SESSION '{}'".format(self.connection_id))
        cancel_task_connection_context.close()

    def get_status(self):
        return self.target_obj._status


class AutomaticEmptyObjProxy(object):
    def __init__(self, progress_indicator_id, connection_context: ConnectionContext, highlight_metric):
        self.progress_indicator_id = progress_indicator_id
        self.connection_context = connection_context
        self.highlight_metric = highlight_metric

        self.connection_id = None

        self.use_auto_sql_content = True
        self.auto_sql_content_schema = 'PAL_CONTENT'

        self.is_simple_mode = True

    def switch_to_another_fetch_table(self):
        self.use_auto_sql_content = not(self.use_auto_sql_content)
        new_conn = EmbeddedUI.create_connection_context(self.connection_context)
        self.connection_context.close()
        self.connection_context = new_conn

    def create_fetch_table_task(self, task_manager, fetch_table_interval):
        fetch_table_task = None
        if self.use_auto_sql_content:
            fetch_table_task = FetchProgressStatusFromAutoSQLContent(task_manager, fetch_table_interval, self.connection_context, self.auto_sql_content_schema)
        else:
            fetch_table_task = FetchProgressStatusFromSystemTableTask(task_manager, fetch_table_interval, self.connection_context)
        return fetch_table_task

    def reset_data(self):
        pass

    def clear_data(self):
        pass

    def cancel_task(self):
        if self.connection_id is not None:
            cancel_task_connection_context = EmbeddedUI.create_connection_context(self.connection_context)
            cancel_task_connection_context.execute_sql("ALTER SYSTEM CANCEL WORK IN SESSION '{}'".format(self.connection_id))
            cancel_task_connection_context.close()

    def get_status(self):
        return 0


class TaskManager(threading.Thread):
    def __init__(self, automatic_obj_proxy: AutomaticObjProxy, update_ui_interval, fetch_table_interval):
        threading.Thread.__init__(self)

        self.completed = False    # fetch complete or obj end execute
        self.interrupted = False  # raise exception
        self.cancelling = False   # fronted send cancel
        self.cancelled = False

        self.automatic_obj_proxy = automatic_obj_proxy
        self.fetch_table_interval = fetch_table_interval
        self.already_switch_to_another_fetch_table = False  # default fetch table: PAL Content Table | auto detect and switch to another table

        self.automatic_obj_proxy.reset_data()
        self.fetch_table_task = self.automatic_obj_proxy.create_fetch_table_task(self, fetch_table_interval)

        self.runtime_platform = EmbeddedUI.get_runtime_platform()[1]
        if self.runtime_platform in ['console', 'databricks']:
            self.update_to_ui_task = UpdateProgressStatusToConsoleTask(self, update_ui_interval)
        else:
            self.update_to_ui_task = UpdateProgressStatusToUITask(self, update_ui_interval)

        self.true_flag = '__js_true'
        self.false_flag = '__js_false'

    def is_interrupted(self):
        return self.interrupted

    def is_completed(self):
        return self.completed

    def is_cancelling(self):
        return self.cancelling

    def is_cancelled(self):
        return self.cancelled

    def set_interrupted(self):
        self.interrupted = True

    def set_completed(self):
        self.completed = True

    def set_cancelling(self):
        self.cancelling = True

    def set_cancelled(self):
        self.cancelled = True

    def switch_to_another_fetch_table(self):
        if self.already_switch_to_another_fetch_table:
            self.set_cancelling()
        else:
            self.already_switch_to_another_fetch_table = True
            self.fetch_table_task.interrupt_fetch_thread()
            self.automatic_obj_proxy.switch_to_another_fetch_table()
            self.fetch_table_task = self.automatic_obj_proxy.create_fetch_table_task(self, self.fetch_table_interval)
            self.fetch_table_task.start()

    def check_status(self):
        if self.automatic_obj_proxy.get_status() < 0:
            self.set_interrupted()
        elif self.automatic_obj_proxy.get_status() > 0 or self.fetch_table_task.is_fetch_completed():
            self.set_completed()
        else:
            if self.runtime_platform != 'console' and os.path.exists(self.update_to_ui_task.frame_file_path):
                self.set_cancelling()

    def remove_temp_file(self):
        if self.runtime_platform != 'console' and os.path.exists(self.update_to_ui_task.frame_file_path):
            os.remove(self.update_to_ui_task.frame_file_path)

    def run(self):
        self.fetch_table_task.start()
        self.update_to_ui_task.start()

        if self.runtime_platform in ['vscode', 'bas']:
            if self.automatic_obj_proxy.is_simple_mode:
                print('task.type: simple mode')
            print('task.start: {}: {}'.format(self.update_to_ui_task.tempdir_path + os.sep, self.update_to_ui_task.iframe_id))

        while True:
            self.check_status()
            if self.is_interrupted() or self.is_completed():
                if self.runtime_platform in ['vscode', 'bas']:
                    print('task.end: {}'.format(self.update_to_ui_task.iframe_id))
                break
            if self.is_cancelling():
                self.automatic_obj_proxy.cancel_task()
                self.set_cancelled()
                if self.runtime_platform in ['vscode', 'bas']:
                    print('task.cancel: {}'.format(self.update_to_ui_task.iframe_id))
                break
        self.automatic_obj_proxy.clear_data()
        self.remove_temp_file()


class FetchProgressStatusFromSystemTableTask(threading.Thread):
    def __init__(self, manager: TaskManager, fetch_table_interval, connection_context: ConnectionContext):
        threading.Thread.__init__(self)

        self.manager = manager
        self.fetch_table_interval = fetch_table_interval
        self.connection_context = connection_context

        self.fetch_completed = False
        self.offset = 0
        self.limit = 1000
        self.connection_cursor = connection_context.connection.cursor()
        self.connection_cursor.setfetchsize(32000)

        self.initialized_progress_status = None
        self.fetch_sql = """
            SELECT {}
            from _SYS_AFL.FUNCTION_PROGRESS_IN_AFLPAL
            WHERE EXECUTION_ID='{}' limit {} offset {}
        """
        self.initialized_columns = ['FUNCTION_NAME', 'CONNECTION_ID', 'PROGRESS_CURRENT', 'PROGRESS_MESSAGE', 'PROGRESS_TIMESTAMP']
        self.simplified_columns = ['PROGRESS_CURRENT', 'PROGRESS_MESSAGE', 'PROGRESS_TIMESTAMP']

        self.progresscurrent_2_message = {}
        self.progresscurrent_2_status = {}
        self.can_read_max_progresscurrent = -1
        self.current_read_progresscurrent = -1
        self.read_completed = False

        self.max_continuous_none_result_count = 60
        self.continuous_none_result_count = 0

    def parse_fetched_data(self, fetched_data, fetched_columns):
        fetched_data_df = pd.DataFrame(fetched_data, columns=fetched_columns)

        if self.initialized_progress_status is None:
            head_row = fetched_data_df.head(1)
            self.initialized_progress_status = {
                'running': self.manager.true_flag,
                'f': str(list(head_row['FUNCTION_NAME'])[0])
            }
            if self.manager.automatic_obj_proxy.is_simple_mode is False:
                # on simple ui, the following code can result in cancelling automl procedure.
                self.manager.automatic_obj_proxy.connection_id = str(list(head_row['CONNECTION_ID'])[0])

        progress_current_list = list(fetched_data_df['PROGRESS_CURRENT'])
        progress_msg_list = list(fetched_data_df['PROGRESS_MESSAGE'])
        progress_timestamp_list = list(fetched_data_df['PROGRESS_TIMESTAMP'])
        for row_index in range(0, fetched_data_df.shape[0]): # row_count
            progress_current = progress_current_list[row_index]
            if progress_current >= 0: # fetch completed -1
                # when progress_current is 2, progress_current=1 can read
                self.can_read_max_progresscurrent = progress_current - 1
                progress_msg = progress_msg_list[row_index]
                progress_timestamp = progress_timestamp_list[row_index]
                if self.progresscurrent_2_message.get(progress_current) is None:
                    self.progresscurrent_2_message[progress_current] = []
                    self.progresscurrent_2_status[progress_current] = {
                        'c': progress_current,
                        't': str(progress_timestamp)
                    }
                if progress_msg is not None and progress_msg.strip() != '':
                    if progress_msg.find('early_stop') >= 0:
                        self.fetch_completed = True
                    if progress_msg.find('{"state":"finished"}') >= 0:
                        self.fetch_completed = True
                    self.progresscurrent_2_message[progress_current].append(progress_msg)
            # elif progress_current == -1:
            #     self.fetch_completed = True

    def do_fetch(self, fetched_columns):
        sql = self.fetch_sql.format(', '.join(fetched_columns), self.manager.automatic_obj_proxy.progress_indicator_id, self.limit, self.offset)
        self.connection_cursor.execute(sql)
        fetched_data = self.connection_cursor.fetchall()
        fetched_count = len(fetched_data)
        if fetched_count > 0:
            self.parse_fetched_data(fetched_data, fetched_columns)
            self.offset = self.offset + fetched_count
        else:
            if self.manager.is_completed():
                self.can_read_max_progresscurrent = self.can_read_max_progresscurrent + 1
                self.set_fetch_completed()
            else:
                if self.manager.automatic_obj_proxy.is_simple_mode:
                    if self.initialized_progress_status is None:
                        if self.continuous_none_result_count > self.max_continuous_none_result_count:
                            self.manager.switch_to_another_fetch_table()
                        else:
                            self.continuous_none_result_count = self.continuous_none_result_count + 1

    def fetch(self):
        if self.initialized_progress_status is None:
            self.do_fetch(self.initialized_columns)
        else:
            self.do_fetch(self.simplified_columns)

    def is_read_completed(self):
        if self.is_fetch_completed() and (self.current_read_progresscurrent + 1 > self.can_read_max_progresscurrent):
            return True
        else:
            return False

    def get_next_progress_status(self):
        next_progress_status = None
        if self.can_read_max_progresscurrent >= 0:
            if self.current_read_progresscurrent + 1 <= self.can_read_max_progresscurrent:
                next_progress_current = self.current_read_progresscurrent + 1
                if self.progresscurrent_2_message.get(next_progress_current) is not None:
                    progress_message = ''.join(self.progresscurrent_2_message.get(next_progress_current))
                    if progress_message.strip() == '':
                        progress_message = 'None'
                    next_progress_status = self.progresscurrent_2_status.get(next_progress_current)
                    next_progress_status['m'] = progress_message
                    self.current_read_progresscurrent = next_progress_current
                    # decorate progress status
                    if next_progress_current == 0:
                        next_progress_status.update(self.initialized_progress_status)
                    else:
                        next_progress_status.update({'running': self.manager.true_flag})
        return next_progress_status

    def is_fetch_completed(self):
        return self.fetch_completed

    def set_fetch_completed(self):
        self.fetch_completed = True

    def run(self):
        while True:
            if self.manager.is_interrupted() or self.manager.is_cancelling() or self.is_fetch_completed():
                self.connection_context.close()
                break
            self.fetch()
            time.sleep(self.fetch_table_interval)


class FetchProgressStatusFromAutoSQLContent(threading.Thread):
    def __init__(self, manager: TaskManager, fetch_table_interval, connection_context: ConnectionContext, auto_sql_content_schema):
        threading.Thread.__init__(self)

        self.manager = manager
        self.fetch_table_interval = fetch_table_interval
        self.connection_context = connection_context
        self.auto_sql_content_schema = auto_sql_content_schema

        self.fetch_completed = False
        self.offset = 0
        self.limit = 1000
        self.connection_cursor = connection_context.connection.cursor()
        self.connection_cursor.setfetchsize(32000)

        self.initialized_progress_status = None
        self.fetch_sql = """
            SELECT {}
            from {}.AUTOML_LOG
            WHERE EXECUTION_ID='{}' limit {} offset {}
        """
        self.initialized_columns = ['EVENT_KEY', 'SEQ', 'EVENT_MESSAGE', 'EVENT_TIMESTAMP']
        self.simplified_columns = ['SEQ', 'EVENT_MESSAGE', 'EVENT_TIMESTAMP']

        self.progresscurrent_2_message = {}
        self.progresscurrent_2_status = {}
        self.can_read_max_progresscurrent = -1
        self.current_read_progresscurrent = -1
        self.read_completed = False

        self.is_self_thread_interrupted = False
        self.max_continuous_none_result_count = 2 * 60
        self.continuous_none_result_count = 0

    def parse_fetched_data(self, fetched_data, fetched_columns):
        fetched_data_df = pd.DataFrame(fetched_data, columns=fetched_columns)

        if self.initialized_progress_status is None:
            self.initialized_progress_status = {
                'running': self.manager.true_flag,
                'f': fetched_data_df.head(1)["EVENT_KEY"].iat[0]  # FUNCTION_NAME
            }

        progress_current_list = list(fetched_data_df['SEQ'])
        progress_msg_list = list(fetched_data_df['EVENT_MESSAGE'])
        progress_timestamp_list = list(fetched_data_df['EVENT_TIMESTAMP'])
        for row_index in range(0, fetched_data_df.shape[0]): # row_count
            progress_current = progress_current_list[row_index]
            if progress_current >= 0: # fetch completed -1
                # when progress_current is 2, progress_current=1 can read
                self.can_read_max_progresscurrent = progress_current - 1
                progress_msg = progress_msg_list[row_index]
                progress_timestamp = progress_timestamp_list[row_index]
                if self.progresscurrent_2_message.get(progress_current) is None:
                    self.progresscurrent_2_message[progress_current] = []
                    self.progresscurrent_2_status[progress_current] = {
                        'c': progress_current,  # PROGRESS_CURRENT
                        't': str(progress_timestamp)  # PROGRESS_TIMESTAMP
                    }
                if progress_msg is not None and progress_msg.strip() != '':
                    if progress_msg.find('early_stop') >= 0:
                        self.fetch_completed = True
                    if progress_msg.find('{"state":"finished"}') >= 0:
                        self.fetch_completed = True
                    self.progresscurrent_2_message[progress_current].append(progress_msg)

    def do_fetch(self, fetched_columns):
        sql = self.fetch_sql.format(', '.join(fetched_columns), self.auto_sql_content_schema, self.manager.automatic_obj_proxy.progress_indicator_id, self.limit, self.offset)
        self.connection_cursor.execute(sql)
        fetched_data = self.connection_cursor.fetchall()
        fetched_count = len(fetched_data)
        if fetched_count > 0:
            self.parse_fetched_data(fetched_data, fetched_columns)
            self.offset = self.offset + fetched_count
        else:
            if self.manager.is_completed():
                self.can_read_max_progresscurrent = self.can_read_max_progresscurrent + 1
                self.set_fetch_completed()
            else:
                if self.manager.automatic_obj_proxy.is_simple_mode:
                    if self.initialized_progress_status is None:
                        if self.continuous_none_result_count > self.max_continuous_none_result_count:
                            self.manager.switch_to_another_fetch_table()
                        else:
                            self.continuous_none_result_count = self.continuous_none_result_count + 1

    def fetch(self):
        if self.initialized_progress_status is None:
            self.do_fetch(self.initialized_columns)
        else:
            self.do_fetch(self.simplified_columns)

    def is_read_completed(self):
        if self.is_fetch_completed() and (self.current_read_progresscurrent + 1 > self.can_read_max_progresscurrent):
            return True
        else:
            return False

    def get_next_progress_status(self):
        next_progress_status = None
        if self.can_read_max_progresscurrent >= 0:
            if self.current_read_progresscurrent + 1 <= self.can_read_max_progresscurrent:
                next_progress_current = self.current_read_progresscurrent + 1
                if self.progresscurrent_2_message.get(next_progress_current) is not None:
                    progress_message = ''.join(self.progresscurrent_2_message.get(next_progress_current))
                    if progress_message.strip() == '':
                        progress_message = 'None'
                    next_progress_status = self.progresscurrent_2_status.get(next_progress_current)
                    next_progress_status['m'] = progress_message  # PROGRESS_MESSAGE
                    self.current_read_progresscurrent = next_progress_current
                    # decorate progress status
                    if next_progress_current == 0:
                        next_progress_status.update(self.initialized_progress_status)
                    else:
                        next_progress_status.update({'running': self.manager.true_flag})
        return next_progress_status

    def is_fetch_completed(self):
        return self.fetch_completed

    def set_fetch_completed(self):
        self.fetch_completed = True

    def interrupt_fetch_thread(self):
        self.is_self_thread_interrupted = True

    def run(self):
        while True:
            if self.manager.is_interrupted() or self.manager.is_cancelling() or self.is_fetch_completed():
                self.connection_context.close()
                break
            elif self.is_self_thread_interrupted:
                break
            self.fetch()
            time.sleep(self.fetch_table_interval)


class UpdateProgressStatusToUITask(EmbeddedUI):
    def __init__(self, manager: TaskManager, update_ui_interval):
        super().__init__()
        self.manager = manager
        self.update_ui_interval = update_ui_interval
        self.runtime_platform = manager.runtime_platform
        self.self_timer = None

        self.iframe_id = self.get_uuid()
        self.tempdir_path = self.get_resource_temp_dir_path()
        self.frame_file_path = self.tempdir_path + os.sep + self.iframe_id

    def display(self, js_str):
        if self.runtime_platform == 'bas':
            self.execute_js_str("{}".format(js_str))
        else:
            self.execute_js_str("{}".format(js_str), self_display_id=self.iframe_id)

    def update_display(self, js_str):
        if self.runtime_platform == 'bas':
            self.execute_js_str("{};".format(js_str))
        elif self.runtime_platform == 'jupyter':
            self.execute_js_str_for_update("{};".format(js_str), updated_display_id=self.iframe_id)
        elif self.runtime_platform == 'vscode':
            vscode_script = "const scripts = document.getElementsByTagName('script');for (let i = 0; i < scripts.length; i++) {const hanamlPipelinePNode = scripts[i].parentNode;if(hanamlPipelinePNode.tagName == 'DIV' && scripts[i].innerText.indexOf('hanamlPipelinePNode') >= 0){hanamlPipelinePNode.remove();}}"
            self.execute_js_str_for_update("{};{};".format(js_str, vscode_script), updated_display_id=self.iframe_id)

    def send_msgs(self, msgs):
        msgs_str = str(msgs).replace("'{}'".format(self.manager.true_flag), 'true').replace("'{}'".format(self.manager.false_flag), 'false')
        js_str = "targetWindow['{}']={}".format('FRAME_P_S', msgs_str)
        js_str = "for (let i = 0; i < window.length; i++) {const targetWindow = window[i];if(targetWindow['frameId']){if(targetWindow['frameId'] === '" + self.iframe_id + "'){" + js_str + "}}}"
        self.update_display(js_str)

    def get_progress_status_list(self):
        msgs = []
        size = 0
        # 1000: Maximum number of UI status updates per time
        while (size <= 999):
            # next_progress_status: None | 'xxx'
            next_progress_status = self.manager.fetch_table_task.get_next_progress_status()
            if next_progress_status is None:
                break
            else:
                msgs.append(next_progress_status)
                size = size + 1
        if len(msgs) == 0:
            return None
        else:
            return msgs

    def __task(self):
        if self.manager.is_cancelled():
            self.send_msgs([{'cancelled': self.manager.true_flag}])
            return

        if self.manager.is_interrupted():
            # self.update_display("document.getElementById('{}').style.display = 'none';".format(self.frame_id))
            return

        if self.manager.fetch_table_task.is_read_completed():
            self.send_msgs([{'running': self.manager.false_flag}])
            return

        if self.manager.is_cancelling():
            self.send_msgs([{'cancelling': self.manager.true_flag}])
        else:
            msgs = self.get_progress_status_list()
            if msgs is not None:
                self.send_msgs(msgs)
        self.__run()

    def __run(self):
        self.self_timer = threading.Timer(self.update_ui_interval, self.__task)
        self.self_timer.start()

    def start(self):
        self.display("")

        is_simple_mode = 'false'
        if self.manager.automatic_obj_proxy.is_simple_mode:
            is_simple_mode = 'true'
        html_str = self.get_resource_template('pipeline_progress.html').render(
            executionId=self.manager.automatic_obj_proxy.progress_indicator_id,
            frameId=self.iframe_id,
            highlighted_metric_name=self.manager.automatic_obj_proxy.highlight_metric,
            is_simple_mode=is_simple_mode,
            msgs_str='[]')
        self.render_html_str(self.get_iframe_str(html_str, self.iframe_id, 1000))

        if self.runtime_platform in ['vscode', 'bas']:
            print('In order to cancel AutoML execution or monitor execution on the BAS or VSCode platform, you must import the VSCode extension package manually.')
            print('VSCode extension package path: \n{}'.format(self.get_resource_root_dir_path() + os.sep + 'hanamlapi-monitor-1.2.0.vsix'))

        self.self_timer = threading.Timer(self.update_ui_interval, self.__task)
        self.self_timer.start()


class UpdateProgressStatusToConsoleTask(EmbeddedUI):
    def __init__(self, manager: TaskManager, update_ui_interval):
        super().__init__()
        self.manager = manager
        self.update_ui_interval = update_ui_interval
        self.runtime_platform = manager.runtime_platform
        self.progress_id = manager.automatic_obj_proxy.progress_indicator_id
        self.self_timer = None

        self.creation_time = None
        self.function_name = None

        self.status = "Running"
        self.pipeline_num = "*"
        self.generation_num = "*"
        self.current_generation = -1
        self.current_progress = 0

        self.all_msgs = []

        self.progress_table = PrettyTable()
        self.progress_table.field_names = [
            "Status",
            "Pipeline Number",
            "Generation Number",
            "Current Generation",
            "Progress"
        ]

        self.current_generation_details = {}
        self.evaluating_count = 0
        self.succeeded_count = 0
        self.failed_count = 0
        self.timeout_count = 0
        self.statistic_table = PrettyTable()
        self.red = '\033[31m'
        self.green = '\033[32m'
        self.blue = '\033[34m'
        self.black = '\033[39m'
        self.statistic_table.field_names = [
            "Evaluating",
            "Evaluated",
            "Succeeded",
            "Failed",
            "Timeout"
        ]

    def print_main_info(self):
        self.progress_table.clear_rows()
        self.progress_table.add_row([
            self.status,
            self.pipeline_num,
            self.generation_num,
            "Initialization" if self.current_generation == 0 else self.current_generation,
            "{} %".format(self.current_progress)
        ])

        self.clear_output(self.runtime_platform)
        print('Progress Indicator Id: ', self.progress_id)
        print('Creation Time: ', self.creation_time)
        print('Function Name: ', self.function_name)
        print(self.progress_table)
        print("")

    def print_current_generation_details(self):
        self.statistic_table.clear_rows()
        self.statistic_table.add_row([self.evaluating_count, (self.succeeded_count + self.failed_count + self.timeout_count), self.succeeded_count, self.failed_count, self.timeout_count])
        print('Current Generation Details: ', "Initialization" if self.current_generation == 0 else self.current_generation)
        print(self.statistic_table)
        for item in self.current_generation_details.items():
            # succeeded failed timeout
            color = None
            if item[1].find('succeeded') >= 0:
                color = self.green
            elif item[1].find('failed') >= 0:
                color = self.red
            elif item[1].find('timeout') >= 0:
                color = self.red
            else:
                color = self.blue
            print(color + item[1], self.black + item[0])
        print("")

    def send_msgs(self, msgs):
        for msg in msgs:
            if self.creation_time is None:
                self.creation_time = msg['t']
            if self.function_name is None:
                self.function_name = msg['f']
            m = json.loads(msg['m'])
            if m.get('pipeline_num') is not None:
                self.pipeline_num = m.get('pipeline_num')
            elif m.get('generation_num') is not None:
                self.generation_num = m.get('generation_num')
            elif m.get('generation') is not None:
                self.evaluating_count = 0
                self.succeeded_count = 0
                self.failed_count = 0
                self.timeout_count = 0
                self.current_generation = m.get('generation')
                self.current_generation_details.clear()
            elif m.get('current_best') is not None:
                self.current_progress = int(((self.current_generation + 1) / (self.generation_num + 1)) * 100)
                best_pipeline = str(m.get('current_best').get('pipeline'))
                self.current_generation_details[best_pipeline] = 'Best'
            elif m.get('evaluating') is not None:
                evaluating_pipeline = str(m.get('evaluating'))
                self.current_generation_details[evaluating_pipeline] = 'Evaluating'
                self.evaluating_count = self.evaluating_count + 1
            elif m.get('pipeline_evaluated') is not None:
                evaluated_pipeline = str(m.get('pipeline_evaluated').get('pipeline'))
                # succeeded failed timeout
                state = str(m.get('pipeline_evaluated').get('state'))
                if state == 'succeeded':
                    self.succeeded_count = self.succeeded_count + 1
                elif state == 'failed':
                    self.failed_count = self.failed_count + 1
                elif state == 'timeout':
                    self.timeout_count = self.timeout_count + 1
                self.current_generation_details[evaluated_pipeline] = 'Evaluated({})'.format(state)
        self.print_main_info()
        self.print_current_generation_details()

    def get_progress_status_list(self):
        msgs = []
        size = 0
        # 1000: Maximum number of UI status updates per time
        while (size <= 999):
            # next_progress_status: None | 'xxx'
            next_progress_status = self.manager.fetch_table_task.get_next_progress_status()
            if next_progress_status is None:
                break
            else:
                msgs.append(next_progress_status)
                self.all_msgs.append(next_progress_status)
                size = size + 1
        if len(msgs) == 0:
            return None
        else:
            return msgs

    def __task(self):
        if self.manager.is_interrupted():
            return

        if self.manager.fetch_table_task.is_read_completed():
            self.status = 'Completed'
            if self.generation_num == self.current_generation:
                self.current_generation = -1
            self.print_main_info()
            if self.runtime_platform == 'databricks':
                self.all_msgs.append({'running': self.manager.false_flag})
                msgs_str = str(self.all_msgs).replace("'{}'".format(self.manager.true_flag), 'true').replace("'{}'".format(self.manager.false_flag), 'false')
                iframe_id = self.get_uuid()
                html_str = self.get_resource_template('pipeline_progress.html').render(
                    executionId=self.progress_id,
                    frameId=iframe_id,
                    highlighted_metric_name=self.manager.automatic_obj_proxy.highlight_metric,
                    is_simple_mode='false',
                    msgs_str=msgs_str)
                self.render_html_str(self.get_iframe_str(html_str, iframe_id, 1000))
            return

        msgs = self.get_progress_status_list()
        if msgs is not None:
            self.send_msgs(msgs)
        self.__run()

    def __run(self):
        self.self_timer = threading.Timer(self.update_ui_interval, self.__task)
        self.self_timer.start()

    def start(self):
        self.self_timer = threading.Timer(self.update_ui_interval, self.__task)
        self.self_timer.start()


class PipelineProgressStatusMonitor(object):
    """
    The instance of this class can monitor the progress of AutoML execution.
    This real-time monitoring allows users to understand at what stage the automated machine learning execution is,
    thus providing insights and transparency about the process.

    Parameters
    ----------
    connection_context : :class:`~hana_ml.dataframe.ConnectionContext`
        The connection to the SAP HANA system.

        For example:

        .. only:: latex

            >>> from hana_ml.dataframe import ConnectionContext as CC
            >>> progress_status_monitor = PipelineProgressStatusMonitor(connection_context=CC(url, port, user, pwd),
                                                                        automatic_obj=auto_c)

        .. raw:: html

            <iframe allowtransparency="true" style="border:1px solid #ccc; background: #eeffcb;"
                src="_static/automl_progress_example.html" width="100%" height="100%" sandbox="">
            </iframe>

    automatic_obj : :class:`~hana_ml.algorithms.pal.auto_ml.AutomaticClassification` or :class:`~hana_ml.algorithms.pal.auto_ml.AutomaticRegression`
        An instance object of the AutomaticClassification type or AutomaticRegression type
        that contains the progress_indicator_id attribute.

    fetch_table_interval : float, optional
        Specifies the time interval of fetching the table of pipeline progress.

        Defaults to 1s.

    runtime_platform : str, optional
        Specify the running environment of the monitor.

        - 'console': output content in plain text format.
        - 'jupyter': running on the JupyterLab or Jupyter Notebook platform.
        - 'vscode': running on the VSCode platform.
        - 'bas': running on the SAP Business Application Studio platform.
        - 'databricks': running on the Databricks platform.

        By default, the running platform will be automatically detected. If an incorrect value is passed in, this parameter will be ignored.

        Defaults to None.

    Examples
    --------
    Create an AutomaticClassification instance:

    >>> progress_id = "automl_{}".format(uuid.uuid1())
    >>> auto_c = AutomaticClassification(generations=5,
                                         population_size=10,
                                         offspring_size=10,
                                         progress_indicator_id=progress_id)
    >>> auto_c.enable_workload_class("MY_WORKLOAD")

    Establish a PipelineProgressStatusMonitor object and then invoke start():

    >>> progress_status_monitor = PipelineProgressStatusMonitor(connection_context=dataframe.ConnectionContext(url, port, user, pwd),
                                                                automatic_obj=auto_c)
    >>> progress_status_monitor.start()
    >>> auto_c.fit(data=df_train)

    Output:

    .. image:: image/progress_classification.png

    In order to cancel AutoML execution on the BAS or VSCode platform, you must import the Visual Studio Code Extension (VSIX) manually.

    - .. image:: image/cancel_automl_execution_button.png

    Follow the image below to install hanamlapi-monitor-1.2.0.vsix file on VSCode or BAS.

    - .. image:: image/import_vscode_extension_0.png

    - .. image:: image/import_vscode_extension_2.png

    - .. image:: image/import_vscode_extension_3.png

    - .. image:: image/import_vscode_extension_4.png
    """
    def __init__(self, connection_context: ConnectionContext, automatic_obj, fetch_table_interval=1, runtime_platform=None):
        self.original_connection_context = connection_context
        self.automatic_obj = automatic_obj
        self.update_ui_interval = fetch_table_interval  # Specifies the time interval of updating the UI of pipeline progress.
        self.fetch_table_interval = fetch_table_interval

    def start(self):
        """
        Call the method before executing the fit method of Automatic Object.
        """
        new_connection_context = EmbeddedUI.create_connection_context(self.original_connection_context)
        self.task_manager = TaskManager(AutomaticObjProxy(self.automatic_obj, new_connection_context), self.update_ui_interval, self.fetch_table_interval)
        self.task_manager.start()


class SimplePipelineProgressStatusMonitor(object):
    """

    An instance of this class offers functionality to monitor and track the progress of AutoML's execution at any given time through the progress_indicator_id.

    Parameters
    ----------
    connection_context : :class:`~hana_ml.dataframe.ConnectionContext`
        The connection to the SAP HANA system.

    fetch_table_interval : float, optional
        Specifies the time interval of fetching the table of pipeline progress.

        Defaults to 1s.

    runtime_platform : str, optional
        Specify the running environment of the monitor.

        - 'console': output content in plain text format.
        - 'jupyter': running on the JupyterLab or Jupyter Notebook platform.
        - 'vscode': running on the VSCode platform.
        - 'bas': running on the SAP Business Application Studio platform.
        - 'databricks': running on the Databricks platform.

        By default, the running platform will be automatically detected. If an incorrect value is passed in, this parameter will be ignored.

        Defaults to None.

    Examples
    --------
    Create an AutomaticClassification instance:

    >>> progress_id = "automl_{}".format(uuid.uuid1())
    >>> auto_c = AutomaticClassification(generations=5,
                                         population_size=10,
                                         offspring_size=10,
                                         progress_indicator_id=progress_id)
    >>> auto_c.enable_workload_class("MY_WORKLOAD")

    Establish a SimplePipelineProgressStatusMonitor object and invoke start():

    >>> progress_status_monitor = SimplePipelineProgressStatusMonitor(connection_context=dataframe.ConnectionContext(url, port, user, pwd))
    >>> progress_status_monitor.start(progress_indicator_id=progress_id, highlight_metric='ACCURACY')
    >>> auto_c.fit(data=df_train)

    Output:

    .. image:: image/simple_progress_classification.png

    In order to cancel monitor execution on the BAS or VSCode platform, you must import the Visual Studio Code Extension (VSIX) manually.

    - .. image:: image/cancel_monitor_execution_button.png

    Follow the image below to install hanamlapi-monitor-1.2.0.vsix file on VSCode or BAS.

    - .. image:: image/import_vscode_extension_0.png

    - .. image:: image/import_vscode_extension_2.png

    - .. image:: image/import_vscode_extension_3.png

    - .. image:: image/import_vscode_extension_4.png
    """
    def __init__(self, connection_context: ConnectionContext, fetch_table_interval=1, runtime_platform=None):
        self.original_connection_context = connection_context
        self.update_ui_interval = fetch_table_interval
        self.fetch_table_interval = fetch_table_interval

    def start(self, progress_indicator_id, highlight_metric=None):
        """
        This method can be called at any time.

        Parameters
        ----------
        progress_indicator_id : str
            A unique identifier which represents the ongoing automatic task.

        highlight_metric : str, optional
            Specify the metric that need to be displayed on the UI.
        """
        new_connection_context = EmbeddedUI.create_connection_context(self.original_connection_context)
        self.task_manager = TaskManager(AutomaticEmptyObjProxy(progress_indicator_id, new_connection_context, highlight_metric), self.update_ui_interval, self.fetch_table_interval)
        self.task_manager.start()
