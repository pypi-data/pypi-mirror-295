from tf_image_processing.utils import io, plot
from tf_image_processing.processing import combination

image_1_path = "./image-processing-package/image_processing/Sample/image_1.jpg"
image_2_path= "./image-processing-package/image_processing/Sample/image_2.jpg"


image_1 = io.read_image(image_1_path)
image_2 = io.read_image(image_2_path)

#plot.plot_image(image_1)
#plot.plot_image(image_2)

result_image = combination.transfer_histogram(image_1, image_2)

plot.plot_result(image_1, image_2, result_image)

plot.plot_image(result_image)

result_img_path = "./image-processing-package/result_image.jpg"
io.save_image(result_image, result_img_path)
