-- Striim Metadata repository creation script (Postgres)

-- Install Postgres 9.6 version
-- Connect to postgres database
-- Run the two commands below as specified

-- a. CREATE USER striim WITH PASSWORD 'striim';
-- b. CREATE DATABASE striimdb;
-- c. GRANT CREATE ON DATABASE striimdb TO striim;
-- ( Connect to striimdb database using striim user )
-- d. create schema striim;
-- e. ALTER ROLE striim SET search_path TO striim;
-- Run Striim/conf/DefineMetadataReposPostgres.sql on postgres schema created abov

-- create table holding version number. update it with EVERY release
create table webaction_version (
                            version varchar(20) not null constraint version_pk primary key );
insert into webaction_version values ('4.1.0.1');

-- create the global UUID to URL mapping table
-- objid is the primary key
-- name can be null, for anonymous objects
-- schema id can be null for schema object
-- Type - 1 - Schema, 2 - Type, 3 - Stream, 4 - Window, 5 - CQ,  6 - Source, 7 - Target, 8 - Flow, 9 - Property Set, 10 - Wactionstore, 11 - Property Template,
-- 12 - Cache
create table WactionObject( objectid varchar(100) not null constraint objid_pk primary key,
                            metaObjectClass varchar(1024),
                            uri varchar(256) not null constraint uri_uk unique,
                            name varchar(256),
                            namespaceId varchar(100),
                            nsName varchar(256),
                            owner varchar(256),
                            version varchar(256),
                            type varchar(256),
                            CreationTime varchar(256),
                            description varchar(4096),
                            sourceText TEXT,
                            metaInfoStatus varchar(1024),
                            reverseIndexObjectDependencies TEXT,
                            coDependentObjects TEXT);



-- schema table for namespaces
create table WactionSchema( objectid varchar(100) not null constraint schid_pk primary key);

-- pre populate the wactionobject for the global schema;
begin;
insert into WactionObject values (
                            '01e2c3ec-e7fc-0e51-b069-28cfe9165d2d',
                            'com.webaction.runtime.meta.MetaInfo$Namespace',
                            'GLOBAL:NAMESPACE:GLOBAL:1',
                            'Global',
                            '01e2c3ec-e7fc-0e51-b069-28cfe9165d2d',
                            'Global',
                            '0',
                            '1',
                            '22',
                            '1369343304629',
                            'Global Namespace',
                            NULL,
                            '{"anonymous":false,"class":"com.webaction.runtime.meta.MetaInfoStatus","dropped":false,"valid":true}',
                            NULL,
                            NULL);

insert into WactionSchema values ('01e2c3ec-e7fc-0e51-b069-28cfe9165d2d');
commit;

-- Type Table
create table WactionType (  objectid varchar(100) not null constraint tid_pk primary key,
                            generated varchar(1000),
                            typeAlias varchar(256),
                            classname varchar(256),
                            classId integer,
                            extendstype varchar(100),
                            extendedby TEXT,
                            keyfields TEXT,
                            fields TEXT,
                            fieldAlias TEXT);

-- Stream Table
create table WactionStream (objectid varchar(100) not null constraint strmid_pk primary key,
                            TypeId varchar(100) not null,
                            PartitionExpressions TEXT,
                            PartitionKeyFactory bytea,
                            gracePeriodInterval varchar(100),
                            gracePeriodField varchar(100),
                            propertyset TEXT,
                            avroSchema TEXT);

-- Stream Generator Table
create table WactionStreamGen (
                            objectid varchar(100) not null constraint strmgenid_pk primary key,
                            TypeId varchar(100) not null,
                            className varchar(1024),
                            args bytea);

-- Window Table
create table WactionWindow (objectid varchar(100) not null constraint wid_pk primary key,
                            jumping varchar(1000),
                            persistent varchar(1000),
                            strmid varchar(100) not null,
                            partitionfields varchar(1024),
                            intervalpolicy varchar(1024),
                            slidepolicy varchar(1024),
                            implicit varchar(1000));

-- CQ Table
create table WactionCQ (    objectid varchar(100) not null constraint cqid_pk primary key,
                            strmid varchar(100),
                            plan TEXT,
                            slcttxt TEXT,
                            fieldList TEXT,
                            uiConfig TEXT,
                            isAdHocQuery varchar(1000));

-- Open Processor Table
create table WactionOpenProcessor (
                            objectid varchar(100) not null constraint pcid_pk primary key,
                            strmid varchar(100),
                            dataSources TEXT,
                            loadedProcess bytea,
                            properties TEXT,
                            moduleName varchar(1000),
                            scmFile varchar(4096),
                            enrichmentComponent varchar(1024));

