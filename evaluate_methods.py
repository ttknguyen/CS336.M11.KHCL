import argparse
import os
import time
import pickle
import pdb

import numpy as np

import torch
from torch.utils.model_zoo import load_url
from torchvision import transforms

from cirtorch.networks.imageretrievalnet import init_network, extract_vectors
from cirtorch.datasets.testdataset import configdataset
from cirtorch.utils.download import download_train, download_test
from cirtorch.utils.evaluate import compute_map_and_print
from cirtorch.utils.general import get_data_root, htime

from cirtorch.networks.imageretrievalnet import extract_ss, extract_ms
from torch.utils.model_zoo import load_url
from torchvision import transforms
from tqdm import tqdm
import tensorflow_hub as hub
from Module.delf import feature_extraction, match_images, run_delf
from Module.cnnImageRetrievalPytorch import Searching, load_network
from Module.resnet_image_retrieval import load_model, feature_extraction_resnet, retrieval_resnet
import numpy as np
import cv2 as cv
import os, glob2
import tensorflow as tf


PRETRAINED = {
    'rSfM120k-tl-resnet50-gem-w'        : 'http://cmp.felk.cvut.cz/cnnimageretrieval/data/networks/retrieval-SfM-120k/rSfM120k-tl-resnet50-gem-w-97bf910.pth',
    'rSfM120k-tl-resnet101-gem-w'       : 'http://cmp.felk.cvut.cz/cnnimageretrieval/data/networks/retrieval-SfM-120k/rSfM120k-tl-resnet101-gem-w-a155e54.pth',
    'rSfM120k-tl-resnet152-gem-w'       : 'http://cmp.felk.cvut.cz/cnnimageretrieval/data/networks/retrieval-SfM-120k/rSfM120k-tl-resnet152-gem-w-f39cada.pth',
    'gl18-tl-resnet50-gem-w'            : 'http://cmp.felk.cvut.cz/cnnimageretrieval/data/networks/gl18/gl18-tl-resnet50-gem-w-83fdc30.pth',
    'gl18-tl-resnet101-gem-w'           : 'http://cmp.felk.cvut.cz/cnnimageretrieval/data/networks/gl18/gl18-tl-resnet101-gem-w-a4d43db.pth',
    'gl18-tl-resnet152-gem-w'           : 'http://cmp.felk.cvut.cz/cnnimageretrieval/data/networks/gl18/gl18-tl-resnet152-gem-w-21278d5.pth',
}

datasets_names = ['oxford5k', 'roxford5k']

parser = argparse.ArgumentParser(description='PyTorch CNN Image Retrieval Testing End-to-End')

# test options
parser.add_argument('--network', '-n', metavar='NETWORK',
                    help="network to be evaluated: " +
                        " | ".join(PRETRAINED.keys()))
parser.add_argument('--datasets', '-d', metavar='DATASETS', default='roxford5k',
                    help="comma separated list of test datasets: " + 
                        " | ".join(datasets_names) + 
                        " (default: 'roxford5k,rparis6k')")
parser.add_argument('--image-size', '-imsize', default=1024, type=int, metavar='N',
                    help="maximum size of longer image side used for testing (default: 1024)")
parser.add_argument('--multiscale', '-ms', metavar='MULTISCALE', default='[1]', 
                    help="use multiscale vectors for testing, " + 
                    " examples: '[1]' | '[1, 1/2**(1/2), 1/2]' | '[1, 2**(1/2), 1/2**(1/2)]' (default: '[1]')")

# GPU ID
parser.add_argument('--gpu-id', '-g', default='0', metavar='N',
                    help="gpu id used for testing (default: '0')")

def method_1(query_path, bbx, feature_corpus, images):
    net, transform, ms = load_network()
    net.cuda()
    net.eval()

    feature_query = extract_vectors(net, [query_path], 1024, transform, bbxs= [bbx], ms=ms)
    results = Searching(feature_query, feature_corpus, 20)
    final_results = [images.index(i[0]) for i in results]
    
    return final_results

def method_0(query_path, bbx, feature_corpus, model, images):
    image = cv.imread(query_path)
    image = image[int(bbx[1]):int(bbx[3]), int(bbx[0]):int(bbx[2])]
    
    feature_query = feature_extraction_resnet(model, image)
    results = retrieval_resnet(feature_query, feature_corpus, len(feature_corpus))
    final_results = [images.index(i[0]) for i in results]
    return final_results

def method_2(query_path, bbx, feature_corpus, delf, images):
    image = cv.imread(query_path)
    image = image[int(bbx[1]):int(bbx[3]), int(bbx[0]):int(bbx[2])]
    loc, des = feature_extraction(image)
    fq = {'locations': loc, 'descriptors': des}
    #[fq] = np.apply_along_axis(signature_bit,1,[fe],None)    

    results = {}
    with tf.device('/device:GPU:0'):
        for i in feature_corpus:
            f = {'locations': feature_corpus[i][0], 'descriptors': feature_corpus[i][1]}

            results[i] = match_images(fq, f)

        
    results = sorted(results.items(), key = lambda kv:(kv[1], kv[0]), reverse=True)
    final_results = [images.index(i[0]) for i in results]
    return final_results

