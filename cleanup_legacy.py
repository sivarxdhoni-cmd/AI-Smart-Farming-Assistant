
from vector_store import get_collection


def cleanup_legacy_records():

    collection = get_collection()

    data = collection.get(
        include=["metadatas"]
    )

    ids = data["ids"]
    metadatas = data["metadatas"]

    legacy_records = []
    new_records = []

    for record_id, metadata in zip(ids, metadatas):

        if record_id.startswith("agri_chunk_"):
            legacy_records.append((record_id, metadata))
        else:
            new_records.append((record_id, metadata))

    print("Legacy records:", len(legacy_records))
    print("New records:", len(new_records))

    # Safety check: expected six old and six new records
    if len(legacy_records) != 6 or len(new_records) != 6:
        print("Cleanup cancelled: Unexpected record count!")
        return

    # Verify every old chunk has a matching new chunk
    new_pairs = {
        (
            metadata.get("source"),
            metadata.get("chunk_index")
        )
        for _, metadata in new_records
    }

    for _, metadata in legacy_records:

        pair = (
            metadata.get("source"),
            metadata.get("chunk_index")
        )

        if pair not in new_pairs:
            print("Cleanup cancelled: Matching new record missing!")
            return

    # Delete only verified legacy records
    old_ids = [
        record_id
        for record_id, _ in legacy_records
    ]

    collection.delete(ids=old_ids)

    print("\nLegacy records removed successfully!")
    print("Remaining vectors:", collection.count())


if __name__ == "__main__":
    cleanup_legacy_records()

