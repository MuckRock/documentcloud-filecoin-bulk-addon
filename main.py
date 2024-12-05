""" 
DocumentCloud Add-On that allows you to upload documents
to the IPFS/Filecoin networks in batches """
import math
from itertools import islice

from documentcloud.addon import AddOn

FILECOIN_ID = 104


class FilecoinBulkUpload(AddOn):
    """
    Splits docs into 25 doc batches and uploads the new batch to filecoin
    """

    def main(self):
        """Retrieves our vars from config.yaml, searches for not uploaded docs,
        and uploads them
        """
        proj = self.data["project_id"]
        batch_sz = self.data["batch_size"]
        batch_num = math.ceil(batch_sz / 25)
        print(batch_sz)
        # Search for all documents in the current project that have not yet been uploaded.
        documents = self.client.documents.search(f"+project:{proj} -data_ipfsUrl:*")
        for i in range(batch_num):
            # Pull out the IDs for a batch of the documents
            doc_ids = [
                d.id for d in islice(documents, i * batch_sz, (i + 1) * batch_sz)
            ]
            # Run the Filecoin Add-On for this batch of documents
            self.client.post(
                "addon_runs/",
                json={
                    "addon": FILECOIN_ID,
                    "parameters": {},
                    "documents": doc_ids,
                    "dismissed": True,
                },
            )


if __name__ == "__main__":
    FilecoinBulkUpload().main()
