import tensorflow as tf
import numpy as np
import os
import logging

# Suppress TensorFlow logs
logging.getLogger('tensorflow').setLevel(logging.ERROR)  # Hide all but errors

# Disable oneDNN optimizations to avoid further logs
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
# 0: All logs (default)
# 1: Filter out INFO logs
# 2: Filter out INFO and WARNING logs
# 3: Filter out all logs except errors

def clsfr(inputs,val_true,lrn_rt,steps):
    inputs = inputs.astype(np.float32)
    val_true = val_true.astype(np.float32)
    val_true = val_true.reshape(val_true.shape[0],1)
    # inputs - only hold the features no output 
    # val_true - only hold the outputs no features
    dim = [inputs.shape[1],val_true.shape[1]]
    # dim[0] ~ dimension of input , dim[1] ~ dimension of output

    # w ~ weights of dim_ input.shape[1]{no of features} X 1
    w = tf.Variable(initial_value = tf.random.uniform(shape=(dim[0],1)))
    # b ~ biases of dim_ 1 X 1
    b = tf.Variable(initial_value = tf.zeros(shape = (dim[1],1)))

    # input{2000 X 2}.weight{2 X 1} ~ 2000 x 2 + {1x1} - this happens due to broadcasting
    def model(inputs):
        return tf.matmul(inputs,w)+b
    
    #cost = (val_true - val_pred)**2/(2000{inputs.shape[0]})
    def cost(val_true,val_pred):
        sqred_loss = tf.square(val_true-val_pred)
        return tf.reduce_mean(sqred_loss)
    
    alpha = lrn_rt
    def train( val_true,inputs):
        with tf.GradientTape() as tape:
            val_pred = model(inputs)
            cost_grd = cost(val_true,val_pred)
        loss_wrt_w,loss_wrt_b = tape.gradient(cost_grd,[w,b])
        w.assign_sub(loss_wrt_w*alpha)
        b.assign_sub(loss_wrt_b*alpha)
        return cost_grd
    
    # print('hello beautiful')
    # for step in range(1,steps*10):
    #     loss = train(val_true,inputs)
    #     if(step%((step*10)/10)==0):
    #         print(f'Loss[{step}]:{loss}')

    if steps <= 10:
        step_interval = 1
    else:
        # Divide into 10 equal intervals
        step_interval = steps // 10
    
    printed_steps = 0  # Count the number of printed steps

    for step in range(0, steps + 1, step_interval):
        loss = train(val_true,inputs)
        if printed_steps < 10:
            print(f'Loss[{step}]:{loss}')
            printed_steps += 1

    # If we didn't hit exactly 10 steps (due to rounding), print the final step
    if printed_steps < 10 and step != steps:
        print(f'Loss[{step}]:{loss}')
        # Ensure the last step is always printed

    val_pred = model(inputs)
    return val_pred,w,b

def dataset_1(sample_size):
    positive = np.random.multivariate_normal(
    mean = [3,0],
    cov = [[1,0.5],[0.5,1]],
    size = sample_size )

    negative = np.random.multivariate_normal(
    mean = [0,3],
    cov = [[1,0.5],[0.5,1]],
    size = sample_size )

    inputs = np.vstack((negative,positive))
    val_true = np.vstack((np.zeros((sample_size, 1), dtype='float32'),
                    np.ones((sample_size,1),dtype='float32')))
    
    return inputs,val_true

def dataset_2(num):
    if(num == 1): # AND OPERATION
        test_inputs = np.array([[0,0], [0,1], [1,0], [1,1]])
        test_val_true = np.array([0, 0, 0, 1]) 
        return(test_inputs,test_val_true)
    
    elif(num == 2): # OR OPERATION
        test_inputs = np.array([[0,0], [0,1], [1,0], [1,1]])
        test_val_true = np.array([0, 1, 1, 1]) 
        return(test_inputs,test_val_true)
    
    elif(num == 3): # XOR OPERATION
        test_inputs = np.array([[0,0], [0,1], [1,0], [1,1]])
        test_val_true = np.array([0, 1, 1, 0]) 
        return(test_inputs,test_val_true)
    
    elif(num == 4): # XNOR OPERATION
        test_inputs = np.array([[0,0], [0,1], [1,0], [1,1]])
        test_val_true = np.array([1, 0, 0, 1]) 
        return(test_inputs,test_val_true)
    
    else: # AND OPERATION
        test_inputs = np.array([[0,0], [0,1], [1,0], [1,1]])
        test_val_true = np.array([0, 0, 0, 1]) 
        return(test_inputs,test_val_true)
    
    