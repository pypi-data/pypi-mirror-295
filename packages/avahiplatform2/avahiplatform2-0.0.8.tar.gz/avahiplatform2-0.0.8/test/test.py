# import avahiai
import avahiplatform

summarization_output = avahiplatform.summarize("summarize.txt")
# summarization_output = avahiplatform.summarize("s3://avahi-python-package-data/summarize.txt")
print(summarization_output[0])
