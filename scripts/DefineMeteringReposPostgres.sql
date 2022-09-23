-- Striim Metering Schema creation script (Postgres)
-- For on-prem deployment, run as MDR user after running the MDR define script
-- For saas deployment, follow the instructions below

-- Connect to the postgres database (striimdb) created for the MDR
-- Run the commands below as specified

-- a. CREATE USER striim_metering WITH PASSWORD '<password>';
-- b. GRANT CREATE ON DATABASE striimdb TO striim_metering;
-- c. CREATE SCHEMA striim_metering;
-- d. GRANT ALL ON SCHEMA striim_metering TO striim_metering;
-- e. ALTER ROLE striim_metering SET search_path TO striim_metering;
-- Connect using striim_metering user
-- Run the following SQL Statements

create table signature (
    signature      varchar(250)  not null primary key
);

create table sequencer (
    seq_name       varchar(100)  not null primary key,
    seq_count      bigint
);

create table billing_tier (
    tier_id        int           not null primary key, -- product tier
    tier_name      varchar(250),
    weight         double precision  -- usage unit to USD conversion weight
);

create table adapter_rate (
    tier_id        int           not null primary key, -- adapter tier
    tier_name      varchar(250),
    units_per_mil  double precision, -- usage units per million events
    weight         double precision  -- adapter accelerator
);

create table sms_rate (
    tier_id        int           not null primary key,
    tier_name      varchar(250),
    units_per_mig_mil double precision,   -- usage units per million migration events
    units_per_rep_mil double precision    -- usage units per million replication events
);

create table billing_cycle (
    billing_id     bigint        not null primary key,
    label          varchar(250),
    start_time     bigint,       -- inclusive
    end_time       bigint,       -- exclusive
    tier_id        int           not null references billing_tier,
    last_metering_id bigint
);
create unique index billing_cycle_uk_idx   on billing_cycle (start_time, end_time);
create        index billing_cycle_tier_idx on billing_cycle (tier_id);

create table metering_cycle (
    billing_id     bigint        not null references billing_cycle,
    metering_id    bigint        not null primary key,
    start_time     bigint,       -- inclusive
    end_time       bigint,       -- exclusive
    generated_at   bigint
);
create unique index metering_cycle_uk_idx      on metering_cycle (start_time, end_time);
create        index metering_cycle_billing_idx on metering_cycle (billing_id);

create table cycle_rate (
    metering_id    bigint        not null primary key references metering_cycle,
    rates          varchar(4000)
);

create table consumption_unit (
    unit_id        char(1)       not null primary key,
    raw_unit       varchar(250),
    scaled_unit    varchar(250)
);

create table component_type (
    type_id        char(1)       not null primary key,
    type_name      varchar(250),
    unit_id        char(1)       not null references consumption_unit
);
create index component_type_unit_idx on component_type (unit_id);

create table application_type (
    type_id        char(1)       not null primary key,
    type_name      varchar(250)
);

create table adapter (
    adapter_id     int           not null primary key,
    adapter_name   varchar(250), -- source/target adapter name
    name_suffix    varchar(250),
    app_type       char(1)       not null references application_type,
    type_id        char(1)       not null references component_type,
    tier_id        int           not null references adapter_rate, -- for events based adapters in striim apps
    weight         double precision  -- for non-events based (non-tiered) adapters in striim apps
                                     -- for storage bytes based adapters: units per GiB-hour
                                     -- for feature items: feature accelerator
);
create index adapter_app_idx  on adapter (app_type);
create index adapter_type_idx on adapter (type_id);
create index adapter_tier_idx on adapter (tier_id);

create table application (
    project_id     varchar(100)  references application, -- null for project
    app_id         varchar(100)  not null primary key,
    app_name       varchar(250), -- name of the application
    app_type       char(1)       not null references application_type,
    tombstone      varchar(10)
);
create index application_project_idx  on application (project_id);
create index application_app_idx      on application (app_type);

create table component (
    component_id   varchar(100)  not null primary key,
    component_name varchar(250), -- name of the component
    app_id         varchar(100)  not null references application,
    adapter_id     int           not null references adapter,
    tombstone      varchar(10)
);
create index component_app_idx     on component (app_id);
create index component_adapter_idx on component (adapter_id);