-- Property Template Table - Holds Properties for various readers
create table WactionPropTemplate(
                            objectid varchar(100) not null constraint ptid_pk primary key,
                            properties TEXT,
                            className varchar(256),
                            adaptertype varchar(256),
                            type varchar(256),
                            inputClassName varchar(256),
                            outputClassName varchar(256),
                            requiresParser varchar(1000),
                            requiresFormatter varchar(1000),
                            adapterVersion varchar(24),
                            isParallelizable varchar(1000));

-- Properties Table - Properties that have changed from the template
create table WactionPropset(objectid varchar(100) not null constraint prid_pk primary key,
                            properties TEXT);

-- Property Variable Table
create table WactionPropVariable(
                            objectid varchar(100) not null constraint pri_pk primary key,
                            properties TEXT);

-- Source Table
create table WactionSource( objectid varchar(100) not null constraint srcid_pk primary key,
                            adapterclassname varchar(256),
                            outputstream varchar(256),
                            outputClauses TEXT,
                            properties TEXT,
                            parserProperties TEXT);

-- Target Table
create table WactionTarget( objectid varchar(100) not null constraint tgtid_pk primary key,
                            adapterclassname varchar(256),
                            inputstream varchar(256),
                            properties TEXT,
                            formatterProperties TEXT,
                            parallelismProperties TEXT);

-- Group Table
create table WactionGroup(  objectid varchar(100) not null constraint grpid_pk primary key,
                            applications TEXT,
                            collapsed varchar(1000),
                            orderNumber int);

-- Flow Table
create table WactionFlow(   objectid varchar(100) not null constraint flwid_pk primary key,
                            objects TEXT,
                            deploymentPlan TEXT,
                            recoveryType integer,
                            recoveryPeriod bigint,
                            encrypted varchar(1000),
                            flowStatus INTEGER,
                            importStatements TEXT,
                            ehandlers TEXT,
                            dataValidation varchar(1000),
                            dataValidationInterval bigint,
                            exceptionstoreName varchar(256),
                            autoResumeCount integer,
                            autoResumeInterval bigint,
                            enableAutoResume varchar(1000),
                            loadBalanceDesiredStatus INTEGER,
                            loadLevel INTEGER);

-- Deployment Group Table
create table WactionDG(     objectid varchar(100) not null constraint dgid_pk primary key,
                            configuredMembers TEXT,
                            minimumRequiredServers integer,
                            maxApps integer);

-- Cache Table
create table WactionCache(  objectid varchar(100) not null constraint cachid_pk primary key,
                            adapterclassname varchar(256),
                            reader_properties TEXT,
                            parser_properties TEXT,
                            query_properties TEXT,
                            typename varchar(256),
                            retType varchar(256));

-- External Cache Table
create table WactionExternalCache(
                            objectid varchar(100) not null constraint extcachid_pk primary key,
                            adapterclassname varchar(256),
                            reader_properties TEXT,
                            query_properties TEXT,
                            external_properties TEXT,
                            external_cache_properties TEXT,
                            typename varchar(256),
                            retType varchar(256));

-- WactionStore Table
create table WactionStore(  objectid varchar(100) not null constraint viewid_pk primary key,
                            contextType varchar(100),
                            frequency varchar(50),
                            eventTypes varchar(1024),
                            eventKeys varchar(1024),
                            properties TEXT,
                            wactionstoretype varchar(16),
                            isExceptionstore varchar(1000));

-- Waction Store View Table
create table WAStoreView(   objectid varchar(100) not null constraint wstid_pk primary key,
                            wastoreID varchar(100),
                            intervalpolicy varchar(1024),
                            isJumping varchar(1000),
                            subscribeToUpdates varchar(1000),
                            query bytea);

-- Users Table
create table Users(         objectid varchar(100) not null constraint user_pk primary key,
                            userId varchar(256),
                            firstName varchar(256),
                            lastName varchar(256),
                            mainEmail varchar(256),
                            password varchar(2048),
                            alias varchar(256),
                            CONTACTS TEXT,
                            permissions TEXT,
                            roles TEXT,
                            DEFAULTNAMESPACE varchar(256),
                            ldap varchar(64),
                            originType varchar(32),
                            usertimezone varchar(256) );

-- Roles Table
create table Roles(         objectid varchar(100) not null constraint role_pk primary key,
                            domain varchar(256),
                            rolename varchar(256),
                            permissions TEXT,
                            roles TEXT,
                            originType varchar(32));

-- Visualization Table
create table visualization( objectid varchar(100) not null constraint visual_pk primary key,
                            fname varchar(256),
                            visName varchar(100),
                            json TEXT );

-- ExceptionHandler Table
create table exceptionhandler(
                            objectid varchar(100) not null constraint exceptionhandler_pk primary key,
                            exceptions varchar(2048),
                            components varchar(2048),
                            cmd varchar(20),
                            properties TEXT );

