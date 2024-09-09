col_width = {
    "requestId": 50,
    "externalIdPrefix": 15,
    "processStatus": 33,
    "failedPpAndShipmentTags": 19,
    "totalTestedTags": 12,
    "passedTags": 9,
    "failedOfflineTags": 13,
    "yield": 8,
    "First Tag": 10,
    "Last Tag": 9,
    "tagId": 31,
    "comment": 43,
    "status": 11,
    'serializationStatus': 20,
    'corruptedStatus': 18,
    'duplicationsStatus': 18,
    'sampleTestStatus': 18,
    'reelName': 18,
    "otherIssuesStatus": 18
}

FULL_COLUMNS = ['requestId', 'processStatus', 'externalIdPrefix', 'reelName', 'totalTestedTags', 'passedTags',
                      'failedOfflineTags', 'yield', 'failedPpAndShipmentTags', 'failedSerializationQty', 'serializationStatus',
                      'corruptedTagsQty', 'corruptedStatus', 'duplicationsQty', 'duplicationsStatus', "otherIssuesQty", 'otherIssuesStatus', 'numOfCommonRunNames', 'commonRunNames',
                      'firstExternalId', 'lastExternalId', 'sampleTestCommonRunName', 'sampleTestTesterStationName', 'sampleTestTestedTags',
                        'sampleTestPassedTags', 'sampleTestRespondedTags', 'sampleTestFailBinStr', 'sampleTestTbpAvg', 'sampleTestStatus', 'uploadedAt']

DISPLAY_COLS = ['requestId', 'externalIdPrefix', 'processStatus', 'yield', 'serializationStatus', 'corruptedStatus', 'duplicationsStatus', 'otherIssuesStatus', 'sampleTestStatus']