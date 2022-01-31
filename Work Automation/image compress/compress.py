import tinify
import os

source_dir = os.path.abspath(r'D:\My Drive\Business\Website\Pages\Product Gallery')

imgs_in_source = [i for i in os.listdir(source_dir) if os.path.splitext(i)[1] == '.jpg']
output_dir = os.path.abspath(r'D:\My Drive\Business\Website\Pages\Product Gallery\resized2')
try:
    tinify.key = "Khw8D60W5YtvJ53HlF8S5XYrBfW17QTW"

    for file in imgs_in_source:
        print('Working on {}'.format(file))

        source = tinify.from_file(os.path.join(source_dir, file))
        resized = source.resize(
            method="fit",
            width=1000,
            height=1000
        )

        resized.to_file(os.path.join(output_dir, os.path.splitext(file)[0] + '_resized' + ".jpg"))
        print('{} is done'.format(file))

except tinify.AccountError as e:
    print("The error message is: {}".format(e))
    # Verify your API key and account limit.
except tinify.ClientError as e:
    # Check your source image and request options.
    print("The error message is: {}".format(e))
except tinify.ServerError as e:
    # Temporary issue with the Tinify API.
    print("The error message is: {}".format(e))
except tinify.ConnectionError as e:
    # A network connection error occurred.
    print("The error message is: {}".format(e))
except Exception as e:
    # Something else went wrong, unrelated to the Tinify API.
    print("The error message is: {}".format(e))