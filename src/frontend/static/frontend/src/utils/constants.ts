/** Accepted file types for a dataset. */
const ACCEPTED_FILE_TYPES: string = '.csv,.tsv,.txt'

/** Maximum file size to show a warning of possible slow upload. */
const MAX_FILE_SIZE_IN_MB_WARN: number = 25

/** Maximum file size to upload a file. */
const MAX_FILE_SIZE_IN_MB_ERROR: number = 50

/** Color used to fill some charts. */
const COLOR_YELLOW_FILL: string = '#a97f00'

/** Color used for strokes. Use it with `COLOR_YELLOW_FILL` constant. */
const COLOR_YELLOW_STROKE: string = '#a97f00'

export {
    ACCEPTED_FILE_TYPES,
    MAX_FILE_SIZE_IN_MB_WARN,
    MAX_FILE_SIZE_IN_MB_ERROR,
    COLOR_YELLOW_FILL,
    COLOR_YELLOW_STROKE
}
