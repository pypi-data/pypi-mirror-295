import logging
import os

import boto3
from boto3.dynamodb.conditions import Attr
from botocore.config import Config


class Client:
    def __init__(self, table_name: str, index_name:str, extension: str|None=None, credentials: dict|None=None,
                 region: str='eu-central-1'):
        """
        Initialize the LedgerHelper class to assist with operations on a specified QLDB ledger.

        :param ledger_name: The name of the QLDB ledger.
        :param table_name: The name of the table within the ledger.
        :param index_name: The primary index name of the table.
        :param extension: Optional. Appends to the ledger name for testing, isolating branches by creating new tables without removing them post-tests.
        :param credentials: Optional. A dictionary containing AWS credentials (AccessKeyId, SecretAccessKey, SessionToken).
        :param region: Optional. The AWS region where the ledger is located, e.g., 'eu-central-1'.
        """

        self.index_name = index_name
        self.table_name = table_name
        self.dynamodb_client = None
        self.table = None
        try:
            branch_name = os.popen('git rev-parse --abbrev-ref HEAD').read().strip()
            if(branch_name != 'master'):
                extension = 'dev'
        except:
            pass
        if extension is not None:
            self.table_name = f'{table_name}-{extension}'

        
        else:
            logging.info("Production environment ledger active")

        if credentials is not None:
            self.dynamodb_client = boto3.client('dynamodb',
                                        aws_access_key_id=credentials['AccessKeyId'],
                                        aws_secret_access_key=credentials['SecretAccessKey'],
                                        aws_session_token=credentials['SessionToken'],
                                        config=Config(region_name=region))
        else:
            self.dynamodb_client = boto3.client("dynamodb", config=Config(region_name=region))

        try:
            if self.table_name not in self.dynamodb_client.list_tables()['TableNames']:
                self.initiate_table(table_name=self.table_name, index_name=self.index_name)

            self.table = boto3.resource('dynamodb', config=Config(region_name=region)).Table(self.table_name)
        except Exception as e:
            logging.warning(f'Error listing tables or creating a new table. '
                            f'Check the permissions of this role. This is expected behavior if you '
                            f'know that the table you want to access already exists '
                            f'and have restricted permissions. Exception message: {e}')

        logging.info(f"Table: {self.table_name}\nMain index: {self.index_name}\n")

    def initiate_table(self, table_name: str, index_name: str = 'id', attribute_type: str = 'S'):
        """
        Create a new table and a primary index within the ledger.

        :param table_name: The name of the table to be created.
        """
        self.dynamodb_client.create_table(
            TableName=table_name,
            KeySchema=[
                {
                    'AttributeName': index_name,
                    'KeyType': 'HASH' 
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': index_name,
                    'AttributeType': attribute_type
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            },
        )
        # Wait until the table is created
        self.dynamodb_client.get_waiter('table_exists').wait(TableName=table_name)


    def read_entry(self, conditions: list = None, column: str = '*', page: int = 1, page_size: int = 10):
        """
        Read entries from the table based on specified conditions, with pagination.
        :param conditions: A list of tuples specifying multiple conditions (AND/OR, column, value).
        :param column: The column(s) to retrieve. '*' retrieves all columns.
        :param page: The page number of the results to retrieve.
        :param page_size: The number of results per page.
        :return: The result of the query execution.
        """
        filter_expression = None
        if conditions:
            for i, (condition_type, col, val) in enumerate(conditions):
                new_condition = Attr(col).eq(val)
                if i == 0:
                    filter_expression = new_condition
                elif condition_type == "AND":
                    filter_expression &= new_condition
                elif condition_type == "OR":
                    filter_expression |= new_condition
        
        scan_params = {
            'FilterExpression': filter_expression if filter_expression else None,
            'ProjectionExpression': column if column != '*' else None,
            'Limit': page_size,
        }
        scan_params = {k: v for k, v in scan_params.items() if v is not None}
        response = self.table.scan(**scan_params)
        current_page = 1
        while 'LastEvaluatedKey' in response and current_page < page:
            current_page += 1
            scan_params['ExclusiveStartKey'] = response['LastEvaluatedKey']
            response = self.table.scan(**scan_params)
        if(current_page != page):
            return []
        
        return response.get('Items', [])

    def add_entry(self, data: dict):
        """
        Insert a new entry into the table.

        :param data: A dictionary representing the data to be inserted into the table.
        """
        self.table.put_item(Item=data)

    def modify_entry(self, data: dict, index: tuple = (None, None)):
        """
        Update an existing entry in the table based on the specified index.

        :param data: A dictionary representing the new data for the entry.
        :param index: A tuple specifying the index of the entry to be updated.
        """
        data = data.copy()
        if not index[0]:
            index = (self.index_name, data[self.index_name])
        pk_tuple = self.make_pk_tuple(index)
        del data[pk_tuple[0]]
            

        # Build the UpdateExpression and ExpressionAttributeValues
        update_expression = "SET "
        expression_attribute_values = {}
        expression_attribute_names = {}

        # Iterate over data dictionary to build the update statement
        for i, (key, value) in enumerate(data.items()):
            update_expression += f"#attr{i} = :val{i}, "
            expression_attribute_values[f":val{i}"] = value
            expression_attribute_names[f"#attr{i}"] = key

        # Remove the trailing comma and space from the update expression
        update_expression = update_expression.rstrip(", ")

        # Perform the update
        
        
        self.table.update_item(
            Key={
                pk_tuple[0]: pk_tuple[1]
            },
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values,
            ExpressionAttributeNames=expression_attribute_names,
            ReturnValues="UPDATED_NEW"
        )

    def make_pk_tuple(self, index: tuple):
        """
        Make a primary key tuple from the specified index.

        :param index: A tuple specifying the index of the entry.
        :return: A tuple containing the primary key and value.
        """

        describe_table_response = self.dynamodb_client.describe_table(TableName=self.table_name)
        
        pk = describe_table_response['Table']['KeySchema'][0]['AttributeName']
        items = self.read_entry([("AND", index[0], index[1])])
        if len(items) == 0:
            return None
        return (pk, items[0][pk])

    def remove_entry(self, data: tuple = None):
        """
         Remove an entry from the table based on the specified index.

         :param data: A tuple specifying the index of the entry to be removed.
         """
        pk_tuple = self.make_pk_tuple(data)
        self.table.delete_item(
            Key={
                pk_tuple[0]: pk_tuple[1]
            }
        )
    
    def add_index(self, index_name, attribute_type='S'):
        """
        Create a new index on the table.

        :param index_name: The name of the new index to be created.
        """
        self.table.update(
            AttributeDefinitions=[
                {
                    'AttributeName': 'SecondaryKey',
                    'AttributeType': attribute_type
                },
            ],
            GlobalSecondaryIndexUpdates=[
                {
                    'Create': {
                        'IndexName': index_name,
                        'KeySchema': [
                            {
                                'AttributeName': 'SecondaryKey',
                                'KeyType': 'HASH' 
                            }
                        ],
                        'Projection': {
                            'ProjectionType': 'ALL' 
                        },
                        'ProvisionedThroughput': {
                            'ReadCapacityUnits': 5,
                            'WriteCapacityUnits': 5
                        }
                    }
                }
            ]
        )

