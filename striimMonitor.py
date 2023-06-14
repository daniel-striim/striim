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
node = '24.53.180.24' # Put your node IP Address or DNS name
username = 'admin' # Use your ADMIN username here
password = 'adminpassword' # User your ADMIN password here

polling_interval_seconds = 10 # This controls how often this will check for updates
run_iterations = 100 # This controls how many times it will loop through this run
log_output_path = '/Users/danielferrara/Documents/striimwatcher.log' # This indicates the path to store the output logs (persisted logging)

# Notes about the Code
# * This code is meant to be run as-is and be able to return valueable Initial Load or CDC Data.
# * This code is provided as a sample, in order to support being able to work with Striim's Rest API
# * This code is not officially supported as part of Striim

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
        self.command = response['command'] if 'command' in response else ''
        self.execution_status = response['executionStatus'] if 'executionStatus' in response else ''
        self.cpu = response['output']['cpu'] if 'output' in response and 'cpu' in response['output'] else ''
        self.cpu_rate_per_node = response['output']['cpuRatePerNode'] if 'output' in response and 'cpuRatePerNode' in response['output'] else ''
        self.cpu_rate = response['output']['cpuRate'] if 'output' in response and 'cpuRate' in response['output'] else ''
        self.number_of_events_seen_per_monitor_snapshot_interval = response['output']['numberOfEventsSeenPerMonitorSnapshotInterval'] if 'output' in response and 'numberOfEventsSeenPerMonitorSnapshotInterval' in response['output'] else ''
        self.ignored_tables_list = response['output']['ignoredTablesList'] if 'output' in response and 'ignoredTablesList' in response['output'] else ''
        self.input = response['output']['input'] if 'output' in response and 'input' in response['output'] else ''
        self.input_rate = response['output']['inputRate'] if 'output' in response and 'inputRate' in response['output'] else ''
        self.last_event_read_age = response['output']['lastEventReadAge'] if 'output' in response and 'lastEventReadAge' in response['output'] else ''
        self.latest_activity = response['output']['latestActivity'] if 'output' in response and 'latestActivity' in response['output'] else ''
        self.num_servers = response['output']['numServers'] if 'output' in response and 'numServers' in response['output'] else ''
        self.rate = response['output']['rate'] if 'output' in response and 'rate' in response['output'] else ''
        self.read_status = response['output']['readStatus'] if 'output' in response and 'readStatus' in response['output'] else ''
        self.source_input = response['output']['sourceInput'] if 'output' in response and 'sourceInput' in response['output'] else ''
        self.source_rate = response['output']['sourceRate'] if 'output' in response and 'sourceRate' in response['output'] else ''
        self.table_information = response['output']['tableInformation'] if 'output' in response and 'tableInformation' in response['output'] else ''
        self.timestamp = response['output']['timestamp'] if 'output' in response and 'timestamp' in response['output'] else ''
        self.row_count = response['output']['rowCount'] if 'output' in response and 'rowCount' in response['output'] else ''

# Used to get components
class StriimHeadComponentResponse:
    def __init__(self, command, executionStatus, output):
        self.command = command
        self.executionStatus = executionStatus
        self.output = StriimHeadComponent(output)

class StriimHeadComponent:
    def __init__(self, component):
        self.entityType = component['entityType'] if 'entityType' in component else ''
        self.fullName = component['fullName'] if 'fullName' in component else ''
        self.statusChange = component['statusChange'] if 'statusChange' in component else ''
        self.rate = component['rate'] if 'rate' in component else ''
        self.sourceRate = component['sourceRate'] if 'sourceRate' in component else ''
        self.cpuRate = component['cpuRate'] if 'cpuRate' in component else ''
        self.numServers = component['numServers'] if 'numServers' in component else ''
        self.latestActivity = component['latestActivity'] if 'latestActivity' in component else ''
        self.applicationComponents = component['applicationComponents'] if "applicationComponents" in component else ''
        self.sources = []

    def add_source(self, source):
        self.sources.append(source)


