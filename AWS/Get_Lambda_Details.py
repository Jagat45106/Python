import boto3
import csv
import datetime

my_aws_profile = "ENTER_YOUR_PROFILE"
region = "ENTER_REGION_NAME"
session = boto3.Session(profile_name=my_aws_profile)
lambda_client = session.client("lambda", region_name=region)

#Get the latest log stream name
def get_latest_invocation_timestamp(function_name):
    logs_client = session.client('logs', region_name=region)
    log_group_name = f'/aws/lambda/{function_name}'

    try:
        response = logs_client.describe_log_streams(logGroupName=log_group_name, orderBy='LastEventTime', descending=True, limit=1)
        log_stream = response.get('logStreams', [])
        if not log_stream:
            return "No Log Stream"
        else:
            log_stream_name = response['logStreams'][0]['logStreamName']
            return log_stream_name
    except Exception as e:
        return "logGroup Not Found"

#Export the result to csv
def export_to_csv(functions_data):
    with open('lambda_functions.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Function Name', 'Runtime', 'Memory (MB)', 'Package Type', 'Last Modified', 'Latest Invocation'])
        for function_data in functions_data:
            writer.writerow(function_data)

#list all functions
def list_lambda_functions():
    functions_data = []
    paginator = lambda_client.get_paginator('list_functions')
    for page in paginator.paginate():
        function_list = page['Functions']
        for function in function_list:
            try:
                function_name = function['FunctionName']
                function_details = lambda_client.get_function(FunctionName=function_name)
                runtime = function_details['Configuration']['Runtime']
                memory = function_details['Configuration']['MemorySize']
                package_type = function_details['Configuration']['PackageType']
                last_modified_timestamp = function_details['Configuration']['LastModified']
                latest_invocation = get_latest_invocation_timestamp(function_name)
                functions_data.append([function_name, runtime, memory, package_type, last_modified_timestamp, latest_invocation])
            except Exception as e:
                functions_data.append([function_name, "not accessible"])
    return functions_data       
if __name__ == "__main__":
    functions_data = list_lambda_functions()
    export_to_csv(functions_data)
