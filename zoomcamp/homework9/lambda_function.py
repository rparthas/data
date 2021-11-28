from keras_image_helper import create_preprocessor
import tflite_runtime.interpreter as tflite

interpreter = tflite.Interpreter(model_path='cats-dogs-v2.tflite')
interpreter.allocate_tensors() 


def predict(x):
    input_index = interpreter.get_input_details()[0]['index']
    output_index = interpreter.get_output_details()[0]['index']
    interpreter.set_tensor(input_index, x) 
    interpreter.invoke() 
    return interpreter.get_tensor(output_index) 


def lambda_handler(event, context): 
    url = event['url'] 
    preprocessor = create_preprocessor('xception', target_size=(150, 150))
    x = preprocessor.from_url(url)
    pred = predict(x)
    return {"result":pred}