import os.path
import tensorflow as tf
import helper
import warnings
from distutils.version import LooseVersion
import project_tests as tests
from tqdm import *

# Check TensorFlow Version
assert LooseVersion(tf.__version__) >= LooseVersion('1.0'), 'Please use TensorFlow version 1.0 or newer.  You are using {}'.format(tf.__version__)
print('TensorFlow Version: {}'.format(tf.__version__))

# Check for a GPU
if not tf.test.gpu_device_name():
    warnings.warn('No GPU found. Please use a GPU to train your neural network.')
else:
    print('Default GPU Device: {}'.format(tf.test.gpu_device_name()))


def load_vgg(sess, vgg_path):
    """
    Load Pretrained VGG Model into TensorFlow.
    :param sess: TensorFlow Session
    :param vgg_path: Path to vgg folder, containing "variables/" and "saved_model.pb"
    :return: Tuple of Tensors from VGG model (image_input, keep_prob, layer3_out, layer4_out, layer7_out)
    """
    #   Use tf.saved_model.loader.load to load the model and weights
    vgg_tag = 'vgg16'
    tf.saved_model.loader.load(sess, [vgg_tag], vgg_path)
    
    vgg_input_tensor_name = 'image_input:0'
    vgg_keep_prob_tensor_name = 'keep_prob:0'
    vgg_layer3_out_tensor_name = 'layer3_out:0'
    vgg_layer4_out_tensor_name = 'layer4_out:0'
    vgg_layer7_out_tensor_name = 'layer7_out:0'
    
    graph = tf.get_default_graph()
    
    input_image = graph.get_tensor_by_name(vgg_input_tensor_name)
    keep_prob = graph.get_tensor_by_name(vgg_keep_prob_tensor_name)
    layer3 = graph.get_tensor_by_name(vgg_layer3_out_tensor_name)
    layer4 = graph.get_tensor_by_name(vgg_layer4_out_tensor_name)
    layer7 = graph.get_tensor_by_name(vgg_layer7_out_tensor_name)
    
    return input_image, keep_prob, layer3, layer4, layer7

#tests.test_load_vgg(load_vgg, tf)

def layers(vgg_layer3_out, vgg_layer4_out, vgg_layer7_out, num_classes):
    """
    Create the layers for a fully convolutional network.  Build skip-layers using the vgg layers.
    :param vgg_layer7_out: TF Tensor for VGG Layer 3 output
    :param vgg_layer4_out: TF Tensor for VGG Layer 4 output
    :param vgg_layer3_out: TF Tensor for VGG Layer 7 output
    :param num_classes: Number of classes to classify
    :return: The Tensor for the last layer of output
    """
    # TODO: Let's make it FCN 8
    
    regularizer = tf.contrib.layers.l2_regularizer(1e-3)
    initializer = tf.truncated_normal_initializer(stddev= 0.01)
    
    conv1x1_7th = tf.layers.conv2d(vgg_layer7_out, num_classes, 1, strides=(1,1), padding="same", kernel_initializer=initializer, kernel_regularizer=regularizer, name="conv1x1_7th")
    
    skip_7 = tf.layers.conv2d_transpose(conv1x1_7th, num_classes, 8, strides=(4,4), padding="same", kernel_initializer=initializer, kernel_regularizer=regularizer, name="skip_7")
    
    conv1x1_4th = tf.layers.conv2d(vgg_layer4_out, num_classes, 1, strides=(1,1), padding="same", kernel_initializer=initializer, kernel_regularizer=regularizer, name="conv1x1_4th")
    
    skip_4 = tf.layers.conv2d_transpose(conv1x1_4th, num_classes, 2, strides=(2,2), padding="same", kernel_initializer=initializer, kernel_regularizer=regularizer, name="skip_4")
    
    added_7_4 = tf.add(skip_4, skip_7, name="added_7_4")
    
    conv1x1_3rd = tf.layers.conv2d(vgg_layer3_out, num_classes, 1, strides=(1,1), padding="same", kernel_initializer=initializer, kernel_regularizer=regularizer, name="conv1x1_3rd")
    
    sum = tf.add(added_7_4, conv1x1_3rd, name="output")
    
    output = tf.layers.conv2d_transpose(sum, num_classes, 16, strides=(8,8), padding="same", kernel_initializer=initializer, kernel_regularizer=regularizer, name="output")
    
    return output

