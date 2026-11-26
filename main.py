"""
DocumentCloud Add-On that allows you to upload documents
to the IPFS/Filecoin networks in batches """
from itertools import islice

from documentcloud.addon import AddOn

FILECOIN_ID = 104
BATCH_SIZE = 50


class FilecoinBulkUpload(AddOn):
    """Sends up to 50 not-yet-uploaded docs to the Push to IPFS Add-On"""

    def main(self):
        """Searches for not-yet-uploaded docs in the project and uploads one batch"""
        self.client.session.headers.update({'User-Agent': 'IPFS Batch Uploader Add-On'})
        proj = self.data["project_id"]
        # Search for all documents in the current project that have not yet been uploaded
        documents = self.client.documents.search(f"+project:{proj} -data_ipfsUrl:* +status:success")

        doc_ids = []
        for doc in islice(documents, BATCH_SIZE):
            doc_ids.append(doc.id)

        if not doc_ids:
            self.set_message("No documents left to upload in this project.")
            return

        # Run the Push to IPFS Add-On for this batch of documents
        self.client.post(
            "addon_runs/",
            json={
                "addon": FILECOIN_ID,
                "parameters": {},
                "documents": doc_ids,
                "dismissed": True,
            },
        )
        self.set_message(f"Sent {len(doc_ids)} documents to Push to IPFS.")


if __name__ == "__main__":
    FilecoinBulkUpload().main()