create table consumption_snapshot (
    snapshot_id    bigint        not null primary key,
    component_id   varchar(100)  not null references component,
    server_id      varchar(100), -- server uuid
    measured_at    bigint,       -- measurement time
    consump_raw    bigint        -- measured raw consumption value
);
create unique index consump_snapshot_uk_idx on consumption_snapshot (component_id, server_id);

create table consumption_chkpt (
    chkpt_id       bigint        not null primary key,
    component_id   varchar(100)  not null references component,
    dist_id        varchar(100)  not null, -- distribution id, if partitioned
    position       TEXT,         -- high watermark position
    pretty_pos     varchar(4000)
);
create unique index consump_chkpt_uk_idx on consumption_chkpt (component_id, dist_id);

create table consumption_incr (
    consump_inc_id bigint        not null primary key,
    metering_id    bigint        not null references metering_cycle,
    component_id   varchar(100)  not null references component,
    server_id      varchar(100),     -- server uuid
    measured_at    bigint,           -- measurement time
    consump_raw    bigint,           -- measured raw consumption for this metering cycle/component/server
    consump_scaled double precision  -- scaled consumption for this metering cycle/component/server
);
create unique index consump_incr_uk_idx        on consumption_incr (metering_id, component_id, server_id);
create        index consump_incr_component_idx on consumption_incr (component_id);

create table consumption_cumul (
    consump_sum_id bigint        not null primary key,
    billing_id     bigint        not null references billing_cycle,
    component_id   varchar(100)  not null references component,
    consump_value  double precision  -- cumulative scaled consumption for this billing cycle/component/server
);
create unique index consump_cumul_uk_idx on consumption_cumul (billing_id, component_id);
create        index consump_cumul_component_idx on consumption_cumul (component_id);

create table usage_incr (
    usage_inc_id   bigint        not null primary key,
    metering_id    bigint        not null references metering_cycle,
    app_id         varchar(100)  not null references application,
    adapter_id     int           not null references adapter,
    consump_value  double precision, -- scaled consumption for this metering cycle/app/adapter
    consump_credit double precision, -- consumption credit applied for this metering cycle/app/adapter
    consump_balance double precision, -- consumption after credit for this metering cycle/app/adapter
    usage_value    double precision, -- accelerated/weighted usage for this metering cycle/app/adapter
    usage_credit   double precision, -- usage credit applied for this metering cycle/app/adapter
    usage_balance  double precision  -- usage after credit for this metering cycle/app/adapter
);
create unique index usage_incr_uk_idx      on usage_incr (metering_id, app_id, adapter_id);
create        index usage_incr_app_idx     on usage_incr (app_id);
create        index usage_incr_adapter_idx on usage_incr (adapter_id);

create table usage_cumul (
    usage_sum_id   bigint        not null primary key,
    billing_id     bigint        not null references billing_cycle,
    app_id         varchar(100)  not null references application,
    adapter_id     int           not null references adapter,
    consump_value  double precision, -- cumulative scaled consumption for this billing cycle/app/adapter
    consump_credit double precision, -- cumulative consumption credit applied for this billing cycle/app/adapter
    consump_balance double precision, -- cumulative consumption after credit for this billing cycle/app/adapter
    usage_value    double precision, -- cumulative accelerated/weighted usage for this billing cycle/app/adapter
    usage_credit   double precision, -- cumulative usage credit applied for this billing cycle/app/adapter
    usage_balance  double precision  -- cumulative usage after credit for this billing cycle/app/adapter
);
create unique index usage_cumul_uk_idx      on usage_cumul (billing_id, app_id, adapter_id);
create        index usage_cumul_app_idx     on usage_cumul (app_id);
create        index usage_cumul_adapter_idx on usage_cumul (adapter_id);

create table usage_summary (
    summary_id     bigint        not null primary key,
    billing_id     bigint        not null references billing_cycle,
    app_id         varchar(100)  not null references application,
    usage_value    double precision, -- cumulative usage for this billing cycle
    usage_credit   double precision, -- cumulative usage credit for this billing cycle
    usage_balance  double precision  -- cumulative usage after credit for this billing cycle
);
create unique index usage_summary_uk_idx  on usage_summary (billing_id, app_id);
create        index usage_summary_app_idx on usage_summary (app_id);