#tests.test_layers(layers)

def optimize(nn_last_layer, correct_label, learning_rate, num_classes):
    """
    Build the TensorFLow loss and optimizer operations.
    :param nn_last_layer: TF Tensor of the last layer in the neural network
    :param correct_label: TF Placeholder for the correct label image
    :param learning_rate: TF Placeholder for the learning rate
    :param num_classes: Number of classes to classify
    :return: Tuple of (logits, train_op, cross_entropy_loss)
    """
    # TODO: Implement function
    
    logits = tf.reshape(nn_last_layer, (-1, num_classes))
    labels = tf.reshape(correct_label, (-1, num_classes))
    print ("Labels shape: ", labels.shape)
    cross_entropy_loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=logits, labels=labels))
    
    optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate)
    
    train_op = optimizer.minimize(cross_entropy_loss)
    
    return logits, train_op, cross_entropy_loss

#tests.test_optimize(optimize)

def train_nn(sess, epochs, batch_size, get_batches_fn, train_op, cross_entropy_loss, input_image, correct_label, keep_prob, learning_rate):
    """
    Train neural network and print out the loss during training.
    :param sess: TF Session
    :param epochs: Number of epochs
    :param batch_size: Batch size
    :param get_batches_fn: Function to get batches of training data.  Call using get_batches_fn(batch_size)
    :param train_op: TF Operation to train the neural network
    :param cross_entropy_loss: TF Tensor for the amount of loss
    :param input_image: TF Placeholder for input images
    :param correct_label: TF Placeholder for label images
    :param keep_prob: TF Placeholder for dropout keep probability
    :param learning_rate: TF Placeholder for learning rate
    """
    print ("Training...")
    # TODO: Implement function
    sess.run(tf.global_variables_initializer())
    for epoch in tqdm(range(epochs)):
        for images, labels in get_batches_fn(batch_size):
            #print ("label batches: ", labels.shape, " images batch: ", images.shape)
            train, loss = sess.run([train_op, cross_entropy_loss], feed_dict={input_image: images, correct_label: labels, keep_prob: 0.7})
            print ("Loss: ", loss)

#tests.test_train_nn(train_nn)

def run():
    num_classes = 2
    image_shape = (160, 576)
    data_dir = './data'
    runs_dir = './runs'
    tests.test_for_kitti_dataset(data_dir)
    epochs = 20
    batch_size = 12
    learning_rate = 0.001
    
    # Download pretrained vgg model
    helper.maybe_download_pretrained_vgg(data_dir)

    #saver = tf.train.Saver()
    
    correct_label = tf.placeholder(tf.float32, shape=[None, image_shape[0], image_shape[1], num_classes])

    with tf.Session() as sess:
        # Path to vgg model
        vgg_path = os.path.join(data_dir, 'vgg')
        
        # Create function to get batches
        get_batches_fn = helper.gen_batch_function(os.path.join(data_dir, 'data_road/training'), image_shape)
       
        # TODO: Build NN using load_vgg, layers, and optimize function
        input_image, keep_prob, layer3, layer4, layer7 = load_vgg(sess, vgg_path)
        
        model_output = layers(layer3, layer4, layer7, num_classes)
        
        logits, train_op, cross_entropy_loss = optimize(model_output, correct_label, learning_rate, num_classes)
        #print ("Logits shape: ", logits.shape)
        # TODO: Train NN using the train_nn function
        train_nn(sess, epochs, batch_size, get_batches_fn, train_op, cross_entropy_loss, input_image, correct_label, keep_prob, learning_rate)
        
        #saver.save(sess, 'model1.ckpt')
        #print ("Model saved: 'model1.ckpt'")
        
        # TODO: Save inference data using helper.save_inference_samples
        helper.save_inference_samples(runs_dir, data_dir, sess, image_shape, logits, keep_prob, input_image)

        # OPTIONAL: Apply the trained model to a video


if __name__ == '__main__':
    run()
