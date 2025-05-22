
# Global variables for window slicing and sliding window

#Size of each sample window
WINDOW_SIZE = 100

# How many frames should we slide each sample for the sliding window procedure.
WINDOW_SLIDE = 10

# How many times should we slide to create samples on each side of the window
# Total number of slices will be  2*WINDOW_SAMPLE_AMOUNT + 1
WINDOW_SAMPLE_AMOUNT = 3

# Parameter for running mean filter
RUNNING_MEAN_PARAM = 10

ESP_NUMBER = 3

TIME_CAP = 0.5

TIME_SIZE = 1

TIME_TOLERANCE = 0.5

VALID_MAC = {
    "0C:8B:95:A5:7B:08",
    "0C:8B:95:A5:70:FC",
    "0C:8B:95:A5:72:64"
}