class StriimComponent:
    def __init__(self, component):
        self.entityType = component['entityType'] if 'entityType' in component else ''
        self.fullName = component['fullName'] if 'fullName' in component else ''
        self.statusChange = component['statusChange'] if 'statusChange' in component else ''
        self.rate = component['rate'] if 'rate' in component else ''
        self.sourceRate = component['sourceRate'] if 'sourceRate' in component else ''
        self.cpuRate = component['cpuRate'] if 'cpuRate' in component else ''
        self.numServers = component['numServers'] if 'numServers' in component else ''
        self.latestActivity = component['latestActivity'] if 'latestActivity' in component else ''


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
        self.total_batches_created = data['Total Batches Created'] if 'Total Batches Created' in data else ''
        self.partition_pruned_batches = data['Partition Pruned Batches'] if 'Partition Pruned Batches' in data else ''
        self.last_successful_merge_time = data['Last successful merge time'] if 'Last successful merge time' in data else ''
        self.total_batches_ignored = data['Total Batches Ignored'] if 'Total Batches Ignored' in data else ''
        self.max_integration_time_in_ms = data['Max Integration Time in ms'] if 'Max Integration Time in ms' in data else ''
        self.avg_in_mem_compaction_time_in_ms = data['Avg In-Mem Compaction Time in ms'] if 'Avg In-Mem Compaction Time in ms' in data else ''
        self.avg_batch_size_in_bytes = data['Avg Batch Size in bytes'] if 'Avg Batch Size in bytes' in data else ''
        self.total_event_info = data['Total event info'] if 'Total event info' in data else ''
        self.avg_event_count_per_batch = data['Avg Event Count Per Batch'] if 'Avg Event Count Per Batch' in data else ''
        self.min_integration_time_in_ms = data['Min Integration Time in ms'] if 'Min Integration Time in ms' in data else ''
        self.mapped_source_table = data['Mapped Source Table'] if 'Mapped Source Table' in data else ''
        self.total_batches_queued = data['Total Batches Queued'] if 'Total Batches Queued' in data else ''
        self.avg_compaction_time_in_ms = data['Avg Compaction Time in ms'] if 'Avg Compaction Time in ms' in data else ''
        self.avg_waiting_time_in_queue_in_ms = data['Avg Waiting Time in Queue in ms'] if 'Avg Waiting Time in Queue in ms' in data else ''
        self.avg_integration_time_in_ms = data['Avg Integration Time in ms'] if 'Avg Integration Time in ms' in data else ''
        self.total_batches_uploaded = data['Total Batches Uploaded'] if 'Total Batches Uploaded' in data else ''
        self.avg_merge_time_in_ms = data['Avg Merge Time in ms'] if 'Avg Merge Time in ms' in data else ''
        self.avg_stage_resources_management_time_in_ms = data['Avg Stage Resources Management Time in ms'] if 'Avg Stage Resources Management Time in ms' in data else ''
        self.avg_upload_time_in_ms = data['Avg Upload Time in ms'] if 'Avg Upload Time in ms' in data else ''
        # self.last_batch_info = Target_BatchInfo(data['Last batch info'])

class Target_BatchInfo:
    def __init__(self, data):
        self.no_of_updates = data['No of updates'] if 'No of updates' in data else ''
        self.batch_event_count = data['Batch Event Count'] if 'Batch Event Count' in data else ''
        self.no_of_inserts = data['No of inserts'] if 'No of inserts' in data else ''
        self.max_record_size_in_batch = data['Max Record Size in batch'] if 'Max Record Size in batch' in data else ''
        self.total_events_merged = data['Total events merged'] if 'Total events merged' in data else ''
        self.no_of_ddls = data['No of DDLs'] if 'No of DDLs' in data else ''
        self.batch_sequence_number = data['Batch Sequence Number'] if 'Batch Sequence Number' in data else ''
        self.batch_size_in_bytes = data['Batch Size in bytes'] if 'Batch Size in bytes' in data else ''
        self.integration_task_time = Target_IntegrationTaskTime(data['Integration Task Time']) if 'Integration Task Time' in data else ''
        self.no_of_deletes = data['No of deletes'] if 'No of deletes' in data else ''
        self.no_of_pkupdates = data['No of pkupdates'] if 'No of pkupdates' in data else ''
        self.batch_accumulation_time_in_ms = data['Batch Accumulation Time in ms'] if 'Batch Accumulation Time in ms' in data else ''


