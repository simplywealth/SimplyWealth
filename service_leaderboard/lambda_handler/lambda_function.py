import json
import update_leaderboard as ul


def lambda_handler(event, context):
    try:
        ul.LeaderBoard().main()
        return {
            'statusCode': 200,
            'body': json.dumps('Finished Updating Leaderboard for this week!')
        }
    except Exception as err:
        return {
            "Error message": err
        }
