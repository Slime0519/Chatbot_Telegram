import torch.nn as nn
from transformers import GPT2LMHeadModel

class GPTmodel(nn.Module):
    def __init__(self):
        super(GPTmodel, self).__init__()
        self.kogpt2 = GPT2LMHeadModel.from_pretrained('skt/kogpt2-base-v2')

    def forward(self, input, labels = None):
        if labels is not None:
            outputs =self.kogpt2(input, labels = labels)
        else:
            outputs = self.kogpt2(input)

        return outputs

    def generate(self,
                 input_ids,
                 do_sample=True,
                 max_length=60,
                 top_p=0.92,
                 top_k=50,
                 temperature=0.6,
                 no_repeat_ngram_size=None,
                 num_return_sequences=3,
                 early_stopping=False,
                 ):
        return self.kogpt2.generate(input_ids,
                                    do_sample=do_sample,
                                    max_length=max_length,
                                    top_p=top_p,
                                    top_k=top_k,
                                    temperature=temperature,
                                    no_repeat_ngram_size=no_repeat_ngram_size,
                                    num_return_sequences=num_return_sequences,
                                    early_stopping=early_stopping,
                                    )
    """
    def generate(self,
                 input_ids,
                 do_sample=True,
                 max_length=50,
                 top_k=50,
                 temperature=0.7):
        return self.kogpt2.generate(input_ids,
                                    do_sample=do_sample,
                                    max_length=max_length,
                                    top_k=top_k,
                                    temperature=temperature)
    """

    def save_pretrained(self, save_directory, save_config:bool = True, state_dict: [dict] = None
                        , push_to_hub: bool = False):
        self.kogpt2.save_pretrained(save_directory=save_directory, save_config=save_config, state_dict=state_dict, push_to_hub=push_to_hub)

    def from_pretrained(self, model_dir):
        self.kogpt2.from_pretrained(model_dir)
        return self