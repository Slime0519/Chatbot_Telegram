from abc import ABC
import json
import logging
import os

import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer

from Language_Model.model import GPTmodel
from transformers import PreTrainedTokenizerFast
from ts.torch_handler.base_handler import BaseHandler

logger = logging.getLogger(__name__)


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
        mapping_file_path = os.path.join(model_dir, "index_to_name.json")

        self.device = torch.device("cuda:" + str(properties.get("gpu_id")) if torch.cuda.is_available() else "cpu")

        model_file_path = os.path.join(model_dir, "modelinfo.json")

        if os.path.isfile(model_file_path):
            with open(model_file_path) as f:
                self.modelconfig = json.load(f)
        else:
            logger.warning("Missing the pretrained GPT model path file")


        self.transfomers_path = self.modelconfig["transformers_path"]
        self.weight_path = model_dir + self.modelconfig["weight_path"]


        # Read model serialize/pt file
        if self.modelconfig["model_name"] == "kogpt2":
            self.model = GPTmodel()
            checkpoint = torch.load(self.weight_path, map_location=self.device)
            model = GPTmodel()
            model.load_state_dict(checkpoint['model_state_dict'])

            tokenizer = PreTrainedTokenizerFast.from_pretrained(self.transfomers_path,
                                                                bos_token='</s>',
                                                                eos_token='</s>',
                                                                unk_token='<unk>',
                                                                pad_token='<pad>', mask_token='<mask>')
        self.model.to(self.device)
        self.model.eval()

        logger.debug('Transformer model from path {0} loaded successfully'.format(model_dir))


        if os.path.isfile(mapping_file_path):
            with open(mapping_file_path) as f:
                self.mapping = json.load(f)
        else:
            logger.warning('Missing the index_to_name.json file. Inference output will not include class name.')
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

        coarse_result = self.model.generate(input_ids = inputs["input_ids"])
        fined_result = self.tokenizer.decode(coarse_result[0].tolist()[inputs["original_length"]+1:],
                                             skip_special_tokens = True)
        logger.info("Model predicted: '%s'", fined_result)
        return [fined_result]

    def postprocess(self, inference_output):
        # TODO: Add any needed post-processing of the model predictions here

        return inference_output

_service = TransformersClassifierHandler()

def handle(data, context):
    try:
        if not _service.initialized:
            _service.initialize(context)

        if data is None:
            return None

        data = _service.preprocess(data)
        data = _service.inference(data)
        data = _service.postprocess(data)

        return data
    except Exception as e:
        raise e