class Target_IntegrationTaskTime:
    def __init__(self, data):
        self.compaction_time_in_ms = data['Compaction Time in ms'] if 'Compaction Time in ms' in data else ''
        self.stage_resources_management_time_in_ms = data['Stage Resources Management Time in ms'] if 'Stage Resources Management Time in ms' in data else ''
        self.upload_time_in_ms = data['Upload Time in ms'] if 'Upload Time in ms' in data else ''
        self.merge_time_in_ms = data['Merge Time in ms'] if 'Merge Time in ms' in data else ''
        self.in_mem_compaction_time_in_ms = data['In-Memory Compaction Time in ms'] if 'In-Memory Compaction Time in ms' in data else ''
        self.pk_update_time_in_ms = data['pk Update Time in ms'] if 'pk Update Time in ms' in data else ''
        self.ddl_execution_time_in_ms = data['DDL Execution Time in ms'] if 'DDL Execution Time in ms' in data else ''
        self.total_integration_time_in_ms = data['Total Integration Time in ms'] if 'Total Integration Time in ms' in data else ''

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

    for app in [app for app in striim_apps if app.status_change not in ['CREATED','DEPLOYED']]:
        # Define the named tuple to store the extracted information
        DataRecord = namedtuple('DataRecord',
                                ['SourceTableName', 'TotalRows', 'schemaGenerationStatus', 'dataReadStatus', 'RowsRead',
                                 'TargetTableName', 'NumberOfInserts', 'LastBatchActivity',
                                 'NumDeletes', 'NumDDL', 'NumPKUpdates', 'NumUpdates', 'NumInserts',
                                 'Target_NumDeletes', 'Target_NumDDL', 'Target_NumPKUpdates', 'Target_NumUpdates', 'Target_NumInserts'])
        data_records = []
        additional_records = []
        # considered_target_components = []

        # Run: mon <app name>
        json_mon_app = runMon(app.full_name)[0]
        # print('json_mon_app:', json_mon_app)
        # print(json_mon_app[0])

        try:
            # print('output:', json_mon_app['output'])

            striim_head_component = StriimHeadComponentResponse(json_mon_app['command'], json_mon_app['executionStatus'], json_mon_app['output']).output
            # print('striim_head_component.applicationComponents:', striim_head_component.applicationComponents)

            # Only consider responses that actually have applicationComponents and either running, success or terminated
            if (striim_head_component.applicationComponents != ''):
                # for app in [app for app in striim_apps if app.status_change not in ['CREATED','DEPLOYED']]
                for striim_component in [striim_component for striim_component in striim_head_component.applicationComponents if striim_component['entityType'] in ['SOURCE', 'TARGET']]:

                    new_component = StriimComponent(striim_component)

                    app.add_component(new_component)

                    # Only look at active sources
                    if new_component.entityType == "SOURCE" and new_component.latestActivity != '':
                        # print("Source!", new_component.fullName)
                        # print(new_component.latestActivity, '-', new_component.statusChange)

                        # Run: mon <source component name>
                        json_source_component = runMon(new_component.fullName)[0]

                        # For debugging, this prints the source JSON
                        # print('json_source_component:', json.dumps(json_source_component, indent=4))

                        striim_source_component = StriimComponentSourceResponse(json_source_component['command'],
                                                                            json_source_component['executionStatus'],
                                                                            json_source_component['output'],
                                                                            json_source_component['responseCode']).output

                        # print('table_information', striim_source_component.table_information)

                        if striim_source_component.table_information != '':
                            try:
                                json_source_data = json.loads(striim_source_component.table_information)

                                # Initial Load Application
                                if striim_source_component.cdc_operation == '':
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
                                                LastBatchActivity='',
                                                NumDeletes='',
                                                NumDDL='',
                                                NumPKUpdates='',
                                                NumUpdates='',
                                                NumInserts='',
                                                Target_NumDeletes=0,
                                                Target_NumDDL=0,
                                                Target_NumPKUpdates=0,
                                                Target_NumUpdates=0,
                                                Target_NumInserts=0
                                            )
                                            data_records.append(record)
                                # CDC Application
                                else:
                                    for source_table_name, data_str in json_source_data.items():
                                        if data_str != '' and 'No of Inserts' in data_str:
                                            data_dict = json.loads(json.dumps(data_str))
                                            record = DataRecord(
                                                SourceTableName=source_table_name,
                                                TotalRows='',
                                                schemaGenerationStatus='',
                                                dataReadStatus='CDC',
                                                RowsRead='',
                                                TargetTableName='',
                                                NumberOfInserts='',
                                                LastBatchActivity='',
                                                NumDeletes=data_dict['No of Deletes'],
                                                NumDDL=data_dict['No of DDLs'],
                                                NumPKUpdates=data_dict['No of PKUpdates'],
                                                NumUpdates=data_dict['No of Updates'],
                                                NumInserts=data_dict['No of Inserts'],
                                                Target_NumDeletes=0,
                                                Target_NumDDL=0,
                                                Target_NumPKUpdates=0,
                                                Target_NumUpdates=0,
                                                Target_NumInserts=0
                                            )
                                            data_records.append(record)

                            except Exception as e:
                                print('error', e)
                            # print("rowcount", striim_source_component.rowcount)

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
                        # print('json_target_component', json_target_component)
                        # parse the input JSON data
                        json_target_data = json.loads(striim_target_component.table_information)

                        # iterate over the data to find matching entry
                        for k, v in json_target_data.items():

                            # Loop through tuple
                            for i, dr in enumerate(data_records):
                                # Track if we update a target table already

                                if dr.SourceTableName in v['Sources']:

                                    # Only one action needs to occur
                                    completedUpdate = False;

                                    if data_records[i].dataReadStatus == 'CDC':
                                        # Check to see if we are updating a record
                                        if data_records[i].TargetTableName == k:  # and new_component.fullName not in considered_target_components:
                                            # We need to update existing entry, since table matches
                                            new_numOfInserts = data_records[i].NumInserts + v['No of Inserts']
                                            new_numOfDeletes = data_records[i].NumDeletes + v['No of Deletes']
                                            new_numOfPKUpdates = data_records[i].NumPKUpdates + v['No of PKUpdates']
                                            new_numOfUpdates = data_records[i].NumUpdates + v['No of Updates']
                                            new_numOfDDL = data_records[i].NumDDL + v['No of DDLs']

                                            data_records[i] = dr._replace(TargetTableName=k)
                                            data_records[i] = data_records[i]._replace(Target_NumInserts=new_numOfInserts)
                                            data_records[i] = data_records[i]._replace(Target_NumDeletes=new_numOfDeletes)
                                            data_records[i] = data_records[i]._replace(Target_NumPKUpdates=new_numOfPKUpdates)
                                            data_records[i] = data_records[i]._replace(Target_NumUpdates=new_numOfUpdates)
                                            data_records[i] = data_records[i]._replace(Target_NumDDL=new_numOfDDL)
                                            data_records[i] = data_records[i]._replace(
                                                LastBatchActivity=v['Last Batch Execution Time'])

                                            completedUpdate = True;
                                        # Check to see if this record is already used
                                        if data_records[i].TargetTableName == '':
                                            # update TargetTableName
                                            data_records[i] = dr._replace(TargetTableName=k)

                                            new_numOfInserts = v['No of Inserts']
                                            new_numOfDeletes = v['No of Deletes']
                                            new_numOfPKUpdates = v['No of PKUpdates']
                                            new_numOfUpdates = v['No of Updates']
                                            new_numOfDDL = v['No of DDLs']

                                            # update NumberOfInserts and LastBatchActivity
                                            data_records[i] = data_records[i]._replace(Target_NumInserts=new_numOfInserts)
                                            data_records[i] = data_records[i]._replace(Target_NumDeletes=new_numOfDeletes)
                                            data_records[i] = data_records[i]._replace(Target_NumPKUpdates=new_numOfPKUpdates)
                                            data_records[i] = data_records[i]._replace(Target_NumUpdates=new_numOfUpdates)
                                            data_records[i] = data_records[i]._replace(Target_NumDDL=new_numOfDDL)
                                            data_records[i] = data_records[i]._replace(
                                                LastBatchActivity=v['Last Batch Execution Time'])

                                            completedUpdate = True;
                                        if not completedUpdate:
                                            # We need a new entry since target table does not match

                                            new_numOfInserts = v['No of Inserts']
                                            new_numOfDeletes = v['No of Deletes']
                                            new_numOfPKUpdates = v['No of PKUpdates']
                                            new_numOfUpdates = v['No of Updates']
                                            new_numOfDDL = v['No of DDLs']

                                            new_record = DataRecord(
                                                SourceTableName=data_records[i].SourceTableName,
                                                TotalRows=data_records[i].TotalRows,
                                                schemaGenerationStatus=data_records[i].schemaGenerationStatus,
                                                dataReadStatus=data_records[i].dataReadStatus,
                                                RowsRead=data_records[i].RowsRead,
                                                TargetTableName=k,
                                                NumberOfInserts=v['No of Inserts'],
                                                LastBatchActivity=v['Last Batch Execution Time'],
                                                NumDeletes=data_records[i].NumDeletes,
                                                NumDDL=data_records[i].NumDDL,
                                                NumPKUpdates=data_records[i].NumPKUpdates,
                                                NumUpdates=data_records[i].NumUpdates,
                                                NumInserts=data_records[i].NumInserts,
                                                Target_NumDeletes=new_numOfDeletes,
                                                Target_NumDDL=new_numOfDDL,
                                                Target_NumPKUpdates=new_numOfPKUpdates,
                                                Target_NumUpdates=new_numOfUpdates,
                                                Target_NumInserts=new_numOfInserts
                                            )
                                            # print(new_record)
                                            additional_records.append(new_record)

                                            # considered_target_components.append(new_component.fullName)
                                            # For this application, build the summary of results.

                                    if data_records[i].dataReadStatus != 'CDC':
                                        # Check to see if we are updating a record
                                        if data_records[i].TargetTableName == k: # and new_component.fullName not in considered_target_components:
                                            # We need to update existing entry, since table matches
                                            new_numOfInserts = data_records[i].NumberOfInserts + v['No of Inserts']

                                            data_records[i] = dr._replace(TargetTableName=k)
                                            data_records[i] = data_records[i]._replace(NumberOfInserts=new_numOfInserts)
                                            data_records[i] = data_records[i]._replace(
                                                LastBatchActivity=v['Last Batch Execution Time'])

                                            completedUpdate = True;
                                        # Check to see if this record is already used
                                        if data_records[i].TargetTableName == '':
                                            # update TargetTableName
                                            data_records[i] = dr._replace(TargetTableName=k)

                                            # update NumberOfInserts and LastBatchActivity
                                            data_records[i] = data_records[i]._replace(NumberOfInserts=v['No of Inserts'])
                                            data_records[i] = data_records[i]._replace(
                                                LastBatchActivity=v['Last Batch Execution Time'])

                                            completedUpdate = True;
                                        if not completedUpdate:
                                            # We need a new entry since target table does not match
                                            new_record = DataRecord(
                                                                SourceTableName=data_records[i].SourceTableName,
                                                                TotalRows=data_records[i].TotalRows,
                                                                schemaGenerationStatus=data_records[i].schemaGenerationStatus,
                                                                dataReadStatus=data_records[i].dataReadStatus,
                                                                RowsRead=data_records[i].RowsRead,
                                                                TargetTableName=k,
                                                                NumberOfInserts=v['No of Inserts'],
                                                                LastBatchActivity=v['Last Batch Execution Time'],
                                                                NumDeletes='',
                                                                NumDDL='',
                                                                NumPKUpdates='',
                                                                NumUpdates='',
                                                                NumInserts='',
                                                                Target_NumDeletes=0,
                                                                Target_NumDDL=0,
                                                                Target_NumPKUpdates=0,
                                                                Target_NumUpdates=0,
                                                                Target_NumInserts=0
                                                            )
                                            # print(new_record)
                                            additional_records.append(new_record)

                                            # considered_target_components.append(new_component.fullName)
                                            # For this application, build the summary of results.

            did_print = False;

            data_records.extend(additional_records)

            if len(data_records) > 0:
                print(" > Reviewing App:", app.full_name, '(' + app.status_change + ')')
                logging.info(" > Reviewing App: " + app.full_name + ' (' + app.status_change + ')')
                did_print = True;

            # Sort the data_records list based on the dataReadStatus field
            # sorted_data = sorted(data_records, key=lambda r: r.dataReadStatus == 'Completed', reverse=True)

            # Sort based on LastBatchActivity
            sorted_data = sorted(data_records, key=lambda r: r.LastBatchActivity, reverse=True)

            strCompletedSourceList = ''
            strRemainingSourceList = ''

            # Loop through the sorted list and print the fields
            for record in sorted_data:
                if record.dataReadStatus == 'CDC':
                    print(f" > *** CDC Application *** - {record.LastBatchActivity}")
                    print(f" > - {record.SourceTableName}")
                    if record.NumInserts > 0 or record.Target_NumInserts > 0:
                        print(f" > -------  {record.NumInserts} Source Inserts -> {record.Target_NumInserts} Target Inserts - Difference: {record.NumInserts - record.Target_NumInserts} records ({round((record.Target_NumInserts - record.NumInserts) / record.Target_NumInserts * 100 if record.Target_NumInserts != 0 else 0, 3)}%)")
                        logging.info(f" > -------  {record.NumInserts} Source Inserts -> {record.Target_NumInserts} Target Inserts - Difference: {record.NumInserts - record.Target_NumInserts} records ({round((record.Target_NumInserts - record.NumInserts) / record.Target_NumInserts * 100 if record.Target_NumInserts != 0 else 0, 3)}%)")
                    if record.NumUpdates > 0 or record.Target_NumUpdates > 0:
                        print(f" > -------  {record.NumUpdates} Source Updates -> {record.Target_NumUpdates} Target Updates - Difference: {record.NumUpdates - record.Target_NumUpdates} records ({round((record.Target_NumUpdates - record.NumUpdates) / record.Target_NumUpdates * 100 if record.Target_NumUpdates != 0 else 0, 3)}%)")
                        logging.info(f" > -------  {record.NumUpdates} Source Updates -> {record.Target_NumUpdates} Target Updates - Difference: {record.NumUpdates - record.Target_NumUpdates} records ({round((record.Target_NumUpdates - record.NumUpdates) / record.Target_NumUpdates * 100 if record.Target_NumUpdates != 0 else 0, 3)}%)")
                    if record.NumDeletes > 0 or record.Target_NumDeletes > 0:
                        print(f" > -------  {record.NumDeletes} Source Deletes -> {record.Target_NumDeletes} Target Deletes - Difference: {record.NumDeletes - record.Target_NumDeletes} records ({round((record.Target_NumDeletes - record.NumDeletes) / record.Target_NumDeletes * 100 if record.Target_NumDeletes != 0 else 0, 3)}%)")
                        logging.info(f" > -------  {record.NumDeletes} Source Deletes -> {record.Target_NumDeletes} Target Deletes - Difference: {record.NumDeletes - record.Target_NumDeletes} records ({round((record.Target_NumDeletes - record.NumDeletes) / record.Target_NumDeletes * 100 if record.Target_NumDeletes != 0 else 0, 3)}%)")
                    if record.NumPKUpdates > 0 or record.Target_NumPKUpdates > 0:
                        print(f" > -------  {record.NumPKUpdates} Source PKUpdts -> {record.Target_NumPKUpdates} Target PKUpdts - Difference: {record.NumPKUpdates - record.Target_NumPKUpdates} records ({round((record.Target_NumPKUpdates - record.NumPKUpdates) / record.Target_NumPKUpdates * 100 if record.Target_NumPKUpdates != 0 else 0, 3)}%)")
                        logging.info(f" > -------  {record.NumPKUpdates} Source PKUpdts -> {record.Target_NumPKUpdates} Target PKUpdts - Difference: {record.NumPKUpdates - record.Target_NumPKUpdates} records ({round((record.Target_NumPKUpdates - record.NumPKUpdates) / record.Target_NumPKUpdates * 100 if record.Target_NumPKUpdates != 0 else 0, 3)}%)")
                    if record.NumDDL > 0 or record.Target_NumDDL > 0:
                        print(f" > -------  {record.NumDDL} Source DDLs    -> {record.Target_NumDDL} Target Inserts - Difference: {record.NumDDL - record.Target_NumDDL} records ({round((record.Target_NumDDL - record.NumDDL) / record.Target_NumDDL * 100 if record.Target_NumDDL != 0 else 0, 3)}%)")
                        logging.info(f" > -------  {record.NumDDL} Source DDLs    -> {record.Target_NumDDL} Target Inserts - Difference: {record.NumDDL - record.Target_NumDDL} records ({round((record.Target_NumDDL - record.NumDDL) / record.Target_NumDDL * 100 if record.Target_NumDDL != 0 else 0, 3)}%)")
                    logging.info(f" > - {record.LastBatchActivity} --- Complete: {record.SourceTableName} ({record.RowsRead} rows)\t-> {record.TargetTableName} ({record.NumberOfInserts} rows)")
                    did_print = True;
                else:
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
        except Exception as e:
            print('error', e)

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
