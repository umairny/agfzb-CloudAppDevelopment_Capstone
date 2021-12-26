from cloudant.client import Cloudant
from cloudant.error import CloudantException
import requests

def main(dict):

    if dict["name"]:

        databaseName = "reviews"

        try:
            client = Cloudant.iam(
                account_name=dict["COUCH_USERNAME"],
                api_key=dict["IAM_API_KEY"],
                connect=True,
            )
            #print("Databases: {0}".format(client.all_dbs()))

            db = client[databaseName] 
            
            #add auto id fiild
            view = db.all_docs(include_docs=True) # returns all docs in the database
            total = view["total_rows"]
            id = total + 1

            # Create review document content data
            if dict["purchase"] == False:
                data = {
                    'id': id,
                    'name': dict["name"],
                    'dealership': dict["dealership"],
                    "review": dict["review"],
                    "purchase": dict["purchase"],
                    }
            else:
                data = {
                    'id': id,
                    'name': dict["name"],
                    'dealership': dict["dealership"],
                    "review": dict["review"],
                    "purchase": dict["purchase"],
                    "purchase_date": dict["purchase_date"],
                    "car_make": dict["car_make"],
                    "car_model": dict["car_model"],
                    "car_year": dict["car_year"]
                    }

            # Create a document using the Database API
            my_document = db.create_document(data)

            # Check that the document exists in the database
            if my_document.exists():
                print('SUCCESS!!')
                return({"status":200,"message": "Review added"})
    
        except CloudantException as ce:
            print("unable to connect")
            return {"error": ce}
        except (requests.exceptions.RequestException, ConnectionResetError) as err:
            print("connection error")
            return {"error": err}

    else:
        return {"status":500,"message":"Error: missing name"}