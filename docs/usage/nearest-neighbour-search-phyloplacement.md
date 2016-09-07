#  Nearest neighbour search / phyloplacement


To run `atlas place` you'll first need to have run [`atlas genotype`](genotyping) on your sample. 



Then, insert the genotype output into your local atlas database:





	 atlas add-gt --db_name atlas_db genotype_out.json 
Then running place is as simple as running 

	 atlas place --db_name atlas_db :sample_id 
Output should looks something like:

	 {
	    "sample_id": {
	        "neighbours": {
	            "0": {
	                "7abf9701-1a11-4869-9e4b-297c10cd4ef7": {
	                    "distance": 0
	                }
	            },
	            "1": {
	                "8e8aa6db-175f-4078-9a14-692ace90b884": {
	                    "distance": 4
	                }
	            },
	            "2": {
	                "122768c5-55a4-4756-b0e6-9406548188d7": {
	                    "distance": 4
	                }
	            },
	            "3": {
	                "aa406f86-ca21-4644-a3ff-8041c86e295a": {
	                    "distance": 5
	                }
	            },
	            "4": {
	                "0c79e09a-4908-42bc-b48f-5b5af1f065ec": {
	                    "distance": 5
	                }
	            }
	        }
	    }
	} 
Where distance is the SNP distance of the query sample to the sample in the database.