create table credit_consumption (
    c_credit_id    bigint        not null primary key,
    begin_at       bigint,
    expiry_at      bigint,
    project_id     varchar(100)  not null references application,
    adapter_id     int           not null references adapter,
    credit_award   double precision, -- awarded scaled consumption credit for this adapter
    credit_remain  double precision  -- remaining credit
);
create index credit_consumption_proj_idx    on credit_consumption (project_id);
create index credit_consumption_adapter_idx on credit_consumption (adapter_id);

create table credit_usage (
    u_credit_id    bigint        not null primary key,
    begin_at       bigint,
    expiry_at      bigint,
    project_id     varchar(100)  not null references application,
    credit_award   double precision, -- awarded usage credit
    credit_remain  double precision  -- remaining credit
);
create index credit_usage_proj_idx on credit_usage (project_id);

create table credit_allocation (
    allocation_id  bigint        not null primary key,
    usage_inc_id   bigint        references usage_incr,
    c_credit_id    bigint        references credit_consumption,
    consump_match  double precision,
    u_credit_id    bigint        references credit_usage,
    usage_match    double precision
);
create index credit_allocation_usage_idx  on credit_allocation (usage_inc_id);
create index credit_allocation_c_cred_idx on credit_allocation (c_credit_id);
create index credit_allocation_u_cred_idx on credit_allocation (u_credit_id);

create table property_value (
    property       varchar(250)  not null primary key,
    value          varchar(4000),
    updated_at     bigint
);

commit;

insert into signature values ('~Streaming Integration and Intelligence~');

insert into sequencer values ('billing_seq',        0);
insert into sequencer values ('metering_seq',       0);
insert into sequencer values ('snapshot_seq',       0);
insert into sequencer values ('chkpt_seq',          0);
insert into sequencer values ('consump_inc_seq',    0);
insert into sequencer values ('consump_sum_seq',    0);
insert into sequencer values ('usage_inc_seq',      0);
insert into sequencer values ('usage_sum_seq',      0);
insert into sequencer values ('meter_summary_seq',  0);
insert into sequencer values ('consump_credit_seq', 0);
insert into sequencer values ('usage_credit_seq',   0);
insert into sequencer values ('allocation_seq',     0);

insert into billing_tier values (1, 'Standard',        0.25);
insert into billing_tier values (2, 'Enterprise',      1.00);
insert into billing_tier values (3, 'MissionCritical', 2.00);
insert into billing_tier values (4, 'NonSegmented',    1.00);
insert into billing_tier values (9, 'Unknown',         1.00);

insert into consumption_unit values ('E', 'Events',        'Million-Events');
insert into consumption_unit values ('S', 'Storage Bytes', 'GiB-Hour');
insert into consumption_unit values ('L', 'License',       'License');
insert into consumption_unit values ('U', 'Unknown',       'Unknown');

insert into component_type values ('S', 'Source',            'E');
insert into component_type values ('T', 'Target',            'E');
insert into component_type values ('P', 'Persistent Stream', 'S');
insert into component_type values ('W', 'WAction Store',     'S');
insert into component_type values ('F', 'Feature',           'L');
insert into component_type values ('U', 'Unknown',           'U');

insert into application_type values ('S', 'StriimApp');
insert into application_type values ('M', 'SmsMigration');
insert into application_type values ('R', 'SmsReplication');
insert into application_type values ('P', 'Project');
insert into application_type values ('U', 'Unknown');

insert into sms_rate     values (1, 'NotSelected', 0.0, 0.00);
insert into adapter_rate values (1, 'Tier-0',      0.0, 0.00);
insert into adapter_rate values (3, 'Tier-100',    0.0, 1.00);
insert into adapter_rate values (9, 'Non-Tiered',  0.0, 0.00);

insert into property_value values ('MeteringRateConfigured', null, null);
insert into billing_cycle  values (-1, 'Orphans', null, null, 9, null);
insert into application    values (null, '00000000-0000-0000-0000-000000000000', 'Default Project', 'P', 'false');

