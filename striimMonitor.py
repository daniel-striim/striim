# This is a sample Python script.
import time
import requests
from datetime import datetime
import logging

import json
from collections import namedtuple

"""
This script contains a set of parameters listed below. Optionally, update this to use sys.argv[x] as indicated:
"""
node = '35.227.185.202' # sys.argv[1]
username = 'admin' # sys.argv[2]
password = 'admin' # sys.argv[3]

polling_interval_seconds = 10 # sys.argv[4]
run_iterations = 100 # sys.argv[5]
log_output_path = '/Users/danielferrara/Documents/striimwatcher.log' # sys.argv[6]
append_log = True # sys.argv[7]

#generate REST API authentication token
data = {'username': username, 'password': password}
resp = requests.post('http://' + node + ':9080/security/authenticate', data=data)
jkvp = json.loads(resp.text)
sToken = jkvp['token']

logging.basicConfig(filename=log_output_path, level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

#define headers
headers = {'authorization':'STRIIM-TOKEN ' + sToken, 'content-type': 'text/plain'}


class StriimSource:
    def __init__(self, json_response):
        response = json.loads(json_response)[0]
        self.command = response['command']
        self.execution_status = response['executionStatus']
        self.cpu = response['output']['cpu']
        self.cpu_rate_per_node = response['output']['cpuRatePerNode']
        self.cpu_rate = response['output']['cpuRate']
        self.number_of_events_seen_per_monitor_snapshot_interval = response['output']['numberOfEventsSeenPerMonitorSnapshotInterval']
        self.ignored_tables_list = response['output']['ignoredTablesList']
        self.input = response['output']['input']
        self.input_rate = response['output']['inputRate']
        self.last_event_read_age = response['output']['lastEventReadAge']
        self.latest_activity = response['output']['latestActivity']
        self.num_servers = response['output']['numServers']
        self.rate = response['output']['rate']
        self.read_status = response['output']['readStatus']
        self.source_input = response['output']['sourceInput']
        self.source_rate = response['output']['sourceRate']
        self.table_information = response['output']['tableInformation']
        self.timestamp = response['output']['timestamp']
        self.row_count = response['output']['rowCount']

# Used to get components
class StriimHeadComponentResponse:
    def __init__(self, command, executionStatus, output):
        self.command = command
        self.executionStatus = executionStatus
        self.output = StriimHeadComponent(output)

class StriimHeadComponent:
    def __init__(self, component):
        self.entityType = component['entityType']
        self.fullName = component['fullName']
        self.statusChange = component['statusChange']
        self.rate = component['rate']
        self.sourceRate = component['sourceRate']
        self.cpuRate = component['cpuRate']
        self.numServers = component['numServers']
        self.latestActivity = component['latestActivity']
        self.applicationComponents = component['applicationComponents'] if "applicationComponents" in component else ''
        self.sources = []

    def add_source(self, source):
        self.sources.append(source)


class StriimComponent:
    def __init__(self, component):
        self.entityType = component['entityType']
        self.fullName = component['fullName']
        self.statusChange = component['statusChange']
        self.rate = component['rate']
        self.sourceRate = component['sourceRate']
        self.cpuRate = component['cpuRate']
        self.numServers = component['numServers']
        self.latestActivity = component['latestActivity']


class StriimComponentSourceResponse:
    def __init__(self, command, execution_status, output, response_code):
        self.command = command
        self.execution_status = execution_status
        self.output = StriimComponentSource(output)
        self.response_code = response_code

class StriimComponentSource:
    def __init__(self, component):
        # component = json.loads(json_string)
        self.catalog_evolution_duration = component['catalogEvolutionDuration'] if 'catalogEvolutionDuration' in component else ''
        self.schema_evolution_status = component['schemaEvolutionStatus'] if 'schemaEvolutionStatus' in component else ''
        self.cdc_operation = component['cdcOperation'] if 'cdcOperation' in component else ''
        self.cpu = component['cpu'] if 'cpu' in component else ''
        self.cpu_rate_per_node = component['cpuRatePerNode'] if 'cpuRatePerNode' in component else ''
        self.cpu_rate = component['cpuRate'] if 'cpuRate' in component else ''
        self.number_of_events_seen_per_monitor_snapshot_interval = component['numberOfEventsSeenPerMonitorSnapshotInterval'] if 'numberOfEventsSeenPerMonitorSnapshotInterval' in component else ''
        self.high_water_mark = component['highWaterMark'] if 'highWaterMark' in component else ''
        self.input = component['input'] if 'input' in component else ''
        self.input_rate = component['inputRate'] if 'inputRate' in component else ''
        self.largest_transaction_details = component['largestTransactionDetails'] if 'largestTransactionDetails' in component else ''
        self.last_event_position = component['lastEventPosition'] if 'lastEventPosition' in component else ''
        self.last_event_read_age = component['lastEventReadAge'] if 'lastEventReadAge' in component else ''
        self.latest_activity = component['latestActivity'] if 'latestActivity' in component else ''
        self.logminer_start_duration = component['logminerStartDuration'] if 'logminerStartDuration' in component else ''
        self.oldest_open_transactions = component['oldestOpenTransactions'] if 'oldestOpenTransactions' in component else ''
        self.longest_transaction_details = component['longestTransactionDetails'] if 'longestTransactionDetails' in component else ''
        self.open_transactions_in_cache = component['openTransactionsInCache'] if 'openTransactionsInCache' in component else ''
        self.transactions_with_no_dml_operations = component['transactionsWithNoDmlOperations'] if 'transactionsWithNoDmlOperations' in component else ''
        self.num_servers = component['numServers'] if 'numServers' in component else ''
        self.oracle_reader_current_scn = component['oracleReaderCurrentScn'] if 'oracleReaderCurrentScn' in component else ''
        self.current_scn_range = component['currentScnRange'] if 'currentScnRange' in component else ''
        self.oracle_reader_last_scn = component['oracleReaderLastScn'] if 'oracleReaderLastScn' in component else ''
        self.oracle_reader_last_timestamp = component['oracleReaderLastTimestamp'] if 'oracleReaderLastTimestamp' in component else ''
        self.total_logminer_records_read = component['totalLogminerRecordsRead'] if 'totalLogminerRecordsRead' in component else ''
        self.redo_switch_count = component['redoSwitchCount'] if 'redoSwitchCount' in component else ''
        self.oracle_reader_thread_specific_last_scn = component['oracleReaderThreadSpecificLastScn'] if 'oracleReaderThreadSpecificLastScn' in component else ''
        self.rate = component['rate'] if 'rate' in component else ''
        self.read_lag = component['readLag'] if 'readLag' in component else ''
        self.read_timestamp = component['readTimestamp'] if 'readTimestamp' in component else ''
        self.rowcount = component['rowCount'] if 'rowCount' in component else ''
        self.source_freshness = component['sourceFreshness'] if 'sourceFreshness' in component else ''
        self.source_input = component['sourceInput'] if 'sourceInput' in component else ''
        self.source_rate = component['sourceRate'] if 'sourceRate' in component else ''
        self.startscn = component['startscn'] if 'startscn' in component else ''
        self.table_information = component['tableInformation'] if 'tableInformation' in component else ''
        self.timestamp = component['timestamp'] if 'timestamp' in component else ''
        self.top_open_transactions = component['topOpenTransactions(#OfOps)'] if 'topOpenTransactions(#OfOps)' in component else ''
        self.operations_in_the_cache = component['operationsInTheCache'] if 'operationsInTheCache' in component else ''
        self.total_number_of_reconnects = component['totalNumberOfReconnects'] if 'totalNumberOfReconnects' in component else ''


class StriimComponentTargetResponse:
    def __init__(self, command, execution_status, output, response_code):
        self.command = command
        self.execution_status = execution_status
        self.output = StriimComponentTarget(output)
        self.response_code = response_code

class StriimComponentTarget:
    def __init__(self, component):
        # component = json.loads(json_str)

        self.accepted = component['accepted'] if 'accepted' in component else ''
        self.no_of_events_accepted_per_interval = component['no.ofEventsAcceptedPerInterval'] if 'no.ofEventsAcceptedPerInterval' in component else ''
        self.accepted_rate = component['acceptedRate'] if 'acceptedRate' in component else ''
        self.commit_lag = component['commitLag'] if 'commitLag' in component else {}
        self.last_commit_latency = component['lastCommitLatency'] if 'lastCommitLatency' in component else ''
        self.cpu = component['cpu'] if 'cpu' in component else ''
        self.cpu_rate_per_node = component['cpuRatePerNode'] if 'cpuRatePerNode' in component else ''
        self.cpu_rate = component['cpuRate'] if 'cpuRate' in component else ''
        self.ddl_information = component['ddlInformation'] if 'ddlInformation' in component else {}
        self.discarded_event_count = component['discardedEventCount'] if 'discardedEventCount' in component else ''
        self.number_of_events_seen_per_monitor_snapshot_interval = component['numberOfEventsSeenPerMonitorSnapshotInterval'] if 'numberOfEventsSeenPerMonitorSnapshotInterval' in component else ''
        self.external_i_o_latency = component['externalI/oLatency'] if 'externalI/oLatency' in component else ''
        self.input = component['input'] if 'input' in component else ''
        self.input_rate = component['inputRate'] if 'inputRate' in component else ''
        self.last_commit_time = component['lastCommitTime'] if 'lastCommitTime' in component else ''
        self.last_i_o_time = component['lastI/oTime'] if 'lastI/oTime' in component else ''
        self.last_event_write_age = component['lastEventWriteAge'] if 'lastEventWriteAge' in component else ''
        self.latest_activity = component['latestActivity'] if 'latestActivity' in component else ''
        self.max_lee_from_all_sources = component['maxLeeFromAllSources'] if 'maxLeeFromAllSources' in component else ''
        self.no_op_operations = component['no-opOperations'] if 'no-opOperations' in component else {}
        self.num_servers = component['numServers'] if 'numServers' in component else ''
        self.exceptions_ignored = component['exceptionsIgnored'] if 'exceptionsIgnored' in component else ''
        self.individual_operation_count = component['individualOperationCount'] if 'individualOperationCount' in component else {}
        self.output = component['output'] if 'output' in component else ''
        self.processed = component['processed'] if 'processed' in component else ''
        self.rate = component['rate'] if 'rate' in component else ''
        self.source_rate = component['sourceRate'] if 'sourceRate' in component else ''
        self.table_information = component['tableInformation'] if 'tableInformation' in component else {}
        self.target_acked = component['targetAcked'] if 'targetAcked' in component else ''
        self.target_commit_position = component['targetCommitPosition'] if 'targetCommitPosition' in component else ''
        self.target_output = component['targetOutput'] if 'targetOutput' in component else ''
        self.target_rate = component['targetRate'] if 'targetRate' in component else ''
        self.timestamp = component['timestamp'] if 'timestamp' in component else ''
        self.total_events_in_last_commit = component['totalEventsInLastCommit'] if 'totalEventsInLastCommit' in component else ''
        self.total_events_in_last_i_o = component['totalEventsInLastI/o'] if 'totalEventsInLastI/o' in component else ''
        self.total_number_of_reconnects = component['totalNumberOfReconnects'] if 'totalNumberOfReconnects' in component else ''
        self.write_bytes = component['writeBytes'] if 'writeBytes' in component else ''

        self.table_write_information = component['tableWriteInformation'] if 'tableWriteInformation' in component else ''

        self.details = {}

        if self.table_write_information != '':
            # Convert string to JSON object
            tblinfo = json.loads(self.table_write_information)

            output = {}

            # Loop through JSON object and extract information
            for item in tblinfo:
                # Get the key of the current item
                key = list(item.keys())[0]
                # Get the information for the current item
                info = item[key]
                # Create a new dictionary to store the information
                new_info = {}
                # Loop through the information and extract nested information
                for k, v in info.items():
                    if isinstance(v, dict):
                        for nk, nv in v.items():
                            new_info[f"{k}.{nk}"] = nv
                    else:
                        new_info[k] = v
                # Add the new information to the output dictionary with the key as the table name
                output[key] = new_info

            # Convert output dictionary to JSON string
            json_output = json.dumps(output, indent=2)

            self.details = json_output

            # Print output
            print('json_output',json_output)

class Target_TableInformation:
    def __init__(self, cmpt):
        data = cmpt[0]
        self.total_batches_created = data['Total Batches Created']
        self.partition_pruned_batches = data['Partition Pruned Batches']
        self.last_successful_merge_time = data['Last successful merge time']
        self.total_batches_ignored = data['Total Batches Ignored']
        self.max_integration_time_in_ms = data['Max Integration Time in ms']
        self.avg_in_mem_compaction_time_in_ms = data['Avg In-Mem Compaction Time in ms']
        self.avg_batch_size_in_bytes = data['Avg Batch Size in bytes']
        self.total_event_info = data['Total event info']
        self.avg_event_count_per_batch = data['Avg Event Count Per Batch']
        self.min_integration_time_in_ms = data['Min Integration Time in ms']
        self.mapped_source_table = data['Mapped Source Table']
        self.total_batches_queued = data['Total Batches Queued']
        self.avg_compaction_time_in_ms = data['Avg Compaction Time in ms']
        self.avg_waiting_time_in_queue_in_ms = data['Avg Waiting Time in Queue in ms']
        self.avg_integration_time_in_ms = data['Avg Integration Time in ms']
        self.total_batches_uploaded = data['Total Batches Uploaded']
        self.avg_merge_time_in_ms = data['Avg Merge Time in ms']
        # self.last_batch_info = Target_BatchInfo(data['Last batch info'])
        self.avg_stage_resources_management_time_in_ms = data['Avg Stage Resources Management Time in ms']
        self.avg_upload_time_in_ms = data['Avg Upload Time in ms']

class Target_BatchInfo:
    def __init__(self, data):
        self.no_of_updates = data['No of updates']
        self.batch_event_count = data['Batch Event Count']
        self.no_of_inserts = data['No of inserts']
        self.max_record_size_in_batch = data['Max Record Size in batch']
        self.total_events_merged = data['Total events merged']
        self.no_of_ddls = data['No of DDLs']
        self.batch_sequence_number = data['Batch Sequence Number']
        self.batch_size_in_bytes = data['Batch Size in bytes']
        self.integration_task_time = Target_IntegrationTaskTime(data['Integration Task Time'])
        self.no_of_deletes = data['No of deletes']
        self.no_of_pkupdates = data['No of pkupdates']
        self.batch_accumulation_time_in_ms = data['Batch Accumulation Time in ms']

class Target_IntegrationTaskTime:
    def __init__(self, data):
        self.compaction_time_in_ms = data['Compaction Time in ms']
        self.stage_resources_management_time_in_ms = data['Stage Resources Management Time in ms']
        self.upload_time_in_ms = data['Upload Time in ms']
        self.merge_time_in_ms = data['Merge Time in ms']
        self.in_mem_compaction_time_in_ms = data['In-Memory Compaction Time in ms']
        self.pk_update_time_in_ms = data['pk Update Time in ms']
        self.ddl_execution_time_in_ms = data['DDL Execution Time in ms']
        self.total_integration_time_in_ms = data['Total Integration Time in ms']


class StriimApplication:
    def __init__(self, entity_type, full_name, status_change, rate, source_rate, cpu_rate, num_servers, latest_activity):
        self.entity_type = entity_type
        self.full_name = full_name
        self.status_change = status_change
        self.rate = rate
        self.source_rate = source_rate
        self.cpu_rate = cpu_rate
        self.num_servers = num_servers
        self.latest_activity = latest_activity
        self.components = []

    def add_component(self, component):
        self.components.append(component)

class StriimClusterNode:
    def __init__(self, entity_type, name, version, free_memory, cpu_rate, uptime):
        self.entity_type = entity_type
        self.name = name
        self.version = version
        self.free_memory = free_memory
        self.cpu_rate = cpu_rate
        self.uptime = uptime

class Elasticsearch:
    def __init__(self, elasticsearchReceiveThroughput, elasticsearchTransmitThroughput, elasticsearchClusterStorageFree, elasticsearchClusterStorageTotal):
        self.elasticsearchReceiveThroughput = elasticsearchReceiveThroughput
        self.elasticsearchTransmitThroughput = elasticsearchTransmitThroughput
        self.elasticsearchClusterStorageFree = elasticsearchClusterStorageFree
        self.elasticsearchClusterStorageTotal = elasticsearchClusterStorageTotal

#
#  Usage: striim_apps, striim_nodes, es_nodes = map_mon_json_response(json_response)
#

def map_mon_json_response(json_response):
    parsed_json = json_response #json.loads(json_response)
    striim_applications = []

    for app in parsed_json[0]["output"]["striimApplications"]:
        app_data = app #[0]
        striim_applications.append(
            StriimApplication(
                app_data["entityType"],
                app_data["fullName"],
                app_data["statusChange"],
                app_data["rate"],
                app_data["sourceRate"],
                app_data["cpuRate"],
                app_data["numServers"],
                app_data["latestActivity"]
            )
        )

    striim_cluster_nodes = []
    for node in parsed_json[0]["output"]["striimClusterNodes"]:
        node_data = node #[0]
        striim_cluster_nodes.append(
            StriimClusterNode(
                node_data["entityType"],
                node_data["name"],
                node_data["version"],
                node_data["freeMemory"],
                node_data["cpuRate"],
                node_data["uptime"]
            )
        )

    elasticsearch_nodes = []

    es_data = parsed_json[0]["output"]["elasticsearch"]

    elasticsearch_nodes.append(
        Elasticsearch(
            es_data["elasticsearchReceiveThroughput"],
            es_data["elasticsearchTransmitThroughput"],
            es_data["elasticsearchClusterStorageFree"],
            es_data["elasticsearchClusterStorageTotal"]
        )
    )

    # for es_node in parsed_json[0]["output"]["elasticsearch"]:
    #     print(es_node)
    #     es_data = es_node # json.loads(es_node) #[0]
    #     elasticsearch_nodes.append(
    #         Elasticsearch(
    #             es_data["elasticsearchReceiveThroughput"],
    #             es_data["elasticsearchTransmitThroughput"],
    #             es_data["elasticsearchClusterStorageFree"],
    #             es_data["elasticsearchClusterStorageTotal"]
    #         )
    #     )

    return (striim_applications, striim_cluster_nodes, elasticsearch_nodes)

# Example: update_application_components(applications[0], json_response)

def update_application_components(application, json_response):
    app_components = json.loads(json_response)[0]["output"]["striimApplications"][0]["applicationComponents"]
    for component in app_components:
        application.components.append(component)

def runMon(component=''):
    data = 'mon;'
    if component != '':
        data = 'mon ' + component + ';'

    resp = requests.post('http://' + node + ':9080/api/v2/tungsten', headers=headers, data=data)

    return json.loads(resp.text)

def runReview():
    # Use a breakpoint in the code line below to debug your script.

    # Get node information: mon;
    json_response = runMon()

    # print(json_response)

    # Assign values
    striim_apps, striim_nodes, es_nodes = map_mon_json_response(json_response)

    for app in striim_apps:
        # Define the named tuple to store the extracted information
        DataRecord = namedtuple('DataRecord',
                                ['SourceTableName', 'TotalRows', 'schemaGenerationStatus', 'dataReadStatus', 'RowsRead',
                                 'TargetTableName', 'NumberOfInserts', 'LastBatchActivity'])
        data_records = []
        additional_records = []

        # Run: mon <app name>
        json_mon_app = runMon(app.full_name)[0]
        # print(json_mon_app)
        # print(json_mon_app[0])

        striim_head_component = StriimHeadComponentResponse(json_mon_app['command'], json_mon_app['executionStatus'], json_mon_app['output']).output

        # print(striim_head_component.applicationComponents)

        # Only consider responses that actually have applicationComponents
        if (striim_head_component.applicationComponents != ''):
            for striim_component in striim_head_component.applicationComponents:

                new_component = StriimComponent(striim_component)

                app.add_component(new_component)

                # Only look at active sources
                if new_component.entityType == "SOURCE" and new_component.latestActivity != '':
                    # print("Source!", new_component.fullName)
                    # print(new_component.latestActivity, '-', new_component.statusChange)

                    # Run: mon <source component name>
                    json_source_component = runMon(new_component.fullName)[0]

                    striim_source_component = StriimComponentSourceResponse(json_source_component['command'],
                                                                        json_source_component['executionStatus'],
                                                                        json_source_component['output'],
                                                                        json_source_component['responseCode']).output

                    # For debugging, this prints the source information
                    # print('src', striim_source_component.table_information)

                    json_source_data = json.loads(striim_source_component.table_information)

                    # print("rowcount", striim_source_component.rowcount)

                    for source_table_name, data_str in json_source_data.items():
                        if data_str != '' and 'TotalRows' in data_str:
                            data_dict = json.loads(data_str)
                            record = DataRecord(
                                SourceTableName=source_table_name,
                                TotalRows=data_dict['TotalRows'],
                                schemaGenerationStatus=data_dict['schemaGenerationStatus'],
                                dataReadStatus=data_dict['dataReadStatus'],
                                RowsRead=data_dict['RowsRead'],
                                TargetTableName='',
                                NumberOfInserts='',
                                LastBatchActivity=''
                            )
                            data_records.append(record)

                # Only look at active targets
                if new_component.entityType == "TARGET" and new_component.latestActivity != '':
                    # print("Target!", new_component.fullName)
                    # print(new_component.latestActivity, '-', new_component.statusChange)

                    # Run: mon <source component name>
                    json_target_component = runMon(new_component.fullName)[0]

                    striim_target_component = StriimComponentTargetResponse(json_target_component['command'],
                                                                        json_target_component['executionStatus'],
                                                                        json_target_component['output'],
                                                                        json_target_component['responseCode']).output

                    # parse the input JSON data
                    json_target_data = json.loads(striim_target_component.table_information)

                    # iterate over the data to find matching entry
                    for k, v in json_target_data.items():

                        # Loop through tuple
                        for i, dr in enumerate(data_records):
                            # Track if we update a target table already

                            if dr.SourceTableName in v['Sources']:
                                # Check to see if this record is already used
                                if data_records[i].TargetTableName == '':
                                    # print('Updating existing entry...')

                                    # update TargetTableName
                                    data_records[i] = dr._replace(TargetTableName=k)

                                    # update NumberOfInserts and LastBatchActivity
                                    data_records[i] = data_records[i]._replace(NumberOfInserts=v['No of Inserts'])
                                    data_records[i] = data_records[i]._replace(
                                        LastBatchActivity=v['Last Batch Execution Time'])
                                if data_records[i].TargetTableName == k:
                                    # We need to update existing entry, since table matches
                                    new_numOfInserts = data_records[i].NumberOfInserts + v['No of Inserts']

                                    data_records[i] = dr._replace(NumberOfInserts=new_numOfInserts)
                                    data_records[i] = data_records[i]._replace(
                                        LastBatchActivity=v['Last Batch Execution Time'])
                                else:
                                    # We need a new entry since target table does not match
                                    new_record = DataRecord(
                                                        SourceTableName=data_records[i].SourceTableName,
                                                        TotalRows=data_records[i].TotalRows,
                                                        schemaGenerationStatus=data_records[i].schemaGenerationStatus,
                                                        dataReadStatus=data_records[i].dataReadStatus,
                                                        RowsRead=data_records[i].RowsRead,
                                                        TargetTableName=k,
                                                        NumberOfInserts=v['No of Inserts'],
                                                        LastBatchActivity=v['Last Batch Execution Time']
                                                    )
                                    # print(new_record)
                                    additional_records.append(new_record)
                                    # For this application, build the summary of results.

        did_print = False;

        if len(data_records) > 0:
            print(" > Reviewing App:", app.full_name)
            logging.info(" > Reviewing App: " + app.full_name)
            did_print = True;

        data_records.extend(additional_records)

        # Sort the data_records list based on the dataReadStatus field
        # sorted_data = sorted(data_records, key=lambda r: r.dataReadStatus == 'Completed', reverse=True)

        # Sort based on LastBatchActivity
        sorted_data = sorted(data_records, key=lambda r: r.LastBatchActivity, reverse=True)

        strCompletedSourceList = ''
        strRemainingSourceList = ''

        # Loop through the sorted list and print the fields
        for record in sorted_data:
            # Check statuses
            if record.NumberOfInserts == record.RowsRead:
                strCompletedSourceList += record.SourceTableName + ';'
                print(f" > - {record.LastBatchActivity} --- Complete: {record.SourceTableName} ({record.RowsRead} rows)\t-> {record.TargetTableName} ({record.NumberOfInserts} rows)")
                logging.info(f" > - {record.LastBatchActivity} --- Complete: {record.SourceTableName} ({record.RowsRead} rows)\t-> {record.TargetTableName} ({record.NumberOfInserts} rows)")
                did_print = True;
            else:
                strRemainingSourceList += record.SourceTableName + ';'
                completeProgress = 0
                if record.RowsRead != 0:
                    # This value is inaccurate; RowsRead will continue to increase until Striim has detected all rows.
                    completeProgress = 0 #int(record.NumberOfInserts) / int(record.RowsRead)
                print(f" > - {record.LastBatchActivity} - Progress: {record.SourceTableName} ({record.RowsRead} rows)\t-> {record.TargetTableName} ({record.NumberOfInserts} rows)")
                logging.info(f" > - {record.LastBatchActivity} - Progress: {record.SourceTableName} ({record.RowsRead} rows)\t-> {record.TargetTableName} ({record.NumberOfInserts} rows)")
                did_print = True;

        if strCompletedSourceList != '':
            print(" > Completed Sources: ", strCompletedSourceList)
            logging.info(" > Completed Sources: " + strCompletedSourceList)
            did_print = True;
        if strRemainingSourceList != '':
            print(" > Remaining Sources: ", strRemainingSourceList)
            logging.info(" > Remaining Sources: "+ strRemainingSourceList)
            did_print = True;

        if did_print:
            print(f"------------------------------ Next run in {polling_interval_seconds} seconds ------------------------------------")
            logging.info(f"------------------------------ Next run in {polling_interval_seconds} seconds ------------------------------------")


if __name__ == '__main__':
    continueRun = True;
    numberOfTimes = run_iterations;
    print('Logging Enabled. Storing at: ' + log_output_path)
    while(continueRun):
        print('Executing at', str(datetime.now()))
        logging.info('Executing at ' + str(datetime.now()))
        runReview()
        numberOfTimes = numberOfTimes - 1;
        print('Run completed at', datetime.now(), '-', str(numberOfTimes), 'runs remaining.')
        logging.info('Run completed at ' + str(datetime.now()) + ' - ' + str(numberOfTimes) + ' runs remaining.')
        time.sleep(polling_interval_seconds)
        if numberOfTimes == 0:
            continueRun = False;
    #print(runMon('oracle.Oracle_CDC_Continuous'))

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
