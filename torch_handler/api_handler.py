from abc import ABC
import json
import logging
import os

import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer

from Language_Model.model import GPTmodel
from transformers import PreTrainedTokenizerFast
#from ts.torch_handler.base_handler import BaseHandler

logger = logging.getLogger(__name__)


#torch-model-archiver --model-name chatter-kogpt2 --version 1.0 --model-file Language_Model/model.py
#--serialized-file Language_Model kogpt2-wellnesee-auto-regressive1.pth --handler torch_handler/api_handler.py
#torchserve --start --ncs --model-store model_store --models densenet161.mar
#docker run --rm -it --gpus all -p 8080:8080 -p 8081:8081 -p 8082:8082 -p 7070:7070 -p 7071:
#7071 --name mar -v $(pwd)/workspace:/home/model-server/workspace -v $(pwd)/serve/model-store:/home/model-server/model-
#store -v $(pwd)/serve/examples:/home/model-server/examples pytorch/torchserve:latest-gpu

class TransformersClassifierHandler(BaseHandler, ABC):
    """
    Transformers text classifier handler class. This handler takes a text (string) and
    as input and returns the classification text based on the serialized transformers checkpoint.
    """
    def __init__(self):
        super(TransformersClassifierHandler, self).__init__()
        self.initialized = False

    def initialize(self, ctx):
        self.manifest = ctx.manifest

        properties = ctx.system_properties
        model_dir = properties.get("model_dir")

        # Read the mapping file, index to object name
        #mapping_file_path = os.path.join(model_dir, "index_to_name.json")

        self.device = torch.device("cuda:" + str(properties.get("gpu_id")) if torch.cuda.is_available() else "cpu")

        #model_file_path = os.path.join(model_dir, "modelinfo.json")

        #if os.path.isfile(model_file_path):
        #    with open(model_file_path) as f:
        #        self.modelconfig = json.load(f)
        #else:
        #    logger.warning("Missing the pretrained GPT model path file")


        #self.transfomers_path = self.modelconfig["transformers_path"]
        self.transformers_path = "skt/kogpt2-base-v2"
        serialized_file = self.manifest['model']['serializedFile']
        model_pt_path = os.path.join(model_dir, serialized_file)
        if not os.path.isfile(model_pt_path):
            raise RuntimeError("Missing the model.pt file")

        # Read model serialize/pt file
        #if self.modelconfig["model_name"] == "kogpt2":

        checkpoint = torch.load(model_pt_path, map_location=self.device)
        self.model = GPTmodel()
        self.model.load_state_dict(checkpoint['model_state_dict'])

        self.tokenizer = PreTrainedTokenizerFast.from_pretrained(self.transformers_path, \
                                                                bos_token='</s>', \
                                                                eos_token='</s>', \
                                                                unk_token='<unk>', \
                                                                pad_token='<pad>', mask_token='<mask>')
        self.model.to(self.device)
        self.model.eval()

        logger.debug('Transformer model from path {0} loaded successfully'.format(model_dir))
        self.initialized = True

    def preprocess(self, data):
        """ Very basic preprocessing code - only tokenizes.
            Extend with your own preprocessing steps as needed.
        """
        text = data[0].get("data")
        if text is None:
            text = data[0].get("body")
        sentences = text.decode('utf-8')
        logger.info("Received text: '%s'", sentences)

        encoded_context = self.tokenizer.encode(
            sentences,
            #add_special_tokens=True,
            #return_tensors="pt"
        )

        input_ids = torch.tensor([self.tokenizer.bos_token_id] + encoded_context + [self.tokenizer.eos_token_id] + \
                              [self.tokenizer.bos_token_id]).unsqueeze(0)
        inputs = {"input_ids" : input_ids, "original_length" : len(encoded_context)}

        return inputs

    def inference(self, inputs):
        """
        Predict the class of a text using a trained transformer model.
        """
        # NOTE: This makes the assumption that your model expects text to be tokenized
        # with "input_ids" and "token_type_ids" - which is true for some popular transformer models, e.g. bert.
        # If your transformer model expects different tokenization, adapt this code to suit
        # its expected input format.
        input_ids = inputs["input_ids"]
        input_ids = input_ids.to(self.device)

        coarse_result = self.model.generate(input_ids = input_ids)
        coarse_result = coarse_result.to("cpu")
        fined_result = self.tokenizer.decode(coarse_result[0].tolist()[inputs["original_length"]+1:],
                                             skip_special_tokens = True)
        #logger.info("Model predicted: '%s'", fined_result)
        return [fined_result]

    def postprocess(self, inference_output):
        # TODO: Add any needed post-processing of the model predictions here

        return inference_output

    def handle(self, data, context):
        try:
            if not self.initialized:
                self.initialize(context)

            if data is None:
                return None

            data = self.preprocess(data)
            data = self.inference(data)
            data = self.postprocess(data)

            return data
        except Exception as e:
            raise e

if __name__ == "__main__":
    transformers_path = "skt/kogpt2-base-v2"
    tokenizer = PreTrainedTokenizerFast.from_pretrained(transformers_path, \
                                                        bos_token='</s>', \
                                                        eos_token='</s>', \
                                                        unk_token='<unk>', \
                                                        pad_token='<pad>', mask_token='<mask>')

    print("complete load tokenizer")
