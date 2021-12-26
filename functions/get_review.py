from cloudant.client import Cloudant
from cloudant.error import CloudantException
import requests

def main(dict):
    databaseName = "reviews"

    try:
        client = Cloudant.iam(
            account_name=dict["COUCH_USERNAME"],
            api_key=dict["IAM_API_KEY"],
            url=dict["COUCH_URL"],
            connect=True,
        )
        
        #Get the db by name
        db = client[databaseName]

        try:
            #selct the dealershipId where the review is lived
            selector = {'dealership': {'$eq': int(dict['dealerID'])}}
            #get the all review from seleted dealerID
            res = db.get_query_result(selector,raw_result=True,limit=100)
            #for remove warning in qurey and clear the data
            result = res["docs"]
        except:
            #Get all documents
            view = db.all_docs(include_docs=True) # returns all docs in the database
            result = view["rows"]

            

    except CloudantException as ce:
        print("unable to connect")
        return {"error": ce}
    except (requests.exceptions.RequestException, ConnectionResetError) as err:
        print("connection error")
        return {"error": err}

    return { "reviews": result }
 