-- StriimCheckpoints
create table StriimCheckpoints(
                            id integer not null constraint striim_checkpoints_pk primary key,
                            appUuid varchar(512),
                            appUri varchar(512),
                            checkpointTimestamp bigint,
                            properties varchar(512),
                            description varchar(512),
                            format char,
                            checkpoint TEXT,
                            updated timestamp);

-- AppCheckpoint Table - deprecated
create table AppCheckpoint( id integer not null constraint checkpoint_pk primary key,
                            flowUuid varchar(255),
                            pathItems varchar(4096),
                            lowSourcePosition TEXT,
                            highSourcePosition TEXT,
                            atOrAfter varchar(1000),
                            updated timestamp);

create unique index AppCheckpointIndex on AppCheckpoint (flowuuid, pathitems);

-- PendingAppCheckpoint Table - deprecated
create table PendingAppCheckpoint(
                            id integer not null constraint pending_checkpoint_pk primary key,
                            flowUuid varchar(255),
                            pathItems varchar(4096),
                            lowSourcePosition TEXT,
                            highSourcePosition TEXT,
                            atOrAfter varchar(1000),
                            commandTimestamp bigint,
                            updated timestamp);

create index PendingAppCheckpointIndex on PendingAppCheckpoint (flowUuid);

-- AppCheckpointSummary Table - deprecated
create table AppCheckpointSummary(
                            id integer not null constraint checkpointsummary_pk primary key,
                            flowUri varchar(512),
                            componentUri varchar(512),
                            sourceUri varchar(512),
                            lowSourcePosition TEXT,
                            lowSourcePositionText varchar(512),
                            highSourcePosition TEXT,
                            highSourcePositionText varchar(512),
                            atOrAfter varchar(1000),
                            nodeUri varchar(255),
                            updated timestamp);

-- PendingAppCheckpointSummary Table - deprecated
create table PendingAppCheckpointSummary(
                            id integer not null constraint pending_checkpointsummary_pk primary key,
                            flowUri varchar(512),
                            componentUri varchar(512),
                            sourceUri varchar(512),
                            lowSourcePosition TEXT,
                            lowSourcePositionText varchar(512),
                            highSourcePosition TEXT,
                            highSourcePositionText varchar(512),
                            atOrAfter varchar(1000),
                            commandTimestamp bigint,
                            nodeUri varchar(255),
                            updated timestamp);

-- AppCheckpointHistory Table - deprecated
create table AppCheckpointHistory(
                            id integer not null constraint checkpointhistory_pk primary key,
                            applicationName varchar(512),
                            sourcePositionSummary TEXT,
                            targetPositionSummary TEXT,
                            checkpointType varchar(100),
                            checkpointRecordedTime timestamp);

-- Router Table
create table WactionRouter (
                            objectid varchar(100) not null constraint router_pk primary key,
							inStream varchar(100),
							StreamType varchar(100),
							forwardingRules bytea,
							ExprProcessor bytea);

-- Sorter Table
create table WactionSorter (objectid varchar(100) not null constraint sorter_pk primary key,
                            errorStream varchar(100),
                            sortTimeInterval varchar(100),
                            inOutRules bytea);

-- Dashboard Table
create table Dashboard(     objectid varchar(100) not null constraint dashboard_pk primary key,
                            title varchar(256),
                            pages TEXT,
                            defaultLandingPage varchar(256));

-- Page Table
create table Page(          objectid varchar(100) not null constraint page_pk primary key,
                            title varchar(256),
                            gridJSON TEXT,
                            queryVisualizations TEXT);

-- Query Visualization Table
create table QueryVisualization(
                            objectid varchar(100) not null constraint queryVisualization_pk primary key,
                            title varchar(256),
                            visualizationType varchar(256),
                            query TEXT,
                            config TEXT);

-- Query Table
create table Query(         objectid varchar(100) not null constraint query_pk primary key,
                            adhocQuery varchar(1000),
                            appUUID varchar(255),
                            cqUUID varchar(255),
                            streamUUID varchar(255),
                            queryDefinition varchar(4096),
                            queryParameters varchar(4096),
                            projectionFields TEXT,
                            typeInfo TEXT,
                            bindParameters TEXT);

-- CDC Metadata Extension
-- Any changes in DDL are stored here, has nothing to do with meta objects
create table CDCMetadata(   typeUUID varchar(100) not null constraint typeUUID_pk primary key,
                            tableMetadata TEXT,
                            parentComponent varchar(4096),
                            dictBeginOffset bigint,
                            dictEndOffset bigint,
                            tableName varchar(100),
                            DDLcommand varchar(4096));

