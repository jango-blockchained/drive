import frappe
import pycrdt
import base64
from datetime import datetime


def execute():
    import frappe
    import pycrdt
    import base64
    from datetime import datetime

    files = frappe.get_all(
        "Drive File", filters={"document": ("!=", "")}, fields=["name", "document"]
    )
    yjs_map = {k["name"]: frappe.get_doc("Drive Document", k["document"]).content for k in files}

    for name, yjs_data in yjs_map.items():
        drive_file = frappe.get_doc("Drive File", name)
        try:
            uint8_bytes = base64.b64decode(yjs_data)

            doc = pycrdt.Doc()
            doc.apply_update(uint8_bytes)
            annotations = doc.get("docAnnotations", type=pycrdt.Array)
            MAP = {}
            for annotation in annotations:
                name = annotation.get("id")
                content = annotation.get("content")
                owner = annotation.get("ownerEmail")
                created_at = datetime.fromtimestamp(annotation.get("createdAt", 0) / 1000)

                comment = frappe.get_doc(
                    {
                        "doctype": "Drive Comment",
                        "name": name,
                        "content": content,
                    }
                )
                drive_file.append("comments", comment)
                comment.insert(ignore_permissions=True)
                drive_file.save(ignore_permissions=True)
                MAP[name] = (owner, created_at)

                replies = annotation.get("replies")
                for reply in replies:
                    content = reply.get("content")
                    owner = reply.get("ownerEmail")
                    created_at = datetime.fromtimestamp(reply.get("createdAt", 0) / 1000)
                    reply_doc = frappe.get_doc(
                        {
                            "doctype": "Drive Comment",
                            "content": content,
                        }
                    )
                    comment.append("replies", reply_doc)
                    reply_doc.insert(ignore_permissions=True)
                    MAP[reply_doc.name] = (owner, created_at)
                comment.save(ignore_permissions=True)

            # Separate to avoid DB write conflicts
            for name, (owner, created_at) in MAP.items():
                frappe.db.set_value("Drive Comment", name, "owner", owner)
                frappe.db.set_value("Drive Comment", name, "creation", created_at)
        except Exception as e:
            print("ERROR", e)
            frappe.log_error(f"Error processing Yjs content: {e}")

        doc = frappe.get_doc("Drive Document", drive_file.document)
        if "data-annotation-id" in doc.raw_content:
            doc.raw_content = doc.raw_content.replace("data-annotation-id", "data-comment-id")
            doc.save()
