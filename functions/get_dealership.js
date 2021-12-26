const Cloudant = require('@cloudant/cloudant'); 

async function main(params) { 
    //Connect to db
     const cloudant = Cloudant({ 
         url: params.COUCH_URL, 
         plugins: { iamauth: { iamApiKey: params.IAM_API_KEY } } 
     }); 

    try { 
        let dbList = await cloudant.db.use("dealerships"); 
        let res=""
        if (params.dealerID) {
            res = await dbList.find({ "selector": { "id": parseInt(params.dealerID) } })
            return { "dealership": res.docs }; 
        }
        else if (params.state) {
            //console.log(params.state)
            res = await dbList.find({ "selector": { "st" : params.state } })
            return { "dealership": res.docs }; 
        }

        else {
        res = await dbList.list({include_docs: true});
        return { "dealership": res }; 
        }
     } catch (error) { 
         return { error: error.description }; 
     } 
}