insert into adapter values (101, 'ContinuousGenerator',           'Adapter', 'S', 'S', 9, 0.00);
insert into adapter values (102, 'GGTrailReader',                 'Adapter', 'S', 'S', 3, 0.00);
insert into adapter values (103, 'GooglePubSubReader',            'Adapter', 'S', 'S', 1, 0.00);
insert into adapter values (104, 'HDFSReader',                    'Adapter', 'S', 'S', 1, 0.00);
insert into adapter values (105, 'HPNonStopEnscribeReader',       'Adapter', 'S', 'S', 3, 0.00);
insert into adapter values (106, 'HPNonStopSQLMPReader',          'Adapter', 'S', 'S', 3, 0.00);
insert into adapter values (107, 'HPNonStopSQLMXReader',          'Adapter', 'S', 'S', 3, 0.00);
insert into adapter values (108, 'HTTPReader',                    'Adapter', 'S', 'S', 1, 0.00);
insert into adapter values (109, 'IncrementalBatchReader',        'Adapter', 'S', 'S', 1, 0.00);
insert into adapter values (110, 'JMSReader',                     'Adapter', 'S', 'S', 1, 0.00);
insert into adapter values (111, 'JMXReader',                     'Adapter', 'S', 'S', 1, 0.00);
insert into adapter values (112, 'KafkaReader',                   'Adapter', 'S', 'S', 1, 0.00);
insert into adapter values (113, 'MQTTReader',                    'Adapter', 'S', 'S', 1, 0.00);
insert into adapter values (114, 'MSSqlReader',                   'Adapter', 'S', 'S', 1, 0.00);
insert into adapter values (115, 'MapRFSReader',                  'Adapter', 'S', 'S', 1, 0.00);
insert into adapter values (116, 'MariaDBReader',                 'Adapter', 'S', 'S', 1, 0.00);
insert into adapter values (117, 'MongoDBReader',                 'Adapter', 'S', 'S', 1, 0.00);
insert into adapter values (118, 'MultiFileReader',               'Adapter', 'S', 'S', 1, 0.00);
insert into adapter values (119, 'MysqlReader',                   'Adapter', 'S', 'S', 1, 0.00);
insert into adapter values (120, 'OPCUAReader',                   'Adapter', 'S', 'S', 1, 0.00);
insert into adapter values (122, 'OracleReader',                  'Adapter', 'S', 'S', 3, 0.00);
insert into adapter values (124, 'PostgreSQLReader',              'Adapter', 'S', 'S', 1, 0.00);
insert into adapter values (125, 'S3Reader',                      'Adapter', 'S', 'S', 1, 0.00);
insert into adapter values (126, 'SalesForcePlatformEventReader', 'Adapter', 'S', 'S', 1, 0.00);
insert into adapter values (127, 'SalesForcePushTopicReader',     'Adapter', 'S', 'S', 1, 0.00);
insert into adapter values (128, 'SalesForceReader',              'Adapter', 'S', 'S', 1, 0.00);
insert into adapter values (129, 'SpannerBatchReader',            'Adapter', 'S', 'S', 3, 0.00);
insert into adapter values (130, 'TCPReader',                     'Adapter', 'S', 'S', 1, 0.00);
insert into adapter values (131, 'UDPReader',                     'Adapter', 'S', 'S', 1, 0.00);
insert into adapter values (132, 'WindowsEventLogReader',         'Adapter', 'S', 'S', 1, 0.00);
insert into adapter values (133, 'MSJet',                         'Adapter', 'S', 'S', 3, 0.00);
insert into adapter values (134, 'OJet',                          'Adapter', 'S', 'S', 3, 0.00);
insert into adapter values (135, 'CosmosDBReader',                'Adapter', 'S', 'S', 1, 0.00);
insert into adapter values (136, 'MongoCosmosDBReader',           'Adapter', 'S', 'S', 1, 0.00);
insert into adapter values (137, 'RanReader',                     'Adapter', 'S', 'S', 9, 0.00);
insert into adapter values (138, 'StreamReader',                  'Adapter', 'S', 'S', 9, 0.00);