def main():
    args = parser.parse_args()

    # check if there are unknown datasets
    for dataset in args.datasets.split(','):
        if dataset not in datasets_names:
            raise ValueError('Unsupported or unknown dataset: {}!'.format(dataset))

    # check if test dataset are downloaded
    # and download if they are not
    #download_train(get_data_root())
    download_test(get_data_root())

    # setting up the visible GPU
    os.environ['CUDA_VISIBLE_DEVICES'] = args.gpu_id

    # loading network
    # pretrained networks (downloaded automatically)
    print(">> Loading network:\n>>>> '{}'".format(args.network))
    state = load_url(PRETRAINED[args.network], model_dir=os.path.join(get_data_root(), 'networks'))
    # parsing net params from meta
    # architecture, pooling, mean, std required
    # the rest has default values, in case that is doesnt exist
    net_params = {}
    net_params['architecture'] = state['meta']['architecture']
    net_params['pooling'] = state['meta']['pooling']
    net_params['local_whitening'] = state['meta'].get('local_whitening', False)
    net_params['regional'] = state['meta'].get('regional', False)
    net_params['whitening'] = state['meta'].get('whitening', False)
    net_params['mean'] = state['meta']['mean']
    net_params['std'] = state['meta']['std']
    net_params['pretrained'] = False
    # network initialization
    net = init_network(net_params)
    net.load_state_dict(state['state_dict'])
        
    print(">>>> loaded network: ")
    print(net.meta_repr())

    # setting up the multi-scale parameters
    ms = list(eval(args.multiscale))
    print(">>>> Evaluating scales: {}".format(ms))

    # moving network to gpu and eval mode
    net.cuda()
    net.eval()

    # set up the transform
    normalize = transforms.Normalize(
        mean=net.meta['mean'],
        std=net.meta['std']
    )
    transform = transforms.Compose([
        transforms.ToTensor(),
        normalize
    ])

    # evaluate on test datasets
    datasets = args.datasets.split(',')
    for dataset in datasets: 
        if (dataset == 'oxford5k'):
          tmp = 47
        else:
          tmp = 48
        print('>> {}: Extracting...'.format(dataset))

        # prepare config structure for the test dataset
        cfg = configdataset(dataset, os.path.join(get_data_root(), 'test'))
        images = [cfg['im_fname'](cfg,i) for i in range(cfg['n'])]
        qimages = [cfg['qim_fname'](cfg,i) for i in range(cfg['nq'])]
        try:
            bbxs = [tuple(cfg['gnd'][i]['bbx']) for i in range(cfg['nq'])]
        except:
            bbxs = None  # for holidaysmanrot and copydays


        print("____EVALUATING METHOD 0____")
        path = '/content/CS336.M11.KHCL/data/'
        model = load_model('/content/CS336.M11.KHCL/data/networks/')
        fe = {}
        print(">> Loading features:")
        with tqdm(total=len(images)) as pbar:
            for img in images:
                fe[img] = np.load(path + 'feature_extraction_method_0/' + img[tmp:-3] + 'npy')
                pbar.update(1)

        ranks_0 = []
        print(">> Evaluating ...")
        with tqdm(total=len(qimages)) as pbar:
            for q in range(len(qimages)):
                score = method_0(qimages[q], bbxs[q], fe, model, images)
                ranks_0.append(score)
                pbar.update(1)
        ranks_0 = np.array(ranks_0)
        print("_____________________________________\n")


        print("____EVALUATING METHOD 1____")
        # extract database and query vectors
        print('>> {}: database images...'.format(dataset))
        vecs = extract_vectors(net, images, args.image_size, transform, ms=ms)
        print('>> {}: query images...'.format(dataset))
        qvecs = extract_vectors(net, qimages, args.image_size, transform, bbxs=bbxs, ms=ms)
        
        print('>> {}: Evaluating...'.format(dataset))
        print(vecs.shape, qvecs.shape)
        # convert to numpy
        vecs = vecs.numpy()
        qvecs = qvecs.numpy()
        
        # search, rank, and print
        scores = np.dot(vecs.T, qvecs)
        ranks_1 = np.argsort(-scores, axis=0)
        print("_____________________________________\n")
        
        print("____EVALUATING METHOD 2____")

        fe_2 = {}
        print(">> Loading features:")
        with tqdm(total=len(images)) as pbar:
            for img in images:
                loc = np.load(path + 'feature_extraction_method_2/' + img[tmp:-4] + '_loc.npy')
                des = np.load(path + 'feature_extraction_method_2/' + img[tmp:-4] + '_des.npy')
                fe_2[img] = [loc, des]
                pbar.update(1)
        ranks_2 = []
        delf = hub.load('https://tfhub.dev/google/delf/1').signatures['default']
        print(">> Evaluating ...")
        with tqdm(total=len(qimages)) as pbar:
            for q in range(len(qimages)):
                score = method_2(qimages[q], bbxs[q], fe_2, delf, images)
                ranks_2.append(score)
                pbar.update(1)
        ranks_2 = np.array(ranks_2)
        print("_____________________________________\n")

        print("\n\nResult Evaluate Method 0:")
        compute_map_and_print(dataset, ranks_0.T, cfg['gnd'])
        # print("Result Evaluate Method 1:")
        # compute_map_and_print(dataset, ranks_1.T, cfg['gnd'])
        print("Result Evaluate Method 2:")
        compute_map_and_print(dataset, ranks_2.T, cfg['gnd'])
        #print('>> {}: elapsed time: {}'.format(dataset, htime(time.time()-start)))

if __name__ == '__main__':
    main()