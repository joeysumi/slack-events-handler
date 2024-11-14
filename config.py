# Set where you would like the photo files to be stored - "s3" or "sftp"
SOURCE_CONNECTION = "s3"

# Path to credential JSON file within application
CREDENTIALS_PATH = "./app-credentials.json"

# Path to WordPress files gallery
GALLERY_PATH = "public_html/wp-content/gallery"

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
