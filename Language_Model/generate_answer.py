import os
import numpy as np
import torch

from Language_Model.model import GPTmodel
from transformers import PreTrainedTokenizerFast

device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")

datapath = "kogpt2-wellnesee-auto-regressive1.pth"

if __name__ == "__main__":
    tokenizer = PreTrainedTokenizerFast.from_pretrained('skt/kogpt2-base-v2',
                                                        bos_token='</s>',
                                                        eos_token='</s>',
                                                        unk_token='<unk>',
                                                        pad_token='<pad>', mask_token='<mask>')

    checkpoint = torch.load(datapath, map_location=device)
    model = GPTmodel()
    model.load_state_dict(checkpoint['model_state_dict'])

    model.eval()

    count = 0
    output_size = 200

    while True:
        sent = input("Question: ")
        tokenized_indicies = tokenizer.encode(sent)
        input_ids = torch.tensor([tokenizer.bos_token_id] + tokenized_indicies + [tokenizer.eos_token_id] + [tokenizer.bos_token_id]).unsqueeze(0)

        sample_output = model.generate(input_ids=input_ids)
        print(input_ids)
        print(tokenizer.decode(input_ids[0]))
        print(sample_output)
        print("Answer: " + tokenizer.decode(sample_output[0].tolist()[len(tokenized_indicies)+1:],
                                            skip_special_tokens=True))
        print(100 * '-')