# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import requests

import json

"""
python3 main.py localhost admin password /Users/<username>/Downloads/StriimApps/
Script command-line arguments:
            1st arg: script name in this case runOrderedInitialLoad.py
            2nd arg: hostname where the application is running in this case localhost
            3rd arg: login for Striim URL, in this case, admin
            4th arg: password for Striim URL, in this case, test
            5th arg: location of CSV file on the server (include trailing "/")
"""
node = '34.82.51.202' # sys.argv[1]
username = 'admin' # sys.argv[2]
password = 'admin' # sys.argv[3]

#create full appOrder.csv file path
dir = '' # sys.argv[4]
file = "appOrder.csv"
fullPath = dir + file

#generate REST API authentication token
data = {'username': username, 'password': password}
resp = requests.post('http://' + node + ':9080/security/authenticate', data=data)
jkvp = json.loads(resp.text)
sToken = jkvp['token']

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
        self.output = StriimHeadComponentSource(output)
        self.response_code = response_code

class StriimHeadComponentSource:
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
        self.source_freshness = component['sourceFreshness'] if 'sourceFreshness' in component else ''
        self.source_input = component['sourceInput'] if 'sourceInput' in component else ''
        self.source_rate = component['sourceRate'] if 'sourceRate' in component else ''
        self.startscn = component['startscn'] if 'startscn' in component else ''
        self.table_information = component['tableInformation'] if 'tableInformation' in component else ''
        self.timestamp = component['timestamp'] if 'timestamp' in component else ''
        self.top_open_transactions = component['topOpenTransactions(#OfOps)'] if 'topOpenTransactions(#OfOps)' in component else ''
        self.operations_in_the_cache = component['operationsInTheCache'] if 'operationsInTheCache' in component else ''
        self.total_number_of_reconnects = component['totalNumberOfReconnects'] if 'totalNumberOfReconnects' in component else ''


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

    # Get node information
    json_response = runMon()

    # print(json_response)

    # Assign values
    striim_apps, striim_nodes, es_nodes = map_mon_json_response(json_response)

    for app in striim_apps:
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

                if new_component.entityType == "SOURCE":
                    print("Source!", new_component.fullName)
                    print(new_component.latestActivity, '-', new_component.statusChange)
                    json_source_component = runMon(new_component.fullName)[0]
                    striim_source_component = StriimComponentSourceResponse(json_source_component['command'],
                                                                        json_source_component['executionStatus'],
                                                                        json_source_component['output'],
                                                                        json_source_component['responseCode']).output

                    print(striim_source_component.table_information)

        # app.add_component(striim_component)

        # print(striim_component.entityType + ":" + striim_component.fullName)


        # app.add_component()



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    runReview()
    #print(runMon('oracle.Oracle_CDC_Continuous'))

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
