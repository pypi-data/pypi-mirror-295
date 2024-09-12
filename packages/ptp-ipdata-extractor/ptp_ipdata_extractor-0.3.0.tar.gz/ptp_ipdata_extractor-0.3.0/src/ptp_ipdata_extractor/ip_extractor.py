import json
import pandas as pd
import requests
from requests_kerberos import HTTPKerberosAuth, OPTIONAL

kerberos_auth = HTTPKerberosAuth(mutual_authentication=OPTIONAL)
IBI_DAAS_API = "https://ibi-daas.intel.com/daas/web/services/"


def query_ibi(service, command):
    """
    Query external data using the provided service and command, using Kerberos authentication.

    Args:
        service (str): The service to query.
        command (str): The command to execute.

    Returns:
        pd.DataFrame: Data retrieved from the external service as a pandas DataFrame.
    """
    url = f"{IBI_DAAS_API}{service}?command={command}"
    headers = {'Content-Type': 'application/json'}

    try:
        # Make the request using Kerberos authentication
        response = requests.get(url, headers=headers, auth=kerberos_auth, verify=False)

        # Check if the request was successful
        if response.status_code == 200:
            # Decode the response content using utf-8-sig to remove BOM
            content = response.content.decode('utf-8-sig')

            # Parse the JSON from the decoded content
            data = json.loads(content)

            # Extract the "Data" part and convert it to a pandas DataFrame
            data_list = data.get("Data", [])
            df = pd.DataFrame(data_list)

            return df
        else:
            raise Exception(f"Failed to retrieve data: {response.status_code} - {response.reason}")

    except json.JSONDecodeError:
        raise Exception('Failed to decode JSON from response')
    except requests.RequestException as e:
        raise Exception(f"Request failed: {str(e)}")


def get_available_ips_releases():
    """
    Retrieves a list of all available IPs in PTP Central.

    This function queries a user table to get all available IPs and returns them as a list.

    Returns:
        list: A list of all available IPs retrieved from the database. Returns an empty list
              if no IPs are found or if there is an issue with the query.

    Raises:
        Exception: If there is an issue with querying the database.
    """
    try:
        command = "SELECT distinct ip, release FROM V_PTP_CENTRAL_ALL_IPS_OFFICIAL_RELEASES"
        # Query the database using the predefined command
        result_df = query_ibi(service='sql', command=command)
        # Initialize an empty dictionary to store the IPs and their releases
        ip_releases_dict = {}
        # Group the data by 'IP' and aggregate the 'Release' values into a list
        grouped = result_df.groupby('ip')['release'].apply(list).to_dict()
        # Update the dictionary with the grouped data
        ip_releases_dict.update(grouped)
        return ip_releases_dict
    except Exception as error:
        print(f"Couldn't retrieve IP and release data, exception is: {error}")
        return {}


def get_ip_release_data(ip, release, **kwargs):
    """
    Fetches data from a database based on provided IP and release.
    If additional keyword arguments (`kwargs`) are provided, they are added as filtering conditions in the SQL query.

    Parameters:
    ip (str): The IP value for which data is being queried.
    release (str): The release version for which data is being queried.
    **kwargs: Optional additional keyword arguments to further filter the query.

    Returns:
    pandas.DataFrame: DataFrame containing the results of the query if not empty.
    If no valid IP and release are provided, or if the query fails, the function prints an appropriate message.

    Example usage:
    get_ip_release_data(ip="some_ip", release="v1.0")
    get_ip_release_data(ip="some_ip", release="v1.0", version="1.2", status="official")
    """

    if ip and release:
        # Base command for both cases (with or without kwargs)
        command = f"select * from V_PNP_IP_{ip} where release='{release}'"

        # If kwargs are provided, adding them to the SQL query as additional conditions
        if kwargs:
            for key, value in kwargs.items():
                command += f" and {key}='{value}'"

        try:
            # Execute the command
            ip_release_df = query_ibi(service='sql', command=command)

            # Return the DataFrame if it's not empty
            if ip_release_df.empty is False:
                return ip_release_df
        except Exception as error:
            print(f"Couldn't provide data for {ip} IP for this release - {release}, exception: {error}")
    else:
        print("No valid IP and Release were provided.")


def get_latest_data_per_ip(ip):
    """
       Retrieves the latest data for a specific IP from the database.

       This function queries a database view specific to the provided IP and retrieves all columns
       for the row with the most recent date.

       Args:
           ip (str): The IP identifier to query data for. The IP must be used to construct
                     the table/view name in the SQL query.

       Returns:
           pandas.DataFrame: A DataFrame containing the latest data for the given IP.
                             Returns an empty DataFrame if no data is found.

       Raises:
           Exception: If there is an issue with querying the database or if no data is found
                      for the given IP.
    """
    if ip:
        try:
            command = f"select * from V_PNP_IP_{ip} where date=(select max(date) from V_PNP_IP_{ip})"
            ip_release_df = query_ibi(service='sql', command=command)
            if ip_release_df.empty is False:
                return ip_release_df
        except Exception as error:
            print(f"Couldn't provide latest data for {ip} ip, exception is: {error}")
    else:
        print("No valid IP and Release were provided")


def get_ip_release_unique_params(ip, release, *args):
    """
    Fetches distinct data from a database based on provided IP and release.
    If additional columns (`args`) are provided, they will be included in the DISTINCT clause of the SQL query.

    Parameters:
    ip (str): The IP value for which data is being queried.
    release (str): The release version for which data is being queried.
    *args: Optional column names to apply DISTINCT to in the query.

    Returns:
    pandas.DataFrame: DataFrame containing the results of the query if not empty.
    If no valid IP and release are provided, or if the query fails, the function prints an appropriate message.

    Example usage:
    get_ip_release_unique_params(ip="some_ip", release="v1.0", "column1", "column2")
    """

    if ip and release:
        # Start building the base SQL command
        if args:
            # Include only specified columns in DISTINCT
            distinct_columns = ', '.join(args)
            command = f"select distinct {distinct_columns} from V_PNP_IP_{ip} where release='{release}'"
        else:
            # Default to selecting all columns with DISTINCT
            command = f"select distinct * from V_PNP_IP_{ip} where release='{release}'"

        try:
            # Execute the SQL query
            ip_release_df = query_ibi(service='sql', command=command)

            # Return the DataFrame if it's not empty
            if ip_release_df.empty is False:
                return ip_release_df
        except Exception as error:
            print(f"Couldn't provide data for {ip} IP for this release - {release}, exception: {error}")
    else:
        print("No valid IP and Release were provided.")