insert into adapter values (201, 'FileReader',                    'Adapter', 'S', 'S', 1, 0.00);
insert into adapter values (202, 'DatabaseReader',                'Adapter', 'S', 'S', 1, 0.00);

insert into adapter values (301, 'ADLSGen1Writer',                'Adapter', 'S', 'T', 1, 0.00);
insert into adapter values (302, 'ADLSGen2Writer',                'Adapter', 'S', 'T', 1, 0.00);
insert into adapter values (303, 'AzureBlobWriter',               'Adapter', 'S', 'T', 1, 0.00);
insert into adapter values (304, 'AzureEventHubWriter',           'Adapter', 'S', 'T', 1, 0.00);
insert into adapter values (305, 'AzureSQLDWHWriter',             'Adapter', 'S', 'T', 1, 0.00);
insert into adapter values (306, 'BigQueryWriter',                'Adapter', 'S', 'T', 1, 0.00);
insert into adapter values (307, 'CassandraCosmosDBWriter',       'Adapter', 'S', 'T', 1, 0.00);
insert into adapter values (308, 'CassandraWriter',               'Adapter', 'S', 'T', 1, 0.00);
insert into adapter values (309, 'ClouderaHiveWriter',            'Adapter', 'S', 'T', 1, 0.00);
insert into adapter values (310, 'CosmosDBWriter',                'Adapter', 'S', 'T', 1, 0.00);
insert into adapter values (311, 'EmailAdapter',                  'Adapter', 'S', 'T', 1, 0.00);
insert into adapter values (312, 'GCSWriter',                     'Adapter', 'S', 'T', 1, 0.00);
insert into adapter values (313, 'GooglePubSubWriter',            'Adapter', 'S', 'T', 1, 0.00);
insert into adapter values (314, 'HBaseWriter',                   'Adapter', 'S', 'T', 1, 0.00);
insert into adapter values (315, 'HDFSWriter',                    'Adapter', 'S', 'T', 1, 0.00);
insert into adapter values (316, 'HDInsightHDFSWriter',           'Adapter', 'S', 'T', 1, 0.00);
insert into adapter values (317, 'HDInsightKafkaWriter',          'Adapter', 'S', 'T', 1, 0.00);
insert into adapter values (318, 'HTTPWriter',                    'Adapter', 'S', 'T', 1, 0.00);
insert into adapter values (319, 'HazelcastWriter',               'Adapter', 'S', 'T', 1, 0.00);
insert into adapter values (320, 'HiveWriter',                    'Adapter', 'S', 'T', 1, 0.00);
insert into adapter values (321, 'HortonworksHiveWriter',         'Adapter', 'S', 'T', 1, 0.00);
insert into adapter values (322, 'JMSWriter',                     'Adapter', 'S', 'T', 1, 0.00);
insert into adapter values (323, 'JPAWriter',                     'Adapter', 'S', 'T', 1, 0.00);
insert into adapter values (324, 'KafkaWriter',                   'Adapter', 'S', 'T', 1, 0.00);
insert into adapter values (325, 'KinesisWriter',                 'Adapter', 'S', 'T', 1, 0.00);
insert into adapter values (326, 'KuduWriter',                    'Adapter', 'S', 'T', 1, 0.00);
insert into adapter values (327, 'MQTTWriter',                    'Adapter', 'S', 'T', 1, 0.00);
insert into adapter values (328, 'MapRDBWriter',                  'Adapter', 'S', 'T', 1, 0.00);
insert into adapter values (329, 'MapRFSWriter',                  'Adapter', 'S', 'T', 1, 0.00);
insert into adapter values (330, 'MapRStreamWriter',              'Adapter', 'S', 'T', 1, 0.00);
insert into adapter values (331, 'MongoDBWriter',                 'Adapter', 'S', 'T', 1, 0.00);
insert into adapter values (332, 'RedshiftWriter',                'Adapter', 'S', 'T', 1, 0.00);
insert into adapter values (333, 'S3Writer',                      'Adapter', 'S', 'T', 1, 0.00);
insert into adapter values (334, 'SnowflakeWriter',               'Adapter', 'S', 'T', 1, 0.00);
insert into adapter values (335, 'SpannerWriter',                 'Adapter', 'S', 'T', 1, 0.00);
insert into adapter values (336, 'SysOut',                        'Adapter', 'S', 'T', 9, 0.00);
insert into adapter values (337, 'WebAlertAdapter',               'Adapter', 'S', 'T', 1, 0.00);
insert into adapter values (338, 'MongoCosmosDBWriter',           'Adapter', 'S', 'T', 1, 0.00);
insert into adapter values (339, 'LogWriter',                     'Adapter', 'S', 'T', 1, 0.00);
insert into adapter values (340, 'EmailAlert',                    'Adapter', 'S', 'T', 1, 0.00);

