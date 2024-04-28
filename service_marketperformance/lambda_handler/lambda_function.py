import json
import get_market_data as gmd


def lambda_handler(event, context):
    try:
        gmd.MarketStocksDetails().start_process()
        return {
            'statusCode': 200,
            'body': json.dumps("Successfully Updated Today's Market Metrics!")
        }
    except Exception as err:
        return {
            "Error message": err
        }
