FARIO_CMD_TEMPLATE = '''fario-out {} --links --limit={} | fario2json | jq '.[].data.linkBody.targetFid' | sed 's/"//g' '''
ATTRIBUTION_TEXT = 'code by @artlu99 2024-02-07'
SQLITE_DB = 'data/20240206_first20kFids_follows.db'
