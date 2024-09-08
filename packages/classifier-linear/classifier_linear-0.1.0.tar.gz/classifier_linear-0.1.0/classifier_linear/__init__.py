import tensorflow as tf
import numpy as np
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
    
    for step in range(steps):
        loss = train(val_true,inputs)
        if(step%10 == 0):
            print(f'Loss[{step}]:{loss}')

    val_pred = model(inputs)
    return val_pred,w,b