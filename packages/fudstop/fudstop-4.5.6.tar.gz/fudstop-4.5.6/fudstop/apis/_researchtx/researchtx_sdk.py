from imps import *

import os
from dotenv import load_dotenv
load_dotenv()
import requests
case_id = os.environ.get('divorce_case_id')


class ResearchTexasSDK:
    def __init__(self):
        pass


    async def get_filings(self,id:str=case_id, page_size:int=50, search_text:str='', headers:str={'Cookie': 'FedAuth=77u/PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0idXRmLTgiPz48U2VjdXJpdHlDb250ZXh0VG9rZW4gcDE6SWQ9Il9kYTE0NjU0Zi00NzgxLTQ0MTItODJmYS05YjA2OGE3M2M3NTAtRkY2Q0IxNUI0MEI4ODQ0NkNFRTlFN0NEMTRGRUY0RDQiIHhtbG5zOnAxPSJodHRwOi8vZG9jcy5vYXNpcy1vcGVuLm9yZy93c3MvMjAwNC8wMS9vYXNpcy0yMDA0MDEtd3NzLXdzc2VjdXJpdHktdXRpbGl0eS0xLjAueHNkIiB4bWxucz0iaHR0cDovL2RvY3Mub2FzaXMtb3Blbi5vcmcvd3Mtc3gvd3Mtc2VjdXJlY29udmVyc2F0aW9uLzIwMDUxMiI+PElkZW50aWZpZXI+dXJuOnV1aWQ6MDQ2MGMyNTQtYTYxZC00ZWFjLWFhMzQtOTVmMGY1YWViOGE0PC9JZGVudGlmaWVyPjxDb29raWUgeG1sbnM9Imh0dHA6Ly9zY2hlbWFzLm1pY3Jvc29mdC5jb20vd3MvMjAwNi8wNS9zZWN1cml0eSI+dXZhaSt4NW15YkdDUDlnV0tPYnh1S3lrQkV1MHVEcFRpTzVETDhVSTQ3VkFSb3piYjR4UzNhUU9CR2JGNk9XdHc3L2Z4NmxQUnBTNmZGVXdLR3phUjZXRjd5QzRVVDJNOHg2OHIrYzNia3Uyb3I0OENxVk51aFRRdktBbHY1QWVnWTB1STBxaUI3d1JZOTQ4eFlLQkwwZHBLVFFtY0JYbENyc1ZVT29GOHBIb29vOWgvMTZSQVF3bFFMbTAwYTZpQnk3bDViQ2xlVWxWb0g3TjNUUlg4L1UzQ2ZMbGRUMjhrbkR1MjdGdlRjZTNiODJBQ1VYVTJRcHczR3JZMXVZendPSmk3eFRBd1NUWGI0V1UxVXB3RDFxOFphL3FhMWRpYkNHcFJsWTVIUHJCckY0YjZOWUVjK0JGWWZoQ1JnQXkxbFh5T0YxSXJKb2ZTN0pJSjVjT2Yvd0dNMGxFOHlVRG42bjNUc0dWWGVJcmJVTlA2QWIwWDQyQlQwR2hOQXl5Vm5MZXRScXIxTlNYQWllMHhvSm5PNHZLdzZrcjRTY0ZzNU42emxraVJtUUVycUVYcTNRdmdPSWdxYXhWeXdWQjI5YXdFTVB5T3VqVVlhTXRkWW5VaXFnUTFWaFRCd1lsbEh4SlMzSlRtTDdCeWJtNDk1RzhadDZtQUNqcmVSNGpncVNlaW9BZ3VuckxyeDBFRDZjOVRELzQ2LzgwMTRmMzc4YjdnSlMra2VTNlRMMGlyZStzMkxIZG1JSDgyWGk4RG9YMTBqZ081aEdoM25QeEFUajdLWGpicWd3WklHN04zZUdTamtpcFdUVkxGK0F5d0pueDNhWC85UlgxSXpzdUJGNGlaWHJoMEZBc0ZUczJjeEoyc3l0Rkk3ZWFLQUU5ZHdja1owUThHeHRGaElqWWpSdUlSdmhKU0NmbVUvVjJVY3Z5V25yTlJHUkRnQTM3N3NHSFFzU0ZpZWRoaDFYU0Y3WWNOWnV3Y0g0NlZKZmFobjc2MmJ2d0dXaVI5N2tmSnhFR2VYRGZ3dmRyT1VNRGQvMnVvN2UrMy9RVzZWMVVTUVlxWGxwSUFqUmtOSFR2RHRKNVFZZXZKN1BTbTVRSFpaSTZnSnpYM0RFMG5kZEkwNXZjQjFYeFdXUHBaMlFrbEkxNXIrZm5mVkt2emxleXR5VXgwRjJQVDZ1L2s2a1BVOW1aNHJMUGhUYmFUQk1lcTQ5ZUNJbDRpY2ZpQlBqSkFqZ0JMVHNUZEpFM255WThaSGNXSmV2bmZ6eDB5MVlDMnZXTE9qa2hoN3VNZjJQdkZkaUNmQUgwQWdjZCtDb0RDdFVOa3dKYXcrU3hXS0JJaW9CMWQ5bmdROHgvYmNTWmRBZkVqK3o3TERkYWwzN21vVTloN0tIZm13eE82TTcxR0Yv; FedAuth1=NkhKSEpkZzBRV28xTTFLSkxrZzFvSTJnZ0FWY05FS2J2b0tOTmxPL2dNWnY4NkJnbloweWNuWTlINFVSZGJMSm5kamFUb3Z4ZStweXRqRDhDaVZZWlg1cDhSKzFlSUFrTW5keHlIRDVLbml2SzdFa0Yrb2tGS3RuYVhHZTh3bU1IZ2pJdk8vTGhvZGxaZldsMDRsTUo0NGJvZHZOVk5BYk9KTERhcmNzQzhaZkFCQ2F6ektVTjdHMlpscFRDNDlNcGJjaGs4TUQ2ZGpnRiszejRRNmVkNlpVTncrRC9nVFhidld4NjZPUER2VUN3TlE2U2RUYmoxbEUxZFRrc1ZkWXBZSTg4MVpqUjhIbmVPYU8xU21xWld5UCtQTlUvcUpWOXk0SmJyUjZmbzhNcld5cENyTkpZSjJNUHRPWVNCK3FtZjhwYzdEckc0TTE3bHVaUVRSbmRsdmkzRFFqSkd2TlhBSjk5SnMreEEwVkFyN25Tam9Pamk0bzJCbnZ3N1R1YWp0ZWVrUkZtSU5CMzNYYWZmWkRWejhkd3NZS1RvUFg5TUFDZFUyT3ZBSURZTGtYZXp0RUU1K25WR25qSWJxRlNMYXluUEhzY2x6dE5RSmZPYkNxTXkwelU2Y0prODRTTXZ5U3pjcVpQMHA1TnRtY0g4WWphdDJRSmtjRjN5QU4xNmFFWHYxK3RrTWhCT3RpWGMvYlJsZklUMlFSdTRCMmpRMk4wWFVjblNzZFJQZTdpdlF5THF5bVBwdGJVZ1BieXVOWUMyTElMQVJTUDA0UlZyYWZHSS95cEpVRlNkT1d6Z3MvMU1PVGk2NnZIZnBCT1pwUm9WVXU1bmZHYkYwVTFnMkRaMyt4WkU3dGxDUmVGNUt3eHYxMUUxS3RNVTRadDdGTXk0MVdrdzc2blBvYi9TMnc5MTNOK2hMbFRqY3NqZ0JiNHA1djhWYXdDTDZWWTdoYWNpQjRjMXF5cVJRMlIxVUVjNkpobjhndURjc2FXdTlHalNUbGIrRFhvd2hyZ21sYms3OE15WGtkTUdCa0lnelRvVm44VVNhdTEzZTFYK0FyQ0k0QTZZZXBiZmVuV0s3bDlNMnpTdVBOSjVWMWpFYTB4TnRUR2YrVUlNd3FUU0dQZXk2VTFHRGJkUkd2SXRtaG55by9jeWRQcXY0SXNjWlRqT0ZRSnc5T09NZ01lNXl3a29Jaz08L0Nvb2tpZT48L1NlY3VyaXR5Q29udGV4dFRva2VuPg==; _hjSessionUser_1494715=eyJpZCI6IjRiNDYyMDc4LWEwMzUtNTZjZC1hMmMzLTJlMDcyNmZhYWU0NCIsImNyZWF0ZWQiOjE3MDk2NjYxNjMxNDcsImV4aXN0aW5nIjp0cnVlfQ==; __gsas=ID=4d516d6f5ca38367:T=1713325951:RT=1713325951:S=ALNI_MbaDUUAw7SbrtebYA5FiAK5aHGtdQ; __utma=211709392.1976371284.1708528145.1718817048.1720068146.24; __utmz=211709392.1720068146.24.20.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); IdSvr.WsFedTracking=DIG7ZnoatysHiBCz4ZCmIdcLAcuvWYnR-B3jBnRLP0I9JZSLkLtDCLI7sl3YDI1xyw1U8fbS233UeZzzZ6M3l8Q52LIbBkXyG00kV03qykhiUuA7k8ztSPBr40Ed_mZTZa7Kxf_VknVhG7vo7YtMrLccMJNXAf67pbfesJ0aPkcbZ6v6jjaGZKZ09cqkUgFuAFw7IAse7qDwUiRUHheG6oDZ8iQe78NPwTiPwkXo9AgLM2ynknpV1VJco_abThEiPzHypSxTvwnk_57sYIyw3J7xTrVcr5f0HrW6EVvib_w; logged_in=true; idle_timer=2024-08-20T23:41:20.624Z'}):
        """Get case filings"""
        url = f"https://research.txcourts.gov/CourtRecordsSearch/case/{id}/filings"
        
        r = requests.post(url=url, data={"pageSize":page_size,"pageIndex":0,"sortNewestToOldest":False,"searchText":search_text,"isSearchAll":True,"eventType":0}, headers=headers)
        print(r)
        if r.status_code == 200:
            r = r.json()
            
            events = r.get('events')

            filingID = [i.get('filingID') for i in events]
            filingCode = [i.get('filingCode') for i in events]
            description = [i.get('description') for i in events]
            submitted = [i.get('submitted') for i in events]
            submitterFullName = [i.get('submitterFullName') for i in events]
            docketed = [i.get('docketed') for i in events]
            isHiddenFromPublic = [i.get('isHiddenFromPublic') for i in events]
            hasManualSecurityOverride = [i.get('hasManualSecurityOverride') for i in events]
            jurisdiction = [i.get('jurisdiction') for i in events]
            jurisdictionKey = [i.get('jurisdictionKey') for i in events]
            externalKey = [i.get('externalKey') for i in events]
            ofsFilingID = [i.get('ofsFilingID') for i in events]
            hasNoReportedDocuments = [i.get('hasNoReportedDocuments') for i in events]
            case = [i.get('case') for i in events]
            hasHiddenDocument = [i.get('hasHiddenDocument') for i in events]
            hasNoDocument = [i.get('hasNoDocument') for i in events]
            eventType = [i.get('eventType') for i in events]
            documentIndexNumber = [i.get('documentIndexNumber') for i in events]
            type = [i.get('type') for i in events]
            highlights = [i.get('highlights') for i in events]

            documents = [i.get('documents') for i in events]

            flat_docs = [item for sublist in documents for item in sublist]

            documentID = [i.get('documentID') for i in flat_docs]
            documentKey = [i.get('documentKey') for i in flat_docs]
            documentCategoryCode = [i.get('documentCategoryCode') for i in flat_docs]
            documentSecurityCode = [i.get('documentSecurityCode') for i in flat_docs]
            fileName = [i.get('fileName') for i in flat_docs]
            fileSize = [i.get('fileSize') for i in flat_docs]
            pageCount = [i.get('pageCount') for i in flat_docs]
            description = [i.get('description') for i in flat_docs]
            isSecured = [i.get('isSecured') for i in flat_docs]
            isHiddenFromPublic = [i.get('isHiddenFromPublic') for i in flat_docs]
            isSealed = [i.get('isSealed') for i in flat_docs]
            hasManualSecurityOverride = [i.get('hasManualSecurityOverride') for i in flat_docs]
            documentStatus = [i.get('documentStatus') for i in flat_docs]
            isDocumentOnDemand = [i.get('isDocumentOnDemand') for i in flat_docs]
            externalSource = [i.get('externalSource') for i in flat_docs]
            externalKey = [i.get('externalKey') for i in flat_docs]
            jurisdictionKey = [i.get('jurisdictionKey') for i in flat_docs]
            isOwned = [i.get('isOwned') for i in flat_docs]
            isFree = [i.get('isFree') for i in flat_docs]
            isPrivileged = [i.get('isPrivileged') for i in flat_docs]
            price = [i.get('price') for i in flat_docs]
            priceKey = [i.get('priceKey') for i in flat_docs]
            isInCart = [i.get('isInCart') for i in flat_docs]
            expires = [i.get('expires') for i in flat_docs]
            filingId = [i.get('filingId') for i in flat_docs]
            isRedactedVersionAvailable = [i.get('isRedactedVersionAvailable') for i in flat_docs]


            data_dict = {
                'filing_code': filingCode,
                'description': description,
                'submitted': submitted,
                'submitter_full_name': submitterFullName,
                'docketed': docketed,
                'jurisdiction': jurisdiction,
                'jurisdiction_key': jurisdictionKey,
                'external_key': externalKey,
                'ofs_filing_id': ofsFilingID,
                'event_type': eventType,
                'document_index_number': documentIndexNumber,
                'highlights': highlights,
                'document_id': documentID,
                'document_key': documentKey,
                'document_category_code': documentCategoryCode,
                'document_security_code': documentSecurityCode,
                'file_name': fileName,
                'file_size': fileSize,
                'page_count': pageCount,
                'document_status': documentStatus,
                'external_source': externalSource,
                'price': price,
                'price_key': priceKey,
                'is_in_cart': isInCart,
                'expires': expires,
                'filing_id': filingId,
                'is_redacted_version_available': isRedactedVersionAvailable
            }
                        # Find the maximum length
            max_length = max(len(lst) for lst in data_dict.values())

            # Ensure all lists are of the same length by padding shorter lists with None
            for key in data_dict:
                if len(data_dict[key]) < max_length:
                    data_dict[key].extend([None] * (max_length - len(data_dict[key])))
            df = pd.DataFrame(data_dict)

            df.to_csv('filings_divorce.csv')


            return df