insert into adapter values (401, 'FileWriter',                    'Adapter', 'S', 'T', 1, 0.00);
insert into adapter values (402, 'DatabaseWriter',                'Adapter', 'S', 'T', 1, 0.00);

insert into adapter values (511, 'ApacheKafkaCluster',    'Storage Adapter', 'S', 'P', 9, 0.007);
insert into adapter values (512, 'ElasticsearchCluster',  'Storage Adapter', 'S', 'W', 9, 0.007);

insert into adapter values (601, 'PersistentStreams',             'Feature', 'S', 'F', 9, 0.10);
insert into adapter values (602, 'PartitionedStreams',            'Feature', 'S', 'F', 9, 0.00);
insert into adapter values (603, 'Windows',                       'Feature', 'S', 'F', 9, 0.00);
insert into adapter values (604, 'PartitionedWindows',            'Feature', 'S', 'F', 9, 0.15);
insert into adapter values (605, 'Router_Comp',                   'Feature', 'S', 'F', 9, 0.20);
insert into adapter values (606, 'Cache_Comp',                    'Feature', 'S', 'F', 9, 0.00);
insert into adapter values (607, 'External_Cache',                'Feature', 'S', 'F', 9, 0.20);
insert into adapter values (608, 'Waction_Store',                 'Feature', 'S', 'F', 9, 0.00);
insert into adapter values (609, 'OpenProcessor',                 'Feature', 'S', 'F', 9, 0.20);
insert into adapter values (610, 'FLM',                           'Feature', 'S', 'F', 9, 0.15);
insert into adapter values (611, 'MLFunctions',                   'Feature', 'S', 'F', 9, 0.00);
insert into adapter values (612, 'DataValidation',                'Feature', 'S', 'F', 9, 0.25);
insert into adapter values (613, 'Dash_Board',                    'Feature', 'S', 'F', 9, 0.00);
insert into adapter values (614, 'ApplicationGroups',             'Feature', 'S', 'F', 9, 0.00);
insert into adapter values (615, 'AlertManager',                  'Feature', 'S', 'F', 9, 0.00);
insert into adapter values (616, 'Mon_Timeseries_Report',         'Feature', 'S', 'F', 9, 0.00);
insert into adapter values (617, 'LEE_Report',                    'Feature', 'S', 'F', 9, 0.00);
insert into adapter values (618, 'Exception_Store',               'Feature', 'S', 'F', 9, 0.00);
insert into adapter values (619, 'BiDirectional',                 'Feature', 'S', 'F', 9, 0.50);
insert into adapter values (620, 'MetadataManager',               'Feature', 'S', 'F', 9, 0.00);
insert into adapter values (621, 'RestApiFunctions',              'Feature', 'S', 'F', 9, 0.00);
insert into adapter values (622, 'Event_Table',                   'Feature', 'S', 'F', 9, 0.20);

insert into adapter values (711, 'SmsMigrationReader',        'SMS Adapter', 'M', 'S', 9, 0.00);
insert into adapter values (712, 'SmsMigrationWriter',        'SMS Adapter', 'M', 'T', 9, 0.00);
insert into adapter values (713, 'SmsReplicationReader',      'SMS Adapter', 'R', 'S', 9, 0.00);
insert into adapter values (714, 'SmsReplicationWriter',      'SMS Adapter', 'R', 'T', 9, 0.00);

insert into adapter values (9999,'UnknownAdapter',                   'Item', 'U', 'U', 9, 0.00);

commit;
