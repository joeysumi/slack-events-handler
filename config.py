# Set where you would like the photo files to be stored - "s3" or "sftp"
SOURCE_CONNECTION = "s3"

# Path to credential JSON file within application
CREDENTIALS_PATH = "./app-credentials.json"

# Set to False if you want to include images sent in Slack message threads (replies)
EXCLUDE_THREADED_IMAGES = True

# Path to WordPress files gallery
GALLERY_PATH = None  # an example would be "public_html/wp-content/gallery" - to keep it in the base bucket put `None`

# Acceptable image file formats to look for in Slack Event
ACCEPTABLE_FILE_FORMATS = [
    "avif",
    "gif",
    "heic",
    "heif",
    "jpeg",
    "jpg",
    "jpeg2000",
    "png",
    "raw",
    "svg",
    "tiff",
]