-- Generic CDC Metadata Extension
-- Table to store the changes (type/schema) for the DDL commands. This is a generic one
-- in contract to the one for oracle source databases only (CDCMetadata).
create table GenericCDCMetadata(
                            tupleId varchar(100) not null constraint genTupId_pk primary key,
                            uri varchar(100),
                            tupleType int,
                            creationTime timestamp,
                            tableTypeUUID varchar(100) not null,
                            sourceURI varchar(4096),
                            tableName varchar(100),
                            ddlCommand varchar(4096),
                            sourcePosition TEXT,
                            sourcePositionString varchar(4096),
                            tableMetadata bytea,
                            version varchar(256));

create index GenericCDCMetadataIndex on GenericCDCMetadata (sourceURI, tableName);

create table TestCDCMetadata(
                            tupleId varchar(100) not null constraint testTupId_pk primary key,
                            uri varchar(100),
                            tupleType int,
                            creationTime bigint,
                            tableTypeUUID varchar(100) not null,
                            sourceURI varchar(4096),
                            tableName varchar(100) );

-- File Metadata Table
create table FileMetadata(  uniqueKeyUUID varchar(100) not null constraint uuid_pk primary key,
                            parentComponentUUID varchar(100) not null,
                            fileName varchar(1000) not null,
                            status varchar(100) not null,
                            type varchar(256),
                            parentComponent varchar(500) not null,
                            distributionID varchar(500),
                            directoryName varchar(4096),
                            creationTimeStamp bigint,
                            rollOverTimeStamp bigint,
                            reasonForRollOver varchar(100),
                            lastEventCheckPointValue TEXT,
                            sequenceNumber bigint,
                            field1 varchar(100),
                            field2 varchar(100),
                            wrapNumber bigint,
                            numberOfEvents bigint,
                            owner varchar(100),
                            firstEventPosition varchar(100),
                            lastEventPosition varchar(100),
                            firstEventTimestamp bigint,
                            lastEventTimestamp bigint,
                            externalFileCreationTime bigint);

create table OracleLineageMetadata(
                            uniqueKeyUUID varchar(100) not null constraint lineage_pk primary key,
                            threadId varchar(100),
                            firstChangeNumber varchar(100),
                            lastChangeNumber varchar(100));

create table WactionSysAlertRule(
                            objectid varchar(100) not null constraint alert_pk primary key,
                            comparator varchar(20),
                            eventType varchar(20),
                            alertValue varchar(100),
                            alertInterval varchar(100),
                            alertMessage varchar(1000),
                            alertType varchar(20),
                            isEnabled varchar(1000),
                            toAddress varchar(255),
                            objectName varchar(255));

-- create JMSAckCheckpoint table
create table jmsackcheckpoint(
                            checkpointkey varchar(500) not null constraint jms_cpkey_pk primary key,
                            uuid varchar(500),
                            checkpointoffset bigint);

-- create DDLHistory table
create table DDLHistory(uniqueKeyUUID varchar(100) not null constraint ddlhistory_pk primary key,
							fullyqualifiedcomponentname varchar(500) not null,
                            componenttype varchar(100) not null,
                            sourceobjectname varchar(500),
                            targetobjectname varchar(500),
                            ddlPosition bytea,
                            cddlaction varchar(50) not null,
                            status varchar(50),
                            activitytimestamp bigint not null,
                            sourceddlStatement TEXT,
                            targetddlStatement TEXT);
--TODO can we create a index here for the DDLHistory table ?

-- Striim Security Table
create table StriimSecurityTable(
                            objectid varchar(100) not null constraint securityidpk primary key,
                            salt bytea,
                            securityalgorithm varchar(100),
                            securevalue varchar(1000));

-- User Jars Table
create table UserJars(      uuid varchar(100) not null constraint userid_pk primary key,
                            fileName varchar(500),
                            loadedProcess bytea,
                            fileContent bytea,
                            type int);

create table WactionLicense(objectid varchar(100) not null constraint licenseidpk primary key, productTier int, addOnDisabledFeatureList TEXT, addOnEnabledFeatureList TEXT, defaultFeatureList TEXT, notApplicableFeatureList TEXT, isCurrentLicense varchar(1000));

create table WactionVault(
                            objectid varchar(100) not null constraint vault_pk primary key,
                            implementationType int,
                            properties TEXT);

create table StriimVaultContents(
                            vaultUUID varchar(100) not null,
                            vaultKey varchar(100) not null,
                            encryptedValue TEXT,
                            valueType int,
                            constraint vaultcontents_pk primary key (vaultUUID, vaultKey));

-- Load Rebalance Info Table
create table StriimLoadBalanceInfoTable(
                            objectid varchar(100) not null constraint lbinfoid_pk primary key,
                            status integer,
                            policyType integer,
                            startTime bigint,
                            endTime bigint,
                            minCPUUsage real,
                            maxCPUUsage real,
                            oldCheckpointProtection bigint,
                            appBounceProtection bigint,
                            scheduleInADay varchar(20),
                            appUnderLoadBalance TEXT,
                            exceptionApps TEXT,
                            policyConfigs TEXT);
commit;
